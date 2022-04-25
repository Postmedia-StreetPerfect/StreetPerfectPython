# just street perfect models used by both the XpcClient and HttpClient
# models represent the input (request) and the output (response) parameters of
# all api calls

class TokenRequest:
	clientId: str
	clientSecret: str

class RefreshTokenRequest:
	accessToken: str
	refreshToken: str

class TokenResponse:
	accessToken: str
	tokenType: str
	refreshToken: str
	expires: int
	refreshExpireDate: str
	msg: str

class caTypeaheadRequest:
	address_line: str
	city: str
	province: str
	postal_code: str
	start_rec: int
	max_returned: int
	tokenize_qry: bool

class caTypeaheadResponse:
	addr_num: int
	unit_num: str
	suffix: str
	start_rec: int
	total_hits: int
	count: int
	address_list: list
	recs: list
	t_exec_ms: int
	status_flag: str
	status_messages: str
	abc: str



class caAddress:
	"""
	caAddress is the return data record response for /api/ca/search 

	rec_typ_cde: int
	Record Type Code
 
	 Defines the type of address record. Valid values are:
	 1. Street Address Record
	 2. Street Served by Route Record
	 3. Lock Box Address Record
	 4. Route Service Address Record
	 5. General Delivery Address Record

	adr_typ_cde: int
	Address Type Code
 
	 A code denoting whether an address is in the form of a civic address or a delivery installation address. Valid values are:
		1. Civic (Street) Address Format
		2. Delivery Installation (Station) Address Format

	prov_cde: str
	Province Code
 
	 Alphabetic code identifying the province geographically. Valid values are accessible through a query function.

	drctry_area_nme: str
	Directory Area Name
 
	 Major community or greater municipality grouping that contains the street address or its delivery installation. Should not be used.

	st_nme: str
	Street Name
 
	 Official civic name of a roadway or artery

	st_typ_cde: str
	Street Type Code
 
	 Official description used to identify the type of roadway or artery. Valid values are accessible through a query function.

	st_drctn_cde: str
	Street Direction Code
 
	 Street direction component of an official street name. Valid values are accessible through a query function.

	st_adr_seq_cde: str
	Street Address Sequence Code
 
	 This code identifies the sequence associated with the range of street numbers. Valid values are: 
	 1. Odd 
	 2. Even 
	 3. Consecutive

	st_adr_to_nbr: int
	Street Address to Number
 
	 The highest street number in a range of municipal street addresses.

	st_adr_nbr_sfx_to_cde: str
	Street Address Number Suffix to Code
 
	 The address suffix associated with the street address to number. Examples of street numbers with suffixes are 14 1/2 and 22B. A numeric number denotes a fractional suffix. Valid values are:
	 1. 1/4 
	 2. 1/2
	 3. 3/4

	ste_to_nbr: str
	Suite to Number
 
	 Highest value in a range of suites or apartments.

	st_adr_frm_nbr: int
	Street Address from Number

	 The lowest street number in a range of municipal street addresses.

	st_adr_nbr_sfx_frm_cde: str
	Street Address Number Suffix from Code

	 The address suffix associated with the street address from number. Examples of street numbers with suffixes are 14 1/2 and 22B. A numeric number denotes a fractional suffix. Valid values are:
	 1. 1/4 
	 2. 1/2
	 3. 3/4

	ste_frm_nbr: str
	Suite from Number

	 Lowest value in a range of suites or apartments.

	mncplt_nme: str
	Municipality Name

	 A municipality is any village, town or city in Canada that is recognized as a valid mailing address by Canada Post.
	#not used public int? route_serv_box_to_nbr 
	#not used public int? route_serv_box_frm_nbr 

	route_serv_typ_dsc_2: str
	Route Service Type Description for type 2 records

	 The code that identifies the type of route service. Valid values are: 
	 - RR - Rural Route 
	 - SS - Suburban Service 
	 - MR - Mobile Route 
	 - GD - General Delivery 

	route_serv_nbr_2: int
	Route Service Number for type 2 records

	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode

	di_area_nme: str
	Delivery Installation Area Name

	 The name of a village, town, municipality or city that forms part of a Delivery Installation Name. While this field is populated, it is USUALLY not required to be displayed as part of the address.

	di_typ_dsc: str
	Delivery Installation Type Description

	 The category of delivery installation. Valid values are accessible through a query function.

	di_qlfr_nme: str
	Delivery Installation Qualifier Name

	 When more than one delivery installation serves an area, the qualifier name uniquely identifies the delivery installation.

	lock_box_bag_to_nbr: int
	Lock Box bag to Number

	 Highest number in a range of lock boxes.

	lock_box_bag_frm_nbr: int
	Lock Box bag from Number

	 Lowest number in a range of lock boxes.

	route_serv_typ_dsc_4: str
	Route Service Type Description for type 4 records

	 The code that identifies the type of route service. Valid values are the same as for type 2 records.

	route_serv_nbr_4: int
	Route Service Number for type 4 records

	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode

	pstl_cde: str
	Postal Code

	 A ten character, alpha numeric combination (ANANAN) assigned to one or more postal addresses. The postal code is an integral part of every postal address in Canada and is required for the mechanized processing of mail. Postal codes are also used to identify various CPC processing facilities and delivery installations.

	#di_pstl_cde: str
	# Delivery Installation Postal Code
	#
	# The postal code of the delivery installation responsible for delivery to the postal code. Not Used.
	#

	text_record_flag: str
	Text Record Flag

	 Defines the type of record in the TEXT lookup table 
	 * A = Building name record 
	 * B = Large Volume Receiver Name (Street) record 
	 * C = Government Name (Street) record 
	 * D = Large Volume Receiver Name (PO BOX) record 
	 * E = Government Name (PO BOX) record 
	 * F = General Delivery record

	cntry_cde: str
	Country Code

	orig_rec: str
	Original StreetPerfect internal record when debugging
	"""

	rec_typ_cde: int
	adr_typ_cde: int
	prov_cde: str
	drctry_area_nme: str
	st_nme: str
	st_typ_cde: str
	st_drctn_cde: str
	st_adr_seq_cde: str
	st_adr_to_nbr: int
	st_adr_nbr_sfx_to_cde: str
	ste_to_nbr: str
	st_adr_frm_nbr: int
	st_adr_nbr_sfx_frm_cde: str
	ste_frm_nbr: str
	mncplt_nme: str
	route_serv_typ_dsc_2: str
	route_serv_nbr_2: int
	di_area_nme: str
	di_typ_dsc: str
	di_qlfr_nme: str
	lock_box_bag_to_nbr: int
	lock_box_bag_frm_nbr: int
	route_serv_typ_dsc_4: str
	route_serv_nbr_4: int
	pstl_cde: str
	text_record_flag: str
	cntry_cde: str
	orig_rec: str
	
	def __str__(self):
		return "{st_adr_frm_nbr}-{st_adr_to_nbr} {st_nme} {st_typ_cde}, {mncplt_nme}, {prov_cde}, {pstl_cde}".format(**self.__dict__)


class usAddress:
	"""
	Record Type Code
	 
	 This code identifies the record types. Valid values are: 
	 * B = Building 
	 * F = Firm name 
	 * G = General Delivery 
	 * H = Highrise 
	 * M = Military 
	 * P = PO Box 
	 * R – Rural 
	 * S – Urban 
	 * U – Unique
	 * \* – Generic

	orig_rec: str
	Original StreetPerfect record when debugging
	"""
	
	RecordType: str
	CityName: str
	StateAbbreviation: str
	ZipCode: str
	PlusFourAddonLow: str
	PlusFourAddonHigh: str
	StreetNumberLow: str
	StreetNumberHigh: str
	StreetPreDirection: str
	StreetName: str
	StreetSuffix: str
	StreetPostDirection: str
	UnitType: str
	UnitNumberLow: str
	UnitNumberHigh: str
	PrivateMailBoxNumber: str
	LocationName: str
	orig_rec: str


class GetInfoResponse:
	info: list
	status_flag: str
	status_messages: str


class caAddressRequest:
	recipient: str
	address_line: str
	city: str
	province: str
	postal_code: str


class caCorrectionResponse:
	"""
	status_flag: str
	* V = Submitted address is Valid
	 * C = Submitted address is Corrected
	 * N = Submitted address is Not correct
	 * F = Submitted address is Foreign
	"""

	recipient: str
	address_line: str
	city: str
	province: str
	postal_code: str
	extra_information: str
	unidentified_component: str

	status_flag: str

	status_messages: str
	function_messages: list

class caParseResponse:
	"""
	status_flag: str
	Valid Address
	 * P = Parsed &amp; Valid
	 
	 Invalid Address
	 * I = Parsed &amp; Invalid
	"""
	address_type: str
	street_number: str
	street_suffix: str
	street_name: str
	street_type: str
	street_direction: str
	unit_type: str
	unit_number: str
	service_type: str
	service_number: str
	service_area_name: str
	service_area_type: str
	service_area_qualifier: str
	extra_information: str
	unidentified_component: str
	status_flag: str
	status_messages: str
	function_messages: list


class caSearchResponse:
	"""
	status_flag: str

	* N = At least one record found
	 * X = No records found
	"""
	response_count: int
	t_exec_ms: int
	response_address_list: list
	status_flag: str
	status_messages: str
	function_messages: list


# CA legacy non-ProcessAddress functions


class caFetchAddressRequest:
	street_number: str
	unit_number: str
	postal_code: str


class caFetchAddressResponse:
	address_line: str
	city: str
	province: str
	postal_code: str
		#country: str
	status_flag: str
	status_messages: str


class caFormatAddressRequest:
	address_line: str
	city: str
	province: str
	postal_code: str
		#country: str


class caFormatAddressResponse:
	format_line_one: str
	format_line_two: str
	format_line_three: str
	format_line_four: str
	format_line_five: str
	status_flag: str
	status_messages: str


class caValidateAddressRequest:
	address_line: str
	city: str
	province: str
	postal_code: str
		#country: str


class caValidateAddressResponse:
	function_messages: list
	status_flag: str
	status_messages: str


class caQueryRequest:
	"""
	Query Option Value
	 
	 11. Postal Code Search <br/>
	 Input: Requires postal code <br/>
	 Output: Returns pairs of records in the output array <br/>
	  - 132-byte format range records
	 	- 232-byte CPC raw data range records
	 
	 
	 12. Text Record Search <br/>
	 Input: Requires postal code <br/>
	 Output: Returns additional text information in the output array <br/>
	 
	 
	 13. Postal Code Search <br/>
	 Input: Requires postal code <br/>
	 Output: Returns records in the output array <br/>
	  - 232-byte CPC raw data range records
	 
	 
	 14. CPC Raw Data Range Record Format <br/>
	 Input: Requires CPC raw data range record in address line field <br/>
	 Output: Returns two 63-byte format address records in output array <br/>
	 
	 
	 16. Postal Code Search <br/>
	 Input: City and province <br/>
	 Output: Returns postal codes in the output array <br/>
	 
	 
	 20. Rural Address Search all types (GD/ PO BOX/RR) <br/>
	 Input: City and province (optional) <br/>
	 Output: Returns pairs of records in the output array
	  - 132-byte format range records *
	  - 232-byte CPC raw data range records *
	 
	 
	 21. Urban Address Search - ‘STREET’ types <br/>
	 Input: Minimum requirement: street name and city. Additional components such as civic number, street type and province will yield more specific results. Use address line field for input. <br/>
	 Output: Returns pairs of records in the output array
	  - 132-byte format range records
	  - 232-byte CPC raw data range records
	 	
	 	
	 23. Rural Address Search ‘PO BOX’ types <br/>
	 Input: Minimum requirement: city. Additional components such as PO BOX number and province will yield more specific results. Use address line field for input. <br/>
	 Output: Returns pairs of records in the output array
	  - 132-byte format range records
	  - 232-byte CPC raw data range records
	 
	 
	 24. Rural Address Search ‘RR/SS/MR’ types <br/>
	 Input: Minimum requirement: city. Additional components such as route service number and province will yield more specific results. Use address line field for input. <br/>
	 Output: Returns pairs of records in the output array
	  - 132-byte format range records
	  - 232-byte CPC raw data range records
	 	
	 	
	 25. Rural Address Search ‘GD’ types <br/>
	 Input: Minimum requirement: city. Additional components such as province will yield more specific results. Use address line field for input. <br/>
	 Output: Returns pairs of records in the output array
	  - 132-byte format range records
	  - 232-byte CPC raw data range records
	 	
	 	
	 26. CPC Raw Data Range Search <br/>
	 Input: Requires CPC raw data range record. Use address line field for input. <br/>
	 Output: Returns all address matches in CPC raw data range record format in the output array. <br/>
	 
	 
	 31. Return street type table entries.
	 
	 
	 32. Return street direction table entries.
	 
	 
	 33. Return route service type description table entries.
	 
	 
	 34. Return province code table entries.
	 
	 
	 35. Return service type table entries.
	 
	 
	 36. Return delivery installation type table entries.
	 
	 
	 37. Return country code table entries.
	 
	 
	 38. Return US state code table entries.
	 
	 
	 39. Return unit designator table entries.
	 
	 
	 310. Street name search <br/>
	 Input: Partial street name. Use street name field for input. <br/>
	 Output: Matching street name table records in the output array <br/>
	 
	 
	 311. Urban municipality name search <br/>
	 Input: Partial municipality name. Use municipality name field for input. <br/>
	 Output: Matching municipality name table records in the output array. <br/>
	 
	 
	 312. Rural municipality name search <br/>
	 Input: Partial rural municipality name. Use municipality name field for input. <br/>
	 Output: Matching municipality name table records in the output array. <br/>
	 
	 
	 313. Urban and Rural municipality name search <br/>
	 Input: Partial municipality name. Use municipality name field for input. <br/>
	 Output: Matching municipality name table records in the output array. <br/>
	 
	 
	 314. Municipality abbreviations search <br/>
	 Input: Official municipality name and province. <br/>
	 Output: Municipality abbreviations. <br/>
	 
	 
	 315. Return urban extra information table entries
	 
	 
	 316. Return rural extra information table entries
	 
	 
	 42. Text file search <br/>
	 Input: Text string in address line field. <br/>
	 Output: Postal Code and CPC Text information (company name, building name, etc). <br/>
	 
	 
	 43. Municipalities within province <br/>
	 Input: Municipality name (may be partial) and province. <br/>
	 Output: All municipalities within province starting with input municipality name string. This may be effective for implementing a "drill down" feature. <br/>
	 
	 
	 44. Street names within city and province <br/>
	 Input: Street name (may be partial) in address line field and municipality and province. <br/>
	 Output: All streets in input municipality and province starting with input street name string. This may be effective for implementing a "drill down" feature. <br/>
	 
	 
	 Wildcard Searches <br/>
	 Input any combination of: <br/>
	 SP_IN_ST_NME, <br/>
	 SP_IN_CITY <br/>
	 SP_IN_PROV <br/>
	 The civic number is optional in all cases. These searches allow partial entry of street name and city providing a wildcard capability matching everything which starts with the input string. Large volumes of data may be returned from these searches so it is important to wait until a few characters have been entered before executing the function. Additional information is particularly effective at reducing the size of the result set, especially a civic number and the first character of the municipality and / or province. <br/>
	 QT = 6 Returns a 132-byte format range record for each row in the CPC db matching the input suitable for display. <br/>
	 QT = 7 Returns pairs of records <br/>
	 - 132-byte format range records (as above) 
	 - 232-byte CPC raw data range records
	 QO controls the sort order of the output data <br/>
	 
	 
	 61. (71) Province : Municipality : Wildcard Street Name
	 
	 
	 62. (72) Wildcard Street Name: Municipality : Province
	 
	 
	 63. (73) Province : Wildcard Street Name: Municipality
	 
	 
	 64. (74) Municipality : Wildcard Street Name: Province
	 
	 
	 65. (75) Municipality : Province : Wildcard Street Name
	 
	 
	 66. (76) Wildcard Street Name: Province : Municipality
	 
	 
	 67. (77) Province : Municipality : Simple Street Name
	 
	 
	 68. (78) Simple Street Name : Municipality : Province
	 
	 
	 69. (79) Simple Street Name (No civic number)
	 
	"""
	
	query_option: int
	address_line: str
	city: str
	province: str
	postal_code: str
		#country: str


class caQueryResponse:
	function_messages: list
	status_flag: str
	status_messages: str


class caQueryWildcardRequest:
	"""
	sort_by controls the sort order of the output data <br/>
	 
	 1. Province : Municipality : Wildcard Street Name
	 2. Wildcard Street Name: Municipality : Province
	 3. Province : Wildcard Street Name: Municipality
	 4. Municipality : Wildcard Street Name: Province
	 5. Municipality : Province : Wildcard Street Name
	 6. Wildcard Street Name: Province : Municipality
	 7. Province : Municipality : Simple Street Name
	 8. Simple Street Name : Municipality : Province
	 9. Simple Street Name (No civic number)
	 
	 max_returned
 		The maximum number of results to return, actual maximum is 1000. Null or zero returns default max of 1000.

	"""

	sort_by: int
	address_line: str
	city: str
	province: str
	max_returned: int


class caQueryWildcardResponse:
	response_count: int
	t_exec_ms: int
	address_list: list
	status_flag: str
	status_messages: str



# 133 byte SP 'view' record returned by query level 6 & 7 functions -- NOT used
class caRangeAddress:
	"""
	st_adr_seq_cde: str
	Street Address Sequence Code
	 
	 This code identifies the sequence associated with the range of street numbers. Valid values are: 
	 1. Odd 
	 2. Even 
	 3. Consecutive


	st_adr_frm_nbr: int
	Street Address to Number
	 The highest street number in a range of municipal street addresses.


	st_adr_to_nbr: int
	Street Address from Number
	 The lowest street number in a range of municipal street addresses.


	st_nme: str
	Street Name
	 Official civic name of a roadway or artery


	route_serv_typ_dsc_2: str
	Route Service Type Description for type 2 records
	 The code that identifies the type of route service. Valid values are: 
	 - RR - Rural Route 
	 - SS - Suburban Service 
	 - MR - Mobile Route 
	 - GD - General Delivery 


	route_serv_nbr_2: int
	Route Service Number for type 2 records
	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode


	mncplt_nme: str
	Municipality Name
	 A municipality is any village, town or city in Canada that is recognized as a valid mailing address by Canada Post.


	prov_cde: str
	Province Code
	 Alphabetic code identifying the province geographically. Valid values are accessible through a query function.


	pstl_cde: str
	Postal Code
	 A ten character, alpha numeric combination (ANANAN) assigned to one or more postal addresses. The postal code is an integral part of every postal address in Canada and is required for the mechanized processing of mail. Postal codes are also used to identify various CPC processing facilities and delivery installations.


	orig_rec: str
	Original StreetPerfect internal record when debugging
	"""

	st_adr_seq_cde: str
	st_adr_frm_nbr: int
	st_adr_to_nbr: int
	st_nme: str
	route_serv_typ_dsc_2: str
	route_serv_nbr_2: int
	mncplt_nme: str
	pstl_cde: str
	prov_cde: str
	orig_rec: str




class usAddressRequest:
	firm_name: str
	urbanization_name: str
	address_line: str
	city: str
	state: str
	zip_code: str


class usCorrectionResponse:
	firm_name: str
	urbanization_name: str
	address_line: str
	city: str
	state: str
	zip_code: str
	status_flag: str
	status_messages: str
	function_messages: list


class usParseResponse:
	address_type: str
	street_number: str
	street_pre_direction: str
	street_name: str
	street_type: str
	street_post_direction: str
	secondary_type: str
	secondary_number: str
	service_type: str
	service_number: str
	delivery_point_barcode: str
	congressional_district: str
	county_name: str
	county_code: str
	status_flag: str
	status_messages: str
	function_messages: list


class usSearchResponse:
	"""
	status_flag: str
	Valid
	 * S = Single Response
	 * D = Default Response
	 
	 Invalid or Multiple
	 * I = Invalid
	 * M = Multiple Response
	"""

	response_count: int
	response_address_list: list
	status_flag: str
	status_messages: str
	function_messages: list



# not used
class usDeliveryInformationResponse:
	city_abbreviation: str
	post_office_city: str
	post_office_state: str
	delivery_point_bar_code: str
	carrier_route: str
	auto_zone_indicator: str
	lot_number: str
	lot_code: str
	lacs_code: str
	county_code: str
	finance_number: str
	congressional_district: str
	pmb_designator: str
	pmb_number: str

	status_flag: str
	status_messages: str
	function_messages: list
