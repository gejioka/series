import threading

class GlobalVariables:

	def __init__( self, transmission_client ):
		'''
			Description:	Initialize a GlobalVariables object.
		'''
		self.transmission_client = transmission_client
		self.list_of_torrents=[]
		self.status_list=[]
		self.exit_event=threading.Event ( )
		self.exit_event.clear ( )
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

	def add_member_to_status_list ( self, member, status ):
		'''
			Description:	Add a new member with its status to list.
		'''
		with self.lock:
			self.status_list.append ({	'member' 	: member,
										'status'  	: status })

	def remove_member_from_status_list ( self, member ):
		'''
			Description:	Remove the specific member of the list.
		'''
		with self.lock:
			self.status_list = [ x for x  in self.status_list if x['member'] != member ]

	def get_status_list ( self ):
		'''
			Description:	Return status list.
		'''
		return self.status_list

	def get_exit_event ( self ):
		'''
			Description:	Return the exit event.
		'''
		return self.exit_event