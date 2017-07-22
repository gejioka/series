import time
import datetime
import threading
import transmissionrpc
import FileManagement
import PiratebaySearcher

class transmission_manager (threading.Thread):

	def __init__( self, transmission_manager, file_management, curr_torrent, global_variables ):
		'''
			Description:	Initialize a transmission_manager object.
		'''
		threading.Thread.__init__(self)
		self.transmission_manager = transmission_manager
		self.file_management = file_management
		self.curr_torrent = curr_torrent
		self.global_variables = global_variables

	def run ( self ):
		'''
			Description:	It's the code which threads run.
		'''
		dynamic_sleep_time=5
		max_sleep_time=120
		self.global_variables.add_member_to_status_list ( threading.current_thread ( ), 'r' )

		while True:
			try:
				self.torrent = self.transmission_manager.get_torrent ( self.torrent_id )
				if self.torrent.status == 'downloading':
					if dynamic_sleep_time > max_sleep_time / 2:
						dynamic_sleep_time = 5
					if self.torrent.eta.total_seconds ( ) > max_sleep_time:
						dynamic_sleep_time += 5
						print ( 'Thread sleep for ' + str ( dynamic_sleep_time ) + ' seconds.' )	
						time.sleep ( dynamic_sleep_time )
					else:
						dynamic_sleep_time = self.torrent.eta.total_seconds ( )
						print ( 'Thread sleep for ' + str ( dynamic_sleep_time ) + ' seconds.' )
						time.sleep ( dynamic_sleep_time )
				else:
					self.transmission_manager.stop_torrent( self.torrent.id )
					self.transmission_manager.remove_torrent( self.torrent.id )

					self.file_management.create_folders_for_series ( self.file_management.get_root_folder ( ), self.curr_torrent.get_serie_name ( ) )
					self.file_management.place_serie_to_right_folder ( )
					
					#Write serie's informations to file.
					self.file_management.write_serie_info_to_file ( self.curr_torrent.get_serie_info ( ) )

					break
			except ValueError as e:
				print ( e )
				time.sleep ( 5 )

		# Remove member from status list.
		self.global_variables.remove_member_from_status_list ( threading.current_thread ( ) )
		# Wake up the main thread if there are no threads on status list.
		if len ( self.global_variables.get_status_list ( ) ) == 0:
			self.global_variables.get_exit_event ( ).set ( )

	def set_transmission_manager ( self, transmission_manager ):
		'''
			Description:	Set the transmission_manager.
		'''
		self.transmission_manager = transmission_manager

	def get_transmission_manager ( self ):
		'''
			Description:	Return the transmission_manager.
		'''
		return self.transmission_manager

	def set_torrent_id ( self, torrent_id ):
		'''
			Description:	Set the torrent id.
		'''
		self.torrent_id = torrent_id

	def get_torrent_id ( self ):
		'''
			Description:	Return the torrent id.
		'''
		return torrent_id

	def set_torrent ( self, torrent ):
		'''
			Description:	Set the torrent.
		'''
		self.torrent = torrent

	def get_torrent ( self ):
		'''
			Description:	Return the torrent.
		'''
		return torrent

	def add_torrent_to_transmission ( self, manget_link ):
		'''
			Description:	Add a new torrent to transmission.
		'''
		self.torrent = self.transmission_manager.add_torrent ( manget_link )

	def set_torrents_list ( self, torrents_list ):
		'''
			Description:	Set the list of torrents.
		'''
		self.torrents_list = torrents_list

	def get_torrents_list ( self ):
		'''
			Description:	Return the torrent list.
		'''
		return self.torrents_list
