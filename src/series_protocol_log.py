import logging
import sys
from constants import *

###### Global variables ######
logger=None
###### End global vars ######

def configure_logging ( log_file ):
	'''
		Description:	Configure logging format.
	'''
	global logger
	
	logger = logging.getLogger ( log_file ) 		# Get the specific logger.
	handler = logging.StreamHandler ( ) 		# Add a stream handler.

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 	# Create the format of log file.
	handler.setFormatter ( formatter ) 														# Set this format.
	logger.addHandler ( handler )

def find_log_level ( ):
	'''
		Description:	Find the level of logging. This option
				depends of user.
	'''
	if len ( sys.argv ) > 1:
		level_name = sys.argv[1] 						# Get the level as console arg.
		level = LEVELS.get ( level_name, logging.NOTSET ) 			# Find the level of logging.
		logger.setLevel ( level=level ) 						# Set this logging level.
