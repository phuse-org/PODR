#!/usr/bin/python3
# Author: Jose.Lacal@NIHPO.com
# Filename: PHUSE_Generate_SDTM.py
# Purpose: This Python script generates realistic yet fake CDISC SDTM data using guidance from PHUSE's TDF working group.
# Version: Thu 24 September 2020.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
# 
"""
Requirements:
* Please download the "Synthetic_Health_Data_NIHPO.sqlite3" file to the same directory as this script.

Open items [06 October 2020]:
* Modularize code below.
* Add test suite.


Define trial:
* Arms
* Elements
* Visits


Define [Investigator => Site => Country ] Matrix.

Functions:
	random_Individual
	random_Date
	random_Assignment
	random_Visit
	random_Measurement
	random_Adverse_Event


Domains:
	AE
	CM
	DM
	DS
	EX
	LB
	MH
	TA
	TS
	TV
	VS

"""
#
"""

python3 /Users/server/Github/PODR/sample_code/PHUSE_Generate_SDTM.py ID345 /Users/server/___Temp_TDF 100 2018-01-01 2020-10-06


Processing notes:

a.) Take Domain definition off SQLite3 file, listing fields per Domain.
b.) Take Rules definition from SQLite3 file.
c.) Generate a line per Domain, with all required Fields, as per Rules.
d.) Write output to CSV file.
e.) Write output to SAS file.


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
try:
	import pandas as pd
except ImportError:
	print("Install Pandas: pip3 install pandas")
	print("https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html")
	sys.exit(1)
#
#
CT_DEBUG = [1]		# Set to 0 (digit zero) to avoid debug messages. Options: 1 for database results; 
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
#		Each Analysis has a number of Parameters per Analysis.
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
	print("\n\nUsage: python3 PHUSE_Generate_SDTM.py [StudyID] [TargetDirectory] [NumberSubjects] [DateStartRecruitment] [CurrentDate]\nUse YYYY-MM-DD for dates.\n")
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
assert (10 <= CT_NUMBER_SUBJECTS <= 999),"Please enter a value between 10 and 999"
#
# Validate date:
CT_DATE_START_RECRUITMENT = datetime.datetime.strptime(sys.argv[4], '%Y-%m-%d')
assert (CT_DATE_START_RECRUITMENT, "Please enter a valid date using the format YYYY-MM-DD")
#
CT_DATE_CURRENT_DATE = datetime.datetime.strptime(sys.argv[5], '%Y-%m-%d')
assert (CT_DATE_CURRENT_DATE, "Please enter a valid date using the format YYYY-MM-DD")
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

# = = Database connections = =
# Open SQLite3 file:
try:
	conn = sqlite3.connect('file:Synthetic_Health_Data_NIHPO.sqlite3?mode=ro', uri=True)
	cursor = conn.cursor()
except sqlite3.Error as e:
	print ("The SQLite3 file 'Synthetic_Health_Data_NIHPO.sqlite3' should be in your local path.")
	print ("Error {}:".format(e.args[0]))
	sys.exit(1)
#
"""
CREATE TABLE cdisc_sdtm_domain_rules (
	domain_code text,
	per_trial text,
	per_subject text,
	per_arm text,
	per_visit text,
	per_visit_measurement text,
	per_adverse_event text,
	per_concomitant_prior text);


CREATE TABLE cdisc_sdtm_domain_definitions (
	domain_code text,
	variable_name text,
	variable_label text,
	type text,
	controlled_terms text,
	role text,
	cdisc_notes text,
	core text);
"""
#
sql_select_rules = conn.execute("SELECT * FROM cdisc_sdtm_domain_rules ORDER BY domain_code ASC;")
for one_rule in sql_select_rules:
	if (1 in CT_DEBUG):  print (one_rule)
	#
	one_rule_domain_code = one_rule[0]
	one_rule_per_trial = one_rule[1]
	one_rule_per_subject = one_rule[2]
	one_rule_per_arm = one_rule[3]
	one_rule_per_visit = one_rule[4]
	one_rule_per_visit_measurement = one_rule[5]
	one_rule_per_adverse_event = one_rule[6]
	one_rule_per_concomitant_prior = one_rule[7]
	#
	# = = Open output files for writing = =
	var_output_file_name = "%s%s.csv" % (os.path.join(CT_TARGET_DIRECTORY, "PHUSE_TDF_"), one_rule_domain_code)
	output_file = csv.writer(open(var_output_file_name, "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
	#
	# Retrieve field definition for this domain:
	sql_select_domain_definition = conn.execute("SELECT * FROM cdisc_sdtm_domain_definitions WHERE domain_code = '%s' ORDER BY domain_code ASC;" % (one_rule_domain_code))
	for one_definition in sql_select_domain_definition:
		if (1 in CT_DEBUG):  print (one_definition)
		#
		one_definition_domain_code = one_definition[0]
		one_definition_variable_name = one_definition[1]
		one_definition_variable_label = one_definition[2]
		one_definition_type = one_definition[3]
		one_definition_controlled_terms = one_definition[4]
		one_definition_role = one_definition[5]
		one_definition_cdisc_notes = one_definition[6]
		one_definition_core = one_definition[7]
		#
		# Process rules:
		if (one_rule_per_trial == 1):
			# One entry per trial.
			output_file.writerow
			print (one_definition_domain_code)

		if (one_rule_per_subject == 1):
			# One entry per subject
			print (one_definition_domain_code)

		if (one_rule_per_arm == 1):
			# One entry per arm
			print (one_definition_domain_code)

		if (one_rule_per_visit == 1):
			# One entry per visit
			print (one_definition_domain_code)

		if (one_rule_per_visit_measurement == 1):
			# One measurement per visit
			print (one_definition_domain_code)

		if (one_rule_per_adverse_event == 1):
			# One entry per Adverse Event
			print (one_definition_domain_code)

		if (one_rule_per_concomitant_prior == 1):
			# One entry per concomitant prior
			print (one_definition_domain_code)



#
# = = Clean up. = =
conn.close()
print("\n\nThis is the end, Beautiful friend. This is the end. My only friend, the end")



# = = = SAS export = =
"""
# Source: https://github.com/selik/xport
python -m pip install --upgrade xport


import pandas as pd
import xport
import xport.v56

df = pd.DataFrame({
    'alpha': [10, 20, 30],
    'beta': ['x', 'y', 'z'],
})

...  # Analysis work ...

ds = xport.Dataset(df, name='DATA', label='Wonderful data')

# SAS variable names are limited to 8 characters.  As with Pandas
# dataframes, you must change the name on the dataset rather than
# the column directly.
ds = ds.rename(columns={k: k.upper()[:8] for k in ds})

# Other SAS metadata can be set on the columns themselves.
for k, v in ds.items():
    v.label = k.title()
    if v.dtype == 'object':
        v.format = '$CHAR20.'
    else:
        v.format = '10.2'

# Libraries can have multiple datasets.
library = xport.Library({'DATA': ds})

with open('example.xpt', 'wb') as f:
    xport.v56.dump(library, f)
"""





# = = Open Questions = =
"""

[Thu 09/24/2020]

a.) Controlled Terminologies

(ACN)
(AESEV)
(AGEU)
(DIR)
(DSCAT)
(EPOCH)
(ETHNIC)
(FREQ)
(FRM)
(LAT)
(LBSTRESC)
(LBTEST)
(LBTESTCD)
(LOC)
(METHOD)
(MHEDTTYP)
(NCOMPLT)(PROTMLST)
(ND)
(NRIND)
(NY)
(OUT)
(POSITION)
(RACE)
(ROUTE)
(SEX)
(SPECCOND)
(SPECTYPE)
(STENRF)
(TSPARM)
(TSPARMCD)
(UNIT)
(VSRESU)
(VSRESU)
(VSTEST)
(VSTESTCD)
*
ISO 21090 NullFlavor enumeration
ISO 3166-1 Alpha-3
ISO 8601
MedDRA
"""
