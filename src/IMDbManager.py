from imdbpie import Imdb

class IMDbManager:
	def __init__( self, fileManagement ):
		self.imdb = Imdb ( )
		self.fileManagement = fileManagement
		
serie = imdb.search_for_title("flash")


'''
for episode in imdb.get_episodes( serie[0]['imdb_id'] ):
	print ( episode.release_date )
'''
#print (  serie[0]['imdb_id']  + ' ' + serie[0]['title'] )