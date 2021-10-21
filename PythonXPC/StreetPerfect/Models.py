# just street perfect models used by StreetPerfect.Client - and the site
# models represent the input (request) and the output (response) parameters of
# the low level spaa calls


class caTypeaheadResponse:

	def __init__(self):
		self.count = 0
		self.address_list = []
		self.t_exec_ms = 0


class caAddress:
	"""
	caAddress is the return data record response for /api/ca/search 

	rec_typ_cde = 0
	Record Type Code
 
	 Defines the type of address record. Valid values are:
	 1. Street Address Record
	 2. Street Served by Route Record
	 3. Lock Box Address Record
	 4. Route Service Address Record
	 5. General Delivery Address Record

	adr_typ_cde = 0
	Address Type Code
 
	 A code denoting whether an address is in the form of a civic address or a delivery installation address. Valid values are:
		1. Civic (Street) Address Format
		2. Delivery Installation (Station) Address Format

	prov_cde = ''
	Province Code
 
	 Alphabetic code identifying the province geographically. Valid values are accessible through a query function.

	drctry_area_nme = ''
	Directory Area Name
 
	 Major community or greater municipality grouping that contains the street address or its delivery installation. Should not be used.

	st_nme = ''
	Street Name
 
	 Official civic name of a roadway or artery

	st_typ_cde = ''
	Street Type Code
 
	 Official description used to identify the type of roadway or artery. Valid values are accessible through a query function.

	st_drctn_cde = ''
	Street Direction Code
 
	 Street direction component of an official street name. Valid values are accessible through a query function.

	st_adr_seq_cde = ''
	Street Address Sequence Code
 
	 This code identifies the sequence associated with the range of street numbers. Valid values are: 
	 1. Odd 
	 2. Even 
	 3. Consecutive

	st_adr_to_nbr = 0
	Street Address to Number
 
	 The highest street number in a range of municipal street addresses.

	st_adr_nbr_sfx_to_cde = ''
	Street Address Number Suffix to Code
 
	 The address suffix associated with the street address to number. Examples of street numbers with suffixes are 14 1/2 and 22B. A numeric number denotes a fractional suffix. Valid values are:
	 1. 1/4 
	 2. 1/2
	 3. 3/4

	ste_to_nbr = ''
	Suite to Number
 
	 Highest value in a range of suites or apartments.

	st_adr_frm_nbr = 0
	Street Address from Number

	 The lowest street number in a range of municipal street addresses.

	st_adr_nbr_sfx_frm_cde = ''
	Street Address Number Suffix from Code

	 The address suffix associated with the street address from number. Examples of street numbers with suffixes are 14 1/2 and 22B. A numeric number denotes a fractional suffix. Valid values are:
	 1. 1/4 
	 2. 1/2
	 3. 3/4

	ste_frm_nbr = ''
	Suite from Number

	 Lowest value in a range of suites or apartments.

	mncplt_nme = ''
	Municipality Name

	 A municipality is any village, town or city in Canada that is recognized as a valid mailing address by Canada Post.
	#not used public int? route_serv_box_to_nbr 
	#not used public int? route_serv_box_frm_nbr 

	route_serv_typ_dsc_2 = ''
	Route Service Type Description for type 2 records

	 The code that identifies the type of route service. Valid values are: 
	 - RR - Rural Route 
	 - SS - Suburban Service 
	 - MR - Mobile Route 
	 - GD - General Delivery 

	route_serv_nbr_2 = 0
	Route Service Number for type 2 records

	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode

	di_area_nme = ''
	Delivery Installation Area Name

	 The name of a village, town, municipality or city that forms part of a Delivery Installation Name. While this field is populated, it is USUALLY not required to be displayed as part of the address.

	di_typ_dsc = ''
	Delivery Installation Type Description

	 The category of delivery installation. Valid values are accessible through a query function.

	di_qlfr_nme = ''
	Delivery Installation Qualifier Name

	 When more than one delivery installation serves an area, the qualifier name uniquely identifies the delivery installation.

	lock_box_bag_to_nbr = 0
	Lock Box bag to Number

	 Highest number in a range of lock boxes.

	lock_box_bag_frm_nbr = 0
	Lock Box bag from Number

	 Lowest number in a range of lock boxes.

	route_serv_typ_dsc_4 = ''
	Route Service Type Description for type 4 records

	 The code that identifies the type of route service. Valid values are the same as for type 2 records.

	route_serv_nbr_4 = 0
	Route Service Number for type 4 records

	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode

	pstl_cde = ''
	Postal Code

	 A ten character, alpha numeric combination (ANANAN) assigned to one or more postal addresses. The postal code is an integral part of every postal address in Canada and is required for the mechanized processing of mail. Postal codes are also used to identify various CPC processing facilities and delivery installations.

	#di_pstl_cde = ''
	# Delivery Installation Postal Code
	#
	# The postal code of the delivery installation responsible for delivery to the postal code. Not Used.
	#

	text_record_flag = ''
	Text Record Flag

	 Defines the type of record in the TEXT lookup table 
	 * A = Building name record 
	 * B = Large Volume Receiver Name (Street) record 
	 * C = Government Name (Street) record 
	 * D = Large Volume Receiver Name (PO BOX) record 
	 * E = Government Name (PO BOX) record 
	 * F = General Delivery record

	cntry_cde = ''
	Country Code

	orig_rec = ''
	Original StreetPerfect internal record when debugging
	"""

	def __init__(self):
		self.rec_typ_cde = 0
		self.adr_typ_cde = 0
		self.prov_cde = ''
		self.drctry_area_nme = ''
		self.st_nme = ''
		self.st_typ_cde = ''
		self.st_drctn_cde = ''
		self.st_adr_seq_cde = ''
		self.st_adr_to_nbr = 0
		self.st_adr_nbr_sfx_to_cde = ''
		self.ste_to_nbr = ''
		self.st_adr_frm_nbr = 0
		self.st_adr_nbr_sfx_frm_cde = ''
		self.ste_frm_nbr = ''
		self.mncplt_nme = ''
		self.route_serv_typ_dsc_2 = ''
		self.route_serv_nbr_2 = 0
		self.di_area_nme = ''
		self.di_typ_dsc = ''
		self.di_qlfr_nme = ''
		self.lock_box_bag_to_nbr = 0
		self.lock_box_bag_frm_nbr = 0
		self.route_serv_typ_dsc_4 = ''
		self.route_serv_nbr_4 = 0
		self.pstl_cde = ''
		self.text_record_flag = ''
		self.cntry_cde = ''
		self.orig_rec = ''
	
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

	orig_rec = ''
	Original StreetPerfect record when debugging
	"""
	
	def __init__(self):
		self.RecordType = ''
		self.CityName = ''
		self.StateAbbreviation = ''
		self.ZipCode = ''
		self.PlusFourAddonLow = ''
		self.PlusFourAddonHigh = ''
		self.StreetNumberLow = ''
		self.StreetNumberHigh = ''
		self.StreetPreDirection = ''
		self.StreetName = ''
		self.StreetSuffix = ''
		self.StreetPostDirection = ''
		self.UnitType = ''
		self.UnitNumberLow = ''
		self.UnitNumberHigh = ''
		self.PrivateMailBoxNumber = ''
		self.LocationName = ''
		self.orig_rec = ''


class GetInfoResponse:

	def __init__(self):
		self.info = []
		self.status_flag = ''
		self.status_messages = ''


class caAddressRequest:

	def __init__(self):
		self.recipient = ''
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''


class caCorrectionResponse:
	"""
	status_flag = ''
	* V = Submitted address is Valid
	 * C = Submitted address is Corrected
	 * N = Submitted address is Not correct
	 * F = Submitted address is Foreign
	"""

	def __init__(self):
		self.recipient = ''
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''
		self.extra_information = ''
		self.unidentified_component = ''

		self.status_flag = ''

		self.status_messages = ''
		self.function_messages = []

class caParseResponse:
	"""
	status_flag = ''
	Valid Address
	 * P = Parsed &amp; Valid
	 
	 Invalid Address
	 * I = Parsed &amp; Invalid
	"""
	def __init__(self):
		self.address_type = ''
		self.street_number = ''
		self.street_suffix = ''
		self.street_name = ''
		self.street_type = ''
		self.street_direction = ''
		self.unit_type = ''
		self.unit_number = ''
		self.service_type = ''
		self.service_number = ''
		self.service_area_name = ''
		self.service_area_type = ''
		self.service_area_qualifier = ''
		self.extra_information = ''
		self.unidentified_component = ''
		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []


class caSearchResponse:
	"""
	status_flag = ''

	* N = At least one record found
	 * X = No records found
	"""
	def __init__(self):
		self.response_count = 0
		self.t_exec_ms = 0
		self.response_address_list = []
		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []


# CA legacy non-ProcessAddress functions


class caFetchAddressRequest:

	def __init__(self):
		self.street_number = ''
		self.unit_number = ''
		self.postal_code = ''


class caFetchAddressResponse:

	def __init__(self):
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''
		#country = ''
		self.status_flag = ''
		self.status_messages = ''


class caFormatAddressRequest:

	def __init__(self):
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''
		#country = ''


class caFormatAddressResponse:

	def __init__(self):
		self.format_line_one = ''
		self.format_line_two = ''
		self.format_line_three = ''
		self.format_line_four = ''
		self.format_line_five = ''
		self.status_flag = ''
		self.status_messages = ''


class caValidateAddressRequest:

	def __init__(self):
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''
		#country = ''


class caValidateAddressResponse:

	def __init__(self):
		self.function_messages = []
		self.status_flag = ''
		self.status_messages = ''


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
	
	def __init__(self):
		self.query_option = 0
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.postal_code = ''
		#country = ''


class caQueryResponse:

	def __init__(self):
		self.function_messages = []
		self.status_flag = ''
		self.status_messages = ''


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

	def __init__(self):
		self.sort_by = 0
		self.address_line = ''
		self.city = ''
		self.province = ''
		self.max_returned = 0


class caQueryWildcardResponse:

	def __init__(self):
		self.response_count = 0
		self.t_exec_ms = 0
		self.address_list = []
		self.status_flag = ''
		self.status_messages = ''



# 133 byte SP 'view' record returned by query level 6 & 7 functions -- NOT used
class caRangeAddress:
	"""
	st_adr_seq_cde = ''
	Street Address Sequence Code
	 
	 This code identifies the sequence associated with the range of street numbers. Valid values are: 
	 1. Odd 
	 2. Even 
	 3. Consecutive


	st_adr_frm_nbr = 0
	Street Address to Number
	 The highest street number in a range of municipal street addresses.


	st_adr_to_nbr = 0
	Street Address from Number
	 The lowest street number in a range of municipal street addresses.


	st_nme = ''
	Street Name
	 Official civic name of a roadway or artery


	route_serv_typ_dsc_2 = ''
	Route Service Type Description for type 2 records
	 The code that identifies the type of route service. Valid values are: 
	 - RR - Rural Route 
	 - SS - Suburban Service 
	 - MR - Mobile Route 
	 - GD - General Delivery 


	route_serv_nbr_2 = 0
	Route Service Number for type 2 records
	 Number that identifies Rural Route, Suburban Service or Mobile Route delivery mode


	mncplt_nme = ''
	Municipality Name
	 A municipality is any village, town or city in Canada that is recognized as a valid mailing address by Canada Post.


	prov_cde = ''
	Province Code
	 Alphabetic code identifying the province geographically. Valid values are accessible through a query function.


	pstl_cde = ''
	Postal Code
	 A ten character, alpha numeric combination (ANANAN) assigned to one or more postal addresses. The postal code is an integral part of every postal address in Canada and is required for the mechanized processing of mail. Postal codes are also used to identify various CPC processing facilities and delivery installations.


	orig_rec = ''
	Original StreetPerfect internal record when debugging
	"""

	def __init__(self):
		self.st_adr_seq_cde = ''
		self.st_adr_frm_nbr = 0
		self.st_adr_to_nbr = 0
		self.st_nme = ''
		self.route_serv_typ_dsc_2 = ''
		self.route_serv_nbr_2 = 0
		self.mncplt_nme = ''
		self.pstl_cde = ''
		self.prov_cde = ''
		self.orig_rec = ''




class usAddressRequest:

	def __init__(self):
		self.firm_name = ''
		self.urbanization_name = ''
		self.address_line = ''
		self.city = ''
		self.state = ''
		self.zip_code = ''


class usCorrectionResponse:

	def __init__(self):
		self.firm_name = ''
		self.urbanization_name = ''
		self.address_line = ''
		self.city = ''
		self.state = ''
		self.zip_code = ''
		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []


class usParseResponse:

	def __init__(self):
		self.address_type = ''
		self.street_number = ''
		self.street_pre_direction = ''
		self.street_name = ''
		self.street_type = ''
		self.street_post_direction = ''
		self.secondary_type = ''
		self.secondary_number = ''
		self.service_type = ''
		self.service_number = ''
		self.delivery_point_barcode = ''
		self.congressional_district = ''
		self.county_name = ''
		self.county_code = ''
		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []


class usSearchResponse:
	"""
	status_flag = ''
	Valid
	 * S = Single Response
	 * D = Default Response
	 
	 Invalid or Multiple
	 * I = Invalid
	 * M = Multiple Response
	"""

	def __init__(self):
		self.response_count = 0
		self.response_address_list = []
		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []



# not used
class usDeliveryInformationResponse:

	def __init__(self):
		self.city_abbreviation = ''
		self.post_office_city = ''
		self.post_office_state = ''
		self.delivery_point_bar_code = ''
		self.carrier_route = ''
		self.auto_zone_indicator = ''
		self.lot_number = ''
		self.lot_code = ''
		self.lacs_code = ''
		self.county_code = ''
		self.finance_number = ''
		self.congressional_district = ''
		self.pmb_designator = ''
		self.pmb_number = ''

		self.status_flag = ''
		self.status_messages = ''
		self.function_messages = []
