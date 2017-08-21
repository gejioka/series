import ast
import threading
import Queue
import transmissionrpc
from torrent_structure import *
from files_tools import *
from IMDbManager import *
from FileManagement import *
from PiratebaySearcher import *
from TransmissionManager import *
from series_protocol_log import *
from GlobalVariables import *
from seriesdb_handler import *
from imdbpie import Imdb

class series_protocol:
	def __init__( self, global_variables ):
		'''
			Description:	Initialize a new series_protocol object.	
		'''
		# A variable for root folder path.
		self.root_folder = find_root_path ( )
		# A variable for series download path.
		self.download_path = find_download_path ( )
		# A variable for series informations path.
		self.series_info_path = find_file_with_series_info_path ( )
		# Configure series log file.
		configure_logging ( )
		# Find the level of logging
		find_log_level ( )
		# Create the root folder for series.
		create_root_folder ( )
		# Create a file with series info path.
		create_file_with_series_info ( )
		# A variable for global variables.
		self.global_variables = global_variables
		# A variable for series queue.
		self.series_queue = Queue.Queue ( )
		# A variable for main thread of protocol.
		self.main_thread_t = threading.Thread ( target=self.main_thread )
		# Start main thread.
		self.main_thread_t.start ( )

	def add_new_serie ( self, serie_info ):
		'''
			Description:	Add a new serie to series queue.
		'''
		self.series_queue.put ( serie_info )

	def get_serie_from_queue ( self ):
		'''
			Description:	Return the next serie of the queue.
		'''
		return self.series_queue.get ( )

	def delete_existing_serie ( self, serie_info ):
		pass

	def delete_serie_season ( self, serie_season ):
		pass

	def delete_serie_episode ( self, serie_episode ):
		pass

	def print_all_series ( self ):
		pass

	def add_existing_series_to_queue ( self ):
		'''
			Description:	Add all series is stored to file in a queue.
			Headers:		'n' for new serie
							'e' for existing serie
		'''

		# Open series informations file.
		file=None
		try:
			file = open ( self.series_info_path, 'r' )
		except Exception as err:
			write_error_message ( '[!] ' + str ( err ) )

		# Read all file and put all contents to a queue.
		try:
			for line in file:
				# Create serie info structure and add a new header.
				curr = ast.literal_eval ( line )
				# Write debug message to log file.
				write_debug_message ( '[+] Main thread added serie with name ' + str ( curr['serie_name'] ) + ' to queue.' )
				# Write info message to log file.
				write_info_message ( '[+] Main thread add a new task to queue.')
				# Create serie structure to add it to queue.
				serie_info = {	'header' 		: 'e',
								'serie_name' 	: curr['serie_name'],
								'serie_season' 	: curr['serie_season'],
								'serie_episode' : curr['serie_episode'],
								'serie_id' 		: curr['serie_id'] }
								
				# Add serie to queue.
				self.series_queue.put ( serie_info )
		except Exception as e:
			# Write error message to series log file.
			write_error_message ( '[!] ' + str ( e ) )
		
		# Close file.
		try:
			file.close ( )
		except Exception as err:
			write_error_message ( '[!] ' + str ( err ) )

	def find_torrent_object ( self, curr_serie ):
		'''
			Description:	Search list of torrents and return torrent object with same id.
		'''
		for current_torrent in self.global_variables.get_list_of_torrents ( ):
			if current_torrent.get_serie_id ( ) == curr_serie['serie_id'] and int ( current_torrent.get_serie_season ( ) ) == int ( curr_serie['serie_season'] ) \
				and int ( current_torrent.get_serie_episode ( ) ) == int ( curr_serie['serie_episode'] ):
				return current_torrent

	def download_new_episodes ( self ):
		pass

	def main_thread ( self ):
		file_management=None
		current_torrent=None
		piratebaySearcher=None
		torrent=None
		imdb=None
		next_episode=None

		# Write info message to log file.
		write_info_message ( '[!] Created series protocol main thread.' )
		# Add new task to queue.
		self.add_existing_series_to_queue ( )

		write_debug_message ( '[+] There are ' + str ( self.series_queue.qsize ( ) ) + ' available tasks for the protocol.' )
		
		while True:
			# Get next available task from queue.
			curr_serie = self.get_serie_from_queue ( )
			# Write info message to log file.
			write_info_message ( '[+] Thread get next available task.')
			
			if curr_serie['header'] == 'n':
				# Write debug message to log file.
				write_debug_message ( '[-] A new serie with name ' + str ( curr_serie['serie_name'] ) + ' has appeared to queue. This serie' + \
											' has id ' + str ( curr_serie['serie_id'] ) + ' and the first episode that requested from user is ' + \
												str ( curr_serie['serie_season'] ) + ' season and ' + str ( curr_serie['serie_episode'] ) + ' episode.' )

				# Find correct torrent object of list.
				current_torrent = self.find_torrent_object ( curr_serie )
				# Create a file_management object.
				file_management =  FileManagement.FileManagement ( current_torrent, self.global_variables )
				# Create a piratebay searcher object.
				piratebaySearcher = PiratebaySearcher.PiratebaySearcher ( file_management, current_torrent, self.global_variables.get_transmission_client ( ), self.global_variables )
				# Start piratebay searcher.
				piratebaySearcher.start ( )
				# Change header to exist.
				curr_serie['header'] = 'e'

				# Create a new imdb object.
				imdb = IMDbManager ( )

				# Return current episode.
				current_episode = imdb.find_current_episode ( current_torrent.get_serie_name ( ), current_torrent.get_serie_season ( ), current_torrent.get_serie_episode ( ), current_torrent.get_serie_id ( ) )

				# Add new serie season and episode to seriesdb.
				add_new_serie_to_db ( self.global_variables.get_db_connection ( ), curr_serie['serie_name'], curr_serie['serie_id'], curr_serie['year'] )
				add_new_season ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], curr_serie['serie_season'] )
				season_id = get_season_id ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], curr_serie['serie_season'] )[0]
				add_new_episode ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], season_id, current_episode.title, 'unseen', current_episode.release_date, current_episode.type )

			elif curr_serie['header'] == 'e':
				# Write debug message to log file.
				write_debug_message ( '[-] Next task is the ' + str ( curr_serie['serie_episode'] ) + ' episode from ' + str ( curr_serie['serie_season'] ) + \
											' season of serie with name ' + str ( curr_serie['serie_name'] ) + '.' )
				# Create a new torrent object.
				torrent = torrent_structure ( )
				# Create a new imdb object.
				imdb = IMDbManager ( )

				next_episode = imdb.find_next_episode ( curr_serie['serie_name'], curr_serie['serie_season'], curr_serie['serie_episode'], curr_serie['serie_id'] )

				# Set all fields of torrent object.	
				torrent.set_serie_name ( curr_serie['serie_name'] )
				torrent.set_serie_season ( next_episode.season )
				torrent.set_serie_episode ( next_episode.episode )
				torrent.set_serie_id ( curr_serie['serie_id'] )
				torrent.create_serie_info ( )

				# Add torrent to list of torrents.
				self.global_variables.add_torrent_to_list_of_torrents ( torrent )

				# Create a file_management object.
				file_management = FileManagement.FileManagement ( torrent, self.global_variables )
				# Find correct torrent object of list.
				current_torrent = self.find_torrent_object ( torrent.get_serie_info ( ) )
				# Create a piratebay searcher object.
				piratebaySearcher = PiratebaySearcher.PiratebaySearcher ( file_management, current_torrent, self.global_variables.get_transmission_client ( ), self.global_variables )
				# Start piratebay searcher.
				piratebaySearcher.start ( )

				# Return all series seasons.
				seasons = get_all_serie_seasons ( self.global_variables.get_db_connection ( ), curr_serie['serie_name'] )
				
				# Check if season exists.
				new_season=True
				for season in seasons:
					if  next_episode.season <= season[2]: 
						new_season=False

				# If season doesn't exist add it to seriesdb.
				if new_season:
					add_new_season ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], next_episode.season )

				# Add episode to seriesdb.
				season_id = get_season_id ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], next_episode.season )[0]
				add_new_episode ( self.global_variables.get_db_connection ( ), curr_serie['serie_id'], season_id, next_episode.title, 'unseen', next_episode.release_date, next_episode.type )

			elif curr_serie['header'] == 'q':
				# Write debug message to log file.
				write_debug_message ( '[!] Next task is the quit option of the user.' )
				if len ( self.global_variables.get_status_list ( ) ) == 0:
					break
				else:
					self.global_variables.get_exit_event ( ).wait ( )
					break
			else:
				# TODO: Code for bad header.
				pass

		# Write info message to log file.
		write_info_message ( 'Main thread of series protocol close without errors.' )