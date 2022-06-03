import requests, datetime, json, threading, time, urllib3, logging
from . Models import *
from . import StreetPerfectException

logger = logging.getLogger(__name__)

class StreetPerfectHttpException(StreetPerfectException):
    def __init__(self, code, uri, msg):
        super().__init__(msg)
        self.code = code
        self.uri = uri
        self.msg = msg

class BackgroundRefreshTimer(threading.Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            logger.debug('running background timed event')
            self.function(*self.args,**self.kwargs)


class HttpClient:
    def __init__(self, client_id, api_key
        , url=None, use_dev_site=False, verify=True, timeout=20
        , ver='1', debug=False, opt=None):
        session = requests.Session()
        self.session = session
        self.apiKey=api_key
        self.clientId=client_id
        self.debug = debug
        self.timeout = timeout
        self.verfy = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.apiVer = ver
        self.baseAddr = 'https://api.streetperfect.com/api/'
        if use_dev_site:
            self.baseAddr = 'https://apidev.streetperfect.com/api/'
        elif url:
            self.baseAddr = url.rstrip('/') + '/'

        self.token = None
        self.refreshToken = None
        self.expires = 0
        self.lastRefreshed = None
        self.backgroundRefreshTimer = None
        self.options = opt
        self.session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Close()

    def Close(self):
        if self.backgroundRefreshTimer:
            self.backgroundRefreshTimer.cancel()

    def GetToken(self, force=False):
        if not self.token or force:
            self._NewToken()
            if self.backgroundRefreshTimer:
                self.backgroundRefreshTimer.cancel()
            self.backgroundRefreshTimer = BackgroundRefreshTimer(self.expires, self._RefreshToken)
            self.backgroundRefreshTimer.start()
        return self.token

    def _NewToken(self):
        logger.debug('new token')
        req = TokenRequest()
        req.clientId = self.clientId
        req.clientSecret = self.apiKey
        uri = f'{self.baseAddr}token'
        ret = self.session.post(uri
            , data=json.dumps(req.__dict__)
            , verify=self.verfy, timeout=self.timeout)
        if ret.status_code == 200:
            self._ImportToken(ret.json())
        else:
            raise StreetPerfectHttpException(ret.status_code, uri, f'token request error; code:{ret.status_code}, err:{ret.reason}')
    
    def _RefreshToken(self):
        logger.debug('refresh token')
        req = RefreshTokenRequest()
        req.accessToken = self.token
        req.refreshToken = self.refreshToken
        uri = f'{self.baseAddr}token/refresh'
        ret = self.session.post(uri
            , data=json.dumps(req.__dict__)
            , verify=self.verfy, timeout=self.timeout)

        if ret.status_code == 200:
            self._ImportToken(ret.json())
        else:
            raise StreetPerfectHttpException(ret.status_code, uri, f'token refresh error; code:{ret.status_code}, err:{ret.reason}')
    
    def _ImportToken(self, resp):
        logger.debug('import token')
        if not 'accessToken' in resp:
            if 'msg' in resp:
                raise StreetPerfectHttpException(401, '', f"gettoken error; {resp['msg']}")
            else:
                raise StreetPerfectHttpException(401, '', f"unknown gettoken error")
               
        self.token = resp['accessToken']
        self.refreshToken = resp['refreshToken']
        self.expires = (resp['expires'] -1) * 60 
        self.lastRefreshed = datetime.datetime.now()
        print("token refreshed")

    def Post(self, funct, data, ver=None, robj=None, opt=None):
        if ver == None:
            ver = self.apiVer
        uri = f'{self.baseAddr}{ver}/{funct}'
        logger.debug('post %s', uri)

        if opt:
            data.options = opt.__dict__

        token = self.GetToken()
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        ret = self.session.post(uri
            , data=json.dumps(data.__dict__), verify=self.verfy, timeout=self.timeout)
        if ret.status_code == 200:
            resp = ret.json()
            if robj:
               robj.__dict__.update(resp)
               return robj
            return resp
        
        raise StreetPerfectHttpException(ret.status_code, uri, f'post error; uri:{uri}, code:{ret.status_code}, err:{ret.reason}')

    def Get(self, funct, ver=None, robj=None):
        if ver == None:
            ver = self.apiVer
        uri = f'{self.baseAddr}{ver}/{funct}'
        token = self.GetToken()
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        ret = self.session.get(uri, verify=self.verfy, timeout=self.timeout)
        if ret.status_code == 200:
            resp = ret.json()
            if robj:
               robj.__dict__.update(resp)
               return robj
            return resp
        
        raise StreetPerfectHttpException(ret.status_code, uri, f'get error; uri:{uri}, code:{ret.status_code}, err:{ret.reason}')

    def caTypeahead(self,  req: caTypeaheadRequest) -> caTypeaheadResponse:
        """
        Typeahead
            pass caTypeaheadRequest
            returns caTypeaheadResponse
        """
        return self.Post('ca/typeahead', req, robj=caTypeaheadResponse())

    def caTypeheadRec(self,  req: caTypeaheadRequest) -> caTypeaheadResponse:
        """
        TypeheadRec
            pass caTypeaheadRequest
            returns caTypeaheadResponse
        """
        return self.Post('ca/typeahead/rec', req, robj=caTypeaheadResponse())

    def caTypeheadFetch(self,  req: caTypeaheadFetchRequest) -> caTypeaheadFetchResponse:
        """
        TypeheadFetch
            pass caTypeaheadFetchRequest
            returns caTypeaheadFetchResponse
        """
        return self.Post('ca/typeahead/fetch', req, robj=caTypeaheadFetchResponse(), opt=self.options)

    def Info(self):
        """
        Info
            returns GetInfoResponse
        """
        return self.Get('ca/query', robj=GetInfoResponse())


    def caQuery(self, req: caQueryRequest) -> caQueryResponse:
        """
        caQuery
            pass caQueryRequest
            returns caQueryResponse
        """
        return self.Post('ca/query', req, robj=caQueryResponse(), opt=self.options)


    def caFetchAddress(self, req: caFetchAddressRequest) -> caFetchAddressResponse:
        """caFetchAddress
            pass caFetchAddressRequest
            returns caFetchAddressResponse
        """
        return self.Post('ca/fetch', req, robj=caFetchAddressResponse(), opt=self.options)


    def caFormatAddress(self, req: caFormatAddressRequest) -> caFormatAddressResponse:
        """caFormatAddress
            pass caFormatAddressRequest
            returns caFormatAddressResponse
        """
        return self.Post('ca/format', req, robj=caFormatAddressResponse(), opt=self.options)

    def caValidateAddress(self, req:caValidateAddressRequest, opt: Options = None) -> caValidateAddressResponse:
        """caValidateAddress
            pass caValidateAddressRequest
            returns caValidateAddressResponse
        """
        return self.Post('ca/validate', req, robj=caValidateAddressResponse(), opt=self.options)

    def caProcessCorrection(self, req: caAddressRequest) -> caCorrectionResponse:
        """caProcessCorrection
            pass caAddressRequest
            returns caCorrectionResponse req
        """
        return self.Post('ca/correction', req, robj=caCorrectionResponse(), opt=self.options)

    def caProcessParse(self, req: caAddressRequest) -> caParseResponse:
        """caProcessParse
            pass caAddressRequest
            returns caParseResponse req
        """
        return self.Post('ca/parse', req, robj=caParseResponse(), opt=self.options)
        
    def caProcessSearch(self, req: caAddressRequest) -> caSearchResponse:
        """
        caProcessSearch
            pass caAddressRequest
            returns caSearchResponse req
        """
        return self.Post('ca/search', req, robj=caSearchResponse(), opt=self.options)
        

    # US ProcessAddress calls

    def usProcessCorrection(self, req: usAddressRequest) -> usCorrectionResponse:
        """usProcessCorrection
            pass usAddressRequest
            returns  usCorrectionResponse req
        """
        return self.Post('us/correction', req, robj=usCorrectionResponse())        

    def usProcessParse(self, req: usAddressRequest) -> usParseResponse:
        """usProcessParse
            pass usAddressRequest req
            returns usParseResponse
        """
        return self.Post('us/parse', req, jobj=usParseResponse())

    def usProcessSearch(self, req: usAddressRequest) -> usSearchResponse:
        """usProcessSearch
            pass usAddressRequest req
            returns usSearchResponse
        """
        return self.Post('us/search', req, jobj=usParseResponse())

    def usProcessDeliveryInfo(self, req: usAddressRequest) -> usDeliveryInformationResponse:
        """usProcessDeliveryInfo
            pass usAddressRequest req
            returns usDeliveryInformationResponse
        """
        return self.Post('us/info', req, robj=usDeliveryInformationResponse())



