import os
import os.path
from seriesdb_handler import *
from series_protocol_log import *
from difflib import SequenceMatcher

option = None
con = mdb.connect('localhost', 'root', 'oikonomidis24', 'seriesdb')

configure_logging ( )
find_log_level ( )

def select_serie ( ):
	global con

	# Print all series of the seriesdb.
	counter = 1
	for serie in get_all_series ( con ):
		print str ( counter ) + '. ' +  serie[1] + ' , ' + str ( serie[2] )
		counter += 1

	# Tell user select one of the series.
	not_valid=True
	serie=None
	while not_valid:
		try:
			option = int ( raw_input ( '\nSelect one of the above series: ' ) )
			serie = get_all_series ( con )[option - 1]

			not_valid=False
		except Exception:
			print 'Option with id ' + str ( option ) + ' doesnt\'t exist. Try again or press \'q\' to quit.'

	return serie

def select_season ( serie ):
	global con

	# Print all seasons of the specific serie.
	counter = 1
	for season in get_all_serie_seasons ( con, serie[1] ):
		print str ( counter ) + '. ' + 'Season ' + str ( season[2] )
		counter += 1

	# Tell user select one of the seasons.
	not_valid=True
	season=None
	while not_valid:
		try:
			option = int ( raw_input ( '\nSelect one of the above seasons: ' ) )
			season = get_all_serie_seasons ( con, serie[1] )[option - 1]

			not_valid=False
		except Exception:
			print 'Option with id ' + str ( option ) + ' doesnt\'t exist. Try again or press \'q\' to quit.'

	return season

def select_episode ( season ):
	global con

	# Print all episodes of the specific season.
	counter = 1
	for episode in get_season_episodes ( con, season[0], season[1] ):
		print str ( counter ) + '. ' + str ( episode[0] ) + ' , ' + str ( episode[1] )
		counter += 1

	# Tell user select one of the above episodes.
	not_valid=True
	episode=None
	while not_valid:
		try:
			option = int ( raw_input ( '\nSelect one of the above episodes: ' ) )
			episode = get_season_episodes ( con, season[0], season[1] )[option - 1]

			print episode
			not_valid=False
		except Exception as err:
			print 'Option with id ' + str ( option ) + ' doesnt\'t exist. Try again or press \'q\' to quit.'

def similar ( first_file, second_file ):
	'''
		Description:	Find how similar are two different files.
	'''
	return SequenceMatcher ( None, first_file, second_file ).ratio ( )

def find_similar_file ( file_name ):
	'''
		Description:	Find the most similar file with specific filename and return it.
	'''
	similar_w = 0
	filename = ''
	for file in os.listdir ( '/home/christos/Downloads' ):
		if similar ( file, file_name ) > similar_w:
			similar_w = similar ( file, file_name )
			filename = file

	return similar_w, filename

print find_similar_file ( 'Arrow.S01E01.HDTV.x264-LOL.[VTV].mp4' )

# TODO: Update status from unseen to seen. Tell series protocol to remove specific episode.