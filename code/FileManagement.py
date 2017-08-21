import os
import os.path
import re
import ast
import requests
from difflib import SequenceMatcher
from series_protocol_log import *
from files_tools import *

class FileManagement:
	root_folder=None
	download_path_of_series=None
	path_for_episode=None
	file_name_pattern=None
	serie_info=None
	is_junk=None
	filename=None
	file_with_series_info=None
	series_info_path=None
	global_variables=None
	list_with_series_info=[]

	def __init__( self, torrent_object, global_variables ):
		'''
			Description:	Initialize a FileManagement object. 
		'''
		self.torrent_object = torrent_object
		self.global_variables = global_variables		
		self.set_root_folder ( find_root_path (  ) )
		self.set_download_path_of_series ( find_download_path (  ) )
		self.set_series_info_path ( find_file_with_series_info_path ( ) )

	def set_root_folder ( self, root_folder ):
		'''
			Description:	Set the root folder path.
		'''
		self.root_folder=root_folder

	def get_root_folder ( self ):
		'''
			Description:	Return the root folder path.
		'''
		return self.root_folder

	def set_download_path_of_series ( self, download_path_of_series ):
		'''
			Description:	Set the download path of series.
		'''
		self.download_path_of_series = download_path_of_series

	def get_download_path_of_series ( self ):
		'''
			Description:	Return the download path of series.
		'''
		return download_path_of_series

	def set_series_info_path ( self, series_info_path ):
		'''
			Description:	Set the series info path.
		'''	
		self.series_info_path = series_info_path

	def get_series_info_path ( self ):
		'''
			Description:	Return the series info path.
		'''
		return self.series_info_path

	def create_file_name_pattern ( self ):
		'''
			Description:	Create the name for this serie episode.
		'''
		self.file_name_pattern=self.torrent_object.get_serie_name ( ).title ( ) + "S" + str( self.torrent_object.get_serie_season ( ) ).zfill ( 2 ) + "E" + str( self.torrent_object.get_serie_episode ( ) ).zfill ( 2 )

	def set_file_name_pattern ( self, file_name_pattern ):
		'''
			Description:	Set the name for this episode.
		'''
		self.file_name_pattern=file_name_pattern

	def get_file_name_pattern ( self ):
		'''
			Description:	Return the name for this serie.
		'''
		return self.file_name_pattern

	def set_torrent_name ( self, filename ):
		'''
			Description:	Set the serie torrent name.
		'''
		self.filename = filename

	def get_torrent_name ( self ):
		'''
			Description:	Return the serie torrent name.
		'''
		return filename

	def set_list_with_series_info ( self, list_with_series_info ):
		'''
			Description:	Set the list with serie informations.
		'''
		self.list_with_series_info = list_with_series_info

	def create_path_for_episode ( self ):
		'''
			Description:	Create the path for episode.
		'''
		self.path_for_episode = self.root_folder + self.torrent_object.get_serie_name ( ) + "/" + "Season " + str ( self.torrent_object.get_serie_season ( ) ) + "/" + "Episode " + str ( self.torrent_object.get_serie_episode ( ) ) + "/"

	def set_path_for_episode ( self, path_for_episode ):
		'''
			Description:	Set the path for this episode.
		'''
		self.path_for_episode=path_for_episode

	def get_path_for_episode ( self ):
		'''
			Description:	Return the path for this episode.
		'''
		return self.path_for_episode

	def set_is_junk ( self, is_junk ):
		'''
			Description:	Set if the this episode is already exists.
		'''
		self.is_junk = is_junk

	def get_is_junk ( self ):
		'''
			Description:	Return if this episode is already exists.
		'''
		return self.is_junk

	def write_serie_info_to_file ( self, serie_info ):
		'''
			Description:	Write new serie or update old.
		'''
		with self.global_variables.get_lock ( ):
			# Open file with series info for reading.
			target=None
			try:
				target = open ( self.series_info_path, 'r' )
			except Exception as err:
				write_error_message ( '[!] ' + str ( err ) )

			# Read all file.
			data = [x.strip('\n') for x in target.readlines ( )]
			
			# Close file.
			try:
				target.close ( )
			except Exception as err:
				write_error_message ( '[!] ' + str ( err ) )

			# Try to find serie with same id and update it.
			count=0
			serie_dict={}
			for serie in data:
				try:
					serie_dict = ast.literal_eval ( serie )
				except Exception as err:
					write_error_message ( '[!] ' + str ( err ) )

				if serie_dict['serie_id'] == serie_info['serie_id']:
					data[count] = str ( serie_info )
				count += 1
			data_str = "\n".join ( data )
			# Check if serie is the first serie.
			if len ( data ) == 0:
				data_str = str ( serie_info )
				# Write debug message to series log file.
				write_info_message ( '[+] Add a new serie to .series_info file.' )
				write_debug_message ( '[+] Wrote a new serie with name ' + str ( serie_info['serie_name'] ) + ' to .series_info file.')

			# Open a file for writing.
			with  open ( self.series_info_path, 'w' ) as target:
				# Write updated serie to file.
				target.write ( data_str )
				# Write an info message to series log file.
				write_info_message ( '[+] Updated an existance serie.' )
				# Write a debug mesage to series log file.
				write_debug_message ( '[+]Add existance serie with name ' + str ( serie_info['serie_name'] ) + ' to .series_info file.' )
		
	def create_folders_for_series ( self, root_folder="", serie_name="", serie_season="", serie_episode="" ):
		'''
			Description:	Create the folder for this serie.
		'''
		try:
			if not os.path.exists ( root_folder + serie_name + serie_season + serie_episode ):
				os.makedirs ( root_folder + serie_name + serie_season + serie_episode )
		except Exception as err:
			write_error_message ( '[!] ' + str ( err ) )
			
		if serie_season == "":
			self.create_folders_for_series ( root_folder, serie_name, "/Season " + str ( self.torrent_object.get_serie_season ( ) ) + "/" )
			# Write an info message to series log file.
			write_info_message ( '[+] Create a new folder for season.' )
			# Write a debug message to series log file.
			write_debug_message ( '[+] Create a new folder for season ' + str ( serie_season ) + ' of serie with name ' + str ( serie_name ) + '.' )
		elif serie_episode == "":
			self.create_folders_for_series ( root_folder, serie_name, str ( serie_season ), "Episode " + str ( self.torrent_object.get_serie_episode ( ) ) + "/" )
			# Write an info message to series log file.
			write_info_message ( '[+] Create new folder for episode.' )
			# Write a debug message to series log file.
			write_debug_message ( '[+] Create a new folder for episode ' + str ( serie_episode ) + ' of season ' + str ( serie_season ) + ' of serie with name ' + str ( serie_name ) + '.' )
		else:
			# Write debug message to series log file.
			write_debug_message ( '[!] Create all subfolders for this episode succesfull.' )

	def similar ( self, first_file, second_file ):
		'''
			Description:	Find how similar are two different files.
		'''

		return SequenceMatcher ( None, first_file, second_file ).ratio ( )

	def find_similar_file ( self ):
		'''
			Description:	Find the most similar file with specific filename and return it.
		'''
		similar_w = 0
		filename = ''
		for file in os.listdir ( self.download_path_of_series ):
			if self.similar ( file, str ( self.filename ) ) > similar_w:
				similar_w = self.similar ( file, self.filename )
				filename = file

		return similar_w, filename

	def place_serie_to_right_folder ( self ):
		'''
			Description:	Place this serie to right folder.
		'''
		try:
			self.create_path_for_episode ( )
			similar_w, correct_file = self.find_similar_file ( )
			if os.path.isdir ( self.download_path_of_series + correct_file ):
				for file in os.listdir ( self.download_path_of_series + correct_file ):
					os.rename ( os.path.realpath ( self.download_path_of_series + correct_file + '/' + file ), self.path_for_episode + file )
					# Write info message to series log file.
					write_info_message ( '[+] Replace a file to correct folder.' )
					# Write debug message to series log file.
					write_debug_message ( '[+] Replace file with name ' + str ( file ) + ' to ' + str ( self.path_for_episode + file ) + ' path.' )
				# Write info message to series log file.
				write_info_message ( '[-] Remove folder for download path.' )
				# Remove folder.
				os.rmdir ( self.download_path_of_series + correct_file )
			else:
				os.rename ( os.path.realpath ( self.download_path_of_series + correct_file ), self.path_for_episode + correct_file )
				# Write info message to series log file.
				write_info_message ( '[+] Replace a file to correct folder.' )
				# Write debug message to series log file.
				write_debug_message ( '[+] Replace episode file with name ' + str ( correct_file ) + ' to ' + str ( self.path_for_episode + correct_file ) + ' path.' )
		except Exception as e:
			# Write error message to series log file.
			write_error_message ( str ( e ) ) 

	def user_input ( self ):
		'''
			Description:	Add the user input in a dictionary structure.
		'''
		self.serie_info= { 	"serie_name" : self.serie_name,
							"serie_season" : self.serie_season,
							"serie_episode" : self.serie_episode }