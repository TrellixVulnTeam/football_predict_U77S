import os
from os import path
import pymysql

# info about signing into the google cloud sql database
db_user = 'root'
db_password = ''
db_name = 'notes'
db_connection_name = 'private-notes-326216:us-east4:private-notes-sql'

# Establishes connection with Google Cloud SQL database
def get_connection():
	# when deployed to app engine the 'GAE_ENV' variable will be set to 'standard'
	if os.environ.get('GAE_ENV') == 'standard':
		# use the local socket interface for accessing Cloud SQL
		unix_socket = '/cloudsql/{}'.format(db_connection_name)
		conn = pymysql.connect(user=db_user, password=db_password, unix_socket=unix_socket, db=db_name)
	else:
		# if running locally use the TCP connections instead
		# set up Cloud SQL proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
		host = '127.0.0.1'
		conn = pymysql.connect(user=db_user, password=db_password, host=host, db=db_name)

	return conn


# Function to get a user's information from Cloud SQL
def get_notes(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute('SELECT * FROM Notes WHERE UserID=%s', (user_id,))

	notes = cur.fetchall()
	conn.close()

	return notes
