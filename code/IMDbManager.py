import os
from FileManagement import *
from imdbpie import Imdb

class IMDbManager:
	def __init__( self ):
		'''
			Description:	Create a new imdb_manager object.
		'''

		# An imdb object.
		self.imdb = Imdb ( )

	def print_series_match ( self, serie_name ):
		'''
			Description:	Print 20 first results of serie name.
		'''

		# Create lambda expression to clear console.
		clear = lambda: os.system ( 'clear' )
		
		# Find all matches for specific serie_name in imdb.
		options = self.imdb.search_for_title ( serie_name )
		
		# A counter for matches.
		counter = 1
		
		# Clear console.
		clear ( )
		
		print 'Choose one of the following series:\n'
		for serie in options:
			print str ( counter ) + '. Title: ' + serie['title'] + '\t, Year: ', serie['year'] 	
			if counter % 20 == 0: 				
				option = raw_input ( '\nor press [ENTER] if you want see more results ' )
				if option == '':
					clear ( )

					print 'Choose one of the following series:\n'
				else:
					print options[int(option) - 1]['imdb_id']

					return options[int(option) - 1]
			counter += 1

	def episode_exists ( self, serie_season, serie_episode, serie_id ):
		'''
			Description:	Check if episode exists and store all informations about it.
		'''
		episodes = self.imdb.get_episodes ( serie_id )

		for episode in episodes:
			if episode.season == serie_season and episode.episode == serie_episode:
				return True

		print 'This episode doesn\'t exist. Give a different season and episode.'
		return False

	def find_next_episode ( self, serie, curr_season, curr_episode, serie_id ):
		'''
			Description:	Find and return the next episode of specific serie.
		'''

		# A boolean variable.
		next_episode = False
		
		# Search all episodes of the serie and return the next episode.
		for episode in self.imdb.get_episodes ( serie_id ):
			if next_episode:
				return episode

			if episode.season == curr_season and episode.episode == curr_episode:
				next_episode = True

	def find_current_episode ( self, serie, curr_season, curr_episode, serie_id ):
		'''
			Description:	Find and return the next episode of specific serie.
		'''

		# Search all episodes of the serie and return the current episode.
		for episode in self.imdb.get_episodes ( serie_id ):
			if episode.season == curr_season and episode.episode == curr_episode:
				return episode


