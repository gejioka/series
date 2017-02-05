import time
import datetime
import threading
import transmissionrpc
import FileManagement
import PiratebaySearcher

class TransmissionManager (threading.Thread):

	'''
		Initialize a TransmissionManager object.

		parameters: self, transmissionManager, fileManagement
	'''
	def __init__( self, transmissionManager, fileManagement ):
		threading.Thread.__init__(self)
		self.transmissionManager = transmissionManager
		self.fileManagement = fileManagement

	'''
		It's the code which threads run.

		parameters: self
	'''
	def run ( self ):
		dynamicSleepTime=5
		maxSleepTime=120

		while True:
			try:
				self.torrent = self.transmissionManager.get_torrent ( self.torrentId )
				if self.torrent.status == 'downloading':
					if dynamicSleepTime > maxSleepTime / 2:
						dynamicSleepTime = 5
					if self.torrent.eta.total_seconds ( ) > maxSleepTime:
						dynamicSleepTime += 5
						print ( 'Thread sleep for ' + str ( dynamicSleepTime ) + ' seconds.' )	
						time.sleep ( dynamicSleepTime )
					else:
						dynamicSleepTime = self.torrent.eta.total_seconds ( )
						print ( 'Thread sleep for ' + str ( dynamicSleepTime ) + ' seconds.' )
						time.sleep ( dynamicSleepTime )
				else:
					self.transmissionManager.stop_torrent( self.torrent.id )
					self.transmissionManager.remove_torrent( self.torrent.id )
					self.fileManagement.parseTorrentName ( self.torrent.name )
					self.fileManagement.createFoldersForSeries ( self.fileManagement.getRootFolder ( ), self.fileManagement.getSerieName ( ) )
					self.fileManagement.placeSerieToRightFolder ( )

					exit ( )
			except ValueError as e:
				print ( e )
				print ( 'Eta has no value yet.' )
				time.sleep ( 5 )

			except Exception as e:
				print ( e )
				print ( 'There is no specific torrent in torrent list.' )
				exit ( )

	'''
		Set the transmissionManager.

		parameters: self, transmissionManager
	'''
	def setTransmissionManager ( self, transmissionManager ):
		self.transmissionManager = transmissionManager

	'''
		Return the transmissionManager.

		parameters: self
	'''
	def getTransmissionManager ( self ):
		return self.transmissionManager

	'''
		Set the torrent id.

		parameters: self, torrentId
	'''
	def setTorrentId ( self, torrentId ):
		self.torrentId = torrentId

	'''
		Return the torrent id.

		parameters: self
	'''
	def getTorrentId ( self ):
		return torrentId

	'''
		Set the torrent.

		parameters: self, torrent
	'''
	def setTorrent ( self, torrent ):
		self.torrent = torrent

	'''
		Return the torrent.

		parameters: self
	'''
	def getTorrent ( self ):
		return torrent

	'''
		Add a new torrent to transmission.

		parameters: self, mangetLink
	'''
	def addTorrentToTransmission ( self, mangetLink ):
		self.torrent = self.transmissionManager.add_torrent ( mangetLink )

	'''
		Set the list of torrents.

		parameters self, torrentsList
	'''
	def setTorrentsList ( self, torrentsList ):
		self.torrentsList = torrentsList

	'''
		Return the torrent list.

		parameters: self
	'''
	def getTorrentsList ( self ):
		return self.torrentsList
