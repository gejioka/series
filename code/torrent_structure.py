class torrent_structure:
	def __init__( self ):
		self.file_management=None
		self.serie_name=None
		self.serie_season=None
		self.serie_episode=None
		self.episode_name=None
		self.serie_id=None
		self.serie_info=None

	def set_serie_name ( self, serie_name ):
		'''
			Description:	Set the name of the specific serie.
		'''
		self.serie_name=serie_name

	def get_serie_name ( self ):
		'''
			Description:	Return the name of the specific serie.
		'''
		return self.serie_name
	
	def set_serie_season ( self, serie_season ):
		'''
			Description:	Set the season of the specific serie.
		'''
		self.serie_season=serie_season

	def get_serie_season ( self ):
		'''
			Description:	Return the season of the specific serie.
		'''
		return self.serie_season

	def set_serie_episode ( self, serie_episode ):
		'''
			Descriptions:	Set the episode of the specific serie.
		'''
		self.serie_episode=serie_episode

	def get_serie_episode ( self ):
		'''
			Description:	Return the episode of the specific serie.
		'''
		return self.serie_episode

	# Optional
	def set_serie_id ( self, serie_id ):
		'''
			Description:	Set serie id.
		'''
		self.serie_id = serie_id

	# Optional
	def get_serie_id ( self ):
		'''
			Description:	Return serie id.
		'''
		return self.serie_id 

	def create_serie_info ( self ):
		'''
			Description:	Create the informations for this torrent.
		'''
		self.serie_info = {	'header' 		: 'e',
							'serie_name' 	: self.serie_name,
							'serie_season' 	: self.serie_season,
							'serie_episode' : self.serie_episode,
							'serie_id' 		: self.serie_id }

	def set_serie_info ( self, serie_info ):
		'''
			Description:	Set the serie_info file.
		'''
		self.serie_info=serie_info

	def get_serie_info ( self ):
		'''
			Description:	Return the serie_info file.
		'''
		return self.serie_info