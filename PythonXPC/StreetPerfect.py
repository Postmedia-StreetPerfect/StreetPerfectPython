from StreetPerfect.Client import Client
from StreetPerfect import Models, StreetPerfectException


try:

    client = Client("ServiceAddress=127.0.0.1;ServicePort=1330")
    print ("info= {}\n".format("\n".join(client.Info())))

    addr = Models.caFetchAddressRequest()
    addr.postal_code="m4w3l4"
    addr.street_number="365"
    resp = client.caFetchAddress(addr)

    # we could have the client calls raise on non 'N' status flags, might make for a better call pattern
    # maybe do what Requests does and let the user decide by adding: Client.RaiseOnStatus() -although status flags are complex
    if resp.status_flag == 'N':
        print ("caFetchAddress = {address_line}, {city}, {province}, {postal_code}\n".format(**resp.__dict__ ))
    else:
        print ("caFetchAddress Error:{status_flag}\n{status_messages}\n".format(resp.status_flag,  resp.status_messages))


    #100 Queen St W, Toronto, ON M5H 2N1

    caReq = Models.caAddressRequest()
    caReq.address_line = "100 Queen St Z"
    caReq.city="toronto"
    caReq.province="on"
    caReq.postal_code = "M5H 2N1"
    resp = client.caProcessParse(caReq)
    print ("caProcessParse flag={}\n{}\n".format(resp.status_flag, "\n".join(resp.function_messages) ))


    caReq = Models.caAddressRequest()
    caReq.address_line = "100 Queen"
    caReq.postal_code = "M5H2N1"
    resp = client.caProcessSearch(caReq)
    print ("caProcessSearch = stat:{}, {}\n".format(resp.status_flag, resp.status_messages))

    for addr in resp.response_address_list:
        print(str(addr))

except StreetPerfectException as e:
    print("StreetPerfectException: {}".format(e))
	
	