import logging
from StreetPerfect.XpcClient import XpcClient
from StreetPerfect.HttpClient import HttpClient
from StreetPerfect import StreetPerfectException
from StreetPerfect.Models import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_sp_client_id = 'your id'
_sp_api_key = 'your key'
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

        client = HttpClient(_sp_client_id, _sp_api_key, use_dev_site=True, verify=_verify)

        info = client.Info()
        print("\n".join(info.info))

        req = caTypeaheadRequest()
        req.address_line = '3267 flo'
        req.max_returned=100
        req.tokenize_qry = True

        resp = client.caTypeheadRec(req)
        print(resp.count)

        for r in resp.recs:
            print(r)

        # you must call Close to stop the background token refresh timer
        # or you can optionally use 'with' when creating the client
        client.Close()

        # optional syntax to close the client when out of scope
        with HttpClient(_sp_client_id, _sp_api_key, use_dev_site=True, verify=_verify) as client:
            info = client.Info()
            print("\n".join(info.info))

    except StreetPerfectException as e:
        print(f"StreetPerfectHttpException: {e}")


if __name__ == '__main__':
    #XPC_Test()
    Http_Test()