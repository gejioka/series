import FileManagement
import PiratebaySearcher
import TransmissionManager
import GlobalVariables

import transmissionrpc
import threading

globalVariables = GlobalVariables.GlobalVariables ( transmissionrpc.Client('localhost', port=9091) )

while True:
	
	'''
		User input for serie.
	'''

	serieName = raw_input ( 'Enter serie name: ' )
	serieSeason = raw_input ( 'Enter serie season: ' )
	serieEpisode = raw_input ( 'Enter serie episode: ' )

	'''
		Create constructors for file management and piratebay searcher.
		Initialize some values of the objects.
	'''

	'''
		create correct serieName, serieSeason,and serieEpisode by using IMDbManager
	'''

	globalVariables.setSerieName ( serieName )
	globalVariables.setSerieSeason ( serieSeason )
	globalVariables.setSerieEpisode ( serieEpisode )

	fileManagement = FileManagement.FileManagement ( )
	fileManagement.userInput ( serieName, serieSeason, serieEpisode )
	
	piratebaySearcher = PiratebaySearcher.PiratebaySearcher ( fileManagement, globalVariables.getTransmissionClient ( ) )
	piratebaySearcher.start ( )

	'''
		Check if episode exists and if not add it to file 
		and create all folders for this episode.
	'''

	fileManagement.writeSeriesInfoToFile ( )
	piratebaySearcher.getLock ( ).release ( )

