import MySQLdb as mdb
from series_protocol_log import *

def create_series_table ( con ):
	'''
		Description:	Create series table in seriesdb.
	'''
	with con:
		cur = con.cursor ( )
		try:
			cur.execute("CREATE TABLE Series(Id VARCHAR(100) PRIMARY KEY, Name VARCHAR(100), Year VARCHAR(25))")
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( '[+] Created table for series.' )
		except Exception as err:
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( '[!] Series table already exists!!!' )

def create_seasons_table ( con ):
	'''
		Description:	Create a table for all seasons of different series.
	'''
	with con:
		cur = con.cursor ( )
		try:
			cur.execute("CREATE TABLE Seasons(Id INT PRIMARY KEY AUTO_INCREMENT , Serie_id VARCHAR(100), Season INT NOT NULL)")
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( '[+] Created table for seasons of every serie.' )
		except Exception as err:
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( '[!] Seasons table already exists!!!' )

def create_table_for_episodes ( con ):
	'''
		Description:	Create table for episodes.
	'''
	with con:
		cur = con.cursor ( )
		try:
			cur.execute ("CREATE TABLE Episodes(Episode_Id INT PRIMARY KEY AUTO_INCREMENT, Serie_Id VARCHAR(100), Season_Id INT, Episode_Name VARCHAR(100), Status VARCHAR(25), Release_Date VARCHAR(100), Type VARCHAR(25))")
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( 'Created table for episodes.')
		except Exception as err:
			write_info_message ( '############' )
			write_info_message ( '##seriesdb##' )
			write_info_message ( '############' )
			write_info_message ( '[!] Episode table already exists!!!' )

def add_new_serie_to_db ( con, serie_name, serie_id, year ):
	'''
		Description:	Add new serie to series table.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute("INSERT INTO Series(Id, Name, Year) VALUES (%s, %s, %s)", ( serie_id, serie_name, year ) )
		
		write_info_message ( '############' )
		write_info_message ( '##seriesdb##' )
		write_info_message ( '############' )
		write_info_message ( '[+] A new serie added to series table.' )
		write_debug_message ( '[+] A new serie with name ' + str ( serie_name ) + ' and serie id ' + str ( serie_id ) \
									+ ' added to series table. ' )

def add_new_season ( con, serie_id, season ):
	'''
		Description:	Add a new season to Seasons table.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ("INSERT INTO Seasons(Serie_id, Season) VALUES (%s, %s)", ( serie_id, season ) )

		write_info_message ( '############' )
		write_info_message ( '##seriesdb##' )
		write_info_message ( '############' )
		write_info_message ( '[+] A new season added to table of seasons.' )
		write_debug_message ( '[+] A new season with id ' + str ( season ) + ' of serie with id ' \
									+ str ( serie_id ) + ' added to table of seasons.' )

def add_new_episode ( con, serie_id, season_id, episode_name, status, release_date, episode_type ):
	'''
		Description:	Add a new episode to table
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ("INSERT INTO Episodes(Serie_Id,Season_Id,Episode_Name,Status,Release_Date,Type) VALUES (%s,%s,%s,%s,%s,%s)", ( serie_id, season_id, episode_name, status, release_date, episode_type ) )

		write_info_message ( '############' )
		write_info_message ( '##seriesdb##' )
		write_info_message ( '############' )
		write_info_message ( '[+] A new episode added to episodes table.' )
		write_debug_message ( '[+] A new episode with name ' + str ( episode_name ) + \
									' added to table with episodes.' )

def get_season_id ( con, serie_id, season ):
	'''
		Description:	Return season id of the specific serie season.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ("SELECT Id FROM Seasons WHERE Seasons.Serie_Id=%s " \
						+ " AND Seasons.Season=%s", ( serie_id, season ) )
		rows = cur.fetchone ( )

		return rows

def get_all_series ( con ):
	'''
		Description:	Return all series of seriesdb.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ("SELECT  * FROM Series")
		rows = cur.fetchall ( )

		return rows

def get_all_serie_seasons ( con, serie_name ):
	'''
		Description:	Return all seasons of a specific serie.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute("SELECT Series.Id, Seasons.Id, Seasons.Season FROM Series " \
						+ " INNER JOIN Seasons ON Series.Id=Seasons.Serie_id " \
						+ " AND Series.Name=%s", ( serie_name, ) )
		rows = cur.fetchall ( )

		return rows

def get_season_episodes ( con, serie_id, season_id ):
	'''
		Description:	Return all episodes of a specific season.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ( "SELECT Episodes.Episode_Name, Episodes.Status FROM Episodes " \
						+ " INNER JOIN Seasons ON Episodes.Season_Id=Seasons.Id " \
						+ "INNER JOIN Series ON Episodes.Serie_Id=Series.Id " \
						+ " WHERE Episodes.Serie_Id=%s AND Episodes.Season_Id=%s", ( serie_id, season_id ) )
		rows = cur.fetchall ( )
		
		return rows

def update_episode_status ( con, episode_id, status ):
	'''
		Description:	Update episode status from unseen to seen.
	'''
	with con:
		cur = con.cursor ( )
		cur.execute ("UPDATE Episodes SET Status=%s WHERE Episode_Id=%s", ( status, episode_id ) )

		write_info_message ( '############' )
		write_info_message ( '##seriesdb##' )
		write_info_message ( '############' )
		write_info_message ( '[+] Updated status of episode with id ' + str ( episode_id ) + ' to seen.' )

##################### Testing #######################
#con = mdb.connect('localhost', 'seriesuser', '%ge26312', 'seriesdb')
#print get_all_serie_seasons ( con, 'Arrow' )

'''
create_series_table ( con )
create_seasons_table ( con )

con = mdb.connect('localhost', 'seriesuser', '%ge26312', 'seriesdb')

configure_logging ( )
find_log_level ( )

create_table_for_episodes ( con )

add_new_episode ( con, 1, 1, 'Prwto', 'unseen', '1-2-2010', 'tv-episode' )
add_new_episode ( con, 1, 1, 'Deutero', 'unseen', '5-2-2010', 'tv-episode' )
add_new_episode ( con, 1, 1, 'Trito', 'unseen', '10-2-2010', 'tv-episode' )
add_new_episode ( con, 2, 2, 'Tetarto', 'unseen', '20-8-2010', 'tv-episode' )

print 'Series\n'
for serie in get_all_series ( con ):
	print serie

print '\nEpisodes\n'
for episode in get_season_episodes ( con, 1, 1 ):
	print episode[0]
'''