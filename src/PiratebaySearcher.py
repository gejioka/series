from bs4 import BeautifulSoup
import FileManagement
import threading
import requests
import transmissionrpc
import TransmissionManager
import re

class PiratebaySearcher(threading.Thread):
	# A variable for the basic piratebay URL.
	basic_URL=None
	# A variable for mutual excusion.
	lock=None
	# A variable for requested URL.
	requested_URL=None
	# A variable of requested URL in string.
	requested_URL_string=None
	# A variable for HTML parser.
	html_parser=None
	# A variable for torrent name.
	torrent_name=None
	# A variable for magnet of this torrent.
	torrent_magnet=None
	# A variable for the transmission manager.
	transmission_manager=None
	# A variable for most popular torrents (optional). 
	most_popular_torrents_info=None

	def __init__( self, file_management, torrent, transmission_manager, basic_URL='https://thepiratebay.org/' ):
		'''
			Description:	Initialize a PiratebaySearcher object.
		'''
		threading.Thread.__init__(self)
		# Create lock.
		self.lock = threading.Lock ( )
		self.lock.acquire ( )
		# A variable for the specific torrent.
		self.torrent = torrent
		# Set basic URL.
		self.basic_URL = basic_URL
		# Initialize list with most popular torrents informations (optional).
		self.most_popular_torrents_info=[]
		# Set file management.
		self.file_management = file_management
		# Set transmission manager. 
		self.transmission_manager = transmission_manager

	def run ( self ):
		'''
			Description:	It's the code which threads run.
		'''
		#self.lock.acquire ( )

		# Check if the specific episode is garbage.
		#if not self.file_management.get_is_junk ( ):

		# Create requested URL in string.
		self.create_requested_URL_string ( self.torrent.get_serie_name ( ), self.torrent.get_serie_season ( ), self.torrent.get_serie_episode ( ) )
		# Find five most popular torrents (optional). 
		self.find_five_most_popular_torrents_info ( self.torrent.get_serie_name ( ) )
		try:
			# Create a transmission manager object.
			torrentThread = TransmissionManager.transmission_manager ( self.transmission_manager, self.file_management, self.torrent )
			# Add first torrent to transmission.
			torrentThread.add_torrent_to_transmission ( self.most_popular_torrents_info[0]['torrent_magnet'] )
			for current_torrent in self.transmission_manager.get_torrents ( ):
				if self.most_popular_torrents_info[0]['torrent_name'] == current_torrent.name:
					# Set torrent name.
					self.file_management.set_torrent_name ( current_torrent.name )
					# Set torrent id.
					torrentThread.set_torrent_id ( current_torrent.id )
					# Start transmission thread.
					torrentThread.start ( )
				elif '+' in current_torrent.name and self.most_popular_torrents_info[0]['torrent_name'] == current_torrent.name.replace ( '+', ' ' ):
					# Set torrent name.
					self.file_management.set_torrent_name ( current_torrent.name )
					# Set torrent id.
					torrentThread.set_torrent_id ( current_torrent.id )
					# Start transmission thread.
					torrentThread.start ( )
					
		except Exception as e:
			print ( e )

	def set_lock ( self, lock ):
		'''
			Description:	Set the lock.
		'''
		self.lock = lock

	def get_lock ( self ):
		'''
			Description:	Return the lock.
		'''
		return self.lock

	def create_requested_URL_string ( self, serie_name, serie_season, serie_episode ):
		'''
			Description:	Create the url string.
		'''
		serie_name = serie_name.lower ( ).replace ( ' ', '%20' )
		serie_season = 's' + str ( serie_season ).zfill ( 2 )
		serie_episode = 'e' + str ( serie_episode ).zfill ( 2 )

		self.requested_URL_string = self.basic_URL + 'search/' + serie_name + '%20' + serie_season + serie_episode + '/0/99/0'
		self.set_requested_URL ( )
		self.set_html_parser ( )

	def set_requested_URL_string ( self, requested_URL_string ):
		'''
			Description:	Set the requested url.
		'''
		self.requested_URL_string = requested_URL_string

	def get_requested_URL_string ( self ):
		'''
			Description:	Return the requested url.
		'''
		return self.requested_URL_string

	def set_requested_URL ( self ):
		'''
			Description:	Set the requested URL.
		'''
		self.requested_URL = requests.get ( self.requested_URL_string )

	def get_requested_URL ( self ):
		'''
			Description:	Return the requested URL.
		'''
		return self.requested_URL

	def set_html_parser ( self ):
		'''
			Description:	Set the html parser.
		'''
		self.html_parser = BeautifulSoup ( self.requested_URL.text, 'html.parser' )

	def get_html_parser ( self ):
		'''
			Description:	Return the html parser.
		'''
		return self.html_parser

	def find_five_most_popular_torrents_info ( self, serieName ):
		'''
			Description:	Find the most popular torrents.
		'''
		current_name=None
		count=0
		pattern_name = re.compile ( ('.*') +  serieName.lower ( ).replace ( ' ', '.' ) + ('.*') )
		pattern_magnet = re.compile ( 'magnet' )

		for a_tag in self.html_parser.find_all ( 'a' ):
			if ( pattern_name.match ( a_tag.text.lower ( ) ) ):
				current_name = a_tag.text
			if ( pattern_magnet.match ( a_tag.attrs['href'] ) ):
				self.most_popular_torrents_info.append({ 	'torrent_name' 		: current_name,
										'torrent_magnet'	: a_tag.attrs['href']})
				count+=1
			
			if ( count >= 5 ):
				break

	def get_five_most_popular_torrents_info ( self ):
		'''
			Description:	Return the most popular torrents.
		'''
		return self.most_popular_torrents_info


######################## Testing ##########################
'''
file_management = file_management.file_management ( )
file_management.createRootFolder ( )
file_management.createFileWithSeriesInfo ( )
file_management.parseFileName ('Arrow.S05E05.HDTV.x264-LOL[ettv]')
file_management.writeSeriesInfoToFile ( )
file_management.createFoldersForSeries ( file_management.getRootFolder ( ), file_management.getSerieName ( ) + "/" )
file_management.createPathForEpisode ( )

piratebaySearcher = PiratebaySearcher ( )
piratebaySearcher.createrequested_URLString ( file_management.getSerieName ( ), file_management.getSerieSeason ( ), file_management.getSerieEpisode ( ) )
piratebaySearcher.setrequested_URL ( )
piratebaySearcher.sethtml_parser ( )
piratebaySearcher.findFivemost_popular_torrents_info ( file_management.getSerieName ( ) )
'''
'''
file_management = file_management.file_management ( )
file_management.createRootFolder ( )
file_management.createFileWithSeriesInfo ( )
file_management.parseFileName ("Supernatural S01E01 HDTV")
file_management.writeSeriesInfoToFile ( )
file_management.createFoldersForSeries ( file_management.getRootFolder ( ), file_management.getSerieName ( ) + "/" )
file_management.createPathForEpisode ( )

piratebaySearcher = PiratebaySearcher ( )
piratebaySearcher.createrequested_URLString ( file_management.getSerieName ( ), file_management.getSerieSeason ( ), file_management.getSerieEpisode ( ) )
piratebaySearcher.setrequested_URL ( )
piratebaySearcher.sethtml_parser ( )
piratebaySearcher.findFivemost_popular_torrents_info ( file_management.getSerieName ( ) )
'''