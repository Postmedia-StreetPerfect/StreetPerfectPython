import logging, json, time
from StreetPerfect.XpcClient import XpcClient
from StreetPerfect.HttpClient import HttpClient
from StreetPerfect import StreetPerfectException
from StreetPerfect.Models import *

try:
    # my_creds.py simply contains a dict of cred dicts
    """
    creds = {
	    'dev' : {
		    'sp_client_id' : 'bmiller@postmedia.com',
		    'sp_api_key' : 'dev key',
		    'url' : 'https://apidev.streetperfect.com/api/',
		    },
        'prod' : {
 		    'sp_client_id' : 'bmiller@postmedia.com',
		    'sp_api_key' : 'prod key',
		    'url' : 'https://api.streetperfect.com/api/',
		    },
        }
    }
    """
    import my_creds
    creds = my_creds.creds['local']
    _sp_client_id = creds['sp_client_id']
    _sp_api_key = creds['sp_api_key']
    _sp_url = creds['url']
except:
    _sp_client_id = 'your id (email)'
    _sp_api_key = 'your api key'
    _sp_url = None #alternate api url



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
_verify = True 

def XPC_Test():
    try:

        client = XpcClient("ServiceAddress=127.0.0.1;ServicePort=1330")
        info = client.Info()
        print("\n".join(info.info))

        addr = caFetchAddressRequest()
        addr.postal_code="m4w3l4"
        addr.street_number="365"
        resp = client.caFetchAddress(addr)

        if resp.status_flag == 'N':
            print (f"caFetchAddress = {resp.address_line}\n{resp.city}, {resp.province}, {resp.postal_code}\n")
        else:
            print (f"caFetchAddress Error:{resp.status_flag}\n{resp.status_messages}\n")


        #100 Queen St W, Toronto, ON M5H 2N1

        caReq = caAddressRequest()
        caReq.address_line = "100 Queen St Z"
        caReq.city="toronto"
        caReq.province="on"
        caReq.postal_code = "M5H 2N1"
        resp = client.caProcessParse(caReq)
        print (f"caProcessParse flag={resp.status_flag}\n{resp.function_messages}\n")


        caReq = caAddressRequest()
        caReq.address_line = "100 Queen"
        caReq.postal_code = "M5H2N1"
        resp = client.caProcessSearch(caReq)
        print (f"caProcessSearch = stat:{resp.status_flag}, {resp.status_messages}\n")

        for addr in resp.response_address_list:
            print(str(addr))

    except StreetPerfectException as e:
        print(f"StreetPerfectException: {e}")



def Http_Test():


    try:
        print("SP http client test")

        options =  Options()
        options.preferredLanguageStyle = 'F'
        options.outputFormatGuide = '7'
        options.maximumTryMessages = 20

        client = HttpClient(_sp_client_id, _sp_api_key, url=_sp_url, use_dev_site=False if _sp_url else True, verify=_verify, opt=options)

        info = client.Info()
        print("\n".join(info.info))

        req = caTypeaheadRequest()
        req.address_line = '3267 flower'
        req.max_returned=100
        req.tokenize_qry = True

        ta_resp = client.caTypeheadRec(req)
        print(ta_resp.count)

        for r in ta_resp.recs:
            print(r)

        req= caTypeaheadFetchRequest()
        req.autocorrect = True
        req.id = ta_resp.recs[0]['id']
        req.street_num = ta_resp.addr_num
        req.return_components = True

        taf_resp = client.caTypeheadFetch(req)
        print(taf_resp.components)

        # you must call Close to stop the background token refresh timer
        # or you can optionally use 'with' when creating the client
        client.Close()

        # optional syntax to close the client when out of scope
        with HttpClient(_sp_client_id, _sp_api_key, use_dev_site=True, verify=_verify, opt=options) as client:
            info = client.Info()
            print("\n".join(info.info))

    except StreetPerfectException as e:
        print(f"StreetPerfectHttpException: {e}")
    client.Close()


def Http_Batch_Test():


    try:
        print("SP http Batch test")

        options =  Options()
        options.preferredLanguageStyle = 'F'
        options.outputFormatGuide = '7'
        options.maximumTryMessages = 20

        client = HttpClient(_sp_client_id, _sp_api_key, url=_sp_url, use_dev_site=False if _sp_url else True, verify=_verify, opt=options)

        info = client.Info()
        print("\n".join(info.info))

        # upload as a multipart-form
        x = client.caBatchUploadForm(r'StreetPerfectBatchInput_csv_small.zip'
                                     , isZip=True)
        print(f"caBatchUploadForm response: {x.msg}")

        # or upload the batch input file directly as a string
        """
        with open(r'StreetPerfectBatchInput_csv_small.txt') as f:
            data = f.read()
        x = client.caBatchUpload(data)
        print(f"caBatchUpload response: {x.msg}")
        """

        client.caBatchClean("output")

        stat = client.caBatchStatus();
        print(f'batch status == {stat.status}')

        # batch status must be 'InputReady' to run
        # we're using the default CSV config and pass the column ordinals
        if stat.status == "InputReady":
            cfg = BatchConfig(inputKeyOffset = 1, 
                              inputRecipientOffset= 2, 
                              inputAddressLineOffset = 3, 
                              inputCityOffset = 4, 
                              inputProvinceStateOffset = 5, 
                              inputPostalZipCodeOffset = 6)

            client.caBatchStartTask(cfg)
            
            while 1:
                stat = client.caBatchStatus()
                print(f'BatchRun Status: {stat.status}')
                if stat.status == 'OutputReady':
                    print(stat.runInfo)
                    break
                time.sleep(5)

        log_text = client.caBatchDownload('log')
        print(log_text)
        x = client.caBatchDownloadTo('log', "test.txt")
        x = client.caBatchDownloadTo('zip', "test.zip")

        print(client.caBatchDownload('log'))


    except StreetPerfectException as e:
        print(f"StreetPerfectHttpException: {e}")

    client.Close()

if __name__ == '__main__':
    #XPC_Test()
    Http_Test()
    #Http_Batch_Test()
