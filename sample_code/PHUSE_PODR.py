# (c) 2007-2020 NIHPO, Inc.
"""
Purpose:
* This sample Python code connects with PODR and conducts a couple of queries.

Please contact Jose.Lacal@NIHPO.com to request a Username and Password to access PODR.

Requirements:
* Python 3.6+
* psycopg2-binary
* You must have these environment variables defined with the access details provided to you.
	"PHUSE_User"
	"PHUSE_Password"

To set environment variables:

In macOS:
	Open Terminal.

"""
# - - - - -
# Imports Section
import os, sys
try:
	import psycopg2
	import psycopg2.extras
	from psycopg2 import sql
except ImportError:
	print ("sudo pip3 install psycopg2-binary")
	sys.exit()
#
# PostgreSQL:
try:
	pgsql_user = os.environ["PHUSE_User"]
except KeyError: 
	print "Please set the environment variable PHUSE_User"
	sys.exit(1)
#
try:
	pgsql_password = os.environ["PHUSE_Password"]
except KeyError: 
	print "Please set the environment variable PHUSE_Password"
	sys.exit(1)
#
pgsql_dbname = "nihpo"
pgsql_host = "podr.phuse.global"
pgsql_port = 5432
#
# = = = Main Processing = = =
if __name__ == "__main__":
	#
	print ("Starting..")
	#
	## Open database connection:
	try:
		con_string_nihpo = "dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (pgsql_dbname, pgsql_user, pgsql_password, pgsql_host, pgsql_port)
		con_nihpo_target = psycopg2.connect(con_string_nihpo)
		cur = con_nihpo_target.cursor(cursor_factory=psycopg2.extras.DictCursor)	# To be able to access fields by fieldname.
		cur.itersize = 10000 # Define how many records to buffer server-side.
		print ("\nConnected to PostgreSQL database :: [%s]" % (pgsql_dbname))
		print ("At host [%s] with port [%d]\n" % (pgsql_host, pgsql_port))
		#
	except psycopg2.DatabaseError as e:
		print ("PostgreSQL error %s" % e)
		print ("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (pgsql_dbname, pgsql_user, pgsql_password, pgsql_host, pgsql_port))
		sys.exit('I am unable to connect to PODR - PostgreSQL.')
	#




	con_nihpo_target.commit()
	con_nihpo_target.close()
	print ("\nDisconnected from PostgreSQL database :: [%s]" % (pgsql_dbname))
	#