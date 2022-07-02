from asyncio import streams
import requests, datetime, json, threading, time, urllib3, logging
from . HttpClientBase import HttpClientBase
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


class HttpClient(HttpClientBase):

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


	# Batch

	def caBatchUpload(self, data: str ) -> bool:
		"""caBatchUpload, Upload batch input string data.
		"""
		return self.Post('ca/batch/upload', BatchUploadRequest(data), robj=BatchUploadResponse())

	def caBatchUploadForm(self, filename: str, encoding = "utf8", isZip=False ) -> bool:
		"""caBatchUpload, Upload batch input string data.
		"""
		files = {'file': open(filename, 'rb')}
		fields = {
			'encoding': encoding,
			'is_zipped': isZip
			}
		return self.PostForm('ca/batch/upload/form', files=files, fields=fields, robj=BatchUploadResponse())

	def caBatchDownloadTo(self, id: str, local_filename: str ) -> bool:
		"""caBatchDownload, Download batch output results
			pass an output file id and a local filename to write to
			returns true if successful 
		"""
		r = self.Get(f'ca/batch/download/{id}', stream=True)      
		if r.status_code == 200:
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)
			return True
		return False

	def caBatchDownload(self, id: str):
		"""caBatchDownload, Download batch output results
			pass an output file id
			returns the raw bytes (for zip) or text if successful
		"""
		return self.Get(f'ca/batch/download/{id}')      

	def caBatchStatus(self) -> BatchStatus:
		"""caBatchStatus, Return status of a batch task
			returns BatchStatus
		"""
		return self.Get('ca/batch', robj=BatchStatus())


	def caBatchStopTask(self) -> BatchStatus:
		"""caStopBatchTask, stop a running batch task
			Return status of the batch task
			returns BatchStatus
		"""
		return self.Delete('ca/batch', robj=BatchStatus())


	def caBatchStartTask(self, config: BatchConfig) -> BatchStatus:
		"""caStopBatchTask, stop a running batch task
			Return status of the batch task
			returns BatchStatus
		"""
		return self.Post('ca/batch', config, robj=BatchStatus())


	def caBatchClean(self, id: str):
		"""caStopBatchTask, stop a running batch task
			Return status of the batch task
			returns BatchStatus
		"""
		r = self.Delete(f'ca/batch/clean/{id}')
		return r.status_code == 200


	def caBatchEncodings(self) -> list:
		"""caBatchEncodings, Returns a list of all possible text encoidings this system supports
			Returns list of encoding dicts
		"""
		return self.Get(f'/ca/batch/encodings')


