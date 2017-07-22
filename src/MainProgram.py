import FileManagement
import PiratebaySearcher
import TransmissionManager
import GlobalVariables
import transmissionrpc
import threading
import os
from torrent_structure import *
from IMDbManager import *
from series_protocol import *

# Create lambda expression to clear console.
clear = lambda: os.system ( 'clear' )
# Create globalVariables object.
globalVariables = GlobalVariables ( transmissionrpc.Client ( 'localhost', port=9091 ) ) 
# Create a series_protocol object.
series_prot = series_protocol ( globalVariables )
# Variable for imdb.
imdb = None
# A variable that tells you if user give wrong arguments.
bad_name=False
# Clear console.
clear ( )

##### User interface #####
while True:
	# Check user input.
	if bad_name:
		print 'There isn\'t option with name ' + str ( option )
		raw_input ( 'Press [ENTER] for new option: ' )
		clear ( )
		bad_name=False

	# Print all options to users.
	print '-a: 	Add new serie'
	print '-vs: 	View list of series'
	print '-rs: 	Remove a serie' 	
	print '-rss: 	Remove a season of this serie'
	print '-rse: 	Remove an episode of this serie'
	print '-q:	Quit from application\n'	 		

	# Get user option.
	option = raw_input ( 'Choose one of the following options: ' )
	
	# Chech if user option is for adding new serie.	
	if option == '-a':
		# Clear console.
		clear ( )
		# Create an imdb object.
		imdb = IMDbManager ( )
		# Ask user for serie name.
		serie_name = raw_input ( 'Enter serie name: ' )
		# Print first 20 results.
		serie = imdb.print_series_match ( serie_name )

		# Ask user for serie season.
		serie_season = int ( raw_input ( 'Enter serie season: ' ) )
		# Ask user fot serie episode.
		serie_episode = int ( raw_input ( 'Enter serie episode: ' ) )

		if imdb.episode_exists ( serie_season, serie_episode, serie['imdb_id'] ):
			# Create a torrent object.
			torrent = torrent_structure ( )
			
			# Add torrent fields.
			torrent.set_serie_name ( serie['title'] )
			torrent.set_serie_season ( serie_season )
			torrent.set_serie_episode ( serie_episode )
			torrent.set_serie_id ( serie['imdb_id'] )

			# Create torrent and add it to queue.
			serie_info = {	'header' 	: 'n',
							'serie_name' 	: serie['title'],
							'serie_season' 	: serie_season,
							'serie_episode' 	: serie_episode,
							'serie_id' 	: serie['imdb_id'] }

			torrent.set_serie_info ( serie_info )

			# Add torrent to list of torrents.
			globalVariables.add_torrent_to_list_of_torrents ( torrent )

			series_prot.add_new_serie ( serie_info )
	elif option == '-vs':
		pass
		# TODO: Print all series.
	elif option == '-rs':
		pass
		# TODO: Remove serie.
	elif option == '-rss':
		pass
		# TODO: Remove a season of this serie.
	elif option == '-rse':
		pass
		# TODO: Remove an episode of this serie.
	elif option == '-q':
		# Create structure and add it to queue.
		serie_info = {	'header' 	: 'q',
						'data' 		: ''  }
		series_prot.add_new_serie ( serie_info )

		break
	else:
		bad_name=True
	clear ( )

