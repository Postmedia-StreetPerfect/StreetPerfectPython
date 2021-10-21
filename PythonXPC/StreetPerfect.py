from StreetPerfect.Client import Client
from StreetPerfect import Models, StreetPerfectException

try:

    client = Client("ServiceAddress=127.0.0.1;ServsicePort=1330")
    print ("info= {}\n".format("\n".join(client.Info())))

    addr = Models.caFetchAddressRequest()
    addr.postal_code="m4w3l4"
    addr.street_number="365"
    resp = client.caFetchAddress(addr)


    if resp.status_flag == 'N':
        print (f"caFetchAddress = {resp.address_line}\n{resp.city}, {resp.province}, {resp.postal_code}\n")
    else:
        print (f"caFetchAddress Error:{resp.status_flag}\n{resp.status_messages}\n")


    #100 Queen St W, Toronto, ON M5H 2N1

    caReq = Models.caAddressRequest()
    caReq.address_line = "100 Queen St Z"
    caReq.city="toronto"
    caReq.province="on"
    caReq.postal_code = "M5H 2N1"
    resp = client.caProcessParse(caReq)
    print (f"caProcessParse flag={resp.status_flag}\n{resp.function_messages}\n")


    caReq = Models.caAddressRequest()
    caReq.address_line = "100 Queen"
    caReq.postal_code = "M5H2N1"
    resp = client.caProcessSearch(caReq)
    print (f"caProcessSearch = stat:{resp.status_flag}, {resp.status_messages}\n")

    for addr in resp.response_address_list:
        print(str(addr))

except StreetPerfectException as e:
    print(f"StreetPerfectException: {e}")
