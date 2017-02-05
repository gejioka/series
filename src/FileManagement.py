import os
import os.path
import re
import ast
import requests

class FileManagement:
	rootFolder=None
	downloadPathOfSeries=None
	pathForEpisode=None
	folderName=None
	serieName=None
	serieSeason=None
	serieEpisode=None
	fileNamePattern=None
	serieInfo=None
	isJunk=None
	filename=None
	fileWithSeriesInfo=None
	listWithSeriesInfo=[]

	'''
		Initialize a FileManagement object.

		parameters: self, rootFolder, fileWithSeriesInfo, downloadPathOfSeries 
	'''
	def __init__( self, rootFolder=None, fileWithSeriesInfo=None, downloadPathOfSeries=None ):
		self.findRootPath ( )
		self.findDownloadPath ( )
		self.findFileWithSeriesInfoPath ( )

		self.createRootFolder ( )
		self.createFileWithSeriesInfo ( )

	'''
		Find the root folder path.

		parameters:	self
	'''
	def findRootPath ( self ):
		self.rootFolder=os.path.abspath ( '../' ) + '/'

	'''
		Find the download folder path.

		parameters: self
	'''
	def findDownloadPath ( self ):
		self.downloadPathOfSeries=os.path.expanduser("~") + '/Downloads/'

	'''
		Find the file with series informations.

		parameters: self
	'''
	def findFileWithSeriesInfoPath ( self ):
		self.fileWithSeriesInfo=self.rootFolder + '.series_info'
		print self.fileWithSeriesInfo

	'''
		Create the root folder if doesn't exists.

		parameters: self
	'''
	def createRootFolder ( self ):
		if not os.path.exists (self.rootFolder):
			os.makedirs (self.rootFolder)

	'''
		Create the file with series informations.

		parameters: self
	'''
	def createFileWithSeriesInfo ( self ):
		if not os.path.exists ( self.fileWithSeriesInfo ):
			open ( self.fileWithSeriesInfo, 'a' ).close ( )

	'''
		Set the root folder path.

		parameters: self, rootFolder
	'''
	def setRootFolder ( self, rootFolder ):
		self.rootFolder=rootFolder

	'''
		Return the root folder path.

		parameters: self
	'''
	def getRootFolder ( self ):
		return self.rootFolder

	'''
		Set the name of the specific serie.

		parameters: self, serieName
	'''
	def setSerieName ( self, serieName ):
		self.serieName=serieName

	'''
		Return the name of the specific serie.

		parameters: self
	'''
	def getSerieName ( self ):
		return self.serieName
	
	'''
		Set the season of the specific serie.

		parameters: self, serieSeason
	'''
	def setSerieSeason ( self, serieSeason ):
		self.serieSeason=serieSeason

	'''
		Return the season of the specific serie.

		parameters: self
	'''
	def getSerieSeason ( self ):
		return self.serieSeason

	'''
		Set the episode of the specific serie.

		parameters: self, serieEpisode
	'''
	def setSerieEpisode ( self, serieEpisode ):
		self.serieEpisode=serieEpisode

	'''
		Return the episode of the specific serie.

		parameters: self
	'''
	def getSerieEpisode ( self ):
		return self.serieEpisode;

	'''
		Create the name for this serie episode.

		parameters: self
	'''
	def createFileNamePattern ( self ):
		self.fileNamePattern=self.serieName.title ( ) + "S" + str( self.serieSeason ).zfill ( 2 ) + "E" + str( self.serieEpisode ).zfill ( 2 )

	'''
		Set the name for this episode.

		parameters: self, fileNamePattern
	'''
	def setFileNamePattern ( self, fileNamePattern ):
		self.fileNamePattern=fileNamePattern

	'''
		Return the name for this serie.

		parameters: self
	'''
	def getFileNamePattern ( self ):
		return self.fileNamePattern

	'''
		Set the serie filename.

		parameters: self, filename
	'''
	def setFileName ( self, filename ):
		self.filename = filename

	'''
		Return the serie file name.

		parameters: self
	'''
	def getFileName ( self ):
		return filename

	'''
		Set the serie_info file.

		parameters: self, serieInfo
	'''
	def setSerieInfo ( self, serieInfo ):
		self.serieInfo=serieInfo

	'''
		Return the serie_info file.

		parameters: self
	'''
	def getSerieInfo ( self ):
		return self.serieInfo

	'''
		Set the list with serie informations.

		parameters: self, listWithSeriesInfo
	'''
	def setListWithSeriesInfo ( self, listWithSeriesInfo ):
		self.listWithSeriesInfo = listWithSeriesInfo

	'''
		Create the path for episode.

		parameters: self
	'''
	def createPathForEpisode ( self ):
		self.pathForEpisode = self.rootFolder + self.serieName + "/" + "Season " + self.serieSeason + "/" + "Episode " + self.serieEpisode + "/"

	'''
		Set the path for this episode.

		parameters: self, pathForEpisode
	'''
	def setPathForEpisode ( self, pathForEpisode ):
		self.pathForEpisode=pathForEpisode

	'''
		Return the path for this episode.

		parameters: self
	'''
	def getPathForEpisode ( self ):
		return self.pathForEpisode

	'''
		Set if the this episode is already exists.

		parameters: self, isJunk
	'''
	def setIsJunk ( self, isJunk ):
		self.isJunk = isJunk

	'''
		Return if this episode is already exists.

		parameters: self
	'''
	def getIsJunk ( self ):
		return self.isJunk

	'''
		Write new serie or update old.

		parameters: self
	'''
	def writeSeriesInfoToFile ( self ):
		target = open ( self.fileWithSeriesInfo, 'r' )
		
		for line in target.readlines ( ):
			self.listWithSeriesInfo.append ( ast.literal_eval ( line ) )

		target.close ( )

		target = open ( self.fileWithSeriesInfo, 'a' )

		updated=False
		garbage=False
		for i in range ( len ( self.listWithSeriesInfo ) ):
			if ( self.listWithSeriesInfo[i]['serieName'] == self.serieInfo['serieName'] ):
				if ( int ( self.listWithSeriesInfo[i]['serieSeason'] ) <= int ( self.serieInfo['serieSeason'] ) and int ( self.listWithSeriesInfo[i]['serieEpisode'] ) < int ( self.serieInfo['serieEpisode'] ) ):
					self.listWithSeriesInfo[i] = self.serieInfo
					updated=True
				else:
					garbage=True

		if updated:
			target.seek ( 0 )
			target.truncate ( )
			
			for i in range ( len ( self.listWithSeriesInfo ) ):
				target.write ( str ( self.listWithSeriesInfo[i] ) )
				target.write( "\n" )
		elif not garbage:
			target.write ( str ( self.serieInfo ) )
			target.write ( "\n" )
		else:
			print ( "This episode already exists.\n" )

		del self.listWithSeriesInfo[:]
		target.close ( )

		if updated or not garbage:
			self.isJunk = False
			return True
		else:
			self.isJunk = True
			return False

	'''
		Create the folder for this serie.

		parameters: self, rootFolder, serieName, serieSeason, serieEpisode
	'''
	def createFoldersForSeries ( self, rootFolder="", serieName="", serieSeason="", serieEpisode="" ):
		if not os.path.exists ( rootFolder + serieName + serieSeason + serieEpisode ):
			os.makedirs ( rootFolder + serieName + serieSeason + serieEpisode )
			
		if serieSeason == "":
			self.createFoldersForSeries ( rootFolder, serieName, "/Season " + self.serieSeason + "/" )
		elif serieEpisode == "":
			self.createFoldersForSeries ( rootFolder, serieName, serieSeason, "Episode " + self.serieEpisode + "/" )
		else:
			print ( "Create all subfolders for this serie." )

	'''
		Create the serie name for this serie.

		parameters: self, serieName
	'''
	def constractSerieName ( self, serieName ):
		if '.' in serieName:
			self.serieName = serieName.replace ( '.', ' ' )
		elif '+' in serieName:
			self.serieName = serieName.replace ( '+', ' ' )
		else:
			self.serieName = serieName

	'''
		Place this serie to right folder.

		parameters: self
	'''
	def placeSerieToRightFolder ( self ):

		try:
			self.createPathForEpisode ( )
			if os.path.isdir ( self.downloadPathOfSeries + self.filename ):
				for file in os.listdir ( self.downloadPathOfSeries + self.filename ):
					os.rename ( os.path.realpath ( self.downloadPathOfSeries + self.filename + file ), self.pathForEpisode + file )
				os.rmdir ( self.downloadPathOfSeries + self.filename )
			else:
				os.rename ( os.path.realpath ( self.downloadPathOfSeries + self.filename ), self.pathForEpisode + self.filename )
		except Exception as e:
			print ( 'This file ' + '\'' + self.filename + '\'' + ' doesn\'t exist.')

	'''
		Add the user input in a dictionary structure.

		parameters: self, serieName, serieSeason, serieEpisode
	'''
	def userInput ( self, serieName, serieSeason, serieEpisode ):
		self.serieName = serieName
		self.serieSeason = serieSeason
		self.serieEpisode = serieEpisode

		self.serieInfo= { 	"serieName" : self.serieName,
							"serieSeason" : self.serieSeason,
							"serieEpisode" : self.serieEpisode
						}

	'''
		Parse the name of the torrent file.

		parameters: self, filename
	'''
	def parseTorrentName ( self, filename ):
		p = re.compile("(.*)S([0-9]+)E([0-9]+)")
		m = p.match (filename)
		
		if m:
			self.constractSerieName ( m.group ( 1 ) )
			self.setSerieSeason ( m.group ( 2 ) )
			self.setSerieEpisode ( m.group ( 3 ) )

			self.serieInfo = { 	"serieName" : self.serieName,
								"serieSeason" : self.serieSeason,
								"serieEpisode" : self.serieEpisode}
			print ( self.serieInfo )

################# Testing #################
'''
fileManagement = FileManagement ( )
fileManagement.createRootFolder ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("DCs.Legends.of.Tomorrow.S01E16.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )
'''
'''
fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Arrow.S04E15.HDTV.x264-LOL[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )
fileManagement.placeSerieToRightFolder ( "Arrow.S04E15.HDTV.x264-LOL[ettv]" )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Flash.S01E16.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Supernatural.S01E16.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Arrow.S01E17.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Arrow.S02E10.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("Arrow.S03E20.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )

fileManagement = FileManagement ( )
fileManagement.createFileWithSeriesInfo ( )
fileManagement.parseFileName ("DCs.Legends.of.Tomorrow.S03E20.HDTV.XviD-FUM[ettv]")
fileManagement.writeSeriesInfoToFile ( )
fileManagement.createFoldersForSeries ( fileManagement.getRootFolder ( ), fileManagement.getSerieName ( ) + "/" )
fileManagement.createPathForEpisode ( )
'''