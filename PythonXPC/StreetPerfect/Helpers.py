import ctypes
from .Models import caAddress, usAddress

class OutString:
	""" used for return parameters from SP """
	
	def __init__(self, buf_size = 2000):
		self.s = ctypes.create_string_buffer(bytes(b' ')*buf_size)

	def ToString(self): 
		s = self.s.value.decode(encoding='ascii', errors='ignore').strip()
		return s

	def ToInt(self): 
		return int(self.ToString())

	def ToList(self):
		ret = []

		for s in self.ToString().split('\n'):
			sx = s.strip()
			if len(sx) > 0:
				ret.append(sx)
		
		if len(ret) > 0:
			ret.pop(0)
		return ret;

	def ToCaAddrList(self, rec_cnt, debug = False):
		addr_list = []
		helper = caAddressHelper()
		buf = self.ToString()
		for raw_rec in buf.split('\r\n'):
			addr_list.append(helper.MakeCaAddressObject(raw_rec, debug))
		return addr_list


class AddressHelper:

	def MakeAddressObject(self, newRec, sp_addr_bytes, _rec_name, _rec_pos, _rec_len):
		field_index = 0
		num_fields = len(_rec_name)
		row_len = len(sp_addr_bytes)
		for field_name in _rec_name:
			f_pos = _rec_pos[field_index]
			f_len = _rec_len[field_index]
			field_index += 1
			try:
				#field_val = sp_addr_bytes[f_pos:f_pos+f_len].decode(encoding='ascii', errors='ignore').strip()
				field_val = sp_addr_bytes[f_pos:f_pos+f_len].strip()
				if len(field_val):
					if type(getattr(newRec, field_name)) is int:
						field_val = int(field_val)
					setattr(newRec, field_name, field_val)
			except Exception as e:
				print(str(e))

		return newRec


class caAddressHelper(AddressHelper):
	"""returns a caAddress object from the fixed SP rec"""
	CA_rec_name = ( "rec_typ_cde", "adr_typ_cde", "prov_cde", "drctry_area_nme", "st_nme", "st_typ_cde", "st_drctn_cde", "st_adr_seq_cde"
			, "st_adr_to_nbr", "st_adr_nbr_sfx_to_cde", "ste_to_nbr", "st_adr_frm_nbr", "st_adr_nbr_sfx_frm_cde", "ste_frm_nbr", "mncplt_nme"
			, "route_serv_typ_dsc_2", "route_serv_nbr_2", "di_area_nme", "di_typ_dsc", "di_qlfr_nme", "lock_box_bag_to_nbr"
			, "lock_box_bag_frm_nbr", "route_serv_typ_dsc_4", "route_serv_nbr_4", "pstl_cde", "text_record_flag", "cntry_cde" )
	CA_rec_pos = ( 0, 1, 2, 4, 34, 64, 70, 72, 73, 79, 80, 86, 92, 93, 99, 139, 141, 145, 175, 180, 195, 200, 205, 207, 211, 228, 229 )
	CA_rec_len = ( 1, 1, 2, 30, 30, 6, 2, 1, 6, 1, 6, 6, 1, 6, 30, 2, 4, 30, 5, 15, 5, 5, 2, 4, 10, 1, 3 )
	CA_num_fields = 27
	min_rec_len = 232

	def MakeCaAddressObject (self, sp_addr_str, add_orig = False):
		newRec = caAddress()
		if add_orig:
			newRec.orig_rec = sp_addr_str.strip('\r\n')
		return self.MakeAddressObject(newRec, sp_addr_str, self.CA_rec_name, self.CA_rec_pos, self.CA_rec_len)


