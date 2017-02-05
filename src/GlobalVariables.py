'''
	Global variables
'''

class GlobalVariables:

	'''
		Initialize a GlobalVariables object.

		parameters: self, transmissionClient
	'''
	def __init__( self, transmissionClient ):
		self.transmissionClient = transmissionClient

	'''
		Return the transmission client.

		parameters: self
	'''
	def getTransmissionClient ( self ):
		return self.transmissionClient

	'''
		Set the serie name.

		parameters: self, serieName
	'''
	def setSerieName ( self, serieName ):
		self.serieName = serieName

	'''
		Return the serie name.

		parameters: self
	'''
	def getSerieName ( self ):
		return serieName

	'''
		Set the season of serie.

		parameters: self, serieSeason
	'''
	def setSerieSeason ( self, serieSeason ):
		self.serieSeason = serieSeason
	
	'''
		Return the season of serie.

		parameters: self
	'''
	def getSerieSeason ( self ):
		return self.serieSeason

	'''
		Set the episode of serie.

		parameters: self, serieEpisode
	'''
	def setSerieEpisode ( self, serieEpisode ):
		self.serieEpisode = serieEpisode

	'''
		Return the episode for this serie.

		parameters: self
	'''
	def getSerieEpisode ( self ):
		return serieEpisode
