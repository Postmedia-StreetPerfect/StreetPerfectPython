import logging, datetime, time, os, argparse, json
from PythonModule.StreetPerfect.HttpClient import HttpClient
from PythonModule.StreetPerfect import StreetPerfectException
from PythonModule.StreetPerfect.Models import *

_ScriptVer = "v1.2"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sp_batch')

sp_api_id = ""
sp_api_key = ""

input_file= "sample_input_data.zip"

try:

    logger.info('Running StreetPerfect Batch Address Verifier')

    client = HttpClient(sp_api_id, sp_api_key) #, url='http://localhost:8000/api/')

    info = client.Info()
    logger.info('\n'.join(f'{k}={v}' for k, v in info.info.items()))

    cfg = BatchConfig(inputKeyOffset = 1, 
                      inputRecipientOffset= 2, 
                      inputAddressLineOffset = 3, 
                      inputCityOffset = 4, 
                      inputProvinceStateOffset = 5, 
                      inputPostalZipCodeOffset = 6)


    # check status first
    r = client.caBatchStatus()
    if r.status == 'Running':
        client.caBatchStopTask();
        logger.info('batch task shows running, so stopping task')
        while 1:
            # now wait till its done
            # possible statuses are: Unknown, Error, Empty, Starting, Running, Stopping, Stopped, InputReady, OutputReady
            r = client.caBatchStatus()
            logger.info('Stopping task, Status: %s', r.status)
            if r.status != 'Running':
                break
            time.sleep(5)

    # must delete any exiting input & output
    logger.info('deleting all IO files')
    client.caBatchClean('all')
    time.sleep(5)

    # upload as a multipart-form or direct data post as csv
    logger.info('uploading input file; %s', input_file)

    #r = client.caBatchUploadForm(input_file, isZip=input_file.lower().endswith('.zip'))
    r = client.caBatchUploadCsv(input_file, isZip=input_file.lower().endswith('.zip'))
    
    logger.info(f'caBatchUpload response: {r.msg}')
 
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
            client.caBatchDownloadTo('output', 'StreetPerfectGoodRecs.txt')
            client.caBatchDownloadTo('output_errors', 'StreetPerfectBadRecs.txt')
                    
            logger.info(client.caBatchDownload('log').replace('\r', ''))
        else:
            logger.error(f"wrong batch status '{r.status}', should be 'OutputReady'")
    else:
        logger.error(f"wrong batch status '{r.status}', should be 'InputReady'")
            
    logger.info('Complete')
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

