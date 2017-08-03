import logging
import sys
from constants import *

###### Global variables ######
logger=None
###### End global vars ######

def configure_logging ( ):
	'''
		Description:	Configure logging format.
	'''
	global logger
	
	# Get the specific logger.
	logger = logging.getLogger ( SERIES_LOG )
	# Add a stream handler.
	handler = logging.FileHandler ( SERIES_LOG )
	# Create the format of log file.
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	# Set this format.
	handler.setFormatter ( formatter )
	logger.addHandler ( handler )

def find_log_level ( ):
	'''
		Description:	Find the level of logging. This option
						depends of user.
	'''
	global logger
	
	if len ( sys.argv ) > 1:
		# Get the level as console arg.
		level_name = sys.argv[1] 							
		# Find the level of logging.	
		level = LEVELS.get ( level_name, logging.NOTSET )
		# Set this logging level.
		logger.setLevel ( level=level )


def write_debug_message ( message ):
	'''
		Description:	Write a debug message to series log file.
	'''
	global logger

	logger.debug ( message )

def write_info_message ( message ):
	'''
		Description:	Write a information message to series log file.
	'''
	global logger

	logger.info ( message )

def write_warning_message ( message ):
	'''
		Description:	Write a warning message to series log file.
	'''
	global logger

	logger.warning ( message )

def write_error_message ( message ):
	'''
		Description: Write an error message to series log file.
	'''
	global logger

	logger.error ( message ) 