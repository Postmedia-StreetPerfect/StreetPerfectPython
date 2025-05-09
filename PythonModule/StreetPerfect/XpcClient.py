import ctypes, os
from sys import platform
from .Helpers import OutString
from .Models import *
from . import StreetPerfectException

class StreetPerfectException(Exception):
	pass

def InString(param_str):
	if param_str is str:
		return param_str.encode(encoding='ascii', errors='ignore')
	if param_str is bytes:
		return param_str
	if param_str is None:
		return b''
	return str(param_str).encode(encoding='ascii', errors='ignore')


class XpcClient:
	_def_constr = "ServiceAddress=127.0.0.1;ServicePort=1330;"
	_def_win_dll = "SpaaSqaXpcClientNim64.dll"
	_def_linux_so = "libSpaaSqaXpcClientNim64.so"

	_opt_fields = {
        'preferredLanguageStyle' :          {'opt_name': 'PreferredLanguageStyle', 'opt_type': 'str'},
        'userLanguage' :                    {'opt_name': 'UserLanguage', 'opt_type': 'str'},
        'printMessageNumbers' :             {'opt_name': 'PrintMessageNumbers', 'opt_type': 'str'},
        'maximumTryMessages' :              {'opt_name': 'MaximumTryMessages', 'opt_type': 'int'},
        'errorTolerance' :                  {'opt_name': 'ErrorTolerance', 'opt_type': 'int'},
        'preferredUnitDesignatorKeyword' :  {'opt_name': 'PreferredUnitDesignatorKeyword', 'opt_type': 'str'},
        'preferredUnitDesignatorStyle' :    {'opt_name': 'PreferredUnitDesignatorStyle', 'opt_type': 'str'},
        'outputFormatGuide' :               {'opt_name': 'OutputFormatGuide', 'opt_type': 'str'},
        'exceptionReportLevel' :            {'opt_name': 'ExceptionReportLevel', 'opt_type': 'str'},
        'optimizeAddress' :                 {'opt_name': 'OptimizeAddress', 'opt_type': 'str'},
        'printInformationMessages' :        {'opt_name': 'PrintInformationMessages', 'opt_type': 'bool'},
        'printChangeMessages' :             {'opt_name': 'PrintChangeMessages', 'opt_type': 'bool'},
        'printErrorMessages' :              {'opt_name': 'PrintErrorMessages', 'opt_type': 'bool'},
        'printTryMessages' :                {'opt_name': 'PrintTryMessages', 'opt_type': 'bool'},
        'printOptimizeMessages' :           {'opt_name': 'PrintOptimizeMessages', 'opt_type': 'bool'},
    }

	def __init__(self, connectionString = _def_constr, dll=None, opt=None, debug=False):

		if dll is None:
			path = os.path.dirname(__file__)
			if platform == "win32":
				dll = os.path.join(path, self._def_win_dll)
			else:
				dll = os.path.join(path, self._def_linux_so)
		
		self.SetOptions(opt)
		self.hDll = ctypes.cdll.LoadLibrary(dll)
		self.debug = debug

		connectionString = connectionString.strip(' \r\n\t,:;') + ';'
		self.connectionString =  connectionString.encode('ascii')
	

	def SetOptions(self, options) -> str:
		buf = ''
		if options:
			for k,v in self._opt_fields.items():
				attr = getattr(options, k, None)
				if attr is not None:
					ot = v.get('opt_type')
					if ot == 'str1':
						if len(attr) == 1:
							buf += f"{v['opt_name']}={attr.upper()};"
					elif ot == 'str':
						if len(attr) > 0:
							buf += f"{v['opt_name']}={attr};"
					elif ot == 'bool':
						buf += f"{v['opt_name']}={'Y' if attr else 'N'};"
					elif ot == 'int':
						buf += f"{v['opt_name']}={attr};"
		self.options_str = buf.encode('ascii')
		return buf
		

	def GetConnectionString(self):
		return self.connectionString + self.options_str


	def _CheckForError(self, ret_status, ret_status_msg):
		if ret_status.ToString().strip() != 'N':
			raise StreetPerfectException(ret_status_msg.ToString())


	def Info(self) -> GetInfoResponse:

		ret_info = OutString()
		ret_status = OutString(10)
		ret_status_msg = OutString(200)
		ret = self.hDll.StreetPerfectQueryAddress(self.GetConnectionString(),
								b"99",
								b'',
								b'',
								b'',
								b'',
								b'',
								ret_info.s,
								ret_status.s,
								ret_status_msg.s)
		self._CheckForError(ret_status, ret_status_msg, )
		resp = GetInfoResponse()
		resp.info = ret_info.ToList()
		resp.status_flag = ret_status
		resp.status_messages = ret_status_msg
		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectQueryAddress() returned error code: {ret}"
		return resp


	def caQuery(self, req: caQueryRequest) -> caQueryResponse:
		""" 
		caQuery
			pass caQueryRequest
			returns caQueryResponse 
		"""

		buf_size = 1000000
		if req.query_option >= 70:
			buf_size = 468500  #buffer space for 1000 results
		elif req.query_option > 30:
			buf_size = 20000
		elif req.query_option == 16:
			buf_size = 300000

		PS_ARG_out_function_messages = OutString(buf_size)
		PS_ARG_out_status_flag = OutString(10)
		PS_ARG_out_status_messages = OutString()
		_in_not_used = b""

		ret = self.hDll.StreetPerfectQueryAddress(self.GetConnectionString(),
				InString(req.query_option),
				InString(req.address_line),
				InString(req.city),
				InString(req.province),
				InString(req.postal_code),
				_in_not_used,
				PS_ARG_out_function_messages.s,
				PS_ARG_out_status_flag.s,
				PS_ARG_out_status_messages.s)

		resp = caQueryResponse()
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectQueryAddress() returned error code: {ret}"
		return resp



	def caFetchAddress(self, req: caFetchAddressRequest) -> caFetchAddressResponse:
		"""caFetchAddress
			pass caFetchAddressRequest
			returns caFetchAddressResponse
		"""
		PS_CAN_out_address_line = OutString()
		PS_CAN_out_city = OutString()
		PS_CAN_out_province = OutString()
		PS_CAN_out_postal_code = OutString()
		PS_CAN_out_country = OutString()
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		ret = self.hDll.StreetPerfectFetchAddress(self.GetConnectionString(), 
										InString(req.street_number),
										InString(req.unit_number),
										InString(req.postal_code)
			, PS_CAN_out_address_line.s, PS_CAN_out_city.s, PS_CAN_out_province.s
			, PS_CAN_out_postal_code.s, PS_CAN_out_country.s, PS_ARG_out_status_flag.s
			, PS_ARG_out_status_messages.s)

		resp = caFetchAddressResponse()
		resp.address_line = PS_CAN_out_address_line.ToString()
		resp.city = PS_CAN_out_city.ToString()
		resp.province = PS_CAN_out_province.ToString()
		resp.postal_code = PS_CAN_out_postal_code.ToString()
		#resp.country = PS_CAN_out_country.ToString()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectFetchAddress() returned error code: {ret}"
		return resp


	def caFormatAddress(self, req: caFormatAddressRequest) -> caFormatAddressResponse:
		"""caFormatAddress
			pass caFormatAddressRequest
			returns caFormatAddressResponse
		"""
		PS_CAN_out_format_line_one = OutString()
		PS_CAN_out_format_line_two = OutString()
		PS_CAN_out_format_line_three = OutString()
		PS_CAN_out_format_line_four = OutString()
		PS_CAN_out_format_line_five = OutString()
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()
		_in_not_used = b""

		ret = self.hDll.StreetPerfectFormatAddress(self.GetConnectionString()
									   , InString(req.address_line)
									   , InString(req.city)
			, InString(req.province), InString(req.postal_code)
			, _in_not_used #req.country
			, PS_CAN_out_format_line_one.s, PS_CAN_out_format_line_two.s
			, PS_CAN_out_format_line_three.s, PS_CAN_out_format_line_four.s
			, PS_CAN_out_format_line_five.s, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s)

		resp = caFormatAddressResponse()

		resp.format_line_one = PS_CAN_out_format_line_one.ToString()
		resp.format_line_two = PS_CAN_out_format_line_two.ToString()
		resp.format_line_three = PS_CAN_out_format_line_three.ToString()
		resp.format_line_four = PS_CAN_out_format_line_four.ToString()
		resp.format_line_five = PS_CAN_out_format_line_five.ToString()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectFormatAddress() returned error code: {ret}"
		return resp



	def caValidateAddress(self, req: caValidateAddressRequest) -> caValidateAddressResponse:
		"""caValidateAddress
			pass caValidateAddressRequest
			returns caValidateAddressResponse
		"""
		PS_ARG_out_function_messages = OutString()
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()
		_in_not_used = b""
			
		ret = self.hDll.StreetPerfectValidateAddress(self.GetConnectionString()
							, InString(req.address_line), InString(req.city)
			, InString(req.province), InString(req.postal_code)
			, _in_not_used #req.country
			, PS_ARG_out_function_messages.s, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s)

		resp = caValidateAddressResponse()
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectValidateAddress() returned error code: {ret}"
		return resp



	def caProcessCorrection(self, req: caAddressRequest) -> caCorrectionResponse:
		"""caProcessCorrection
			pass caAddressRequest
			returns caCorrectionResponse req
		"""
		PS_ARG_out_function_messages = OutString(4000)
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		PS_CAN_out_recipient = OutString()
		PS_CAN_out_address_line = OutString()
		PS_CAN_out_city = OutString()
		PS_CAN_out_province = OutString()
		PS_CAN_out_postal_code = OutString()
		PS_CAN_out_extra_information = OutString()
		PS_CAN_out_unidentified_component = OutString()

		_in_not_used = b""
		_out_not_used = OutString(10)

		ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"CAN_AddressCorrection"
			, InString(req.recipient), InString(_in_not_used), InString(req.address_line), InString(req.city)
			, InString(req.province), InString(req.postal_code)
			, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
			, PS_CAN_out_recipient.s, _out_not_used.s, PS_CAN_out_address_line.s, PS_CAN_out_city.s
			, PS_CAN_out_province.s, PS_CAN_out_postal_code.s, PS_CAN_out_extra_information.s, PS_CAN_out_unidentified_component.s
			, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s)

		resp = caCorrectionResponse()
			
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		resp.recipient = PS_CAN_out_recipient.ToString()
		resp.address_line = PS_CAN_out_address_line.ToString()
		resp.city = PS_CAN_out_city.ToString()
		resp.postal_code = PS_CAN_out_postal_code.ToString()
		resp.province = PS_CAN_out_province.ToString()
		resp.extra_information = PS_CAN_out_extra_information.ToString()
		resp.unidentified_component = PS_CAN_out_unidentified_component.ToString()
		
		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

		return resp


	def caProcessParse(self, req: caAddressRequest) -> caParseResponse:
		"""caProcessParse
			pass caAddressRequest 
			returns caParseResponse req
		"""
		PS_ARG_out_function_messages = OutString(4000)
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		PS_CAN_out_address_type = OutString()
		PS_CAN_out_street_number = OutString()
		PS_CAN_out_street_suffix = OutString()
		PS_CAN_out_street_name = OutString()
		PS_CAN_out_street_type = OutString()
		PS_CAN_out_street_direction = OutString()
		PS_CAN_out_unit_type = OutString()
		PS_CAN_out_unit_number = OutString()
		PS_CAN_out_service_type = OutString()
		PS_CAN_out_service_number = OutString()
		PS_CAN_out_service_area_name = OutString()
		PS_CAN_out_service_area_type = OutString()
		PS_CAN_out_service_area_qualifier = OutString()
		PS_CAN_out_extra_information = OutString()
		PS_CAN_out_unidentified_component = OutString()

		_in_not_used = b""
		_out_not_used = OutString(10)

		ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"CAN_AddressParse"
			, InString(req.recipient), _in_not_used
			, InString(req.address_line), InString(req.city)
			, InString(req.province), InString(req.postal_code)
			, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
			, PS_CAN_out_address_type.s
			, PS_CAN_out_street_number.s
			, PS_CAN_out_street_suffix.s
			, PS_CAN_out_street_name.s
			, PS_CAN_out_street_type.s
			, PS_CAN_out_street_direction.s
			, PS_CAN_out_unit_type.s
			, PS_CAN_out_unit_number.s
			, PS_CAN_out_service_type.s
			, PS_CAN_out_service_number.s
			, PS_CAN_out_service_area_name.s
			, PS_CAN_out_service_area_type.s
			, PS_CAN_out_service_area_qualifier.s
			, PS_CAN_out_extra_information.s
			, PS_CAN_out_unidentified_component.s
			)

		resp = caParseResponse()
			
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		resp.address_type = PS_CAN_out_address_type.ToString()
		resp.street_number = PS_CAN_out_street_number.ToString()
		resp.street_suffix = PS_CAN_out_street_suffix.ToString()
		resp.street_name = PS_CAN_out_street_name.ToString()
		resp.street_type = PS_CAN_out_street_type.ToString()
		resp.street_direction = PS_CAN_out_street_direction.ToString()
		resp.unit_type = PS_CAN_out_unit_type.ToString()
		resp.unit_number = PS_CAN_out_unit_number.ToString()
		resp.service_type = PS_CAN_out_service_type.ToString()
		resp.service_number = PS_CAN_out_service_number.ToString()
		resp.service_area_name = PS_CAN_out_service_area_name.ToString()
		resp.service_area_type = PS_CAN_out_service_area_type.ToString()
		resp.service_area_qualifier = PS_CAN_out_service_area_qualifier.ToString()
		resp.extra_information = PS_CAN_out_extra_information.ToString()
		resp.unidentified_component = PS_CAN_out_unidentified_component.ToString()
			
		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"
		return resp
		


	def caProcessSearch(self, req: caAddressRequest) -> caSearchResponse:
		"""
		caProcessSearch
			pass caAddressRequest 
			returns caSearchResponse req
		"""

		
		#Stopwatch sw = Stopwatch()
		#sw.Start()

		expected_count = 20
		for tries in range(2):
			
			PS_ARG_out_function_messages = OutString(4000)
			PS_ARG_out_status_flag = OutString()
			PS_ARG_out_status_messages = OutString()

			PS_CAN_out_response_count = OutString()
			PS_CAN_out_response_available = OutString()
			PS_CAN_out_response_address_list = OutString(expected_count * 250)

			_in_not_used = b""
			_out_not_used = OutString(10)

			ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"CAN_AddressSearch"
				, InString(req.recipient), _in_not_used
				, InString(req.address_line)
				, InString(req.city)
				, InString(req.province)
				, InString(req.postal_code)
				, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
				, PS_CAN_out_response_count.s
				, PS_CAN_out_response_available.s
				, PS_CAN_out_response_address_list.s
				, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s
				, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s
				)

			status_flag = PS_ARG_out_status_flag.ToString()
			response_count = PS_CAN_out_response_count.ToInt()
			response_available = PS_CAN_out_response_available.ToInt()

			response_address_list = [] #List<caAddress>()
			if response_count > 0:
				
				if response_available != response_count: # just in case we need to requery with bigger - does a big make a difference though?
					expected_count = response_available
					continue
					
				response_address_list = PS_CAN_out_response_address_list.ToCaAddrList(response_count, self.debug)
				

			if len(response_address_list) != response_count:
				raise StreetPerfectException("caProcessSearch response_count is different from results row count")
				

			resp = caSearchResponse()
				
			resp.function_messages = PS_ARG_out_function_messages.ToList()
			resp.status_flag = status_flag
			resp.status_messages = PS_ARG_out_status_messages.ToString()
			resp.response_count = response_count
			resp.response_address_list = response_address_list
			#resp.t_exec_ms = sw.ElapsedMilliseconds

			if ret != 0 and not resp.status_flag:
				resp.status_flag = 'X'
				resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

			return resp
		
		raise StreetPerfectException("requery failed to resp = all expected results")
		


	# US ProcessAddress calls

	def usProcessCorrection(self, req: usAddressRequest) -> usCorrectionResponse:
		"""usProcessCorrection
			pass usAddressRequest 
			returns usCorrectionResponse req
		"""
		
		PS_ARG_out_function_messages = OutString(4000)
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		PS_USA_out_firm_name = OutString()
		PS_USA_out_urbanization_name = OutString()
		PS_USA_out_address_line = OutString()
		PS_USA_out_city = OutString()
		PS_USA_out_state = OutString()
		PS_USA_out_zip_code = OutString()

		_out_not_used = OutString(10)

		ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"USA_AddressCorrection"
			, InString(req.firm_name), InString(req.urbanization_name), InString(req.address_line), InString(req.city), InString(req.state), InString(req.zip_code)
			, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
			, PS_USA_out_firm_name.s
			, PS_USA_out_urbanization_name.s
			, PS_USA_out_address_line.s
			, PS_USA_out_city.s
			, PS_USA_out_state.s
			, PS_USA_out_zip_code.s
			, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s
			, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s)

		resp = usCorrectionResponse()
			
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		resp.firm_name = PS_USA_out_firm_name.ToString()
		resp.urbanization_name = PS_USA_out_urbanization_name.ToString()
		resp.address_line = PS_USA_out_address_line.ToString()
		resp.city = PS_USA_out_city.ToString()
		resp.state = PS_USA_out_state.ToString()
		resp.zip_code = PS_USA_out_zip_code.ToString()

		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

		return resp	
		


	def usProcessParse(self, req: usAddressRequest) -> usParseResponse:
		"""usProcessParse
			pass usAddressRequest
			returns usParseResponse req
		"""

		PS_ARG_out_function_messages = OutString(4000)
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		PS_USA_out_address_type = OutString()
		PS_USA_out_street_number = OutString()
		PS_USA_out_street_pre_direction = OutString()
		PS_USA_out_street_name = OutString()
		PS_USA_out_street_type = OutString()
		PS_USA_out_street_post_direction = OutString()
		PS_USA_out_secondary_type = OutString()
		PS_USA_out_secondary_number = OutString()
		PS_USA_out_service_type = OutString()
		PS_USA_out_service_number = OutString()
		PS_USA_out_delivery_point_barcode = OutString()
		PS_USA_out_congressional_district = OutString()
		PS_USA_out_county_name = OutString()
		PS_USA_out_county_code = OutString()

		_out_not_used = OutString(10)

		ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"USA_AddressParse"
			, InString(req.firm_name), InString(req.urbanization_name), InString(req.address_line), InString(req.city)
			, InString(req.state), InString(req.zip_code)
			, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
			, PS_USA_out_address_type.s
			, PS_USA_out_street_number.s
			, PS_USA_out_street_pre_direction.s
			, PS_USA_out_street_name.s
			, PS_USA_out_street_type.s
			, PS_USA_out_street_post_direction.s
			, PS_USA_out_secondary_type.s
			, PS_USA_out_secondary_number.s
			, PS_USA_out_service_type.s
			, PS_USA_out_service_number.s
			, PS_USA_out_delivery_point_barcode.s
			, PS_USA_out_congressional_district.s
			, PS_USA_out_county_name.s
			, PS_USA_out_county_code.s
			, _out_not_used.s
			)

		resp = usParseResponse()
			
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		resp.address_type = PS_USA_out_address_type.ToString()
		resp.street_number = PS_USA_out_street_number.ToString()
		resp.street_pre_direction = PS_USA_out_street_pre_direction.ToString()
		resp.street_name = PS_USA_out_street_name.ToString()
		resp.street_type = PS_USA_out_street_type.ToString()
		resp.street_post_direction = PS_USA_out_street_post_direction.ToString()
		resp.secondary_type = PS_USA_out_secondary_type.ToString()
		resp.secondary_number = PS_USA_out_secondary_number.ToString()
		resp.service_type = PS_USA_out_service_type.ToString()
		resp.service_number = PS_USA_out_service_number.ToString()
		resp.delivery_point_barcode = PS_USA_out_delivery_point_barcode.ToString()
		resp.congressional_district = PS_USA_out_congressional_district.ToString()
		resp.county_name = PS_USA_out_county_name.ToString()
		resp.county_code = PS_USA_out_county_code.ToString()
		
		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

		return resp
		


	def usProcessSearch(self, req: usAddressRequest) -> usSearchResponse:
		"""usProcessSearch
			pass usAddressRequest
			returns usSearchResponse req
		"""
		expected_count = 20
		for tries  in range(2):
			
			PS_ARG_out_function_messages = OutString(4000)
			PS_ARG_out_status_flag = OutString()
			PS_ARG_out_status_messages = OutString()

			PS_USA_out_response_count = OutString()
			PS_USA_out_response_available = OutString()
			PS_USA_out_response_address_list = OutString(expected_count * 250)

			_out_not_used = OutString(10)

			ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"USA_AddressSearch"
				, InString(req.firm_name), InString(req.urbanization_name), InString(req.address_line), InString(req.city)
				, InString(req.state), InString(req.zip_code)
				, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
				, PS_USA_out_response_count.s
				, PS_USA_out_response_available.s
				, PS_USA_out_response_address_list.s
				, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s
				, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s, _out_not_used.s
				)

			status_flag = PS_ARG_out_status_flag.ToString()
			response_count = PS_USA_out_response_count.ToInt()
			response_available = PS_USA_out_response_available.ToInt()

			response_address_list = [] #List<usAddress>()
			if response_count > 0:
				if response_available != response_count: # just in case we need to requery with bigger - does a big make a difference though?
					expected_count = response_available
					continue
					
				response_address_list = PS_USA_out_response_address_list.ToUsAddrList(response_count, self.debug)

			if response_address_list.Count() != response_count:
				raise StreetPerfectException("caProcessSearch response_count is different from results row count")
				

			resp = usSearchResponse()
				
			resp.function_messages = PS_ARG_out_function_messages.ToList()
			resp.status_flag = status_flag
			resp.status_messages = PS_ARG_out_status_messages.ToString()
			resp.response_count = response_count
			resp.response_address_list = response_address_list

			if ret != 0 and not resp.status_flag:
				resp.status_flag = 'X'
				resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

			return resp

		raise StreetPerfectException("requery failed to resp = all expected results")
		
			   

	def usProcessDeliveryInfo(self, req: usAddressRequest) -> usDeliveryInformationResponse:
		"""usProcessDeliveryInfo
			pass usAddressRequest
			returns usDeliveryInformationResponse  req
		"""
		
		PS_ARG_out_function_messages = OutString(4000)
		PS_ARG_out_status_flag = OutString()
		PS_ARG_out_status_messages = OutString()

		PS_USA_out_city_abbreviation = OutString()
		PS_USA_out_post_office_city = OutString()
		PS_USA_out_post_office_state = OutString()
		PS_USA_out_delivery_point_bar_code = OutString()
		PS_USA_out_carrier_route = OutString()
		PS_USA_out_auto_zone_indicator = OutString()
		PS_USA_out_lot_number = OutString()
		PS_USA_out_lot_code = OutString()
		PS_USA_out_lacs_code = OutString()
		PS_USA_out_county_code = OutString()
		PS_USA_out_finance_number = OutString()
		PS_USA_out_congressional_district = OutString()
		PS_USA_out_pmb_designator = OutString()
		PS_USA_out_pmb_number = OutString()

		_out_not_used = OutString(10)

		ret = self.hDll.StreetPerfectProcessAddress(self.GetConnectionString(), b"USA_DeliveryInformation"
			, InString(req.firm_name), InString(req.urbanization_name), InString(req.address_line), InString(req.city)
			, InString(req.state), InString(req.zip_code)
			, PS_ARG_out_status_flag.s, PS_ARG_out_status_messages.s, PS_ARG_out_function_messages.s
			, PS_USA_out_city_abbreviation.s
			, PS_USA_out_post_office_city.s
			, PS_USA_out_post_office_state.s
			, PS_USA_out_delivery_point_bar_code.s
			, PS_USA_out_carrier_route.s
			, PS_USA_out_auto_zone_indicator.s
			, PS_USA_out_lot_number.s
			, PS_USA_out_lot_code.s
			, PS_USA_out_lacs_code.s
			, PS_USA_out_county_code.s
			, PS_USA_out_finance_number.s
			, PS_USA_out_congressional_district.s
			, PS_USA_out_pmb_designator.s
			, PS_USA_out_pmb_number.s
			, _out_not_used.s
			)

		resp = usDeliveryInformationResponse()
			
		resp.function_messages = PS_ARG_out_function_messages.ToList()
		resp.status_flag = PS_ARG_out_status_flag.ToString()
		resp.status_messages = PS_ARG_out_status_messages.ToString()

		resp.city_abbreviation = PS_USA_out_city_abbreviation.ToString()
		resp.post_office_city = PS_USA_out_post_office_city.ToString()
		resp.post_office_state = PS_USA_out_post_office_state.ToString()
		resp.delivery_point_bar_code = PS_USA_out_delivery_point_bar_code.ToString()
		resp.carrier_route = PS_USA_out_carrier_route.ToString()
		resp.auto_zone_indicator = PS_USA_out_auto_zone_indicator.ToString()
		resp.lot_number = PS_USA_out_lot_number.ToString()
		resp.lot_code = PS_USA_out_lot_code.ToString()
		resp.lacs_code = PS_USA_out_lacs_code.ToString()
		resp.county_code = PS_USA_out_county_code.ToString()
		resp.finance_number = PS_USA_out_finance_number.ToString()
		resp.congressional_district = PS_USA_out_congressional_district.ToString()
		resp.pmb_designator = PS_USA_out_pmb_designator.ToString()
		resp.pmb_number = PS_USA_out_pmb_number.ToString()
			
		if ret != 0 and not resp.status_flag:
			resp.status_flag = 'X'
			resp.status_messages = f"StreetPerfectProcessAddress() returned error code: {ret}"

		return resp

