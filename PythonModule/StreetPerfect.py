import logging
from StreetPerfect.Client import Client
from StreetPerfect.HttpClient import HttpClient, StreetPerfectHttpException
from StreetPerfect import StreetPerfectException
from StreetPerfect.Models import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
 

def XPC_Test():
    try:

        client = Client("ServiceAddress=127.0.0.1;ServicePort=1330")
        print ("info= {}\n".format("\n".join(client.Info())))

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

        client = HttpClient('bmiller@postmedia.com'
        , '9ra1lm44k5c30ah9bngrtm7sfa663i9x76kxk40pzc12c5xf1b'
        , use_dev_site=True, verify=False)

        client.GetToken()

        info = client.Info()
        print(info)

        req = caTypeaheadRequest()
        req.address_line = '3267 flow'
        req.max_returned=100
        req.tokenize_qry = True

        resp = client.caTypeheadRec(req)
        print(resp.count)

        for r in resp.recs:
            print(r)
    except StreetPerfectHttpException as e:
        print(f"StreetPerfectHttpException: {e}")


if __name__ == '__main__':
    Http_Test()