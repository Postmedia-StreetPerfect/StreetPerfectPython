# StreetPerfectPython

Easy to use

```Python
from StreetPerfect.Client import Client
from StreetPerfect import Models, StreetPerfectException

try:

    # pass your SP connection string when creating the client
    client = Client("ServiceAddress=127.0.0.1;ServicePort=1330")
    print ("info= {}\n".format("\n".join(client.Info())))

    # use our standard request/response models 
    addr = Models.caFetchAddressRequest()
    addr.postal_code="m4w3l4"
    addr.street_number="365"
    resp = client.caFetchAddress(addr)

    if resp.status_flag == 'N':
        print (f"caFetchAddress = {resp.address_line}\n{resp.city}, {resp.province}, {resp.postal_code}\n")
    else:
        print (f"caFetchAddress Error:{resp.status_flag}\n{resp.status_messages}\n")
        
except StreetPerfectException as e:
    print(f"StreetPerfectException: {e}")
```    
    
