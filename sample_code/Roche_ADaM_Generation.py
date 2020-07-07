#!/usr/bin/python3
# (c) 2007-2020 NIHPO, Inc.   http://NIHPO.com   Contact: Jose.Lacal@NIHPO.com
# Filename: Roche_ADaM_Generation.py
# Purpose: This Python script generates realistic yet fake CDISC ADaM data using Roche's sample spreadsheet.
# Version: Tue 07 July 2020.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
# 
"""
To call this script:
	python3 Roche_ADaM_Generation.py [StudyID] [TargetDirectory] [NumberSubjects] [DateStartRecruitment] [CurrentDate]\nUse YYYY-MM-DD for dates.

For example:
	python3 Roche_ADaM_Generation.py 1234 /Users/server/Github/PODR/sample_code/ 1000 2016-01-01 2020-07-03


Requirements:
* This script requires Pythin 3.7x
* The SQLite3 file "Synthetic_Health_Data_NIHPO.sqlite3" must be in the current directory. [Available at https://github.com/phuse-org/PODR/tree/master/sample_code]
"""


# Imports Section
import csv
import datetime
import os
import random
import sqlite3
import sys
import uuid
#
CT_DEBUG = 0		# Set to 0 (digit zero) to avoid debug messages.
#
# = = = Trial definition = = =
CT_FEMALE_SPLIT = 48	# Percentage of the desired number of Synthetic Subjects assigned a Female / Male gender: MUST be under 100.
CT_GENDER_SPLIT = ['F'] * CT_FEMALE_SPLIT + ['M'] * (100-CT_FEMALE_SPLIT)
#
CT_AGE_MINIMUM = 18
CT_AGE_MAXIMUM = 89
#
# Race splits must add up to 100:
CT_RACE_SPLIT_AMERICAN_INDIAN = 10
CT_RACE_SPLIT_ASIAN = 13
CT_RACE_SPLIT_BLACK = 19
CT_RACE_SPLIT_NATIVE_HAWAIIAN = 7
CT_RACE_SPLIT_WHITE = 40
CT_RACE_SPLIT_NOT_REPORTED = 10
CT_RACE_SPLIT_UNKNOWN = 1
#
CT_RACE_HISPANIC = 13
#
# US Department of Health and Human Services, Food and Drug Administration. Collection of race and ethnicity data in clinical trials. Guidance for industry and Food and Drug Administration staff. https://www.fda.gov/media/75453/download. Published October 26, 2016.
# Percentage of the desired number of Synthetic Subjects assigned to each race type. Must add up to 100.
CT_RACE_SPLIT = ['AMERICAN INDIAN OR ALASKA NATIVE'] * CT_RACE_SPLIT_AMERICAN_INDIAN + ['ASIAN'] * CT_RACE_SPLIT_ASIAN + ['BLACK OR AFRICAN AMERICAN'] * CT_RACE_SPLIT_BLACK + ['NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER'] * CT_RACE_SPLIT_NATIVE_HAWAIIAN + ['WHITE'] * CT_RACE_SPLIT_WHITE + ['NOT REPORTED'] * CT_RACE_SPLIT_NOT_REPORTED + ['UNKNOWN'] * CT_RACE_SPLIT_UNKNOWN
#
CT_ETHNICITY = ['Hispanic'] * CT_RACE_HISPANIC + ['Non-Hispanic'] * (100 - CT_RACE_HISPANIC)
#

# The Python dictionary described below defines this structure:
#	Each Visit has a number of Analysis per Visit
#		Each Analysis has number of Parameters per Analysis.
#
# Each Visit definition includes:
#	Visit ID
#	Visit Name:
# 	Days after enrollment
#	Participation rate: % of enrolled subjects that participate in this Visit.
#
# Each Analysis definition includes:
#	Analysis ID
#	Analysis Name
#	Days in delay for receiving results
#
# Each Parameter definition includes:
#	Paramater ID
#	Parameter Name
#	Lower limit of expected value
#	Upper limit of expected value
#	"Fuzz" factor: percentage above Upper and below Lower values to be used to trigger analytics rules and to validate Quality Control processes.
#
CT_VISIT_ANALYSIS_PARAMETER = {"visits": [
	{"visit_id" : "Visit_01", "visit_name" : "Visit 01 Name", "days_after_enrollment": 5, "participation_rate": 95, "analysis_list" : [
		{"analysis_id": "Analysis_01", "analysis_name": "Visit 01 Name - Analysis 01 Name", "parameter_list" : [
			{"parameter_id": "Parameter_01", "parameter_name": "Visit 01 Name - Analysis 01 - Parameter Name 01", "days_delay": 12, "value_list": [
					{"Lower limit": 12},
					{"Upper limit": 45},
					{"Fuzz factor": 0.35},
				]}, 			
			{"parameter_id": "Parameter_02", "parameter_name": "Visit 01 Name - Analysis 01 - Parameter Name 02",  "days_delay": 1, "value_list": [
					{"Lower limit": 120},
					{"Upper limit": 450},
					{"Fuzz factor": 0.15},
				]}, 
			{"parameter_id": "Parameter_03", "parameter_name": "Visit 01 Name - Analysis 01 - Parameter Name 03",  "days_delay": 6, "value_list": [
					{"Lower limit": 0.97},
					{"Upper limit": 2.67},
					{"Fuzz factor": 0.47},
				]
			}]
		}, 
		{"analysis_id": "Analysis_02", "analysis_name": "Visit 01 Name - Analysis 02 Name", "parameter_list" : [
			{"parameter_id": "Parameter_01", "parameter_name": "Visit 01 Name - Analysis 02 - Parameter Name 01",  "days_delay": 3, "value_list": [
					{"Lower limit": 1200},
					{"Upper limit": 4500},
					{"Fuzz factor": 0.15},
				]}, 			
			{"parameter_id": "Parameter_02", "parameter_name": "Visit 01 Name - Analysis 02 - Parameter Name 02",  "days_delay": 9, "value_list": [
					{"Lower limit": 12},
					{"Upper limit": 27},
					{"Fuzz factor": 0.68},
				]
			}]
		},],
	},
	{"visit_id" : "Visit_02", "visit_name" : "Visit 02 Name", "days_after_enrollment": 50, "participation_rate": 80, "analysis_list" :
		[{"analysis_id": "Analysis_01", "analysis_name": "Visit 02 Name - Analysis 01 Name", "parameter_list" : [
			{"parameter_id": "Parameter_01", "parameter_name": "Visit 02 Name - Analysis 01 - Parameter Name 01",  "days_delay": 2, "value_list": [
					{"Lower limit": 456},
					{"Upper limit": 678},
					{"Fuzz factor": 0.15},
				]}, 			
			{"parameter_id": "Parameter_02", "parameter_name": "Visit 02 Name - Analysis 01 - Parameter Name 02",  "days_delay": 10, "value_list": [
					{"Lower limit": 345678},
					{"Upper limit": 987654},
					{"Fuzz factor": 0.05},
				]}, 
			{"parameter_id": "Parameter_03", "parameter_name": "Visit 02 Name - Analysis 01 - Parameter Name 03",  "days_delay": 7, "value_list": [
					{"Lower limit": 0.0001},
					{"Upper limit": 0.0045},
					{"Fuzz factor": 0.04},
				]
			}]
		}],
	},
	{"visit_id" : "Visit_03", "visit_name" : "Visit 03 Name", "days_after_enrollment": 73, "participation_rate": 60, "analysis_list" :
		[{"analysis_id": "Analysis_01", "analysis_name": "Visit 03 Name - Analysis 01 Name", "parameter_list" : [
			{"parameter_id": "Parameter_01", "parameter_name": "Visit 03 Name - Analysis 01 - Parameter Name 01",  "days_delay": 2, "value_list": [
					{"Lower limit": 9},
					{"Upper limit": 13},
					{"Fuzz factor": 0.11},
				]}, 			
			{"parameter_id": "Parameter_02", "parameter_name": "Visit 03 Name - Analysis 01 - Parameter Name 02",  "days_delay": 10, "value_list": [
					{"Lower limit": 456},
					{"Upper limit": 1876},
					{"Fuzz factor": 0.51},
				]}, 
			{"parameter_id": "Parameter_03", "parameter_name": "Visit 03 Name - Analysis 01 - Parameter Name 03",  "days_delay": 7, "value_list": [
					{"Lower limit": 0.0001},
					{"Upper limit": 0.0045},
					{"Fuzz factor": 0.04},
				]},
			{"parameter_id": "Parameter_04", "parameter_name": "Visit 03 Name - Analysis 01 - Parameter Name 04",  "days_delay": 10, "value_list": [
					{"Lower limit": 1.3},
					{"Upper limit": 4.67},
					{"Fuzz factor": 0.16},
				]}, 
			{"parameter_id": "Parameter_05", "parameter_name": "Visit 03 Name - Analysis 01 - Parameter Name 05",  "days_delay": 7, "value_list": [
					{"Lower limit": 0.001},
					{"Upper limit": 0.045},
					{"Fuzz factor": 0.41},
				]
			}]
		}],
	},
]}
#
#
CT_DELAY_ANALYSIS_RESULT = 5	# Maximum number of days of delay in providing results of analysis.
#
# Trial site definitions:
#	Site name
#	Percentage of subjects enrolled at this site (MUST add up to 100):
CT_SITE_IDS = ['Site_01'] * 10 + ['Site_02'] * 20 + ['Site_03'] * 50 + ['Site_04'] * 20
#
CT_REFERENCE_RANGE_INDICATOR = ['NORMAL'] * 20 + ['LOW'] * 20 + ['HIGH'] * 20 + ['LOW LOW'] * 20 + ['HIGH HIGH'] * 20
#
CT_INVESTIGATORS = [['Investigator 01', 'INV01'], ['Investigator 02', 'INV02'], ['Investigator 03', 'INV03'], ['Investigator 04', 'INV04'], ['Investigator 05', 'INV05']]
#
CT_PERCENTAGE_DEATHS = ['DEATH'] * 15 + ['NONE'] * 85					# Percentage of subjects that die during the trial.
CT_CAUSES_DEATH = ['CAUSE OF DEATH 01'] * 15 + ['CAUSE OF DEATH 02'] * 35 + ['CAUSE OF DEATH 03'] * 50
CT_PERCENTAGE_DISCONTINUATION = ['DROP-OFF'] * 23 + ['FINISH'] * 77 	# Percentage of subjects that do not finish all phases of the trial.
CT_PERCENTAGE_ADVERSE_EVENTS = ['ADV-EV'] * 10 + ['NONE'] * 90			# Percentage of subjects taht experience at least 01 adverse event.
#
CT_GROUPS = ['Group_01'] * 10 + ['Group_02'] * 20 + ['Group_03'] * 50 + ['Group_04'] * 20
CT_ARM_NAMES = [['Arm 01', 'ARM01'], ['Arm 02', 'ARM02'], ['Arm 03', 'ARM03']]
#
CT_COUNTRY_ENROLLMENT = ['DE'] * 30 + ['ES'] * 20 + ['UK'] * 20 + ['VE'] * 10 + ['ZA'] * 10
#
CT_CSV_SEPARATOR = "|"	# Try NOT to use ',' (commas) to prevent file importing errors.
#
# = = = = = Do not change anything below this line = = = = =
#
if (len(sys.argv) != 6):
	print("Usage: python3 Roche_ADaM_Generation.py [StudyID] [TargetDirectory] [NumberSubjects] [DateStartRecruitment] [CurrentDate]\nUse YYYY-MM-DD for dates.\n")
	sys.exit()
	#
if (not os.path.isdir(sys.argv[2])):
	print("Error: TargetDirectory [%s] does not exist.\n" % (sys.argv[1]))
	sys.exit()
	#
CT_STUDY_ID = sys.argv[1]
CT_TARGET_DIRECTORY = sys.argv[2]
#
# Validate number of subjects:
CT_NUMBER_SUBJECTS = int(sys.argv[3])
assert (10 <= CT_NUMBER_SUBJECTS <= 999999),"Please enter a value between 10 and 999,999"
#
# Validate date:
CT_DATE_START_RECRUITMENT = datetime.datetime.strptime(sys.argv[4], '%Y-%m-%d')
assert (CT_DATE_START_RECRUITMENT, "Please enter a valid date using the format YYYY-MM-DD")
#
CT_DATE_CURRENT_DATE = datetime.datetime.strptime(sys.argv[5], '%Y-%m-%d')
assert (CT_DATE_CURRENT_DATE, "Please enter a valid date using the format YYYY-MM-DD")
#
# = = Common file headers = =
const_header_01 = """# (c) 2007-2020 NIHPO, Inc. - http://NIHPO.com   Licensed to PHUSE for non-commercial purposes only.   Contact: Jose.Lacal@NIHPO.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3."
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details."
# You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html"
# WARNING: This information is completely fake. Values such as Age and Gender are randomly assigned using a Weighted Random Generator."
# CREDIT: The specific fields used in this file are defined by a sample 'Analysis Dataset Programming Specification' Excel file generously provided by Roche."""
const_header_02 = """# This file was generated using the following parameters:
# 	Number of subjects: %d. Study ID: %s
# 	Minimum age: %d; Maximum age: %d
# 	Date recruitment started: %s. Date indicated as current date: %s
# 	Female split: %d
# 	Race splits:
# 		AMERICAN_INDIAN = %d
#		ASIAN = %d
#		BLACK = %d
#		NATIVE HAWAIIAN = %d
#		WHITE = %d
#		NOT REPORTED = %d
#		UNKNOWN = %d
# 	Percentage of 'Hispanic' race: %d
# 	The CSV separator is %s  """ % (CT_NUMBER_SUBJECTS, CT_STUDY_ID, CT_AGE_MINIMUM, CT_AGE_MAXIMUM, CT_DATE_START_RECRUITMENT, CT_DATE_CURRENT_DATE, CT_FEMALE_SPLIT, CT_RACE_SPLIT_AMERICAN_INDIAN, CT_RACE_SPLIT_ASIAN, CT_RACE_SPLIT_BLACK, CT_RACE_SPLIT_NATIVE_HAWAIIAN, CT_RACE_SPLIT_WHITE, CT_RACE_SPLIT_NOT_REPORTED, CT_RACE_SPLIT_UNKNOWN, CT_RACE_HISPANIC, CT_CSV_SEPARATOR)
#
# Open SQLite3 file:
try:
	nihpo_conn = sqlite3.connect('file:Synthetic_Health_Data_NIHPO.sqlite3?mode=ro', uri=True)
	nihpo_cursor = nihpo_conn.cursor()
except sqlite3.Error as e:
	print ("The SQLite3 file 'Synthetic_Health_Data_NIHPO.sqlite3' should be in your local path.")
	print ("Error {}:".format(e.args[0]))
	sys.exit(1)
#
#
# = = = Common functions = = =
def func_nihpo_synth_data_random_value (in_sqlite3_cursor, in_codelist):
	"""
	This function returns a random value from a particular codelist from the SQLite3 file "Synthetic_Health_Data_NIHPO.sqlite3"
	Inputs:
		in_sqlite3_cursor : [SQLite3 cursor] : Cursor to SQLite3 file.
		in_codelist : [String] : Code of interest.

	Return:
		Single value, randomly selected.

	To call this function:
		func_nihpo_synth_data_random_value(nihpo_cursor, <..>)
	"""
	var_sql = '''SELECT cdisc_submission_value FROM cdisc_terminology WHERE codelist_code = '%s' ORDER BY RANDOM() LIMIT 1;''' % (in_codelist)
	in_sqlite3_cursor.execute(var_sql)
	return in_sqlite3_cursor.fetchone()[0]
#
#
def func_nihpo_random_date_birth (in_base_date_object, in_minimum_age, in_maximum_age):
	"""
	This function returns a random Date of Birth, using a base date, and with a range of ages defined by a Minimum Age and a Maximum Age.
	Inputs:
		in_base_date_object 	[Date object]	Date object formatted as YYYY-MM-DD 
		in_minimum_age	[Integer]		Minimum age (in years) at in_base_date 
		in_maximum_age	[Integer]		Maximum age (in years) at in_base_date 

	Return:
		Date string, randomly selected.

	To call this function:
		func_nihpo_random_date_birth(DateObject=>"2020-01-25", 15, 80)
	"""
	#
	# Validation:
	assert (CT_AGE_MINIMUM <= in_minimum_age <= CT_AGE_MAXIMUM),"Please enter a value between %d and %d" % (CT_AGE_MINIMUM, CT_AGE_MAXIMUM)
	assert (in_minimum_age <= in_maximum_age <= CT_AGE_MAXIMUM),"Please enter a value between %d and %d" % (in_minimum_age, CT_AGE_MAXIMUM)
	#
	var_number_days_latest = in_minimum_age * 365		# Number of days before in_base_date for minimum age. 
	var_number_days_earliest = in_maximum_age * 365		# Number of days before in_base_date for maximum age. 
	#
	var_days_birth_before_in_base_date = random.randrange(var_number_days_latest, var_number_days_earliest)
	var_dob = in_base_date_object - datetime.timedelta(days=var_days_birth_before_in_base_date)
	#
	return var_dob.strftime('%Y-%m-%d')
#
#
def func_nihpo_random_date (in_start_date_string, in_minimum_days, in_maximum_days):
	"""
	This function returns a random Date, using a start date, and with a range of minimum and maximum additional days.
	Inputs:
		in_start_date_string 	[Date string]	Date formatted as YYYY-MM-DD 
		in_minimum_days	[Integer]		Minimum number of additional days.
		in_maximum_days	[Integer]		Maximum number of additional days. 

	Return:
		Date string, randomly selected.

	To call this function:
		func_nihpo_random_date("2020-01-25", 1, 17)
	"""
	# Validate date:
	start_date = datetime.datetime.strptime(in_start_date_string, '%Y-%m-%d')
	assert (start_date, "Please enter a valid date using the format YYYY-MM-DD")
	#
	assert (in_minimum_days < in_maximum_days),"Please a minimum number of days less than the maximum numnber of days."
	#
	var_random_days = random.randrange(in_minimum_days, in_maximum_days)
	var_random_date = datetime.datetime.strptime(in_start_date_string, '%Y-%m-%d') + datetime.timedelta(days=var_random_days)
	#
	return var_random_date.strftime('%Y-%m-%d')
#
#
def func_nihpo_random_date_between_range (in_start_date_object, in_end_date_object):
	"""
	This function returns a random Date between a starting date and and end date range.
	Inputs:
		in_start_date_object 	[Date object]	Date object formatted as YYYY-MM-DD 
		in_end_date_object		[Date object]	Date object formatted as YYYY-MM-DD 

	Return:
		Date 	[String] 	Randomly selected date within defined range of dates.
		Number 	[Integer]	Number of days after start date.

	To call this function:
		func_nihpo_random_date_between_range(DateObject=>"2020-01-25", DateObject=>"2020-06-25")
	"""
	#
	# Validation:
	assert (in_start_date_object < in_end_date_object),"Please ensure Start Date is earlier than End Date"
	#
	var_number_days_between_dates = (in_end_date_object - in_start_date_object).days		# Number of days between dates.
	var_random_number_days = random.randrange(1, var_number_days_between_dates)
	#
	var_random_date = in_start_date_object + datetime.timedelta(days=var_random_number_days)
	#
	return var_random_date.strftime('%Y-%m-%d'), var_random_number_days
#
#
def func_nihpo_random_value (in_lower_limit, in_upper_limit, in_fuzz_factor):
	"""
	This function returns a random value within a Lower limit and an Upper limit. With a fuzz factor to throw off calculations..
	Inputs:
		in_lower_limit	[Float] 	Minimum value to use for randomization.
		in_upper_limit	[Float] 	Maximum value to use.
		in_fuzz_factor	[Float] 	Maximum percentage the returned value can be below the Lower or above the Upper range.

	Return:
		Value Float, randomly selected.

	To call this function:
		func_nihpo_random_value(1, 2, .5)
	"""
	#
	# Validation:
	assert (in_lower_limit < in_upper_limit),"Please ensure Lower limit value is smaller than Upper limit value."
	assert(in_fuzz_factor <= 1), "Please enter a Fuzz Factor value below 1"
	#
	return random.uniform(in_lower_limit * (1+in_fuzz_factor), in_upper_limit * (1+in_fuzz_factor))
#
#

#
# = = Open output files for writing = =
var_output_file_ADSL = csv.writer(open(r"ADSL.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADSL.writerow([const_header_01])
var_output_file_ADSL.writerow([const_header_02])
var_output_file_ADSL.writerow(["# Dataset: ADSL", "Description: Subject Level Analysis Dataset"])
var_output_file_ADSL.writerow(["STUDYID", "USUBJID",  "SUBJID", "SITEID", "AGE", "AGEU", "SEX", "RACE", "ETHNIC", "COUNTRY", "DMDTC", "DMDY", "BRTHDTC", "DTHDTC", "DTHFL", "RFSTDTC", "RFENDTC", "RFXSTDTC", "RFXENDTC", "RFICDTC", "RFPENDTC", "INVID", "INVNAM", "ARM", "ARMCD", "ACTARM", "ACTARMCD", "BRTHDTF", "AAGE", "AAGEU", "AGEGR1", "ITTFL", "SAFFL", "PPROTFL", "FASFL", "TRT01P", "TRT01A", "RFICDT", "RANDDT", "BRTHDT", "TRTSDTM", "TRTSDT", "TRTEDTM", "TRTEDT", "TRTDURD", "EOSSTT", "EOSDT", "EOTSTT", "EOSDY", "EOSRDY", "DCSREAS", "DCSREASP", "DTHDT", "DTHCAUS", "ADTHAUT", "DTHADY", "AEWITHFL", "LSTALVDT"])
#
var_output_file_ADAE = csv.writer(open(r"ADAE.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADAE.writerow([const_header_01])
var_output_file_ADAE.writerow([const_header_02])
var_output_file_ADAE.writerow(["# Dataset: ADAE", "Description: Adverse Events Analysis Dataset"])
var_output_file_ADAE.writerow([	"STUDYID", "USUBJID", "SUBJID", "SITEID", "COUNTRY", "ETHNIC", "AGE", "AGEU", "AAGE", "AAGEU", "SEX", "RACE", "ITTFL", "SAFFL", "PPROTFL", "TRT01P", "TRT01A", "TRTSDTM", "TRTSDT", "TRTEDTM", "TRTEDT", "DOMAIN", "AESEQ", "AEGRPID", "AESPID", "AETERM", "AEMODIFY", "AELLT", "AELLTCD", "AEDECOD", "AEPTCD", "AEHLT", "AEHLTCD", "AEHLGT", "AEHLGTCD", "AECAT", "AESCAT", "AEPRESP", "AEBODSYS", "AEBDSYCD", "AESOC", "AESOCCD", "AELOC", "AESEV", "AESER", "AEACN", "AEACNOTH", "AEREL", "AERELNST", "AEPATT", "AEOUT", "AESCAN", "AESCONG", "AESDISAB", "AESDTH", "AESHOSP", "AESLIFE", "AESOD", "AESMIE", "AECONTRT", "AETOXGR", "EPOCH", "AESTDTC", "AEENDTC", "AESTDY", "AEENDY", "AEDUR", "AESTRTPT", "AESTTPT", "AEENRTPT", "AEENTPT", "AETRTEM", "ASTDTM", "ASTDT", "ASTDTF", "ASTTMF", "ASTDY", "AENDTM", "AENDT", "AENDTF", "AENTMF", "AENDY", "TRTEMFL", "PREFL", "FUPFL", "AREL", "ATOXGR", "ADURN", "ADURU", "LDOSEDTM", "LDOSEDT", "LDRELD", "AOCCIFL", "AOCCPIFL", "AOCCSIFL", "AOCXIFL", "AOCXPIFL", "AOCXSIFL", "ANL01FL"])
#
var_output_file_ADLB = csv.writer(open(r"ADLB.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADLB.writerow([const_header_01])
var_output_file_ADLB.writerow([const_header_02])
var_output_file_ADLB.writerow(["# Dataset: ADLB", "Description: Laboratory Analysis Dataset"])
var_output_file_ADLB.writerow(['STUDYID', 'USUBJID', 'SUBJID', 'SITEID', 'ASEQ', 'COUNTRY', 'ETHNIC', 'AGE', 'AGEU', 'AAGE', 'AAGEU', 'SEX', 'RACE', 'ITTFL', 'SAFFL', 'PPROTFL', 'TRT01P', 'TRT01A', 'TRTSDTM', 'TRTSDT', 'TRTEDTM', 'TRTEDT', 'DOMAIN', 'LBSEQ', 'LBGRPID', 'LBREFID', 'LBSPID', 'LBTESTCD', 'LBTEST', 'LBCAT', 'LBSCAT', 'LBORRES', 'LBORRESU', 'LBORNRLO', 'LBORNRHI', 'LBSTRESC', 'LBSTRESN', 'LBSTRESU', 'LBSTNRLO', 'LBSTNRHI', 'LBSTNRC', 'LBNRIND', 'LBSTAT', 'LBREASND', 'LBNAM', 'LBSPEC', 'LBSPCCND', 'LBMETHOD', 'LBBLFL', 'LBFAST', 'VISITNUM', 'VISIT', 'EPOCH', 'LBDTC', 'LBENDTC', 'LBDY', 'LBENDY', 'LBTPT', 'LBTPTNUM', 'LBELTM', 'LBTPTREF', 'LBTSTDTL', 'PARAM', 'PARAMCD', 'PARCAT1', 'PARCAT2', 'AVAL', 'AVALC', 'AVALU', 'AVALCAT1', 'BASE', 'BASETYPE', 'ABLFL', 'CHG', 'PCHG', 'ANRHI', 'ANRLO', 'ANRIND', 'BNRIND', 'R2BASE', 'R2ANRLO', 'R2ANRHI', 'SHIFT1', 'ATOXGR', 'BTOXGR', 'ADTM', 'ADT', 'ADTF', 'ATMF', 'ADY', 'ATPT', 'ATPTN', 'AVISIT', 'AVISITN', 'ONTRTFL', 'LAST01FL', 'WORS01FL', 'WGRHIFL', 'WGRLOFL', 'WGRHIVFL', 'WGRLOVFL', 'ANL01FL'])
#
var_output_file_ADHY = csv.writer(open(r"ADHY.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADHY.writerow([const_header_01])
var_output_file_ADHY.writerow([const_header_02])
var_output_file_ADHY.writerow(["# Dataset: ADHY", "Description: Hys Law Analysis Dataset"])
var_output_file_ADHY.writerow(['STUDYID','USUBJID','SUBJID','SITEID','ASEQ','COUNTRY','ETHNIC','AGE','AGEU','AAGE','AAGEU','SEX','RACE','ITTFL','SAFFL','PPROTFL','TRT01P','TRT01A','TRTSDTM','TRTSDT','TRTEDTM','TRTEDT','PARAM','PARAMCD','AVAL','AVALC','AVALU','BASE','BASEC','ABLFL','ANRLO','ANRHI','ADTM','ADT','ADY','ADTF','ATMF','AVISIT','AVISITN','ONTRTFL','CRIT1','CRIT1FL','CRIT1FN','CRIT2','CRIT2FL','CRIT2FN','MCRIT1','MCRIT1ML','SRCDOM','SRCVAR','SRCSEQ','ANL01FL'])
#
var_output_file_ADSAFTTE = csv.writer(open(r"ADSAFTTE.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADSAFTTE.writerow([const_header_01])
var_output_file_ADSAFTTE.writerow([const_header_02])
var_output_file_ADSAFTTE.writerow(["# Dataset: ADSAFTTE", "Description: Safety Time to Event Analysis Dataset"])
var_output_file_ADSAFTTE.writerow(['STUDYID','USUBJID','SUBJID','SITEID','ASEQ','REGION1','COUNTRY','ETHNIC','AGE','AGEU','AAGE','AAGEU','AGEGR1','AGEGR2','AGEGR3','STRATwNM','STRATw','STRATwV','SEX','RACE','ITTFL','SAFFL','PPROTFL','TRT01P','TRTxxP','TRT01A','TRTxxA','TRTSEQP','TRTSEQA','TRTSDTM','TRTSDT','TRTEDTM','TRTEDT','DCUTDT','PARAM','PARAMCD','PARCAT1','AVAL','AVALU','STARTDT','STARTDTF','ADT','ADY','ADTF','CNSR','EVNTDESC','CNSDTDSC','SRCDOM','SRCVAR','SRCSEQ','ANL01FL'])
#


# = = NOTICE = =
# Fields where the content looks like this "-DMDTC-" (with a starting and an ending dash '-') still need processing.
# = =


#
# Global Counters:
var_subject_counter = 1
var_ADAE_Sequence_Number = 1
var_Analysis_Sequence_Number = 1
var_Specimen_ID = 12376
#
while var_subject_counter <= CT_NUMBER_SUBJECTS:
	print ("Processing subject # %d \n" % (var_subject_counter))
	#
	# = ADSL file =
	# One record per subject
	var_ADSL_STUDYID = CT_STUDY_ID											# Study Identifier	text	8		
	var_ADSL_USUBJID = str(uuid.uuid4())									# Unique Subject Identifier	text	50		
	var_ADSL_SUBJID = str(uuid.uuid4())										# Subject Identifier for the Study	text	50		
	var_ADSL_SITEID = random.choice(CT_SITE_IDS)							# Study Site Identifier	text	20		
	#
	var_ADSL_BRTHDTC = func_nihpo_random_date_birth(CT_DATE_START_RECRUITMENT, CT_AGE_MINIMUM, CT_AGE_MAXIMUM)				# Date/Time of Birth	dateTime	25		ISO8601
	var_ADSL_AGE = CT_DATE_START_RECRUITMENT.year - datetime.datetime.strptime(var_ADSL_BRTHDTC, '%Y-%m-%d').year 			# Age	integer	8		
	#
	var_ADSL_AGEU = "Years"													# Age Units	text	6	C66781	Age Unit
	var_ADSL_SEX = random.choice(CT_GENDER_SPLIT)							# Sex	text	2	C66731	Sex
	var_ADSL_RACE = random.choice(CT_RACE_SPLIT)							# Race	text	200	C74457	Race
	var_ADSL_ETHNIC = random.choice(CT_ETHNICITY)							# Ethnicity	text	200		
	var_ADSL_COUNTRY = random.choice(CT_COUNTRY_ENROLLMENT)					# Country	text	3		ISO3166
	var_ADSL_DMDTC = "-DMDTC-"												# Date/Time of Collection	dateTime	25		ISO8601
	var_ADSL_DMDY = "-DMDY-"												# Study Day of Collection	integer	8
	#
	# - Death-related fields -	
	# First, determine if this subject would die during the trial:
	var_ADSL_death = random.choice(CT_PERCENTAGE_DEATHS)
	if (var_ADSL_death == 'DEATH'):
		var_ADSL_DTHFL = "YES"												# Subject Death Flag	text	2	C66742	No Yes Response
		var_ADSL_DTHDTC, var_ADSL_DTHADY = func_nihpo_random_date_between_range(CT_DATE_START_RECRUITMENT, CT_DATE_CURRENT_DATE)
		# DTHDTC = Date/Time of Death	dateTime	25		ISO8601
		# DTHADY = Relative Day of Death	integer	8
		var_ADSL_DTHDT = var_ADSL_DTHDTC									# Date of Death	integer	8		
		var_ADSL_DTHCAUS = random.choice(CT_CAUSES_DEATH)					# Cause of Death	text	200		
		var_ADSL_ADTHAUT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')											# Autopsy Performed	text	1	C66742	No Yes Response												
		var_ADSL_LSTALVDT = var_ADSL_DTHDTC									# Date Last Known Alive	integer	8
	else:
		var_ADSL_DTHFL = "NO"												# Subject Death Flag	text	2	C66742	No Yes Response
		var_ADSL_DTHDTC = "-DTHDTC-"											# Date/Time of Death	dateTime	25		ISO8601
		var_ADSL_DTHDT = "-DTHDT-"												# Date of Death	integer	8		
		var_ADSL_DTHCAUS = "-DTHCAUS-"											# Cause of Death	text	200		
		var_ADSL_ADTHAUT = "-ADTHAUT-"											# Autopsy Performed	text	1	C66742	No Yes Response
		var_ADSL_DTHADY = "-DTHADY-"											# Relative Day of Death	integer	8		
		var_ADSL_LSTALVDT = "-LSTALVDT-"										# Date Last Known Alive	integer	8
	#
	var_ADSL_RFSTDTC = "-RFSTDTC-"											# Subject Reference Start Date/Time	dateTime	25		ISO8601
	var_ADSL_RFENDTC = "-RFENDTC-"											# Subject Reference End Date/Time	dateTime	25		ISO8601
	var_ADSL_RFXSTDTC = "-RFXSTDTC-"										# Date/Time of First Study Treatment	dateTime	25		ISO8601
	var_ADSL_RFXENDTC = "-RFXENDTC-"										# Date/Time of Last Study Treatment	dateTime	25		ISO8601
	var_ADSL_RFICDTC = "-RFICDTC-"											# Date/Time of Informed Consent	dateTime	25		ISO8601
	var_ADSL_RFPENDTC = "-RFPENDTC-"										# Date/Time of End of Participation	dateTime	25		ISO8601
	#
	var_investigator_name, var_investigator_code = random.choice(CT_INVESTIGATORS)
	var_ADSL_INVID = var_investigator_code									# Investigator Identifier	text	20		
	var_ADSL_INVNAM = var_investigator_name									# Investigator Name	text	200		
	#
	var_arm_name, var_arm_code = random.choice(CT_ARM_NAMES)
	var_ADSL_ARM = var_arm_name												# Description of Planned Arm	text	200	L00060	Description of Planned Arm
	var_ADSL_ARMCD = var_arm_code											# Planned Arm Code	text	20	L00059	Planned Arm Code
	var_ADSL_ACTARM = var_arm_name											# Description of Actual Arm	text	200		
	var_ADSL_ACTARMCD = var_arm_code										# Actual Arm Code	text	20		
	#
	var_ADSL_BRTHDTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')							# Imputed Birth Date Flag	text	1	C81223	Date Imputation Flag
	var_ADSL_AAGE = var_ADSL_AGE											# Analysis Age	integer	8		
	var_ADSL_AAGEU = var_ADSL_AGEU											# Analysis Age Unit	text	6	C66781	Age Unit
	var_ADSL_AGEGR1 = "AGEGR1"												# Pooled Age Group 1	text	10		
	var_ADSL_ITTFL = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')					# Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
	var_ADSL_SAFFL = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')					# Safety Population Flag	text	1	C66742	No Yes Response
	var_ADSL_PPROTFL = "PPROTFL"											# Per-Protocol Population Flag	text	1	C66742	No Yes Response
	var_ADSL_FASFL = "FASFL"												# Full Analysis Set Population Flag	text	1	C66742	No Yes Response
	var_ADSL_TRT01P = "TRT01P"												# Planned Treatment for Period 01	text	200		
	var_ADSL_TRT01A = "TRT01A"												# Actual Treatment for Period 01	text	200		
	var_ADSL_RFICDT = "RFICDT"												# Date of Informed Consent	integer	8		
	var_ADSL_RANDDT = "RANDDT"												# Date of Randomization	integer	8		
	var_ADSL_BRTHDT = "BRTHDT"												# Imputed Birth Date	integer	8		
	var_ADSL_TRTSDTM = "TRTSDTM"											# Datetime of First Exposure to Treatment	integer	8		
	var_ADSL_TRTSDT = "TRTSDT"												# Date of First Exposure to Treatment	integer	8		
	var_ADSL_TRTEDTM = "TRTEDTM"											# Datetime of Last Exposure to Treatment	integer	8		
	var_ADSL_TRTEDT = "TRTEDT"												# Date of Last Exposure to Treatment	integer	8		
	var_ADSL_TRTDURD = "TRTDURD"											# Total Treatment Duration (Days)	integer	8		
	var_ADSL_EOSSTT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C124296')				# End of Study Status	text	12	C124296	Subject Trial Status
	var_ADSL_EOSDT = "EOSDT"												# End of Study Date	integer	8		
	var_ADSL_EOTSTT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C124296')				# End of Treatment Status	text	12	C124296	Subject Trial Status
	var_ADSL_EOSDY = "EOSDY"												# End of Study Relative Day	integer	8		
	var_ADSL_EOSRDY = "EOSRDY"												# End of Study Day Rel to Randomization	integer	8		
	var_ADSL_DCSREAS = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66727')				# Reason for Discontinuation from Study	text	200	C66727	Completion/Reason for Non-Completion
	var_ADSL_DCSREASP = "DCSREASP"											# Reason Spec for Discont from Study	text	200		
	var_ADSL_AEWITHFL = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# AE Leading to Drug Withdrawal Flag	text	1	C66742	No Yes Response		
	#
	#
	# = ADAE file =
	# One record per each record in the corresponding SDTM domain.
	# First, determine if this subject would suffer an Adverse Event during the trial:
	var_ADAE_adverse_event = random.choice(CT_PERCENTAGE_ADVERSE_EVENTS)
	if (var_ADAE_adverse_event == 'ADV-EV'):
		#
		var_ADAE_STUDYID = CT_STUDY_ID											# Study Identifier	text	8		
		var_ADAE_USUBJID = var_ADSL_USUBJID										# Unique Subject Identifier	text	50		
		var_ADAE_SUBJID = var_ADSL_SUBJID 										# Subject Identifier for the Study	text	50		
		var_ADAE_SITEID = var_ADSL_SITEID										# Study Site Identifier	text	20		
		var_ADAE_COUNTRY = var_ADSL_COUNTRY										# Country	text	3		ISO3166
		var_ADAE_ETHNIC = var_ADSL_ETHNIC										# Ethnicity	text	200		
		var_ADAE_AGE = var_ADSL_AGE												# Age	integer	8		
		var_ADAE_AGEU = var_ADSL_AGEU 											# Age Units	text	6	C66781	Age Unit
		var_ADAE_AAGE = var_ADSL_AAGE											# Analysis Age	integer	8		
		var_ADAE_AAGEU = var_ADSL_AAGEU											# Analysis Age Unit	text	6	C66781	Age Unit
		var_ADAE_SEX = var_ADSL_SEX												# Sex	text	2	C66731	Sex
		var_ADAE_RACE = var_ADSL_RACE 											# Race	text	200	C74457	Race
		var_ADAE_ITTFL = var_ADSL_ITTFL											# Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
		var_ADAE_SAFFL = var_ADSL_SAFFL											# Safety Population Flag	text	1	C66742	No Yes Response
		var_ADAE_PPROTFL = var_ADSL_PPROTFL										# Per-Protocol Population Flag	text	1	C66742	No Yes Response
		var_ADAE_TRT01P = var_ADSL_TRT01P										# Planned Treatment for Period 01	text	200		
		var_ADAE_TRT01A = var_ADSL_TRT01A										# Actual Treatment for Period 01	text	200		
		var_ADAE_TRTSDTM = var_ADSL_TRTSDTM										# Datetime of First Exposure to Treatment	integer	8		
		var_ADAE_TRTSDT = var_ADSL_TRTSDT										# Date of First Exposure to Treatment	integer	8		
		var_ADAE_TRTEDTM = var_ADSL_TRTEDTM										# Datetime of Last Exposure to Treatment	integer	8		
		var_ADAE_TRTEDT = var_ADSL_TRTEDT										# Date of Last Exposure to Treatment	integer	8		
		var_ADAE_DOMAIN = "-DOMAIN-"											# Domain Abbreviation	text	2	C66734	SDTM Domain Abbreviation
		var_ADAE_AESEQ = var_ADAE_Sequence_Number								# Sequence Number	integer	8
		var_ADAE_AEGRPID = random.choice(CT_GROUPS)								# Group ID	text	40		
		var_ADAE_AESPID = str(uuid.uuid4())										# Sponsor-Defined Identifier	text	200
		#
		var_ADAE_AETERM = "-AETERM-"											# Reported Term for the Adverse Event	text	200		
		var_ADAE_AEMODIFY = "-AEMODIFY-"										# Modified Reported Term	text	200		
		var_ADAE_AELLT = "-AELLT-"												# Lowest Level Term	text	100		MedDRA
		var_ADAE_AELLTCD = "-AELLTCD-"											# Lowest Level Term Code	integer	8		MedDRA
		var_ADAE_AEDECOD = "-AEDECOD-"											# Dictionary-Derived Term	text	200		MedDRA
		var_ADAE_AEPTCD = "-AEPTCD-"											# Preferred Term Code	integer	8		MedDRA
		var_ADAE_AEHLT = "-AEHLT-"												# High Level Term	text	100		MedDRA
		var_ADAE_AEHLTCD = "-AEHLTCD-"											# High Level Term Code	integer	8		MedDRA
		var_ADAE_AEHLGT = "-AEHLGT-"											# High Level Group Term	text	100		MedDRA
		var_ADAE_AEHLGTCD = "-AEHLGTCD-"										# High Level Group Term Code	integer	8		MedDRA
		var_ADAE_AECAT = "-AECAT-"												# Category for Adverse Event	text	100		*
		var_ADAE_AESCAT = "-AESCAT-"											# Subcategory for Adverse Event	text	100		
		var_ADAE_AEPRESP = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')			# Pre-Specified Adverse Event	text	2	C66742	No Yes Response
		var_ADAE_AEBODSYS = "-AEBODSYS-"										# Body System or Organ Class	text	200		MedDRA
		var_ADAE_AEBDSYCD = "-AEBDSYCD-"										# Body System or Organ Class Code	integer	8		MedDRA
		var_ADAE_AESOC = "-AESOC-"												# Primary System Organ Class	text	200		MedDRA
		var_ADAE_AESOCCD = "-AESOCCD-"											# Primary System Organ Class Code	integer	8		MedDRA
		var_ADAE_AELOC = func_nihpo_synth_data_random_value(nihpo_cursor, 'C74456')					# Location of Event	text	200	C74456	Anatomical Location
		var_ADAE_AESEV = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66769')					# Severity/Intensity	text	10	C66769	Severity/Intensity Scale for Adverse Events
		var_ADAE_AESER = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')					# Serious Event	text	2	C66742	No Yes Response
		var_ADAE_AEACN = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66767')					# Action Taken with Study Treatment	text	16	C66767	Action Taken with Study Treatment
		var_ADAE_AEACNOTH = "-AEACNOTH-"										# Other Action Taken	text	200		
		var_ADAE_AEREL = "-AEREL-"												# Causality	text	20		*
		var_ADAE_AERELNST = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Relationship to Non-Study Treatment	text	200	C66742	No Yes Response
		var_ADAE_AEPATT = "-AEPATT-"									#	Pattern of Adverse Event	text	40	L00004	Adverse Event Pattern
		var_ADAE_AEOUT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66768')					# Outcome of Adverse Event	text	40	C66768	Outcome of Event
		var_ADAE_AESCAN = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Involves Cancer	text	2	C66742	No Yes Response
		var_ADAE_AESCONG = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Congenital Anomaly or Birth Defect	text	2	C66742	No Yes Response
		var_ADAE_AESDISAB = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Persist or Signif Disability/Incapacity	text	2	C66742	No Yes Response
		var_ADAE_AESDTH = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Results in Death	text	2	C66742	No Yes Response
		var_ADAE_AESHOSP = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Requires or Prolongs Hospitalization	text	2	C66742	No Yes Response
		var_ADAE_AESLIFE = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Is Life Threatening	text	2	C66742	No Yes Response
		var_ADAE_AESOD = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')					# Occurred with Overdose	text	2	C66742	No Yes Response
		var_ADAE_AESMIE = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Other Medically Important Serious Event	text	2	C66742	No Yes Response
		var_ADAE_AECONTRT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')				# Concomitant or Additional Trtmnt Given	text	2	C66742	No Yes Response
		var_ADAE_AETOXGR = "-AETOXGR-"											# Standard Toxicity Grade	text	1		*
		#
		var_ADAE_EPOCH = func_nihpo_synth_data_random_value(nihpo_cursor, 'C99079')									#	Epoch	text	40	C99079	Epoch
		var_ADAE_AESTDTC = "-AESTDTC-"											# Start Date/Time of Adverse Event	dateTime	25		ISO 8601
		var_ADAE_AEENDTC = "-AEENDTC-"											# End Date/Time of Adverse Event	dateTime	25		ISO 8601
		var_ADAE_AESTDY = "-AESTDY-"											# Study Day of Start of Adverse Event	integer	8		
		var_ADAE_AEENDY = "-AEENDY-"											# Study Day of End of Adverse Event	integer	8		
		var_ADAE_AEDUR = "-AEDUR-"												# Duration of Adverse Event	duration	25		ISO 8601
		var_ADAE_AESTRTPT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66728')									#	Start Relative to Reference Time Point	text	20	C66728	Relation to Reference Period
		var_ADAE_AESTTPT = "-AESTTPT-"											# Start Reference Time Point	text	40		
		var_ADAE_AEENRTPT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66728')									#	End Relative to Reference Time Point	text	20	C66728	Relation to Reference Period
		var_ADAE_AEENTPT = "-AEENTPT-"											# End Reference Time Point	text	40		
		var_ADAE_AETRTEM = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')									#	Treatment Emergent Flag	text	2	C66742	No Yes Response
		#
		var_ADAE_ASTDTM = "-ASTDTM-"											# Analysis Start Date/Time	integer	8		
		var_ADAE_ASTDT = "-ASTDT-"												# Analysis Start Date	integer	8		
		var_ADAE_ASTDTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')									#	Analysis Start Date Imputation Flag	text	1	C81223	Date Imputation Flag
		var_ADAE_ASTTMF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81226')									#	Analysis Start Time Imputation Flag	text	1	C81226	Time Imputation Flag
		var_ADAE_ASTDY = "-ASTDY-"												# Analysis Start Relative Day	integer	8		
		var_ADAE_AENDTM = "-AENDTM-"											# Analysis End Date/Time	integer	8		
		var_ADAE_AENDT = "-AENDT-"												# Analysis End Date	integer	8		
		var_ADAE_AENDTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')									#	Analysis End Date Imputation Flag	text	1	C81223	Date Imputation Flag
		var_ADAE_AENTMF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81226')									#	Analysis End Time Imputation Flag	text	1	C81226	Time Imputation Flag
		var_ADAE_AENDY = "-AENDY-"												# Analysis End Relative Day	integer	8		
		#
		var_ADAE_TRTEMFL = "-TRTEMFL-"											# Treatment Emergent Analysis Flag	text	1	L00052	Yes Response
		var_ADAE_PREFL = "-PREFL-"												# Pre-treatment Flag	text	1	L00052	Yes Response
		var_ADAE_FUPFL = "-FUPFL-"												# Follow-up Flag	text	1	L00052	Yes Response
		var_ADAE_AREL = "-AREL-"												# Analysis Causality	text	50		*
		var_ADAE_ATOXGR = "-ATOXGR-"											# Analysis Toxicity Grade	text	50		*
		var_ADAE_ADURN = "-ADURN-"												# Analysis Duration (N)	float	8		
		var_ADAE_ADURU = func_nihpo_synth_data_random_value(nihpo_cursor, 'C71620')									#	Analysis Duration Units	text	40	C71620	Unit
		var_ADAE_LDOSEDTM = "-LDOSEDTM-"										# End Date/Time of Last Dose	integer	8		
		var_ADAE_LDOSEDT = "-LDOSEDT-"											# End Date of Last Dose	integer	8		
		var_ADAE_LDRELD = "-LDRELD-"											# Day Since Last Dose	integer	8		
		var_ADAE_AOCCIFL = "-AOCCIFL-"											# 1st Max Sev./Int. Occurrence Flag	text	1	L00052	Yes Response
		var_ADAE_AOCCPIFL = "-AOCCPIFL-"										# 1st Max Sev./Int. Occur Within PT Flag	text	1	L00052	Yes Response
		var_ADAE_AOCCSIFL = "-AOCCSIFL-"										# 1st Max Sev./Int. Occur Within SOC Flag	text	1	L00052	Yes Response
		var_ADAE_AOCXIFL = "-AOCXIFL-"											# 1st Max Sev./Int. Occ per Period	text	1	L00052	Yes Response
		var_ADAE_AOCXPIFL = "-AOCXPIFL-"										# 1st Max Sev./Int. Occ in PT per Period	text	1	L00052	Yes Response
		var_ADAE_AOCXSIFL = "-AOCXSIFL-"										# 1st Max Sev./Int. Occ in SOC per Period	text	1	L00052	Yes Response
		var_ADAE_ANL01FL = "-ANL01FL-"											# Analysis Flag 01	text	1	L00052	Yes Response
		#
		var_ADAE_Sequence_Number += 1
		# Write ADAE record to file:
		var_output_file_ADAE.writerow([	var_ADAE_STUDYID, var_ADAE_USUBJID, var_ADAE_SUBJID, var_ADAE_SITEID, var_ADAE_COUNTRY, var_ADAE_ETHNIC, var_ADAE_AGE, var_ADAE_AGEU, var_ADAE_AAGE, var_ADAE_AAGEU, var_ADAE_SEX, var_ADAE_RACE, var_ADAE_ITTFL, var_ADAE_SAFFL, var_ADAE_PPROTFL, var_ADAE_TRT01P, var_ADAE_TRT01A, var_ADAE_TRTSDTM, var_ADAE_TRTSDT, var_ADAE_TRTEDTM, var_ADAE_TRTEDT, var_ADAE_DOMAIN, var_ADAE_AESEQ, var_ADAE_AEGRPID, var_ADAE_AESPID, var_ADAE_AETERM, var_ADAE_AEMODIFY, var_ADAE_AELLT, var_ADAE_AELLTCD, var_ADAE_AEDECOD, var_ADAE_AEPTCD, var_ADAE_AEHLT, var_ADAE_AEHLTCD, var_ADAE_AEHLGT, var_ADAE_AEHLGTCD, var_ADAE_AECAT, var_ADAE_AESCAT, var_ADAE_AEPRESP, var_ADAE_AEBODSYS, var_ADAE_AEBDSYCD, var_ADAE_AESOC, var_ADAE_AESOCCD, var_ADAE_AELOC, var_ADAE_AESEV, var_ADAE_AESER, var_ADAE_AEACN, var_ADAE_AEACNOTH, var_ADAE_AEREL, var_ADAE_AERELNST, var_ADAE_AEPATT, var_ADAE_AEOUT, var_ADAE_AESCAN, var_ADAE_AESCONG, var_ADAE_AESDISAB, var_ADAE_AESDTH, var_ADAE_AESHOSP, var_ADAE_AESLIFE, var_ADAE_AESOD, var_ADAE_AESMIE, var_ADAE_AECONTRT, var_ADAE_AETOXGR, var_ADAE_EPOCH, var_ADAE_AESTDTC, var_ADAE_AEENDTC, var_ADAE_AESTDY, var_ADAE_AEENDY, var_ADAE_AEDUR, var_ADAE_AESTRTPT, var_ADAE_AESTTPT, var_ADAE_AEENRTPT, var_ADAE_AEENTPT, var_ADAE_AETRTEM, var_ADAE_ASTDTM, var_ADAE_ASTDT, var_ADAE_ASTDTF, var_ADAE_ASTTMF, var_ADAE_ASTDY, var_ADAE_AENDTM, var_ADAE_AENDT, var_ADAE_AENDTF, var_ADAE_AENTMF, var_ADAE_AENDY, var_ADAE_TRTEMFL, var_ADAE_PREFL, var_ADAE_FUPFL, var_ADAE_AREL, var_ADAE_ATOXGR, var_ADAE_ADURN, var_ADAE_ADURU, var_ADAE_LDOSEDTM, var_ADAE_LDOSEDT, var_ADAE_LDRELD, var_ADAE_AOCCIFL, var_ADAE_AOCCPIFL, var_ADAE_AOCCSIFL, var_ADAE_AOCXIFL, var_ADAE_AOCXPIFL, var_ADAE_AOCXSIFL, var_ADAE_ANL01FL])



	# = = NOTE = =
	# The following 03 files (ADLB; ADHY; and ADSAFTTE) contain records that are generated as follows:
	# 		One record per subject per parameter per analysis visit per analysis date.
	# 		_x000D_ SDTM variables are populated on new records coming from other single records.  Otherwise, SDTM variables are left blank.


	"""
	[Tue 07 July 2020]
	I probably need to generate a "Baseline" record for each Subject.
	Including (random) starting values for all Parameters addressed in each Analysis.
	Then, during each Visit, Parameters are randomly generated for the visit and compared against the Baseline.

	Create an in-memory dictionary:
		Dates
			* Enrollment
			* Each Visit
			* Date results are available
			* Relative Day (since start of participation)

		Parameter:
			* Baseline value
			* Measure (each Visit)
			* Compare measure with Baseline
	"""

	#
	# = = Process Visit = =
	var_number_visits = len(CT_VISIT_ANALYSIS_PARAMETER['visits'])
	if (CT_DEBUG == 2):
		print ("\n\nThere is(are) %d visit(s) defined for this trial." % (var_number_visits))
	#
	# Loop through each available Visit:
	var_counter_visit = 0			# Reset counter.
	while var_counter_visit < var_number_visits:
		var_current_visit_name = CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['visit_name']
		if (CT_DEBUG == 2):
			print ("\n\n  Processing [%s]" % (var_current_visit_name))
		#
		# = = Process Analysis = =
		var_number_analysis = len(CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'])
		if (CT_DEBUG == 2):
			print ("\n    There is(are) %d analysis item(s) defined for visit [%s]." % (var_number_analysis, var_current_visit_name))
		#

		# Loop through each available Analysis:
		var_counter_analysis = 0	# Reset counter.
		while var_counter_analysis < var_number_analysis:
			var_current_analysis_name = CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'][var_counter_analysis]['analysis_name']
			if (CT_DEBUG == 2):
				print ("\n      Processing [%s] - [%s]" % (var_current_visit_name, var_current_analysis_name))
			#
			# = = Process Parameters = =
			var_number_parameters = len(CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'][var_counter_analysis]['parameter_list'])
			if (CT_DEBUG == 2):
				print ("        There is(are) %d parameter(s) defined for this analysis." % (var_number_parameters))
			#
			# Loop through each available Parameter:
			var_counter_parameter = 0	# Reset counter.
			while var_counter_parameter < var_number_parameters:
				# Returned values are Python dictionaries:
				dict_parameter_lower_limit = CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'][var_counter_analysis]['parameter_list'][var_counter_parameter]['value_list'][0]
				dict_parameter_upper_limit = CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'][var_counter_analysis]['parameter_list'][var_counter_parameter]['value_list'][1]
				dict_parameter_fuzz_factor = CT_VISIT_ANALYSIS_PARAMETER['visits'][var_counter_visit]['analysis_list'][var_counter_analysis]['parameter_list'][var_counter_parameter]['value_list'][2]
				#
				for key, value in dict_parameter_lower_limit.items():
					var_parameter_lower_limit = value
				#
				for key, value in dict_parameter_upper_limit.items():
					var_parameter_upper_limit = value
				#
				for key, value in dict_parameter_fuzz_factor.items():
					var_parameter_fuzz_factor = value
				#
				if (CT_DEBUG == 2):
					print (var_parameter_lower_limit, var_parameter_upper_limit, var_parameter_fuzz_factor)
					print (func_nihpo_random_value (var_parameter_lower_limit, var_parameter_upper_limit, var_parameter_fuzz_factor))

				# = ADLB file =
				var_ADLB_STUDYID = CT_STUDY_ID 									# Study Identifier	text	8		
				var_ADLB_USUBJID = var_ADSL_USUBJID 							# Unique Subject Identifier	text	50		
				var_ADLB_SUBJID = var_ADSL_SUBJID 								# Subject Identifier for the Study	text	50		
				var_ADLB_SITEID  = var_ADSL_SITEID 								# Study Site Identifier	text	20		
				var_ADLB_ASEQ = var_Analysis_Sequence_Number 					# Analysis Sequence Number	integer	8		
				var_ADLB_COUNTRY = var_ADSL_COUNTRY 							# Country	text	32		ISO3166
				var_ADLB_ETHNIC = var_ADSL_ETHNIC								# Ethnicity	text	32		
				var_ADLB_AGE = var_ADSL_AGE										# Age	integer	8		
				var_ADLB_AGEU = var_ADSL_AGEU 									# Age Units	text	5	C66781	Age Unit
				var_ADLB_AAGE = "-AAGE-" 										# Analysis Age	integer	8		
				var_ADLB_AAGEU = "-AAGEU" 										# Analysis Age Unit	text	6	C66781	Age Unit
				var_ADLB_SEX = var_ADSL_SEX										# Sex	text	1	C66731	Sex
				var_ADLB_RACE = var_ADSL_RACE 									# Race	text	32	C74457	Race
				var_ADLB_ITTFL = var_ADSL_ITTFL									# Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
				var_ADLB_SAFFL = var_ADSL_SAFFL									# Safety Population Flag	text	1	C66742	No Yes Response
				var_ADLB_PPROTFL = var_ADSL_PPROTFL								# Per-Protocol Population Flag	text	1	C66742	No Yes Response
				var_ADLB_TRT01P = var_ADSL_TRT01P									#	Planned Treatment for Period 01	text	200		
				var_ADLB_TRT01A = var_ADSL_TRT01A									#	Actual Treatment for Period 01	text	200		
				var_ADLB_TRTSDTM = var_ADSL_TRTSDTM									#	Datetime of First Exposure to Treatment	integer	8		
				var_ADLB_TRTSDT = var_ADSL_TRTSDT									#	Date of First Exposure to Treatment	integer	8		
				var_ADLB_TRTEDTM = var_ADSL_TRTEDTM									#	Datetime of Last Exposure to Treatment	integer	8		
				var_ADLB_TRTEDT = var_ADSL_TRTEDT									#	Date of Last Exposure to Treatment	integer	8		
				var_ADLB_DOMAIN = "-DOMAIN-"											# Domain Abbreviation	text	2	C66734	SDTM Domain Abbreviation
				var_ADLB_LBSEQ = var_ADAE_Sequence_Number									# Sequence Number	integer	8		
				var_ADLB_LBGRPID = "-LBGRPID-"											# Group ID	text	40		
				var_ADLB_LBREFID = var_Specimen_ID											# Specimen ID	text	40		
				#
				try:
					var_ADLB_LBSPID = var_ADAE_AESPID											# Sponsor-Defined Identifier	text	200	
				except NameError: 
					var_ADLB_LBSPID = "-LBSPID-"
				#
				var_ADLB_LBTESTCD = func_nihpo_synth_data_random_value(nihpo_cursor, 'C65047')			# Lab Test or Examination Short Name	text	8	C65047	Laboratory Test Code
				var_ADLB_LBTEST = func_nihpo_synth_data_random_value(nihpo_cursor, 'C67154')			# Lab Test or Examination Name	text	40	C67154	Laboratory Test Name
				var_ADLB_LBCAT = "-LBCAT-"									#	Category for Lab Test	text	100		
				var_ADLB_LBSCAT = "-LBSCAT-"									#	Subcategory for Lab Test	text	100		
				var_ADLB_LBORRES = "-LBORRES-"									#	Result or Finding in Original Units	text	200		
				var_ADLB_LBORRESU = func_nihpo_synth_data_random_value(nihpo_cursor, 'C71620')			# Original Units	text	40	C71620	Unit
				var_ADLB_LBORNRLO = var_parameter_lower_limit											# Reference Range Lower Limit in Orig Unit	text	200		
				var_ADLB_LBORNRHI = var_parameter_upper_limit											# Reference Range Upper Limit in Orig Unit	text	200		
				var_ADLB_LBSTRESC = func_nihpo_synth_data_random_value(nihpo_cursor, 'C102580')			# Character Result/Finding in Std Format	text	200	C102580	Laboratory Test Standard Character Result
				var_ADLB_LBSTRESN = func_nihpo_random_value (var_parameter_lower_limit, var_parameter_upper_limit, var_parameter_fuzz_factor)	# Numeric Result/Finding in Standard Units	float	8		
				var_ADLB_LBSTRESU = func_nihpo_synth_data_random_value(nihpo_cursor, 'C71620')			# Standard Units	text	40	C71620	Unit
				var_ADLB_LBSTNRLO = var_parameter_lower_limit									#	Reference Range Lower Limit-Std Units	float	8		
				var_ADLB_LBSTNRHI = var_parameter_upper_limit									#	Reference Range Upper Limit-Std Units	float	8		
				var_ADLB_LBSTNRC = "-LBSTNRC-"									#	Reference Range for Char Rslt	text	200		
				var_ADLB_LBNRIND = func_nihpo_synth_data_random_value(nihpo_cursor, 'C78736')			# Reference Range Indicator	text	25	C78736	Reference Range Indicator
				var_ADLB_LBSTAT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66789')			# Completion Status	text	8	C66789	Not Done
				var_ADLB_LBREASND = "-LBREASND-"									#	Reason Test Not Done	text	200		
				var_ADLB_LBNAM = "-LBNAM-"									#	Vendor Name	text	200		
				var_ADLB_LBSPEC = func_nihpo_synth_data_random_value(nihpo_cursor, 'C78734')			# Specimen Type	text	40	C78734	Specimen Type
				var_ADLB_LBSPCCND = func_nihpo_synth_data_random_value(nihpo_cursor, 'C78733')									#	Specimen Condition	text	200	C78733	Specimen Condition
				var_ADLB_LBMETHOD = func_nihpo_synth_data_random_value(nihpo_cursor, 'C85492')									#	Method of Test or Examination	text	100	C85492	Method
				var_ADLB_LBBLFL = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')									#	Baseline Flag	text	2	C66742	No Yes Response
				var_ADLB_LBFAST = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66742')									#	Fasting Status	text	2	C66742	No Yes Respons
				var_ADLB_VISITNUM = var_counter_visit									#	Visit Number	integer	8		
				var_ADLB_VISIT = var_current_visit_name									#	Visit Name	text	200		
				var_ADLB_EPOCH = func_nihpo_synth_data_random_value(nihpo_cursor, 'C99079')									#	Epoch	text	40	C99079	Epoch
				var_ADLB_LBDTC = "-LBDTC-"									#	Date/Time of Specimen Collection	dateTime	25		ISO8601
				var_ADLB_LBENDTC = "-LBENDTC-"									#	End Date/Time of Specimen Collection	dateTime	25		ISO8601
				var_ADLB_LBDY = "-LBDY-"									#	Study Day of Specimen Collection	integer	8		
				var_ADLB_LBENDY = "-LBENDY-"									#	Study Day of End of Observation	integer	8		
				var_ADLB_LBTPT = "-LBTPT-"									#	Planned Time Point Name	text	40		
				var_ADLB_LBTPTNUM = "-LBTPTNUM-"									#	Planned Time Point Number	integer	8		
				var_ADLB_LBELTM = "-LBELTM-"									#	Planned Elapsed Time from Time Point Ref	dateTime	25		
				var_ADLB_LBTPTREF = "-LBTPTREF-"									#	Time Point Reference	text	40		
				var_ADLB_LBTSTDTL = "-LBTSTDTL-"									#	Lab Test or Examination Detailed Name	text	200		
				var_ADLB_PARAM = "-PARAM-"									#	Parameter	text	200		
				var_ADLB_PARAMCD = "-PARAMCD-"									#	Parameter Code	text	8		
				var_ADLB_PARCAT1 = random.choice(['CHEMISTRY'] * 33 + ['COAGULATION'] * 34 + ['HEMATOLOGY'] * 33) 			# Parameter Category 1 - Laboratory Class	text	100		CHEMISTRY | COAGULATION | HEMATOLOGY
				var_ADLB_PARCAT2 = random.choice(['LS'] * 33 + ['CV'] * 34 + ['SI'] * 33) 									# Parameter Category 2 - Reporting Classification	text	3		LS | CV | SI
				var_ADLB_AVAL = var_ADLB_LBSTRESN									#	Analysis Value	float	8		
				var_ADLB_AVALC = "-AVALC-"									#	Analysis Value (C)	text	200		
				var_ADLB_AVALU = "-AVALU-"									#	Analysis Value Unit	text	40		
				var_ADLB_AVALCAT1 = random.choice(['SINGLE'] * 33 + ['REPLICATED'] * 34 + ['LAST'] * 33) 				#  	Analysis Value Category 1 Marked Lab Ab	text	20		SINGLE | REPLICATED | LAST
				var_ADLB_BASE = "-BASE-"									#	Baseline Value	float	8		
				var_ADLB_BASETYPE = "LAST"									# Baseline Type	text	30		LAST
				var_ADLB_ABLFL = "-ABLFL-"									#	Baseline Record Flag	text	1	L00052	Yes Response
				var_ADLB_CHG = "CHG"									#	Change from Baseline	float	8		
				var_ADLB_PCHG = "PCHG"									#	Percent Change from Baseline	float	8		
				var_ADLB_ANRHI = "ANRHI"									#	Analysis Normal Range Upper Limit	float	8		
				var_ADLB_ANRLO = "-ANRLO-"									#	Analysis Normal Range Lower Limit	float	8		
				var_ADLB_ANRIND = random.choice(CT_REFERENCE_RANGE_INDICATOR)							# Analysis Reference Range Indicator	text	20		NORMAL | LOW | HIGH | LOW LOW | HIGH HIGH
				var_ADLB_BNRIND = random.choice(CT_REFERENCE_RANGE_INDICATOR) 						# Baseline Reference Range Indicator	text	20		NORMAL | LOW | HIGH | LOW LOW | HIGH HIGH
				var_ADLB_R2BASE = "-R2BASE-"									#	Ratio to Baseline	integer	8		
				var_ADLB_R2ANRLO = "-R2ANRLO-"									#	Ratio of Analysis Val compared to ANRLO	integer	8		
				var_ADLB_R2ANRHI = "-R2ANRHI-"									#	Ratio of Analysis Val compared to ANRHI	integer	8		
				var_ADLB_SHIFT1 = "-SHIFT1-"									#	Shift from Baseline to Analysis Value	text	20		
				var_ADLB_ATOXGR = "-ATOXGR-"									#	Analysis Toxicity Grade	text	2		
				var_ADLB_BTOXGR = "-BTOXGR-"									#	Baseline Toxicity Grade	text	2		
				var_ADLB_ADTM = "-ADTM-"									#	Analysis Datetime	integer	8		
				var_ADLB_ADT = "-ADT-"									#	Analysis Date	integer	8		
				var_ADLB_ADTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')									#	Analysis Date Imputation Flag	text	1	C81223	Date Imputation Flag
				var_ADLB_ATMF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81226')									#	Analysis Time Imputation Flag	text	1	C81226	Time Imputation Flag
				var_ADLB_ADY = "-ADY-"									#	Analysis Relative Day	integer	8		
				var_ADLB_ATPT = "-ATPT-"									#	Analysis Timepoint	text	40		
				var_ADLB_ATPTN = "-ATPTN-"									#	Analysis Timepoint (N)	integer	8
				var_ADLB_AVISIT = var_current_visit_name						#	Analysis Visit	text	200		
				var_ADLB_AVISITN = var_counter_visit							#	Analysis Visit (N)	integer	8		
				var_ADLB_ONTRTFL = "-ONTRTFL-"									#	On Treatment Record Flag	text	1	L00052	Yes Response
				var_ADLB_LAST01FL = "-LAST01FL-"									#	Last Observation in Window Flag 01	text	1	L00052	Yes Response
				var_ADLB_WORS01FL = "-WORS01FL-"									#	Worst Observation in Window Flag 01	text	1	L00052	Yes Response
				var_ADLB_WGRHIFL = "-WGRHIFL-"									#	Worst High Grade per Patient	text	1	L00052	Yes Response
				var_ADLB_WGRLOFL = "-WGRLOFL-"									#	Worst Low Grade per Patient	text	1	L00052	Yes Response
				var_ADLB_WGRHIVFL = "-WGRHIVFL-"									#	Worst High Grade per Patient per Visit	text	1	L00052	Yes Response
				var_ADLB_WGRLOVFL = "-WGRLOVFL-"									#	Worst Low Grade per Patient per Visit	text	1	L00052	Yes Response
				var_ADLB_ANL01FL = "-ANL01FL-"									#	Analysis Flag 01 Baseline Post-Baseline	text	1	L00052	Yes Response
				#
				var_Analysis_Sequence_Number += 1
				var_Specimen_ID += 1
				#
				# Write ADLB record to file:
				if (CT_DEBUG == 1):
					print(var_ADLB_STUDYID, var_ADLB_USUBJID, var_ADLB_SUBJID, var_ADLB_SITEID, var_ADLB_ASEQ, var_ADLB_COUNTRY, var_ADLB_ETHNIC, var_ADLB_AGE, var_ADLB_AGEU, var_ADLB_AAGE, var_ADLB_AAGEU, var_ADLB_SEX, var_ADLB_RACE, var_ADLB_ITTFL, var_ADLB_SAFFL, var_ADLB_PPROTFL, var_ADLB_TRT01P, var_ADLB_TRT01A, var_ADLB_TRTSDTM, var_ADLB_TRTSDT, var_ADLB_TRTEDTM, var_ADLB_TRTEDT, var_ADLB_DOMAIN, var_ADLB_LBSEQ, var_ADLB_LBGRPID, var_ADLB_LBREFID, var_ADLB_LBSPID, var_ADLB_LBTESTCD, var_ADLB_LBTEST, var_ADLB_LBCAT, var_ADLB_LBSCAT, var_ADLB_LBORRES, var_ADLB_LBORRESU, var_ADLB_LBORNRLO, var_ADLB_LBORNRHI, var_ADLB_LBSTRESC, var_ADLB_LBSTRESN, var_ADLB_LBSTRESU, var_ADLB_LBSTNRLO, var_ADLB_LBSTNRHI, var_ADLB_LBSTNRC, var_ADLB_LBNRIND, var_ADLB_LBSTAT, var_ADLB_LBREASND, var_ADLB_LBNAM, var_ADLB_LBSPEC, var_ADLB_LBSPCCND, var_ADLB_LBMETHOD, var_ADLB_LBBLFL, var_ADLB_LBFAST, var_ADLB_VISITNUM, var_ADLB_VISIT, var_ADLB_EPOCH, var_ADLB_LBDTC, var_ADLB_LBENDTC, var_ADLB_LBDY, var_ADLB_LBENDY, var_ADLB_LBTPT, var_ADLB_LBTPTNUM, var_ADLB_LBELTM, var_ADLB_LBTPTREF, var_ADLB_LBTSTDTL, var_ADLB_PARAM, var_ADLB_PARAMCD, var_ADLB_PARCAT1, var_ADLB_PARCAT2, var_ADLB_AVAL, var_ADLB_AVALC, var_ADLB_AVALU, var_ADLB_AVALCAT1, var_ADLB_BASE, var_ADLB_BASETYPE, var_ADLB_ABLFL, var_ADLB_CHG, var_ADLB_PCHG, var_ADLB_ANRHI, var_ADLB_ANRLO, var_ADLB_ANRIND, var_ADLB_BNRIND, var_ADLB_R2BASE, var_ADLB_R2ANRLO, var_ADLB_R2ANRHI, var_ADLB_SHIFT1, var_ADLB_ATOXGR, var_ADLB_BTOXGR, var_ADLB_ADTM, var_ADLB_ADT, var_ADLB_ADTF, var_ADLB_ATMF, var_ADLB_ADY, var_ADLB_ATPT, var_ADLB_ATPTN, var_ADLB_AVISIT, var_ADLB_AVISITN, var_ADLB_ONTRTFL, var_ADLB_LAST01FL, var_ADLB_WORS01FL, var_ADLB_WGRHIFL, var_ADLB_WGRLOFL, var_ADLB_WGRHIVFL, var_ADLB_WGRLOVFL, var_ADLB_ANL01FL)
					#
				var_output_file_ADLB.writerow([var_ADLB_STUDYID, var_ADLB_USUBJID, var_ADLB_SUBJID, var_ADLB_SITEID, var_ADLB_ASEQ, var_ADLB_COUNTRY, var_ADLB_ETHNIC, var_ADLB_AGE, var_ADLB_AGEU, var_ADLB_AAGE, var_ADLB_AAGEU, var_ADLB_SEX, var_ADLB_RACE, var_ADLB_ITTFL, var_ADLB_SAFFL, var_ADLB_PPROTFL, var_ADLB_TRT01P, var_ADLB_TRT01A, var_ADLB_TRTSDTM, var_ADLB_TRTSDT, var_ADLB_TRTEDTM, var_ADLB_TRTEDT, var_ADLB_DOMAIN, var_ADLB_LBSEQ, var_ADLB_LBGRPID, var_ADLB_LBREFID, var_ADLB_LBSPID, var_ADLB_LBTESTCD, var_ADLB_LBTEST, var_ADLB_LBCAT, var_ADLB_LBSCAT, var_ADLB_LBORRES, var_ADLB_LBORRESU, var_ADLB_LBORNRLO, var_ADLB_LBORNRHI, var_ADLB_LBSTRESC, var_ADLB_LBSTRESN, var_ADLB_LBSTRESU, var_ADLB_LBSTNRLO, var_ADLB_LBSTNRHI, var_ADLB_LBSTNRC, var_ADLB_LBNRIND, var_ADLB_LBSTAT, var_ADLB_LBREASND, var_ADLB_LBNAM, var_ADLB_LBSPEC, var_ADLB_LBSPCCND, var_ADLB_LBMETHOD, var_ADLB_LBBLFL, var_ADLB_LBFAST, var_ADLB_VISITNUM, var_ADLB_VISIT, var_ADLB_EPOCH, var_ADLB_LBDTC, var_ADLB_LBENDTC, var_ADLB_LBDY, var_ADLB_LBENDY, var_ADLB_LBTPT, var_ADLB_LBTPTNUM, var_ADLB_LBELTM, var_ADLB_LBTPTREF, var_ADLB_LBTSTDTL, var_ADLB_PARAM, var_ADLB_PARAMCD, var_ADLB_PARCAT1, var_ADLB_PARCAT2, var_ADLB_AVAL, var_ADLB_AVALC, var_ADLB_AVALU, var_ADLB_AVALCAT1, var_ADLB_BASE, var_ADLB_BASETYPE, var_ADLB_ABLFL, var_ADLB_CHG, var_ADLB_PCHG, var_ADLB_ANRHI, var_ADLB_ANRLO, var_ADLB_ANRIND, var_ADLB_BNRIND, var_ADLB_R2BASE, var_ADLB_R2ANRLO, var_ADLB_R2ANRHI, var_ADLB_SHIFT1, var_ADLB_ATOXGR, var_ADLB_BTOXGR, var_ADLB_ADTM, var_ADLB_ADT, var_ADLB_ADTF, var_ADLB_ATMF, var_ADLB_ADY, var_ADLB_ATPT, var_ADLB_ATPTN, var_ADLB_AVISIT, var_ADLB_AVISITN, var_ADLB_ONTRTFL, var_ADLB_LAST01FL, var_ADLB_WORS01FL, var_ADLB_WGRHIFL, var_ADLB_WGRLOFL, var_ADLB_WGRHIVFL, var_ADLB_WGRLOVFL, var_ADLB_ANL01FL])
				#
				#


				# = ADHY file =
				# One record per subject per parameter per analysis visit per analysis date.
				# _x005F_x000D_ SDTM variables are populated on new records coming from other single records.  Otherwise, SDTM variables are left blank.
				var_ADHY_STUDYID = var_ADSL_STUDYID							# Study Identifier	text	8		
				var_ADHY_USUBJID = var_ADSL_USUBJID							# Unique Subject Identifier	text	50		
				var_ADHY_SUBJID = var_ADSL_SUBJID							# Subject Identifier for the Study	text	50		
				var_ADHY_SITEID = var_ADSL_SITEID							# Study Site Identifier	text	20		
				var_ADHY_ASEQ = "Pending"									# Analysis Sequence Number	integer	8		
				var_ADHY_COUNTRY = var_ADSL_COUNTRY							# Country	text	3		ISO3166
				var_ADHY_ETHNIC = var_ADSL_ETHNIC							# Ethnicity	text	200		
				var_ADHY_AGE = var_ADSL_AAGE								# Age	integer	8		
				var_ADHY_AGEU = var_ADSL_AAGEU								# Age Units	text	6	C66781	Age Unit
				var_ADHY_AAGE = "-AAGE-"										# Analysis Age	integer	8		
				var_ADHY_AAGEU = "-AAGEU-"									# Analysis Age Unit	text	6	C66781	Age Unit
				var_ADHY_SEX = var_ADSL_SEX									# Sex	text	2	C66731	Sex
				var_ADHY_RACE = var_ADSL_RACE								# Race	text	200	C74457	Race
				var_ADHY_ITTFL = var_ADLB_ITTFL									#	Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
				var_ADHY_SAFFL = var_ADSL_SAFFL									#	Safety Population Flag	text	1	C66742	No Yes Response
				var_ADHY_PPROTFL = "-PPROTFL-"									#	Per-Protocol Population Flag	text	1	C66742	No Yes Response
				var_ADHY_TRT01P = "-TRT01P-"									#	Planned Treatment for Period 01	text	200		
				var_ADHY_TRT01A = "-TRT01A-"									#	Actual Treatment for Period 01	text	200		
				var_ADHY_TRTSDTM = "-TRTSDTM-"									#	Datetime of First Exposure to Treatment	integer	8		
				var_ADHY_TRTSDT = "-TRTSDT-"									#	Date of First Exposure to Treatment	integer	8		
				var_ADHY_TRTEDTM = "-TRTEDTM-"									#	Datetime of Last Exposure to Treatment	integer	8		
				var_ADHY_TRTEDT = "-TRTEDT-"									#	Date of Last Exposure to Treatment	integer	8		
				var_ADHY_PARAM = "-PARAM-"									#	Parameter	text	200		
				var_ADHY_PARAMCD = "-PARAMCD-"									#	Parameter Code	text	8		
				var_ADHY_AVAL = var_ADLB_LBSTRESN									#	Analysis Value	float	8		
				var_ADHY_AVALC = "-AVALC-"									#	Analysis Value (C)	text	200		
				var_ADHY_AVALU = "-AVALU-"									#	Analysis Value Unit	text	40		
				var_ADHY_BASE = "-BASE-"									#	Baseline Value	float	8		
				var_ADHY_BASEC = "-BASEC-"									#	Baseline Value (C)	text	200		
				var_ADHY_ABLFL = "-ABLFL-"									#	Baseline Record Flag	text	1	L00052	Yes Response
				var_ADHY_ANRLO = "-ANRLO-"									#	Analysis Normal Range Lower Limit	float	8		
				var_ADHY_ANRHI = "-ANRHI-"									#	Analysis Normal Range Upper Limit	float	8		
				var_ADHY_ADTM = "-DTM-"									#	Analysis Datetime	integer	8		
				var_ADHY_ADT = "-ADT-"									#	Analysis Date	integer	8		
				var_ADHY_ADY = "ADY"									#	Analysis Relative Day	integer	8		
				var_ADHY_ADTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')									#	Analysis Date Imputation Flag	text	1	C81223	Date Imputation Flag
				var_ADHY_ATMF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81226')									#	Analysis Time Imputation Flag	text	1	C81226	Time Imputation Flag
				var_ADHY_AVISIT = var_current_visit_name									#	Analysis Visit	text	200		
				var_ADHY_AVISITN = var_counter_visit									#	Analysis Visit (N)	integer	8		
				var_ADHY_ONTRTFL = "-ONTRTFL-"									#	On Treatment Record Flag	text	1	L00052	Yes Response
				var_ADHY_CRIT1 = "-CRIT1-"									#	Analysis Criterion 1	text	40		
				var_ADHY_CRIT1FL = "-CRIT1FL-"									#	Criterion 1 Evaluation Result Flag	text	1	L00052	Yes Response
				var_ADHY_CRIT1FN = "-CRIT1FN-"									#	Criterion 1 Evaluation Result Flag (N)	integer	8		
				var_ADHY_CRIT2 = "-CRIT2-"									#	Analysis Criterion 2	text	40		
				var_ADHY_CRIT2FL = "-CRIT2FL-"									#	Criterion 2 Evaluation Result Flag	text	1	L00052	Yes Response
				var_ADHY_CRIT2FN = "-CRIT2FN-"									#	Criterion 2 Evaluation Result Flag (N)	integer	8		
				var_ADHY_MCRIT1 = "-MCRIT1-"									#	Analysis Multi-Response Criterion 1	text	40		
				var_ADHY_MCRIT1ML = "-MCRIT1ML-"									#	Multi-Response Criterion 1 Evaluation	text	20		
				var_ADHY_SRCDOM = "-SRCDOM-"									#	Source Data	text	10		
				var_ADHY_SRCVAR = "-SRCVAR-"									#	Source Variable	text	50		
				var_ADHY_SRCSEQ = "-SRCSEQ-"									#	Source Sequence Number	integer	8		
				var_ADHY_ANL01FL = "-ANL01FL-"									#	Analysis Flag 01	text	1		
				#
				# Write ADHY record to file:
				if (CT_DEBUG == 1):
					print(var_ADHY_STUDYID, var_ADHY_USUBJID, var_ADHY_SUBJID, var_ADHY_SITEID, var_ADHY_ASEQ, var_ADHY_COUNTRY, var_ADHY_ETHNIC, var_ADHY_AGE, var_ADHY_AGEU, var_ADHY_AAGE, var_ADHY_AAGEU, var_ADHY_SEX, var_ADHY_RACE, var_ADHY_ITTFL, var_ADHY_SAFFL, var_ADHY_PPROTFL, var_ADHY_TRT01P, var_ADHY_TRT01A, var_ADHY_TRTSDTM, var_ADHY_TRTSDT, var_ADHY_TRTEDTM, var_ADHY_TRTEDT, var_ADHY_PARAM, var_ADHY_PARAMCD, var_ADHY_AVAL, var_ADHY_AVALC, var_ADHY_AVALU, var_ADHY_BASE, var_ADHY_BASEC, var_ADHY_ABLFL, var_ADHY_ANRLO, var_ADHY_ANRHI, var_ADHY_ADTM, var_ADHY_ADT, var_ADHY_ADY, var_ADHY_ADTF, var_ADHY_ATMF, var_ADHY_AVISIT, var_ADHY_AVISITN, var_ADHY_ONTRTFL, var_ADHY_CRIT1, var_ADHY_CRIT1FL, var_ADHY_CRIT1FN, var_ADHY_CRIT2, var_ADHY_CRIT2FL, var_ADHY_CRIT2FN, var_ADHY_MCRIT1, var_ADHY_MCRIT1ML, var_ADHY_SRCDOM, var_ADHY_SRCVAR, var_ADHY_SRCSEQ, var_ADHY_ANL01FL)
					#
				var_output_file_ADHY.writerow([var_ADHY_STUDYID, var_ADHY_USUBJID, var_ADHY_SUBJID, var_ADHY_SITEID, var_ADHY_ASEQ, var_ADHY_COUNTRY, var_ADHY_ETHNIC, var_ADHY_AGE, var_ADHY_AGEU, var_ADHY_AAGE, var_ADHY_AAGEU, var_ADHY_SEX, var_ADHY_RACE, var_ADHY_ITTFL, var_ADHY_SAFFL, var_ADHY_PPROTFL, var_ADHY_TRT01P, var_ADHY_TRT01A, var_ADHY_TRTSDTM, var_ADHY_TRTSDT, var_ADHY_TRTEDTM, var_ADHY_TRTEDT, var_ADHY_PARAM, var_ADHY_PARAMCD, var_ADHY_AVAL, var_ADHY_AVALC, var_ADHY_AVALU, var_ADHY_BASE, var_ADHY_BASEC, var_ADHY_ABLFL, var_ADHY_ANRLO, var_ADHY_ANRHI, var_ADHY_ADTM, var_ADHY_ADT, var_ADHY_ADY, var_ADHY_ADTF, var_ADHY_ATMF, var_ADHY_AVISIT, var_ADHY_AVISITN, var_ADHY_ONTRTFL, var_ADHY_CRIT1, var_ADHY_CRIT1FL, var_ADHY_CRIT1FN, var_ADHY_CRIT2, var_ADHY_CRIT2FL, var_ADHY_CRIT2FN, var_ADHY_MCRIT1, var_ADHY_MCRIT1ML, var_ADHY_SRCDOM, var_ADHY_SRCVAR, var_ADHY_SRCSEQ, var_ADHY_ANL01FL])


				# = ADSAFTTE file =
				# One record per subject per parameter per analysis visit per analysis date.
				# _x005F_x000D_ SDTM variables are populated on new records coming from other single records.  Otherwise, SDTM variables are left blank.
				var_ADSAFTTE_STUDYID = var_ADSL_STUDYID				# Study Identifier	text	8		
				var_ADSAFTTE_USUBJID = var_ADSL_USUBJID				# Unique Subject Identifier	text	50		
				var_ADSAFTTE_SUBJID = var_ADSL_SUBJID				# Subject Identifier for the Study	text	50		
				var_ADSAFTTE_SITEID = var_ADSL_SITEID				# Study Site Identifier	text	20		
				var_ADSAFTTE_ASEQ = "-ASEQ-"						# Analysis Sequence Number	integer	8		
				var_ADSAFTTE_REGION1 = "-REGION1-"					# Geographic Region 1	text	200		
				var_ADSAFTTE_COUNTRY = var_ADSL_COUNTRY				# Country	text	3		ISO3166
				var_ADSAFTTE_ETHNIC = var_ADSL_ETHNIC				# Ethnicity	text	200		
				var_ADSAFTTE_AGE = var_ADSL_AGE						# Age	integer	8		
				var_ADSAFTTE_AGEU = var_ADSL_AGEU					# Age Units	text	6	C66781	Age Unit
				var_ADSAFTTE_AAGE = var_ADSL_AAGE					# Analysis Age	integer	8		
				var_ADSAFTTE_AAGEU = var_ADSL_AAGEU					# Analysis Age Unit	text	6	C66781	Age Unit
				var_ADSAFTTE_AGEGR1 = "-AGEGR1-"					# Pooled Age Group 1	text	10		
				var_ADSAFTTE_AGEGR2 = "-AGEGR2-"					# Pooled Age Group 2	text	10		
				var_ADSAFTTE_AGEGR3 = "-AGEGR3-"					# Pooled Age Group 3	text	10		
				var_ADSAFTTE_STRATwNM = "-STRATwNM-"				# Description of Stratum w	text	200		
				var_ADSAFTTE_STRATw = "-STRATw-"					# Randomized Value of Stratum w	text	200		
				var_ADSAFTTE_STRATwV = "-STRATwV-"					# Verified Value of Stratum w	text	200		
				var_ADSAFTTE_SEX = var_ADSL_SEX						# Sex	text	2	C66731	Sex
				var_ADSAFTTE_RACE = var_ADSL_RACE					# Race	text	200	C74457	Race
				var_ADSAFTTE_ITTFL = var_ADLB_ITTFL						# Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
				var_ADSAFTTE_SAFFL = var_ADSL_SAFFL						# Safety Population Flag	text	1	C66742	No Yes Response
				var_ADSAFTTE_PPROTFL = "-PPROTFL-"					# Per-Protocol Population Flag	text	1	C66742	No Yes Response
				var_ADSAFTTE_TRT01P = "-TRT01P-"					# Planned Treatment for Period 01	text	200		
				var_ADSAFTTE_TRTxxP	= "-TRTxxP-"					# Planned Treatment for Period xx	text	200		
				var_ADSAFTTE_TRT01A = "-TRT01A-"					# Actual Treatment for Period 01	text	200		
				var_ADSAFTTE_TRTxxA = "-TRTxxA-"					# Actual Treatment for Period xx	text	200		
				var_ADSAFTTE_TRTSEQP = "-TRTSEQP-"					# Planned Sequence of Treatments	text	200		
				var_ADSAFTTE_TRTSEQA = "-TRTSEQA-"					# Actual Sequence of Treatments	text	200		
				var_ADSAFTTE_TRTSDTM = "-TRTSDTM-"					# Datetime of First Exposure to Treatment	integer	8		
				var_ADSAFTTE_TRTSDT = "-TRTSDT-"					# Date of First Exposure to Treatment	integer	8		
				var_ADSAFTTE_TRTEDTM = "-TRTEDTM-"					# Datetime of Last Exposure to Treatment	integer	8		
				var_ADSAFTTE_TRTEDT = "-TRTEDT-"					# Date of Last Exposure to Treatment	integer	8		
				var_ADSAFTTE_DCUTDT = "-DCUTDT-"					# Date of Data Cut	integer	8		
				var_ADSAFTTE_PARAM = "-PARAM-"						# Parameter	text	200		
				var_ADSAFTTE_PARAMCD = "-PARAMCD-"					# Parameter Code	text	8		
				var_ADSAFTTE_PARCAT1 = "-PARCAT1-"					# Parameter Category 1	text	200		Time to Event | Total Occurrences
				var_ADSAFTTE_AVAL = var_ADLB_LBSTRESN						# Analysis Value	float	8		
				var_ADSAFTTE_AVALU = "-AVALU-"						# Analysis Value Unit	text	40	C71620	Unit
				var_ADSAFTTE_STARTDT = "-STARTDT-"					# Time-to-Event Origin Date for Subject	integer	8		
				var_ADSAFTTE_STARTDTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')				# Origin Date Imputation Flag	text	1	C81223	Date Imputation Flag
				var_ADSAFTTE_ADT = "-ADT-"							# Analysis Date	integer	8		
				var_ADSAFTTE_ADY = "-ADY-"							# Analysis Relative Day	integer	8		
				var_ADSAFTTE_ADTF = func_nihpo_synth_data_random_value(nihpo_cursor, 'C81223')						# Analysis Date Imputation Flag	text	1	C81223	Date Imputation Flag
				var_ADSAFTTE_CNSR = "-CNSR-"						# Censor	integer	8		
				var_ADSAFTTE_EVNTDESC = "-EVNTDESC-"				# Event or Censoring Description	text	200		
				var_ADSAFTTE_CNSDTDSC = "-CNSDTDSC-"				# Censor Date Description	text	200		
				var_ADSAFTTE_SRCDOM = "-SRCDOM-"					# Source Data	text	10		
				var_ADSAFTTE_SRCVAR = "-SRCVAR-"					# Source Variable	text	50		
				var_ADSAFTTE_SRCSEQ = "-SRCSEQ-"					# Source Sequence Number	integer	8		
				var_ADSAFTTE_ANL01FL = "-ANL01FL-"					# Analysis Flag 01	text	1	L00052	Yes Response
				#
				# Write ADSAFTTE record to file:
				if (CT_DEBUG == 1):
					print(var_ADSAFTTE_STUDYID, var_ADSAFTTE_USUBJID, var_ADSAFTTE_SUBJID, var_ADSAFTTE_SITEID, var_ADSAFTTE_ASEQ, var_ADSAFTTE_REGION1, var_ADSAFTTE_COUNTRY, var_ADSAFTTE_ETHNIC, var_ADSAFTTE_AGE, var_ADSAFTTE_AGEU, var_ADSAFTTE_AAGE, var_ADSAFTTE_AAGEU, var_ADSAFTTE_AGEGR1, var_ADSAFTTE_AGEGR2, var_ADSAFTTE_AGEGR3, var_ADSAFTTE_STRATwNM, var_ADSAFTTE_STRATw, var_ADSAFTTE_STRATwV, var_ADSAFTTE_SEX, var_ADSAFTTE_RACE, var_ADSAFTTE_ITTFL, var_ADSAFTTE_SAFFL, var_ADSAFTTE_PPROTFL, var_ADSAFTTE_TRT01P, var_ADSAFTTE_TRTxxP, var_ADSAFTTE_TRT01A, var_ADSAFTTE_TRTxxA, var_ADSAFTTE_TRTSEQP, var_ADSAFTTE_TRTSEQA, var_ADSAFTTE_TRTSDTM, var_ADSAFTTE_TRTSDT, var_ADSAFTTE_TRTEDTM, var_ADSAFTTE_TRTEDT, var_ADSAFTTE_DCUTDT, var_ADSAFTTE_PARAM, var_ADSAFTTE_PARAMCD, var_ADSAFTTE_PARCAT1, var_ADSAFTTE_AVAL, var_ADSAFTTE_AVALU, var_ADSAFTTE_STARTDT, var_ADSAFTTE_STARTDTF, var_ADSAFTTE_ADT, var_ADSAFTTE_ADY, var_ADSAFTTE_ADTF, var_ADSAFTTE_CNSR, var_ADSAFTTE_EVNTDESC, var_ADSAFTTE_CNSDTDSC, var_ADSAFTTE_SRCDOM, var_ADSAFTTE_SRCVAR, var_ADSAFTTE_SRCSEQ, var_ADSAFTTE_ANL01FL)
					#
				var_output_file_ADSAFTTE.writerow([var_ADSAFTTE_STUDYID, var_ADSAFTTE_USUBJID, var_ADSAFTTE_SUBJID, var_ADSAFTTE_SITEID, var_ADSAFTTE_ASEQ, var_ADSAFTTE_REGION1, var_ADSAFTTE_COUNTRY, var_ADSAFTTE_ETHNIC, var_ADSAFTTE_AGE, var_ADSAFTTE_AGEU, var_ADSAFTTE_AAGE, var_ADSAFTTE_AAGEU, var_ADSAFTTE_AGEGR1, var_ADSAFTTE_AGEGR2, var_ADSAFTTE_AGEGR3, var_ADSAFTTE_STRATwNM, var_ADSAFTTE_STRATw, var_ADSAFTTE_STRATwV, var_ADSAFTTE_SEX, var_ADSAFTTE_RACE, var_ADSAFTTE_ITTFL, var_ADSAFTTE_SAFFL, var_ADSAFTTE_PPROTFL, var_ADSAFTTE_TRT01P, var_ADSAFTTE_TRTxxP, var_ADSAFTTE_TRT01A, var_ADSAFTTE_TRTxxA, var_ADSAFTTE_TRTSEQP, var_ADSAFTTE_TRTSEQA, var_ADSAFTTE_TRTSDTM, var_ADSAFTTE_TRTSDT, var_ADSAFTTE_TRTEDTM, var_ADSAFTTE_TRTEDT, var_ADSAFTTE_DCUTDT, var_ADSAFTTE_PARAM, var_ADSAFTTE_PARAMCD, var_ADSAFTTE_PARCAT1, var_ADSAFTTE_AVAL, var_ADSAFTTE_AVALU, var_ADSAFTTE_STARTDT, var_ADSAFTTE_STARTDTF, var_ADSAFTTE_ADT, var_ADSAFTTE_ADY, var_ADSAFTTE_ADTF, var_ADSAFTTE_CNSR, var_ADSAFTTE_EVNTDESC, var_ADSAFTTE_CNSDTDSC, var_ADSAFTTE_SRCDOM, var_ADSAFTTE_SRCVAR, var_ADSAFTTE_SRCSEQ, var_ADSAFTTE_ANL01FL])


				# = = = = = End of Parameter = = =
				var_counter_parameter += 1
				#
			# = = = End of Analysis = = =
			var_counter_analysis += 1
			#
		# = = = End of Visit = = =
		var_counter_visit += 1
		#
	# = = = End of repeating records = = = =
	#
	# This is the LAST subject-specific file to be written.
	# Write ADSL record to file:
	if (CT_DEBUG == 1):
		print (var_ADSL_STUDYID, var_ADSL_USUBJID, var_ADSL_SUBJID, var_ADSL_SITEID, var_ADSL_AGE, var_ADSL_AGEU, var_ADSL_SEX, var_ADSL_RACE, var_ADSL_ETHNIC, var_ADSL_COUNTRY, var_ADSL_DMDTC, var_ADSL_DMDY, var_ADSL_BRTHDTC, var_ADSL_DTHDTC, var_ADSL_DTHFL, var_ADSL_RFSTDTC, var_ADSL_RFENDTC, var_ADSL_RFXSTDTC, var_ADSL_RFXENDTC, var_ADSL_RFICDTC, var_ADSL_RFPENDTC, var_ADSL_INVID, var_ADSL_INVNAM, var_ADSL_ARM, var_ADSL_ARMCD, var_ADSL_ACTARM, var_ADSL_ACTARMCD, var_ADSL_BRTHDTF, var_ADSL_AAGE, var_ADSL_AAGEU, var_ADSL_AGEGR1, var_ADSL_ITTFL, var_ADSL_SAFFL, var_ADSL_PPROTFL, var_ADSL_FASFL, var_ADSL_TRT01P, var_ADSL_TRT01A, var_ADSL_RFICDT, var_ADSL_RANDDT, var_ADSL_BRTHDT, var_ADSL_TRTSDTM, var_ADSL_TRTSDT, var_ADSL_TRTEDTM, var_ADSL_TRTEDT, var_ADSL_TRTDURD, var_ADSL_EOSSTT, var_ADSL_EOSDT, var_ADSL_EOTSTT, var_ADSL_EOSDY, var_ADSL_EOSRDY, var_ADSL_DCSREAS, var_ADSL_DCSREASP, var_ADSL_DTHDT, var_ADSL_DTHCAUS, var_ADSL_ADTHAUT, var_ADSL_DTHADY, var_ADSL_AEWITHFL, var_ADSL_LSTALVDT)
		#
	var_output_file_ADSL.writerow([var_ADSL_STUDYID, var_ADSL_USUBJID, var_ADSL_SUBJID, var_ADSL_SITEID, var_ADSL_AGE, var_ADSL_AGEU, var_ADSL_SEX, var_ADSL_RACE, var_ADSL_ETHNIC, var_ADSL_COUNTRY, var_ADSL_DMDTC, var_ADSL_DMDY, var_ADSL_BRTHDTC, var_ADSL_DTHDTC, var_ADSL_DTHFL, var_ADSL_RFSTDTC, var_ADSL_RFENDTC, var_ADSL_RFXSTDTC, var_ADSL_RFXENDTC, var_ADSL_RFICDTC, var_ADSL_RFPENDTC, var_ADSL_INVID, var_ADSL_INVNAM, var_ADSL_ARM, var_ADSL_ARMCD, var_ADSL_ACTARM, var_ADSL_ACTARMCD, var_ADSL_BRTHDTF, var_ADSL_AAGE, var_ADSL_AAGEU, var_ADSL_AGEGR1, var_ADSL_ITTFL, var_ADSL_SAFFL, var_ADSL_PPROTFL, var_ADSL_FASFL, var_ADSL_TRT01P, var_ADSL_TRT01A, var_ADSL_RFICDT, var_ADSL_RANDDT, var_ADSL_BRTHDT, var_ADSL_TRTSDTM, var_ADSL_TRTSDT, var_ADSL_TRTEDTM, var_ADSL_TRTEDT, var_ADSL_TRTDURD, var_ADSL_EOSSTT, var_ADSL_EOSDT, var_ADSL_EOTSTT, var_ADSL_EOSDY, var_ADSL_EOSRDY, var_ADSL_DCSREAS, var_ADSL_DCSREASP, var_ADSL_DTHDT, var_ADSL_DTHCAUS, var_ADSL_ADTHAUT, var_ADSL_DTHADY, var_ADSL_AEWITHFL, var_ADSL_LSTALVDT])

	#
	var_subject_counter += 1


# = = Clean up files = =
nihpo_conn.close()
#
print ("This is the end, my friend.")


"""
Controlled Terms

codelist_code | codelist_name | # Records
=========================================
C65047 | "Laboratory Test Code" | 4,142
C66727 | "Completion/Reason for Non-Completion" | 33
C66728 | "Relation to Reference Period" | 07
C66731 | "Sex" | 08
C66734 | "SDTM Domain Abbreviation" | 150
C66742 | "No Yes Response" | 12
C66767 | "Action Taken with Study Treatment" | 08
C66768 | "Outcome of Event" | 06
C66769 | "Severity/Intensity Scale for Adverse Events" | 03
C66781 | "Age Unit" | 10
C66789 | "Not Done" | 02
C67154 | "Laboratory Test Name" | 4,142
C71620 | "Unit" | 1,500
C74456 | "Anatomical Location" | 2,226
C74457 | "Race" | 07
C78733 | "Specimen Condition" | 21
C78734 | "Specimen Type" | 108
C78736 | "Reference Range Indicator" | 04
C81223 | "Date Imputation Flag" | 03
C81226 | "Time Imputation Flag" | 03
C85492 | "Method" | 388
C99079 | "Epoch" | 12
C102580 | "Laboratory Test Standard Character Result" | 6
C124296 | "Subject Trial Status" | 03
L00004 | 
L00052
L00059
L00060


= ADSL =
C66727
C66731
C66742
C66781
C74457
C81223
C124296
L00059
L00060


= ADAE =
C66728
C66731
C66734
C66742
C66767
C66768
C66769
C66781
C71620
C74456
C74457
C81223
C81226
C99079
L00004
L00052


= ADLB =
C65047
C66731
C66734
C66742
C66781
C66789
C67154
C71620
C74457
C78733
C78734
C78736
C81223
C81226
C85492
C99079
C102580
L00052


= ADHY =
C66731
C66742
C66781
C74457
C81223
C81226
L00052


= ADSAFTTE =
C66731
C66742
C66781
C71620
C74457
C81223
L00052
"""