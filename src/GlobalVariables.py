import threading

class GlobalVariables:

	def __init__( self, transmission_client ):
		'''
			Description:	Initialize a GlobalVariables object.
		'''
		self.transmission_client = transmission_client
		self.list_of_torrents=[]
		self.lock=threading.Lock ( )

	def get_transmission_client ( self ):
		'''
			Description:	Return the transmission client.
		'''
		return self.transmission_client

	def add_torrent_to_list_of_torrents ( self, torrent ):
		'''
			Description:	Add a new torrent to list of torrents.
		'''
		self.list_of_torrents.append ( torrent )

	def remove_torrent_from_list_of_torrents ( self, torrent ):
		'''
			Description:	Remove torrent from list of torrents.
		'''
		self.list_of_torrents.remove ( torrent )

	def set_list_of_torrents ( self, list_of_torrents ):
		'''
			Description:	Set list of torrents.
		'''
		self.list_of_torrents = list_of_torrents

	def get_list_of_torrents ( self ):
		'''
			Description:	Return list of torrents.
		'''
		return self.list_of_torrents

	def get_lock ( self ):
		'''
			Return the lock.
		'''
		return self.lock