import os
import os.path
from series_protocol_log import *

######## Global variables ########
root_folder=None
download_path_of_series=None
file_with_series_info=None
######## End global vars ########

def find_root_path ( ):
	'''
		Description:	Find the root folder path.
	'''
	global root_folder

	root_folder = os.path.abspath ( '../' ) + '/series/'
	return root_folder

def find_download_path ( ):
	'''
		Description:	Find the download folder path.
	'''
	global download_path_of_series

	download_path_of_series = os.path.expanduser("~") + '/Downloads/'
	return download_path_of_series

def find_file_with_series_info_path ( ):
	'''
		Description:	Find the file with series informations.
	'''
	global root_folder
	global file_with_series_info

	file_with_series_info = root_folder + '.series_info'
	return file_with_series_info

def create_root_folder ( ):
	'''
		Description:	Create the root folder if doesn't exists.
	'''
	global root_folder
	
	if not os.path.exists ( root_folder ):
		os.makedirs ( root_folder )

	# Write messages to series log file.
	write_info_message ( '[+] Root folder created' )
	write_debug_message ( '[+] Root folder created and the real path is: ' + str ( os.path.abspath ( root_folder ) ) )

def create_file_with_series_info ( ):
	'''
		Description:	Create the file with series informations.
	'''
	global file_with_series_info

	try:
		if not os.path.exists ( file_with_series_info ):
			open ( file_with_series_info, 'a' ).close ( )
	except Exception as err:
		# Write error message to series log file.
		write_error_message ( '[!] ' + str ( err ) )