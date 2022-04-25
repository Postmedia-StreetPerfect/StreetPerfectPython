# StreetPerfect Python Clients

The XpcClient uses the native network access of StreetPerfect (XPC).

It is only intended to be used on a local area network without public access.

```Python
from StreetPerfect.XpcClient import XpcClient, StreetPerfectException
from StreetPerfect.Models import *

try:
    # pass your SP connection string when creating the client
    client = Client("ServiceAddress=127.0.0.1;ServicePort=1330")
    print ("info= {}\n".format("\n".join(client.Info())))

    # use our standard request/response models 
    addr = caFetchAddressRequest()
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
    
The Http Client is intended to superseed the XPC Client.

Both the clients use the identical interface and can be interchanged.

```Python
from StreetPerfect.HttpClient import HttpClient, StreetPerfectHttpException
from StreetPerfect.Models import *

try:

    # pass your SP client id and api key
    # you can also point the client to your own local SP server
    client = HttpClient('me@somewhere.com'
        , 'api key'
        , use_dev_site=True)

    info = client.Info()
    print(info)

    # use our standard request/response models 
    addr = caFetchAddressRequest()
    addr.postal_code="m4w3l4"
    addr.street_number="365"
    resp = client.caFetchAddress(addr)

    if resp.status_flag == 'N':
        print (f"caFetchAddress = {resp.address_line}\n{resp.city}, {resp.province}, {resp.postal_code}\n")
    else:
        print (f"caFetchAddress Error:{resp.status_flag}\n{resp.status_messages}\n")
        
except StreetPerfectHttpException as e:
    print(f"StreetPerfectHttpException: {e}")
```    
    