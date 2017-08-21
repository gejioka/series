import logging

# The log file for the serie protocol.
SERIES_LOG = 'series.log'

# The levels of logging: debug, info, warning, error, critical.
LEVELS = {	'debug'		: logging.DEBUG, 	
			'info'		: logging.INFO,
			'warning'	: logging.WARNING,
			'error'		: logging.ERROR,
			'critical'	: logging.CRITICAL}

# A constant to create connection with mysql.
#DB_CONNECTION = mdb.connect('localhost', 'seriesuser', '%ge26312', 'seriesdb')