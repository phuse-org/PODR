# (c) 2007-2020 NIHPO, Inc.
# Jose.Lacal@NIHPO.com - 26 May 2020
#
"""
Purpose:
* This sample Python code connects with PHUSE's Open Data Repository ("PODR") and runs a couple of queries.
* Please keep in mind that you are only allowed 01 connection at the time to PODR's database.

If you are a PHUSE member: please contact Jose.Lacal@NIHPO.com to request a Username and Password to access PODR.

Requirements:
* Python 3.6+
* psycopg2-binary
* You must have these environment variables defined with the access details provided to you.
	"PHUSE_User"
	"PHUSE_Password"


To set environment variables:

In macOS:
	Open Terminal.
	export PHUSE_User="your assigned username here"
	export PHUSE_Password="your assigned password here"

In Windows:
	https://www.techjunkie.com/environment-variables-windows-10/


Process:
a.) Set environment variables.
b.) Run this script:
	python3 PHUSE_PODR.py
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
# Check for PostgreSQL's username and password in your environment:
try:
	pgsql_user = os.environ["PHUSE_User"]
except KeyError: 
	print ("Please set the environment variable 'PHUSE_User'")
	sys.exit(1)
#
try:
	pgsql_password = os.environ["PHUSE_Password"]
except KeyError: 
	print ("Please set the environment variable 'PHUSE_Password'")
	sys.exit(1)
#
pgsql_dbname = "nihpo"
pgsql_host = "podr.phuse.global"
pgsql_port = 5432
#
# = = = Main Processing = = =
if __name__ == "__main__":
	#
	print ("Starting..\n")
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
		sys.exit("There was an error connecting to PHUSE's Open Data Repository.")
	#
	#
	# = = = Sample queries below = = =
	#
	# 01. List all available tables:
	cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	print ("\n\nList of all available tables in PODR:")
	for table in cur.fetchall():
		print(table)
	#
	# 02. List 10 FDA Adverse Events for drug "IMURAN":
	cur.execute("""SELECT caseid, cum_dose_chr, cum_dose_unit, dechal, dose_amt, dose_form, dose_freq, dose_unit, dose_vbm, drug_seq, drugname, exp_dt, lot_num, nda_num, primaryid, prod_ai, rechal, role_cod, route, val_vbm FROM nihpo_fda_aers_drug WHERE drugname = 'IMURAN' LIMIT 10;""")
	print ("\n\n10 Adverse Events from FDA's AERS, table 'nihpo_fda_aers_drug':")
	for adverse_event in cur.fetchall():
		print(adverse_event)
	#
	#
	# = = = The end = = =
	#
	con_nihpo_target.close()
	print ("\n\nYou disconnected from the PHUSE PODR database.")
	#