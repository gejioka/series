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
from GlobalVariables import *

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
		# Create a file with series info path.
		create_file_with_series_info ( )
		# A variable for global variables.
		self.global_variables = global_variables
		# A variable for main thread of protocol.
		self.main_thread_t = threading.Thread ( target=self.main_thread )
		# Start main thread.
		self.main_thread_t.start ( )
		# A variable for series queue.
		self.series_queue = Queue.Queue ( )

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
					Headers:	'n' for new serie
							'e' for existing serie
		'''

		# Open series informations file.
		file = open ( self.series_info_path, 'r' )

		# Read all file and put all contents to a queue.
		try:
			for line in file:
				print line
				# Create serie info structure and add a new header.
				curr = ast.literal_eval ( line )
				serie_info = {	'header' 	: 'e',
						'serie_name' 	: curr['serie_name'],
						'serie_season' 	: curr['serie_season'],
						'serie_episode' 	: curr['serie_episode'],
						'serie_id' 	: curr['serie_id'] }

				# Set serie info for this object.
				#self.torrent.set_serie_info ( serie_info )
				# Add serie to queue.
				self.series_queue.put ( serie_info )
		except Exception as e:
			print e
			print 'There is no serie in file.'
		
		# Close file.
		file.close ( )

	def find_torrent_object ( self, curr_serie ):
		'''
			Description:	Search list of torrents and return torrent object with same id.
		'''
		for current_torrent in self.global_variables.get_list_of_torrents ( ):
			print current_torrent.get_serie_id ( )
			print curr_serie['serie_id']
			print current_torrent.get_serie_season ( )
			print curr_serie['serie_season']
			print current_torrent.get_serie_episode ( )
			print curr_serie['serie_episode']
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

		self.add_existing_series_to_queue ( )
		
		while True:
			curr_serie = self.get_serie_from_queue ( )
			
			if curr_serie['header'] == 'n':
				# Find correct torrent object of list.
				current_torrent = self.find_torrent_object ( curr_serie )
				# Create a file_management object.
				file_management =  FileManagement.FileManagement ( current_torrent, self.global_variables )
				# Create a piratebay searcher object.
				piratebaySearcher = PiratebaySearcher.PiratebaySearcher ( file_management, current_torrent, self.global_variables.get_transmission_client ( ) )
				# Start piratebay searcher.
				piratebaySearcher.start ( )
				# Change header to exist.
				curr_serie['header'] = 'e'

			elif curr_serie['header'] == 'e':
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
				piratebaySearcher = PiratebaySearcher.PiratebaySearcher ( file_management, current_torrent, self.global_variables.get_transmission_client ( ) )
				# Start piratebay searcher.
				piratebaySearcher.start ( )
			else:
				# TODO: Code for bad header.
				pass