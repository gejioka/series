from bs4 import BeautifulSoup
import FileManagement
import threading
import requests
import transmissionrpc
import TransmissionManager
import re


class PiratebaySearcher(threading.Thread):
	basicURL=None
	lock=None
	junkFile=None
	requestedURL=None
	requestedURLString=None
	htmlParser=None
	torrentName=None
	torrentMagnet=None
	transmissionManager=None
	mostPopularTorrentsInfo=None

	'''
		Initialize a PiratebaySearcher object.

		parameters: self, fileManagement, transmissionManager, basicURL
	'''
	def __init__( self, fileManagement, transmissionManager, basicURL='https://thepiratebay.org/' ):
		threading.Thread.__init__(self)
		self.lock = threading.Lock ( )
		self.lock.acquire ( )
		self.basicURL = basicURL
		self.mostPopularTorrentsInfo=[]
		self.fileManagement = fileManagement
		self.transmissionManager = transmissionManager

	'''
		It's the code which threads run.

		parameters: self
	'''
	def run ( self ):
		self.lock.acquire ( )

		if not self.fileManagement.getIsJunk ( ):
			self.createRequestedURLString ( self.fileManagement.getSerieName ( ), self.fileManagement.getSerieSeason ( ), self.fileManagement.getSerieEpisode ( ) )
			self.findFiveMostPopularTorrentsInfo ( self.fileManagement.getSerieName ( ) )

			try:
				torrentThread = TransmissionManager.TransmissionManager ( self.transmissionManager, self.fileManagement )
				torrentThread.addTorrentToTransmission ( self.mostPopularTorrentsInfo[0]['torrent_magnet'] )
				for current_torrent in self.transmissionManager.get_torrents ( ):
					if self.mostPopularTorrentsInfo[0]['torrent_name'] == current_torrent.name:
						self.fileManagement.setFileName ( self.mostPopularTorrentsInfo[0]['torrent_name'])
						torrentThread.setTorrentId ( current_torrent.id )
						torrentThread.start ( )
					elif '+' in current_torrent.name and self.mostPopularTorrentsInfo[0]['torrent_name'] == current_torrent.name.replace ( '+', ' ' ):
						self.fileManagement.setFileName ( self.mostPopularTorrentsInfo[0]['torrent_name'])
						torrentThread.setTorrentId ( current_torrent.id )
						torrentThread.start ( )
						
			except Exception as e:
				print ( e )

	'''
		Set the lock.

		parameters: self, lock
	'''
	def setLock ( self, lock ):
		self.lock = lock

	'''
		Return the lock.

		parameters: self
	'''
	def getLock ( self ):
		return self.lock

	'''
		Create the url string.

		parameters: self, serieName, serieSeason, serieEpisode
	'''
	def createRequestedURLString ( self, serieName, serieSeason, serieEpisode ):

		serieName = serieName.lower ( ).replace ( ' ', '%20' )
		serieSeason = 's' + serieSeason
		serieEpisode = 'e' + serieEpisode

		self.requestedURLString = self.basicURL + 'search/' + serieName + '%20' + serieSeason + serieEpisode + '/0/99/0'
		self.setRequestedURL ( )
		self.setHtmlParser ( )

	'''
		Set the requested url.

		parameters: self, requestedURLString
	'''
	def setRequestedURLString ( self, requestedURLString ):
		self.requestedURLString = requestedURLString

	'''
		Return the requested url.

		parameters: self
	'''
	def getRequestedURLString ( self ):
		return self.requestedURLString

	def setRequestedURL ( self ):
		self.requestedURL = requests.get ( self.requestedURLString )

	def getRequestedURL ( self ):
		return self.requestedURL

	'''
		Set the html parser.

		parameters: self
	'''
	def setHtmlParser ( self ):
		self.htmlParser = BeautifulSoup ( self.requestedURL.text, 'html.parser' )

	'''
		Return the html parser.

		parameters: self
	'''
	def getHtmlParser ( self ):
		return self.htmlParser

	'''
		Find the most popular torrents.

		parameters: self, serieName
	'''
	def findFiveMostPopularTorrentsInfo ( self, serieName ):
		current_name=None
		count=0

		pattern_name = re.compile ( ('.*') +  serieName.lower ( ).replace ( ' ', '.' ) + ('.*') )
		pattern_magnet = re.compile ( 'magnet' )

		for a_tag in self.htmlParser.find_all ( 'a' ):
			if ( pattern_name.match ( a_tag.text.lower ( ) ) ):
				current_name = a_tag.text
			if ( pattern_magnet.match ( a_tag.attrs['href'] ) ):
				self.mostPopularTorrentsInfo.append({ 	'torrent_name' 		: current_name,
														'torrent_magnet'	: a_tag.attrs['href']
													})
				count+=1
			
			if ( count >= 5 ):
				break

		for torrent in self.mostPopularTorrentsInfo:
			print ( torrent )

	'''
		Return the most popular torrents.

		parameters: self
	'''
	def getFiveMostPopularTorrentsInfo ( self ):
		return self.mostPopularTorrentsInfo


######################## Testing ##########################
'''
fileManagement = FileManagement.FileManagement ( )
fileManagement.createRootFolder ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ('Arrow.S05E05.HDTV.x264-LOL[ettv]')
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

piratebaySearcher = PiratebaySearcher ( )
piratebaySearcher.createRequestedURLString ( fileManagement.getSerieName ( ), fileManagement.getSerieSeason ( ), fileManagement.getSerieEpisode ( ) )
piratebaySearcher.setRequestedURL ( )
piratebaySearcher.setHtmlParser ( )
piratebaySearcher.findFiveMostPopularTorrentsInfo ( fileManagement.getSerieName ( ) )
'''
'''
fileManagement = FileManagement.FileManagement ( )
fileManagement.createRootFolder ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Supernatural S01E01 HDTV")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

piratebaySearcher = PiratebaySearcher ( )
piratebaySearcher.createRequestedURLString ( fileManagement.getSerieName ( ), fileManagement.getSerieSeason ( ), fileManagement.getSerieEpisode ( ) )
piratebaySearcher.setRequestedURL ( )
piratebaySearcher.setHtmlParser ( )
piratebaySearcher.findFiveMostPopularTorrentsInfo ( fileManagement.getSerieName ( ) )
'''