import logging, datetime, time, os, argparse, json
from PythonModule.StreetPerfect.HttpClient import HttpClient
from PythonModule.StreetPerfect import StreetPerfectException
from PythonModule.StreetPerfect.Models import *

_ScriptVer = "v1.2"

"""
# bmiller, aug 2022
# This is an example of how to handle running batch correction via python.
# below is a sample sp_creds.json file, it must contain one or more StreetPerfect creds in a dictionary
# you can override this file by passing the creds to the script

{
	"dev" : {
		"api_id" : "user@postmedia.com",
		"api_key" : "api-key",
		"api_url" : "https://apidev.streetperfect.com/api/"
		},
	"prod" : {
		"api_id" : "user@postmedia.com",
		"api_key" : "api-key",
		"api_url" : "https://api.streetperfect.com/api/"
		},
}

"""

logger = None #set in main

def sp_batch(sp_api_id, sp_api_key, sp_url, cfg, input_file, out_good_recs, out_bad_recs, verify_ssl=True):
    '''
    Runs a list of addresses through a remote StreetPerfect batch processor
    :param sp_api_id: str, StreetPerfect user id (your email addr)
    :param sp_api_key: str, your api key (generated on SP site)
    :param sp_url: str, the SP url
    :param cfg: StreetPerfect.Models.BatchConfig, many options see swagger schema docs
    :param input_file: str, the input CSV file
    :param out_good_recs: str, the output CSV file containing validated/corrected addresses
    :param out_bad_recs: str, the output CSV file containing errors
    :return: nothing
    '''
    try:

        logger.info('Running StreetPerfect Batch Address Verifier')

        client = HttpClient(sp_api_id, sp_api_key, url=sp_url, verify=verify_ssl)

        info = client.Info()
        logger.info('\n'.join(f'{k}={v}' for k, v in info.info.items()))

        # check status first
        r = client.caBatchStatus()
        if r.status == 'Running':
            client.caBatchStopTask();
            logger.info('batch task shows running, so stopping task')
            while 1:
                # now wait till its done
                # possible statuses are: Unknown, Error, Empty, Starting, Running, Stopping, Stopped, InputReady, OutputReady
                r = client.caBatchStatus()
                print(f'Stopping task, Status: {r.status}')
                if r.status != 'Running':
                    break
                time.sleep(5)

        # must delete any exiting input & output
        logger.info('deleting all IO files')
        client.caBatchClean('all')
        time.sleep(5)
        # upload as a multipart-form
        logger.info('uploading input file; %s', input_file)
        r = client.caBatchUploadForm(input_file, isZip=input_file.lower().endswith('.zip'))
        logger.info(f'caBatchUploadForm response: {r.msg}')
 
        # fetch status
        r = client.caBatchStatus();
        logger.info(f'batch status == {r.status}')

        # batch status must be 'InputReady' to run
        # we're using the default CSV config and pass the column ordinals
        if r.status == 'InputReady':

            # start the batch task!
            logger.info('starting batch task')
            client.caBatchStartTask(cfg)
            
            while 1:
                # now wait till its done
                # possible statuses are: Unknown, Error, Empty, Starting, Running, Stopping, Stopped, InputReady, OutputReady

                r = client.caBatchStatus()
                print(f'BatchRun Status: {r.status}')
                if r.status not in ['Starting', 'Running']:
                    logger.info(r.runInfo)
                    break
                time.sleep(10)

            if r.status == 'OutputReady':
                client.caBatchDownloadTo('log', 'StreetPerfectBatch.log')
                client.caBatchDownloadTo('zip', 'StreetPerfectBatch.zip')
                client.caBatchDownloadTo('output', out_good_recs)
                client.caBatchDownloadTo('output_errors', out_bad_recs)
                    
                logger.info(client.caBatchDownload('log').replace('\r', ''))
            else:
               logger.error(f"wrong batch status '{r.status}', should be 'OutputReady'")
        else:
            logger.error(f"wrong batch status '{r.status}', should be 'InputReady'")
            

    except StreetPerfectException as e:
        logger.critical(f'StreetPerfectHttpException: {e}')
    except Exception as e:
        logger.critical(f'Exception: {e}')
    finally:
        try:
            r = client.caBatchStatus()
            if r.status == 'Running':
                client.caBatchStopTask();
        except:
            pass
        client.Close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='sp_batch', 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=f'{_ScriptVer}, Executes a StreetPerfect batch validation process against a passed list of addresses.')
    parser.add_argument('-spApiId', help='your StreetPerfect client id (email addr)')
    parser.add_argument('-spApiKey', help='your StreetPerfect api key')
    parser.add_argument('-spApiUrl', help='alt StreetPerfect site api url (other than api[dev].streetperfect.com)')
    parser.add_argument('-spCredKey', help='if using the sp_creds.json file, specify the creds key')
    parser.add_argument('-noSSLval', action='store_true', help='disable ssl validation')

    parser.add_argument('-logDir', help='the path to the logging directory (optional)')
    parser.add_argument('-input', default='StreetPerfectBatchInput.csv', help='input CSV file')
    parser.add_argument('-oBad', default='StreetPerfectBatchOutputErrors.csv', help='output error CSV address file')
    parser.add_argument('-oGood', default='StreetPerfectBatchOutput.csv', help='output good CSV address file')
    parser.add_argument('-ordKey', default=1, help='record key column ordinal (all ords ones based)')
    parser.add_argument('-ordRecip', default=2, help='recipient column ordinal')
    parser.add_argument('-ordAddr', default=3, help='address line column ordinal')
    parser.add_argument('-ordCity', default=4, help='city column ordinal')
    parser.add_argument('-ordProv', default=5, help='province column ordinal')
    parser.add_argument('-ordPostal', default=6, help='postal code column ordinal')

    args = parser.parse_args()

    print ( args )

    # configure logging to file
    if args.logDir:
        filenameString = args.logDir + '/sp_batch_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    else:
        filenameString = './sp_batch_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)-15s] %(levelname)-8s [%(name)-12s] %(message)s',
                        handlers=[logging.FileHandler(filenameString), logging.StreamHandler()] )
    
    logger = logging.getLogger('sp_batch')
    
    cfg = BatchConfig(inputKeyOffset = args.ordKey, 
                      inputRecipientOffset= args.ordRecip, 
                      inputAddressLineOffset = args.ordAddr, 
                      inputCityOffset = args.ordCity, 
                      inputProvinceStateOffset = args.ordProv, 
                      inputPostalZipCodeOffset = args.ordPostal)

    sp_api_id = ''
    sp_api_key = ''
    # override sp_creds.py
    if args.spApiId and args.spApiKey:
        sp_api_id = args.spApiId 
        sp_api_key = args.spApiKey
        sp_url = args.spApiUrl
    else:
        try:
            with open('sp_creds.json') as f:
                sp_creds = json.load(f)            
            creds = sp_creds[args.spCredKey]
            sp_api_id = creds['api_id']
            sp_api_key = creds['api_key']
            sp_url = creds['api_url']
            print('read sp_creds.json')
        except Exception as e:
            print(f'sp_creds.json read error: {e}')

    if not sp_api_id and not sp_api_key:
        raise Exception('no StreetPerfect credentials found (require api id and key)')

    verify_ssl = True
    if args.noSSLval:
        verify_ssl = False

    sp_batch(sp_api_id, sp_api_key, sp_url, cfg, args.input, args.oGood, args.oBad, verify_ssl=verify_ssl)
