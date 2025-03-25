from asyncio import streams
import requests, datetime, json, threading, time, urllib3, logging
from . Models import *
from . import StreetPerfectException

logger = logging.getLogger(__name__)


# bmiller, mar 2025, fixed Python client to handle both on-prremisies api_key and SP.com bearer token
# simply pass api_key= to the client to enable local webapi access

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


class HttpClientBase:

	def __init__(self, client_id:str =None, client_secret:str=None, api_key:str=None
		, url:str=None, verify:bool=True, timeout:int=20
		, ver:str='1', debug:bool=False, opt:dict=None):
		"""
		@param client_id: your StreetPerfect username (email)
		@param client_secret: your StreetPerfect api (secret) key
		@param api_key: your on-premisies server api key
		@param url: optional, url to your on-premisies server http[s]://host[:port]/api
		@param verify: optional, allows you to ignore ssl cert errors by setting False (default True)
		@param timeout: request timeout, default 20 secs
		@param ver: api version, currently 1 is the (default) only option
		@param debug: if True will add extra debug info to responses
		@param opt: default SreetPerfect request Options (see the Options class model)
		"""

		# verify the required params
		if not api_key and (not client_secret or not client_secret):
			raise ValueError("api_key OR client_id and client_secret params required")
		if api_key and not url:
			raise ValueError("api_key requires a valid url setting")
		if api_key and (client_id or client_secret):
			logger.warning("api_key and client_* params found, api_key takes priority, client_* settings ignored")

		session = requests.Session()
		self.session = session
		self.apiKey=api_key
		self.clientId=client_id
		self.clientSecret=client_secret
		self.debug = debug
		self.timeout = timeout
		self.verfy = verify
		if not verify:
			urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		self.apiVer = ver
		self.baseAddr = 'https://api.streetperfect.com/api/'
		if url:
			self.baseAddr = url.rstrip('/') + '/'

		self.token = None
		self.refreshToken = None
		self.expires = 0
		self.lastRefreshed = None
		self.backgroundRefreshTimer = None
		self.options = opt
		self.AddDefaultHeaders()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.Close()

	def AddDefaultHeaders(self):
		self.session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

	def Close(self):
		if self.backgroundRefreshTimer:
			self.backgroundRefreshTimer.cancel()

	# SetAuth decides if it should use the api_key OR get a SAS token
	# it also now sets the self.session.headers directly and returns None
	def SetAuth(self, force=False):
		#apikey overrides any SP site creds
		if self.apiKey:
			self.session.headers.update({'X-Api-Key': self.apiKey})
		else:
			if not self.token or force:
				self._NewToken()
				if self.backgroundRefreshTimer:
					self.backgroundRefreshTimer.cancel()
				self.backgroundRefreshTimer = BackgroundRefreshTimer(self.expires, self._RefreshToken)
				self.backgroundRefreshTimer.start()
			self.session.headers.update({'Authorization': f'Bearer {self.token}'})
		return None

	def _NewToken(self):
		logger.debug('new token')
		req = TokenRequest()
		req.clientId = self.clientId
		req.clientSecret = self.clientSecret
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
		logger.debug("token refreshed")

	def BuildUrl(self, funct, ver=None):
		if ver == None:
			ver = self.apiVer
		if ver:
			ver += '/'
		return f'{self.baseAddr}{ver}{funct}'

	def PostRaw(self, funct, data, robj=None, headers=None, ver=None):
		uri = self.BuildUrl(funct, ver)
		logger.debug('post %s', uri)
		self.SetAuth()
		err=''
		ret = self.session.post(uri
			, data=data, verify=self.verfy, timeout=self.timeout, headers=headers)
		if ret.status_code == 200:
			if not ret.content:
				return ret
			resp = ret.json()
			if robj:
				robj.__dict__.update(resp)
				return robj
			return resp		
		elif ret.status_code == 502:
			if 'json' in ret.headers['Content-Type']:
				resp = ret.json()
				if 'err' in resp:
					err = resp["err"]

		raise StreetPerfectHttpException(ret.status_code, uri, f'post error; uri:{uri}, code:{ret.status_code}, err:{err if err else ret.reason}')



	def Post(self, funct, data, ver=None, robj=None, opt=None, headers=None):
		if opt:
			data.options = opt.__dict__

		return self.PostRaw(funct, json.dumps(data.__dict__), ver=ver, robj=robj, headers=headers)


	def PostForm(self, funct, fields, files, ver=None, robj=None):
		uri = self.BuildUrl(funct, ver)
		logger.debug('post %s', uri)

		self.SetAuth()
		self.session.headers.pop('Content-Type', None) #else it overrides the form post below
		ret = self.session.post(uri
			, data=fields, files=files, verify=self.verfy, timeout=self.timeout)

		self.AddDefaultHeaders()
		#ret = requests.Request('POST', uri, data=fields, files=files)
		#pretty_print_POST(ret.prepare())

		if ret.status_code == 200:
			if not ret.content:
				return ret
			resp = ret.json()
			if robj:
				robj.__dict__.update(resp)
				return robj
			return resp
		elif ret.status_code == 502:
			if 'json' in ret.headers['Content-Type']:
				resp = ret.json()
				if 'err' in resp:
					err = resp["err"]
		
		raise StreetPerfectHttpException(ret.status_code, uri, f'post error; uri:{uri}, code:{ret.status_code}, err:{err if err else ret.reason}')

	def Get(self, funct, ver=None, robj=None, stream=False):
		uri = self.BuildUrl(funct, ver)
		self.SetAuth()
		err = ''
		ret = self.session.get(uri, stream=stream, verify=self.verfy, timeout=self.timeout)
		if ret.status_code == 200:
			if not ret.content or stream:
				return ret
			if 'json' in ret.headers['Content-Type']:
				resp = ret.json()
				if robj:
					robj.__dict__.update(resp)
					return robj
				return resp
			elif "text/plain" in ret.headers['Content-Type']:
				return ret.text
			else:
				return ret.content
		elif ret.status_code == 502:
			if 'json' in ret.headers['Content-Type']:
				resp = ret.json()
				if 'err' in resp:
					err = resp["err"]

		raise StreetPerfectHttpException(ret.status_code, uri, f'get error; uri:{uri}, code:{ret.status_code}, err:{err if err else ret.reason}')

	def Delete(self, funct, ver=None, robj=None):
		uri = self.BuildUrl(funct, ver)
		self.SetAuth()
		ret = self.session.delete(uri, verify=self.verfy, timeout=self.timeout)
		if ret.status_code == 200:
			if not ret.content:
				return ret
			resp = ret.json()
			if robj:
				robj.__dict__.update(resp)
				return robj
			return resp
		elif ret.status_code == 502:
			if 'json' in ret.headers['Content-Type']:
				resp = ret.json()
				if 'err' in resp:
					err = resp["err"]
		
		raise StreetPerfectHttpException(ret.status_code, uri, f'delete error; uri:{uri}, code:{ret.status_code}, err:{err if err else ret.reason}')



	def pretty_print_POST(req):
		"""
		At this point it is completely built and ready
		to be fired; it is "prepared".

		However pay attention at the formatting used in 
		this function because it is programmed to be pretty 
		printed and may differ from the actual request.
		"""
		print('{}\n{}\r\n{}\r\n\r\n{}'.format(
			'-----------START-----------',
			req.method + ' ' + req.url,
			'\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
			req.body,
		))