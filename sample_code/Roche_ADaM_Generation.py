#!/usr/bin/python3
# (c) 2007-2020 http://NIHPO.com  Contact: Jose.Lacal@NIHPO.com
# Filename: Roche_ADaM_Generation.py
# Purpose: This Python script generates realistic yet fake ADaM data using Roche's sample spreadsheet.
# Version: Tue 30 June 2020 - NOT finished yet.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
# 
"""
Requirements:
* This script requires Pythin 3.7x
* SQLite3 file "Synthetic_Health_Data_NIHPO.sqlite3" must be in the current directory.



SQLite3 commands:
	a.) Retrieve random row:
		SELECT * FROM table ORDER BY RANDOM() LIMIT 1;



Controlled Terms

C65047
C66727
C66728
C66731
C66734
C66742
C66767
C66768
C66769
C66781
C66789
C67154
C71620
C74456
C74457
C78733
C78734
C78736
C81223
C81226
C85492
C99079
C102580
C124296
L00004
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




= = = Open Questions = = =

= ADSL =
Analysis Age Unit
Pooled Age Group
Intent-To-Treat Population Flag
Safety Population Flag
Per-Protocol Population Flag
Full Analysis Set Population Flag



"""
CT_DEBUG = 0		# Set to 0 (digit zero) to avoid debug messages.
#
# = = = Trial definition = = =
CT_FEMALE_SPLIT = 48	# Percentage of the desired number of Synthetic Subjects assigned a Female / Male gender: MUST be under 100.
#
CT_AGE_MINIMUM = 18
CT_AGE_MAXIMUM = 89
#
# Race splits must add up to 100:
CT_RACE_SPLIT_AMERICAN_INDIAN = 10
CT_RACE_SPLIT_ASIAN = 15
CT_RACE_SPLIT_BLACK = 20
CT_RACE_SPLIT_NATIVE_HAWAIIAN = 7
CT_RACE_SPLIT_WHITE = 48
#
CT_TRIAL_NUMBER_ANALYSIS_VISITS = 5
CT_DELAY_ANALYSIS_RESULT = 5	# Maximum number of days of delay in providing results of analysis.
#
# Trial site definitions:
#	Site name
#	Percentage of subjects enrolled at this site (MUST add up to 100):
CT_SITE_IDS = ['Site_01'] * 10 + ['Site_02'] * 20 + ['Site_03'] * 50 + ['Site_04'] * 20

CT_REFERENCE_RANGE_INDICATOR = ['NORMAL'] * 20 + ['LOW'] * 20 + ['HIGH'] * 20 + ['LOW LOW'] * 20 + ['HIGH HIGH'] * 20

#
CT_INVESTIGATORS = [['Investigator 01', 'INV01'], ['Investigator 02', 'INV02'], ['Investigator 03', 'INV03'], ['Investigator 04', 'INV04'], ['Investigator 05', 'INV05']]
#
CT_ARM_NAMES = [['Arm 01', 'ARM01'], ['Arm 02', 'ARM02'], ['Arm 03', 'ARM03']]
#
CT_PERCENTAGE_DEATHS = 0.05
CT_PERCENTAGE_DISCONTINUATION = 0.23
#
CT_GROUPS = ['Group_01'] * 10 + ['Group_02'] * 20 + ['Group_03'] * 50 + ['Group_04'] * 20
#
# Definition of Test(s) to be conducted. Including:
#	Test name
#	Minimum valid value
#	Maximum valid value
CT_TEST_ANALYSIS = [['Test01', 0.17, 7.96], ['Test02', 5.43, 16], ['Test03', 4000, 11000]]
#
CT_GENDER_SPLIT = ['F'] * CT_FEMALE_SPLIT + ['M'] * (100-CT_FEMALE_SPLIT)
#
# US Department of Health and Human Services, Food and Drug Administration. Collection of race and ethnicity data in clinical trials. Guidance for industry and Food and Drug Administration staff. https://www.fda.gov/media/75453/download. Published October 26, 2016.
# Percentage of the desired number of Synthetic Subjects assigned to each race type. Must add up to 100.
CT_RACE_SPLIT = ['AMERICAN INDIAN OR ALASKA NATIVE'] * CT_RACE_SPLIT_AMERICAN_INDIAN + ['ASIAN'] * CT_RACE_SPLIT_ASIAN + ['BLACK OR AFRICAN AMERICAN'] * CT_RACE_SPLIT_BLACK + ['NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER'] * CT_RACE_SPLIT_NATIVE_HAWAIIAN + ['WHITE'] * CT_RACE_SPLIT_WHITE
#
CT_CSV_SEPARATOR = "|"	# Try NOT to use ',' (commas) to prevent file importing errors.
#
# = = = = = Do not change anything below this line = = = = =
#
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
	from openpyxl import load_workbook
except ImportError:
	print ("\nsudo pip3 install openpyxl")
	sys.exit(1)
#
if (len(sys.argv) != 5):
	print("Usage: python3 Roche_ADaM_Generation.py [StudyID] [TargetDirectory] [NumberSubjects] [DateStartRecruitment]\nUse YYYY-MM-DD for dates.\n")
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
# Common file header:
const_header_01 = "# (c) 2007-2020 http://NIHPO.com   Licensed to PHUSE for non-commercial purposes only.   Contact: Jose.Lacal@NIHPO.com"
const_header_02 = "# This file's structure is based on the CDISC Therapeutic Areas [https://www.cdisc.org/standards/therapeutic-areas]"
const_header_03 = "# WARNING: This information is completely fake. Values such as Age and Gender are randomly assigned using a Weighted Random Generator."
const_header_04 = "# CREDIT: The specific fields used in this file are defined by a sample 'Analysis Dataset Programming Specification' Excel file generously provided by Roche."
#
# Open SQLite3 file:
try:
	nihpo_conn = sqlite3.connect('file:Synthetic_Health_Data_NIHPO.sqlite3?mode=ro', uri=True)
	nihpo_cursor = nihpo_conn.cursor()
except sqlite3.Error as e:
	print ("Error {}:".format(e.args[0]))
	sys.exit(1)
#
#
# = = = Common functions = = =
def func_nihpo_synth_data_random_value (in_sqlite3_cursor, in_codelist):
	"""
	This function will return a random value from a particular codelist from the SQLite3 file "Synthetic_Health_Data_NIHPO.sqlite3"
	Inputs:
		in_sqlite3_cursor - SQLite3 cursor.
		in_codelist - Code of interest.

	Return:
		Single value, randomly selected.

	To call this function:
		func_nihpo_synth_data_random_value(nihpo_cursor, <..>)

	nihpo_cursor.execute('''SELECT therapeutic_area, domain_code, domain_name FROM cdisc_therapeutic_area_domains;''')
	nihpo_cursor.execute('''SELECT therapeutic_area, domain_name, variable, variable_label, data_type, controlled_term, description_text FROM cdisc_therapeutic_area_variables;''')
	nihpo_cursor.execute('''SELECT source_file, code, codelist_code, codelist_extensible, codelist_name, cdisc_submission_value, cdisc_synonym, cdisc_definition, nci_preferred_term FROM cdisc_terminology;''')
	"""

	var_sql = '''SELECT cdisc_submission_value FROM cdisc_terminology WHERE codelist_code = '%s' ORDER BY RANDOM() LIMIT 1;''' % (in_codelist)
	nihpo_cursor.execute(var_sql)
	#
	return nihpo_cursor.fetchone()[0]


#
# = = Open output files for writing = =
var_output_file_ADSL = csv.writer(open(r"ADSL.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADSL.writerow([const_header_01])
var_output_file_ADSL.writerow([const_header_02])
var_output_file_ADSL.writerow([const_header_03])
var_output_file_ADSL.writerow([const_header_04])
var_output_file_ADSL.writerow(["# Dataset: ADSL", "Description: Subject Level Analysis Dataset"])
var_output_file_ADSL.writerow(["STUDYID", "USUBJID",  "SUBJID", "SITEID", "AGE", "AGEU", "SEX", "RACE", "ETHNIC", "COUNTRY", "DMDTC", "DMDY", "BRTHDTC", "DTHDTC", "DTHFL", "RFSTDTC", "RFENDTC", "RFXSTDTC", "RFXENDTC", "RFICDTC", "RFPENDTC", "INVID", "INVNAM", "ARM", "ARMCD", "ACTARM", "ACTARMCD", "BRTHDTF", "AAGE", "AAGEU", "AGEGR1", "ITTFL", "SAFFL", "PPROTFL", "FASFL", "TRT01P", "TRT01A", "RFICDT", "RANDDT", "BRTHDT", "TRTSDTM", "TRTSDT", "TRTEDTM", "TRTEDT", "TRTDURD", "EOSSTT", "EOSDT", "EOTSTT", "EOSDY", "EOSRDY", "DCSREAS", "DCSREASP", "DTHDT", "DTHCAUS", "ADTHAUT", "DTHADY", "AEWITHFL", "LSTALVDT"])
#
var_output_file_ADAE = csv.writer(open(r"ADAE.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADAE.writerow([const_header_01])
var_output_file_ADAE.writerow([const_header_02])
var_output_file_ADAE.writerow([const_header_03])
var_output_file_ADAE.writerow([const_header_04])
var_output_file_ADAE.writerow(["# Dataset: ADAE", "Description: Adverse Events Analysis Dataset"])
var_output_file_ADAE.writerow([	"STUDYID", "USUBJID", "SUBJID", "SITEID", "COUNTRY", "ETHNIC", "AGE", "AGEU", "AAGE", "AAGEU", "SEX", "RACE", "ITTFL", "SAFFL", "PPROTFL", "TRT01P", "TRT01A", "TRTSDTM", "TRTSDT", "TRTEDTM", "TRTEDT", "DOMAIN", "AESEQ", "AEGRPID", "AESPID", "AETERM", "AEMODIFY", "AELLT", "AELLTCD", "AEDECOD", "AEPTCD", "AEHLT", "AEHLTCD", "AEHLGT", "AEHLGTCD", "AECAT", "AESCAT", "AEPRESP", "AEBODSYS", "AEBDSYCD", "AESOC", "AESOCCD", "AELOC", "AESEV", "AESER", "AEACN", "AEACNOTH", "AEREL", "AERELNST", "AEPATT", "AEOUT", "AESCAN", "AESCONG", "AESDISAB", "AESDTH", "AESHOSP", "AESLIFE", "AESOD", "AESMIE", "AECONTRT", "AETOXGR", "EPOCH", "AESTDTC", "AEENDTC", "AESTDY", "AEENDY", "AEDUR", "AESTRTPT", "AESTTPT", "AEENRTPT", "AEENTPT", "AETRTEM", "ASTDTM", "ASTDT", "ASTDTF", "ASTTMF", "ASTDY", "AENDTM", "AENDT", "AENDTF", "AENTMF", "AENDY", "TRTEMFL", "PREFL", "FUPFL", "AREL", "ATOXGR", "ADURN", "ADURU", "LDOSEDTM", "LDOSEDT", "LDRELD", "AOCCIFL", "AOCCPIFL", "AOCCSIFL", "AOCXIFL", "AOCXPIFL", "AOCXSIFL", "ANL01FL"])
#
var_output_file_ADLB = csv.writer(open(r"ADLB.csv", "w"), delimiter=CT_CSV_SEPARATOR, quoting=csv.QUOTE_MINIMAL)
var_output_file_ADLB.writerow([const_header_01])
var_output_file_ADLB.writerow([const_header_02])
var_output_file_ADLB.writerow([const_header_03])
var_output_file_ADLB.writerow([const_header_04])
var_output_file_ADLB.writerow(["# Dataset: ADLB", "Description: Laboratory Analysis Dataset"])
var_output_file_ADLB.writerow(['STUDYID', 'USUBJID', 'SUBJID', 'SITEID', 'ASEQ', 'COUNTRY', 'ETHNIC', 'AGE', 'AGEU', 'AAGE', 'AAGEU', 'SEX', 'RACE', 'ITTFL', 'SAFFL', 'PPROTFL', 'TRT01P', 'TRT01A', 'TRTSDTM', 'TRTSDT', 'TRTEDTM', 'TRTEDT', 'DOMAIN', 'LBSEQ', 'LBGRPID', 'LBREFID', 'LBSPID', 'LBTESTCD', 'LBTEST', 'LBCAT', 'LBSCAT', 'LBORRES', 'LBORRESU', 'LBORNRLO', 'LBORNRHI', 'LBSTRESC', 'LBSTRESN', 'LBSTRESU', 'LBSTNRLO', 'LBSTNRHI', 'LBSTNRC', 'LBNRIND', 'LBSTAT', 'LBREASND', 'LBNAM', 'LBSPEC', 'LBSPCCND', 'LBMETHOD', 'LBBLFL', 'LBFAST', 'VISITNUM', 'VISIT', 'EPOCH', 'LBDTC', 'LBENDTC', 'LBDY', 'LBENDY', 'LBTPT', 'LBTPTNUM', 'LBELTM', 'LBTPTREF', 'LBTSTDTL', 'PARAM', 'PARAMCD', 'PARCAT1', 'PARCAT2', 'AVAL', 'AVALC', 'AVALU', 'AVALCAT1', 'BASE', 'BASETYPE', 'ABLFL', 'CHG', 'PCHG', 'ANRHI', 'ANRLO', 'ANRIND', 'BNRIND', 'R2BASE', 'R2ANRLO', 'R2ANRHI', 'SHIFT1', 'ATOXGR', 'BTOXGR', 'ADTM', 'ADT', 'ADTF', 'ATMF', 'ADY', 'ATPT', 'ATPTN', 'AVISIT', 'AVISITN', 'ONTRTFL', 'LAST01FL', 'WORS01FL', 'WGRHIFL', 'WGRLOFL', 'WGRHIVFL', 'WGRLOVFL', 'ANL01FL'])



#
var_output_file_ADHY = open(os.path.join(CT_TARGET_DIRECTORY, "ADHY.csv"), "w", buffering=1)
var_output_file_ADHY.write(",,Dataset: ADHY,Description: Hys Law Analysis Dataset\n")
#
var_output_file_ADSAFTTE = open(os.path.join(CT_TARGET_DIRECTORY, "ADSAFTTE.csv"), "w", buffering=1)
var_output_file_ADSAFTTE.write(",,Dataset: ADSAFTTE,Description: Safety Time to Event Analysis Dataset\n")
#
#
# Counters:
var_ADAE_Sequence_Number = 1
var_Analysis_Sequence_Number = 1
var_Specimen_ID = 12376

#
subject_counter = 1
while subject_counter <= CT_NUMBER_SUBJECTS:
	print ("Processing subject # %d \n" % (subject_counter))
	#
	# Define 'ADSL' record:
	# One record per subject
	var_ADSL_STUDYID = CT_STUDY_ID											# Study Identifier	text	8		
	var_ADSL_USUBJID = str(uuid.uuid4())									# Unique Subject Identifier	text	50		
	var_ADSL_SUBJID = str(uuid.uuid4())										# Subject Identifier for the Study	text	50		
	var_ADSL_SITEID = random.choice(CT_SITE_IDS)							# Study Site Identifier	text	20		
	var_ADSL_AGE = str(random.randrange(CT_AGE_MINIMUM, CT_AGE_MAXIMUM))	# Age	integer	8		
	var_ADSL_AGEU = "Years"													# Age Units	text	6	C66781	Age Unit
	var_ADSL_SEX = random.choice(CT_GENDER_SPLIT)							# Sex	text	2	C66731	Sex
	var_ADSL_RACE = random.choice(CT_RACE_SPLIT)							# Race	text	200	C74457	Race
	var_ADSL_ETHNIC = "ETHNIC"												# Ethnicity	text	200		
	var_ADSL_COUNTRY = "COUNTRY"											# Country	text	3		ISO3166
	var_ADSL_DMDTC = "DMDTC"												# Date/Time of Collection	dateTime	25		ISO8601
	var_ADSL_DMDY = "DMDY"													# Study Day of Collection	integer	8		
	var_ADSL_BRTHDTC = "BRTHDTC"											# Date/Time of Birth	dateTime	25		ISO8601
	var_ADSL_DTHDTC = "DTHDTC"												# Date/Time of Death	dateTime	25		ISO8601
	var_ADSL_DTHFL = "DTHFL"												# Subject Death Flag	text	2	C66742	No Yes Response
	var_ADSL_RFSTDTC = "RFSTDTC"											# Subject Reference Start Date/Time	dateTime	25		ISO8601
	var_ADSL_RFENDTC = "RFENDTC"											# Subject Reference End Date/Time	dateTime	25		ISO8601
	var_ADSL_RFXSTDTC = "RFXSTDTC"											# Date/Time of First Study Treatment	dateTime	25		ISO8601
	var_ADSL_RFXENDTC = "RFXENDTC"											# Date/Time of Last Study Treatment	dateTime	25		ISO8601
	var_ADSL_RFICDTC = "RFICDTC"											# Date/Time of Informed Consent	dateTime	25		ISO8601
	var_ADSL_RFPENDTC = "RFPENDTC"											# Date/Time of End of Participation	dateTime	25		ISO8601
	var_ADSL_INVID = "INVID"												# Investigator Identifier	text	20		
	var_ADSL_INVNAM = "INVNAM"												# Investigator Name	text	200		
	var_ADSL_ARM = "ARM"													# Description of Planned Arm	text	200	L00060	Description of Planned Arm
	var_ADSL_ARMCD = "ARMCD"												# Planned Arm Code	text	20	L00059	Planned Arm Code
	var_ADSL_ACTARM = "ACTARM"												# Description of Actual Arm	text	200		
	var_ADSL_ACTARMCD = "ACTARMCD"											# Actual Arm Code	text	20		
	var_ADSL_BRTHDTF = "BRTHDTF"											# Imputed Birth Date Flag	text	1	C81223	Date Imputation Flag
	var_ADSL_AAGE = "AAGE"													# Analysis Age	integer	8		
	var_ADSL_AAGEU = "Years"												# Analysis Age Unit	text	6	C66781	Age Unit
	var_ADSL_AGEGR1 = "AGEGR1"												# Pooled Age Group 1	text	10		
	var_ADSL_ITTFL = "ITTFL"												# Intent-To-Treat Population Flag	text	1	C66742	No Yes Response
	var_ADSL_SAFFL = "SAFFL"												# Safety Population Flag	text	1	C66742	No Yes Response
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
	var_ADSL_EOSSTT = "EOSSTT"												# End of Study Status	text	12	C124296	Subject Trial Status
	var_ADSL_EOSDT = "EOSDT"												# End of Study Date	integer	8		
	var_ADSL_EOTSTT = "EOTSTT"												# End of Treatment Status	text	12	C124296	Subject Trial Status
	var_ADSL_EOSDY = "EOSDY"												# End of Study Relative Day	integer	8		
	var_ADSL_EOSRDY = "EOSRDY"												# End of Study Day Rel to Randomization	integer	8		
	var_ADSL_DCSREAS = "DCSREAS"											# Reason for Discontinuation from Study	text	200	C66727	Completion/Reason for Non-Completion
	var_ADSL_DCSREASP = "DCSREASP"											# Reason Spec for Discont from Study	text	200		
	var_ADSL_DTHDT = "DTHDT"												# Date of Death	integer	8		
	var_ADSL_DTHCAUS = "DTHCAUS"											# Cause of Death	text	200		
	var_ADSL_ADTHAUT = "ADTHAUT"											# Autopsy Performed	text	1	C66742	No Yes Response
	var_ADSL_DTHADY = "DTHADY"												# Relative Day of Death	integer	8		
	var_ADSL_AEWITHFL = "AEWITHFL"											# AE Leading to Drug Withdrawal Flag	text	1	C66742	No Yes Response
	var_ADSL_LSTALVDT = "LSTALVDT"											# Date Last Known Alive	integer	8		
	#
	#
	# ADAE File:
	# One record per each record in the corresponding SDTM domain.
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
	var_ADAE_DOMAIN = "Pending"												# Domain Abbreviation	text	2	C66734	SDTM Domain Abbreviation
	var_ADAE_AESEQ = var_ADAE_Sequence_Number								# Sequence Number	integer	8
	var_ADAE_AEGRPID = random.choice(CT_GROUPS)								# Group ID	text	40		
	var_ADAE_AESPID = str(uuid.uuid4())										# Sponsor-Defined Identifier	text	200
	#
	var_ADAE_AETERM = "AETERM"												# Reported Term for the Adverse Event	text	200		
	var_ADAE_AEMODIFY = "AEMODIFY"											# Modified Reported Term	text	200		
	var_ADAE_AELLT = "AELLT"												# Lowest Level Term	text	100		MedDRA
	var_ADAE_AELLTCD = "AELLTCD"									#	Lowest Level Term Code	integer	8		MedDRA
	var_ADAE_AEDECOD = "Pending"									#	Dictionary-Derived Term	text	200		MedDRA
	var_ADAE_AEPTCD = "Pending"									#	Preferred Term Code	integer	8		MedDRA
	var_ADAE_AEHLT = "Pending"									#	High Level Term	text	100		MedDRA
	var_ADAE_AEHLTCD = "Pending"									#	High Level Term Code	integer	8		MedDRA
	var_ADAE_AEHLGT = "Pending"									#	High Level Group Term	text	100		MedDRA
	var_ADAE_AEHLGTCD = "Pending"									#	High Level Group Term Code	integer	8		MedDRA
	var_ADAE_AECAT = "Pending"									#	Category for Adverse Event	text	100		*
	var_ADAE_AESCAT = "Pending"									#	Subcategory for Adverse Event	text	100		
	var_ADAE_AEPRESP = "Pending"									#	Pre-Specified Adverse Event	text	2	C66742	No Yes Response
	var_ADAE_AEBODSYS = "Pending"									#	Body System or Organ Class	text	200		MedDRA
	var_ADAE_AEBDSYCD = "Pending"									#	Body System or Organ Class Code	integer	8		MedDRA
	var_ADAE_AESOC = "Pending"									#	Primary System Organ Class	text	200		MedDRA
	var_ADAE_AESOCCD = "Pending"									#	Primary System Organ Class Code	integer	8		MedDRA
	var_ADAE_AELOC = "Pending"									#	Location of Event	text	200	C74456	Anatomical Location
	var_ADAE_AESEV = "Pending"									#	Severity/Intensity	text	10	C66769	Severity/Intensity Scale for Adverse Events
	var_ADAE_AESER = "Pending"									#	Serious Event	text	2	C66742	No Yes Response
	var_ADAE_AEACN = "Pending"									#	Action Taken with Study Treatment	text	16	C66767	Action Taken with Study Treatment
	var_ADAE_AEACNOTH = "Pending"									#	Other Action Taken	text	200		
	var_ADAE_AEREL = "Pending"									#	Causality	text	20		*
	var_ADAE_AERELNST = "Pending"									#	Relationship to Non-Study Treatment	text	200	C66742	No Yes Response
	var_ADAE_AEPATT = "Pending"									#	Pattern of Adverse Event	text	40	L00004	Adverse Event Pattern
	var_ADAE_AEOUT = "Pending"									#	Outcome of Adverse Event	text	40	C66768	Outcome of Event
	var_ADAE_AESCAN = "Pending"									#	Involves Cancer	text	2	C66742	No Yes Response
	var_ADAE_AESCONG = "Pending"									#	Congenital Anomaly or Birth Defect	text	2	C66742	No Yes Response
	var_ADAE_AESDISAB = "Pending"									#	Persist or Signif Disability/Incapacity	text	2	C66742	No Yes Response
	var_ADAE_AESDTH = "Pending"									#	Results in Death	text	2	C66742	No Yes Response
	var_ADAE_AESHOSP = "Pending"									#	Requires or Prolongs Hospitalization	text	2	C66742	No Yes Response
	var_ADAE_AESLIFE = "Pending"									#	Is Life Threatening	text	2	C66742	No Yes Response
	var_ADAE_AESOD = "Pending"									#	Occurred with Overdose	text	2	C66742	No Yes Response
	var_ADAE_AESMIE = "Pending"									#	Other Medically Important Serious Event	text	2	C66742	No Yes Response
	var_ADAE_AECONTRT = "Pending"									#	Concomitant or Additional Trtmnt Given	text	2	C66742	No Yes Response
	var_ADAE_AETOXGR = "Pending"									#	Standard Toxicity Grade	text	1		*
	#
	var_ADAE_EPOCH = "Pending"									#	Epoch	text	40	C99079	Epoch
	var_ADAE_AESTDTC = "Pending"									#	Start Date/Time of Adverse Event	dateTime	25		ISO 8601
	var_ADAE_AEENDTC = "Pending"									#	End Date/Time of Adverse Event	dateTime	25		ISO 8601
	var_ADAE_AESTDY = "Pending"									#	Study Day of Start of Adverse Event	integer	8		
	var_ADAE_AEENDY = "Pending"									#	Study Day of End of Adverse Event	integer	8		
	var_ADAE_AEDUR = "Pending"									#	Duration of Adverse Event	duration	25		ISO 8601
	var_ADAE_AESTRTPT = "Pending"									#	Start Relative to Reference Time Point	text	20	C66728	Relation to Reference Period
	var_ADAE_AESTTPT = "Pending"									#	Start Reference Time Point	text	40		
	var_ADAE_AEENRTPT = "Pending"									#	End Relative to Reference Time Point	text	20	C66728	Relation to Reference Period
	var_ADAE_AEENTPT = "Pending"									#	End Reference Time Point	text	40		
	var_ADAE_AETRTEM = "Pending"									#	Treatment Emergent Flag	text	2	C66742	No Yes Response
	#
	var_ADAE_ASTDTM = "Pending"									#	Analysis Start Date/Time	integer	8		
	var_ADAE_ASTDT = "Pending"									#	Analysis Start Date	integer	8		
	var_ADAE_ASTDTF = "Pending"									#	Analysis Start Date Imputation Flag	text	1	C81223	Date Imputation Flag
	var_ADAE_ASTTMF = "Pending"									#	Analysis Start Time Imputation Flag	text	1	C81226	Time Imputation Flag
	var_ADAE_ASTDY = "Pending"									#	Analysis Start Relative Day	integer	8		
	var_ADAE_AENDTM = "Pending"									#	Analysis End Date/Time	integer	8		
	var_ADAE_AENDT = "Pending"									#	Analysis End Date	integer	8		
	var_ADAE_AENDTF = "Pending"									#	Analysis End Date Imputation Flag	text	1	C81223	Date Imputation Flag
	var_ADAE_AENTMF = "Pending"									#	Analysis End Time Imputation Flag	text	1	C81226	Time Imputation Flag
	var_ADAE_AENDY = "Pending"									#	Analysis End Relative Day	integer	8		
	#
	var_ADAE_TRTEMFL = "Pending"									#	Treatment Emergent Analysis Flag	text	1	L00052	Yes Response
	var_ADAE_PREFL = "Pending"									#	Pre-treatment Flag	text	1	L00052	Yes Response
	var_ADAE_FUPFL = "Pending"									#	Follow-up Flag	text	1	L00052	Yes Response
	var_ADAE_AREL = "Pending"									#	Analysis Causality	text	50		*
	var_ADAE_ATOXGR = "Pending"									#	Analysis Toxicity Grade	text	50		*
	var_ADAE_ADURN = "Pending"									#	Analysis Duration (N)	float	8		
	var_ADAE_ADURU = "Pending"									#	Analysis Duration Units	text	40	C71620	Unit
	var_ADAE_LDOSEDTM = "Pending"									#	End Date/Time of Last Dose	integer	8		
	var_ADAE_LDOSEDT = "Pending"									#	End Date of Last Dose	integer	8		
	var_ADAE_LDRELD = "Pending"									#	Day Since Last Dose	integer	8		
	var_ADAE_AOCCIFL = "Pending"									#	1st Max Sev./Int. Occurrence Flag	text	1	L00052	Yes Response
	var_ADAE_AOCCPIFL = "Pending"									#	1st Max Sev./Int. Occur Within PT Flag	text	1	L00052	Yes Response
	var_ADAE_AOCCSIFL = "Pending"									#	1st Max Sev./Int. Occur Within SOC Flag	text	1	L00052	Yes Response
	var_ADAE_AOCXIFL = "Pending"									#	1st Max Sev./Int. Occ per Period	text	1	L00052	Yes Response
	var_ADAE_AOCXPIFL = "Pending"									#	1st Max Sev./Int. Occ in PT per Period	text	1	L00052	Yes Response
	var_ADAE_AOCXSIFL = "Pending"									#	1st Max Sev./Int. Occ in SOC per Period	text	1	L00052	Yes Response
	var_ADAE_ANL01FL = "Pending"									#	Analysis Flag 01	text	1	L00052	Yes Response
	#
	var_ADAE_Sequence_Number += 1
	# Write ADAE record to file:
	var_output_file_ADAE.writerow([	var_ADAE_STUDYID, var_ADAE_USUBJID, var_ADAE_SUBJID, var_ADAE_SITEID, var_ADAE_COUNTRY, var_ADAE_ETHNIC, var_ADAE_AGE, var_ADAE_AGEU, var_ADAE_AAGE, var_ADAE_AAGEU, var_ADAE_SEX, var_ADAE_RACE, var_ADAE_ITTFL, var_ADAE_SAFFL, var_ADAE_PPROTFL, var_ADAE_TRT01P, var_ADAE_TRT01A, var_ADAE_TRTSDTM, var_ADAE_TRTSDT, var_ADAE_TRTEDTM, var_ADAE_TRTEDT, var_ADAE_DOMAIN, var_ADAE_AESEQ, var_ADAE_AEGRPID, var_ADAE_AESPID, var_ADAE_AETERM, var_ADAE_AEMODIFY, var_ADAE_AELLT, var_ADAE_AELLTCD, var_ADAE_AEDECOD, var_ADAE_AEPTCD, var_ADAE_AEHLT, var_ADAE_AEHLTCD, var_ADAE_AEHLGT, var_ADAE_AEHLGTCD, var_ADAE_AECAT, var_ADAE_AESCAT, var_ADAE_AEPRESP, var_ADAE_AEBODSYS, var_ADAE_AEBDSYCD, var_ADAE_AESOC, var_ADAE_AESOCCD, var_ADAE_AELOC, var_ADAE_AESEV, var_ADAE_AESER, var_ADAE_AEACN, var_ADAE_AEACNOTH, var_ADAE_AEREL, var_ADAE_AERELNST, var_ADAE_AEPATT, var_ADAE_AEOUT, var_ADAE_AESCAN, var_ADAE_AESCONG, var_ADAE_AESDISAB, var_ADAE_AESDTH, var_ADAE_AESHOSP, var_ADAE_AESLIFE, var_ADAE_AESOD, var_ADAE_AESMIE, var_ADAE_AECONTRT, var_ADAE_AETOXGR, var_ADAE_EPOCH, var_ADAE_AESTDTC, var_ADAE_AEENDTC, var_ADAE_AESTDY, var_ADAE_AEENDY, var_ADAE_AEDUR, var_ADAE_AESTRTPT, var_ADAE_AESTTPT, var_ADAE_AEENRTPT, var_ADAE_AEENTPT, var_ADAE_AETRTEM, var_ADAE_ASTDTM, var_ADAE_ASTDT, var_ADAE_ASTDTF, var_ADAE_ASTTMF, var_ADAE_ASTDY, var_ADAE_AENDTM, var_ADAE_AENDT, var_ADAE_AENDTF, var_ADAE_AENTMF, var_ADAE_AENDY, var_ADAE_TRTEMFL, var_ADAE_PREFL, var_ADAE_FUPFL, var_ADAE_AREL, var_ADAE_ATOXGR, var_ADAE_ADURN, var_ADAE_ADURU, var_ADAE_LDOSEDTM, var_ADAE_LDOSEDT, var_ADAE_LDRELD, var_ADAE_AOCCIFL, var_ADAE_AOCCPIFL, var_ADAE_AOCCSIFL, var_ADAE_AOCXIFL, var_ADAE_AOCXPIFL, var_ADAE_AOCXSIFL, var_ADAE_ANL01FL])


	# ADLB file:
	# One record per subject per parameter per analysis visit per analysis date.
	# _x000D_ SDTM variables are populated on new records coming from other single records.  Otherwise, SDTM variables are left blank.
	var_ADLB_STUDYID = CT_STUDY_ID 									# Study Identifier	text	8		
	var_ADLB_USUBJID = var_ADSL_USUBJID 							# Unique Subject Identifier	text	50		
	var_ADLB_SUBJID = var_ADSL_SUBJID 								# Subject Identifier for the Study	text	50		
	var_ADLB_SITEID  = var_ADSL_SITEID 								# Study Site Identifier	text	20		
	var_ADLB_ASEQ = var_Analysis_Sequence_Number 					# Analysis Sequence Number	integer	8		
	var_ADLB_COUNTRY = var_ADSL_COUNTRY 							# Country	text	32		ISO3166
	var_ADLB_ETHNIC = var_ADSL_ETHNIC								# Ethnicity	text	32		
	var_ADLB_AGE = var_ADSL_AGE										# Age	integer	8		
	var_ADLB_AGEU = var_ADSL_AGEU 									# Age Units	text	5	C66781	Age Unit
	var_ADLB_AAGE = var_ADAE_AAGE 									# Analysis Age	integer	8		
	var_ADLB_AAGEU = var_ADAE_AAGEU 								# Analysis Age Unit	text	6	C66781	Age Unit
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
	var_ADLB_DOMAIN = var_ADAE_DOMAIN											# Domain Abbreviation	text	2	C66734	SDTM Domain Abbreviation
	var_ADLB_LBSEQ = var_ADAE_Sequence_Number									# Sequence Number	integer	8		
	var_ADLB_LBGRPID = var_ADAE_AEGRPID											# Group ID	text	40		
	var_ADLB_LBREFID = var_Specimen_ID											# Specimen ID	text	40		
	var_ADLB_LBSPID = var_ADAE_AESPID											# Sponsor-Defined Identifier	text	200		
	var_ADLB_LBTESTCD = func_nihpo_synth_data_random_value(nihpo_cursor, 'C65047')			# Lab Test or Examination Short Name	text	8	C65047	Laboratory Test Code
	var_ADLB_LBTEST = func_nihpo_synth_data_random_value(nihpo_cursor, 'C67154')			# Lab Test or Examination Name	text	40	C67154	Laboratory Test Name
	var_ADLB_LBCAT = "Pending"									#	Category for Lab Test	text	100		
	var_ADLB_LBSCAT = "Pending"									#	Subcategory for Lab Test	text	100		
	var_ADLB_LBORRES = "Pending"									#	Result or Finding in Original Units	text	200		
	var_ADLB_LBORRESU = func_nihpo_synth_data_random_value(nihpo_cursor, 'C71620')			# Original Units	text	40	C71620	Unit
	var_ADLB_LBORNRLO = "Pending"									#	Reference Range Lower Limit in Orig Unit	text	200		
	var_ADLB_LBORNRHI = "Pending"									#	Reference Range Upper Limit in Orig Unit	text	200		
	var_ADLB_LBSTRESC = "Pending"									#	Character Result/Finding in Std Format	text	200	C102580	Laboratory Test Standard Character Result
	var_ADLB_LBSTRESN = "Pending"									#	Numeric Result/Finding in Standard Units	float	8		
	var_ADLB_LBSTRESU = func_nihpo_synth_data_random_value(nihpo_cursor, 'C71620')			# Standard Units	text	40	C71620	Unit
	var_ADLB_LBSTNRLO = "Pending"									#	Reference Range Lower Limit-Std Units	float	8		
	var_ADLB_LBSTNRHI = "Pending"									#	Reference Range Upper Limit-Std Units	float	8		
	var_ADLB_LBSTNRC = "Pending"									#	Reference Range for Char Rslt	text	200		
	var_ADLB_LBNRIND = func_nihpo_synth_data_random_value(nihpo_cursor, 'C78736')			# Reference Range Indicator	text	25	C78736	Reference Range Indicator
	var_ADLB_LBSTAT = func_nihpo_synth_data_random_value(nihpo_cursor, 'C66789')			# Completion Status	text	8	C66789	Not Done
	var_ADLB_LBREASND = "Pending"									#	Reason Test Not Done	text	200		
	var_ADLB_LBNAM = "Pending"									#	Vendor Name	text	200		
	var_ADLB_LBSPEC = func_nihpo_synth_data_random_value(nihpo_cursor, 'C78734')			# Specimen Type	text	40	C78734	Specimen Type
	var_ADLB_LBSPCCND = "Pending"									#	Specimen Condition	text	200	C78733	Specimen Condition
	var_ADLB_LBMETHOD = "Pending"									#	Method of Test or Examination	text	100	C85492	Method
	var_ADLB_LBBLFL = "Pending"									#	Baseline Flag	text	2	C66742	No Yes Response
	var_ADLB_LBFAST = "Pending"									#	Fasting Status	text	2	C66742	No Yes Response
	var_ADLB_VISITNUM = "Pending"									#	Visit Number	integer	8		
	var_ADLB_VISIT = "Pending"									#	Visit Name	text	200		
	var_ADLB_EPOCH = "Pending"									#	Epoch	text	40	C99079	Epoch
	var_ADLB_LBDTC = "Pending"									#	Date/Time of Specimen Collection	dateTime	25		ISO8601
	var_ADLB_LBENDTC = "Pending"									#	End Date/Time of Specimen Collection	dateTime	25		ISO8601
	var_ADLB_LBDY = "Pending"									#	Study Day of Specimen Collection	integer	8		
	var_ADLB_LBENDY = "Pending"									#	Study Day of End of Observation	integer	8		
	var_ADLB_LBTPT = "Pending"									#	Planned Time Point Name	text	40		
	var_ADLB_LBTPTNUM = "Pending"									#	Planned Time Point Number	integer	8		
	var_ADLB_LBELTM = "Pending"									#	Planned Elapsed Time from Time Point Ref	dateTime	25		
	var_ADLB_LBTPTREF = "Pending"									#	Time Point Reference	text	40		
	var_ADLB_LBTSTDTL = "Pending"									#	Lab Test or Examination Detailed Name	text	200		
	var_ADLB_PARAM = "Pending"									#	Parameter	text	200		
	var_ADLB_PARAMCD = "Pending"									#	Parameter Code	text	8		
	var_ADLB_PARCAT1 = random.choice(['CHEMISTRY'] * 33 + ['COAGULATION'] * 34 + ['HEMATOLOGY'] * 33) 			# Parameter Category 1 - Laboratory Class	text	100		CHEMISTRY | COAGULATION | HEMATOLOGY
	var_ADLB_PARCAT2 = random.choice(['LS'] * 33 + ['CV'] * 34 + ['SI'] * 33) 									# Parameter Category 2 - Reporting Classification	text	3		LS | CV | SI
	var_ADLB_AVAL = "Pending"									#	Analysis Value	float	8		
	var_ADLB_AVALC = "Pending"									#	Analysis Value (C)	text	200		
	var_ADLB_AVALU = "Pending"									#	Analysis Value Unit	text	40		
	var_ADLB_AVALCAT1 = random.choice(['SINGLE'] * 33 + ['REPLICATED'] * 34 + ['LAST'] * 33) 				#  	Analysis Value Category 1 Marked Lab Ab	text	20		SINGLE | REPLICATED | LAST
	var_ADLB_BASE = "Pending"									#	Baseline Value	float	8		
	var_ADLB_BASETYPE = "LAST"									# Baseline Type	text	30		LAST
	var_ADLB_ABLFL = "Pending"									#	Baseline Record Flag	text	1	L00052	Yes Response
	var_ADLB_CHG = "Pending"									#	Change from Baseline	float	8		
	var_ADLB_PCHG = "Pending"									#	Percent Change from Baseline	float	8		
	var_ADLB_ANRHI = "Pending"									#	Analysis Normal Range Upper Limit	float	8		
	var_ADLB_ANRLO = "Pending"									#	Analysis Normal Range Lower Limit	float	8		
	var_ADLB_ANRIND = random.choice(CT_REFERENCE_RANGE_INDICATOR)							# Analysis Reference Range Indicator	text	20		NORMAL | LOW | HIGH | LOW LOW | HIGH HIGH
	var_ADLB_BNRIND = random.choice(CT_REFERENCE_RANGE_INDICATOR) 						# Baseline Reference Range Indicator	text	20		NORMAL | LOW | HIGH | LOW LOW | HIGH HIGH
	var_ADLB_R2BASE = "Pending"									#	Ratio to Baseline	integer	8		
	var_ADLB_R2ANRLO = "Pending"									#	Ratio of Analysis Val compared to ANRLO	integer	8		
	var_ADLB_R2ANRHI = "Pending"									#	Ratio of Analysis Val compared to ANRHI	integer	8		
	var_ADLB_SHIFT1 = "Pending"									#	Shift from Baseline to Analysis Value	text	20		
	var_ADLB_ATOXGR = "Pending"									#	Analysis Toxicity Grade	text	2		
	var_ADLB_BTOXGR = "Pending"									#	Baseline Toxicity Grade	text	2		
	var_ADLB_ADTM = "Pending"									#	Analysis Datetime	integer	8		
	var_ADLB_ADT = "Pending"									#	Analysis Date	integer	8		
	var_ADLB_ADTF = "Pending"									#	Analysis Date Imputation Flag	text	1	C81223	Date Imputation Flag
	var_ADLB_ATMF = "Pending"									#	Analysis Time Imputation Flag	text	1	C81226	Time Imputation Flag
	var_ADLB_ADY = "Pending"									#	Analysis Relative Day	integer	8		
	var_ADLB_ATPT = "Pending"									#	Analysis Timepoint	text	40		
	var_ADLB_ATPTN = "Pending"									#	Analysis Timepoint (N)	integer	8		
	var_ADLB_AVISIT = "Pending"									#	Analysis Visit	text	200		
	var_ADLB_AVISITN = "Pending"									#	Analysis Visit (N)	integer	8		
	var_ADLB_ONTRTFL = "Pending"									#	On Treatment Record Flag	text	1	L00052	Yes Response
	var_ADLB_LAST01FL = "Pending"									#	Last Observation in Window Flag 01	text	1	L00052	Yes Response
	var_ADLB_WORS01FL = "Pending"									#	Worst Observation in Window Flag 01	text	1	L00052	Yes Response
	var_ADLB_WGRHIFL = "Pending"									#	Worst High Grade per Patient	text	1	L00052	Yes Response
	var_ADLB_WGRLOFL = "Pending"									#	Worst Low Grade per Patient	text	1	L00052	Yes Response
	var_ADLB_WGRHIVFL = "Pending"									#	Worst High Grade per Patient per Visit	text	1	L00052	Yes Response
	var_ADLB_WGRLOVFL = "Pending"									#	Worst Low Grade per Patient per Visit	text	1	L00052	Yes Response
	var_ADLB_ANL01FL = "Pending"									#	Analysis Flag 01 Baseline Post-Baseline	text	1	L00052	Yes Response
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
	# Write ADSL record to file:
	if (CT_DEBUG == 1):
		print (var_ADSL_STUDYID, var_ADSL_USUBJID, var_ADSL_SUBJID, var_ADSL_SITEID, var_ADSL_AGE, var_ADSL_AGEU, var_ADSL_SEX, var_ADSL_RACE, var_ADSL_ETHNIC, var_ADSL_COUNTRY, var_ADSL_DMDTC, var_ADSL_DMDY, var_ADSL_BRTHDTC, var_ADSL_DTHDTC, var_ADSL_DTHFL, var_ADSL_RFSTDTC, var_ADSL_RFENDTC, var_ADSL_RFXSTDTC, var_ADSL_RFXENDTC, var_ADSL_RFICDTC, var_ADSL_RFPENDTC, var_ADSL_INVID, var_ADSL_INVNAM, var_ADSL_ARM, var_ADSL_ARMCD, var_ADSL_ACTARM, var_ADSL_ACTARMCD, var_ADSL_BRTHDTF, var_ADSL_AAGE, var_ADSL_AAGEU, var_ADSL_AGEGR1, var_ADSL_ITTFL, var_ADSL_SAFFL, var_ADSL_PPROTFL, var_ADSL_FASFL, var_ADSL_TRT01P, var_ADSL_TRT01A, var_ADSL_RFICDT, var_ADSL_RANDDT, var_ADSL_BRTHDT, var_ADSL_TRTSDTM, var_ADSL_TRTSDT, var_ADSL_TRTEDTM, var_ADSL_TRTEDT, var_ADSL_TRTDURD, var_ADSL_EOSSTT, var_ADSL_EOSDT, var_ADSL_EOTSTT, var_ADSL_EOSDY, var_ADSL_EOSRDY, var_ADSL_DCSREAS, var_ADSL_DCSREASP, var_ADSL_DTHDT, var_ADSL_DTHCAUS, var_ADSL_ADTHAUT, var_ADSL_DTHADY, var_ADSL_AEWITHFL, var_ADSL_LSTALVDT)
		#
	var_output_file_ADSL.writerow([var_ADSL_STUDYID, var_ADSL_USUBJID, var_ADSL_SUBJID, var_ADSL_SITEID, var_ADSL_AGE, var_ADSL_AGEU, var_ADSL_SEX, var_ADSL_RACE, var_ADSL_ETHNIC, var_ADSL_COUNTRY, var_ADSL_DMDTC, var_ADSL_DMDY, var_ADSL_BRTHDTC, var_ADSL_DTHDTC, var_ADSL_DTHFL, var_ADSL_RFSTDTC, var_ADSL_RFENDTC, var_ADSL_RFXSTDTC, var_ADSL_RFXENDTC, var_ADSL_RFICDTC, var_ADSL_RFPENDTC, var_ADSL_INVID, var_ADSL_INVNAM, var_ADSL_ARM, var_ADSL_ARMCD, var_ADSL_ACTARM, var_ADSL_ACTARMCD, var_ADSL_BRTHDTF, var_ADSL_AAGE, var_ADSL_AAGEU, var_ADSL_AGEGR1, var_ADSL_ITTFL, var_ADSL_SAFFL, var_ADSL_PPROTFL, var_ADSL_FASFL, var_ADSL_TRT01P, var_ADSL_TRT01A, var_ADSL_RFICDT, var_ADSL_RANDDT, var_ADSL_BRTHDT, var_ADSL_TRTSDTM, var_ADSL_TRTSDT, var_ADSL_TRTEDTM, var_ADSL_TRTEDT, var_ADSL_TRTDURD, var_ADSL_EOSSTT, var_ADSL_EOSDT, var_ADSL_EOTSTT, var_ADSL_EOSDY, var_ADSL_EOSRDY, var_ADSL_DCSREAS, var_ADSL_DCSREASP, var_ADSL_DTHDT, var_ADSL_DTHCAUS, var_ADSL_ADTHAUT, var_ADSL_DTHADY, var_ADSL_AEWITHFL, var_ADSL_LSTALVDT])

	#
	subject_counter += 1


# = = Clean up files = =
nihpo_conn.close()
#
var_output_file_ADHY.close()
var_output_file_ADSAFTTE.close()

print ("This is the end, my friend.")


"""
	if 'ADAE' in CT_SHEETS:
		# One record for each record in the corresponding SDTM domain.


	if 'ADLB' in CT_SHEETS:
		# One record per subject per parameter per analysis visit per analysis date._x000D_ SDTM variables are populated on new records coming from other single records.
		# Otherwise, SDTM variables are left blank.

	if 'ADHY' in CT_SHEETS:
		# One record per subject per parameter per analysis visit per analysis date._x000D_ SDTM variables are populated on new records coming from other single records.  
		# Otherwise, SDTM variables are left blank.

	if 'ADSAFTTE' in CT_SHEETS:
		# One record per subject per parameter per analysis visit per analysis date._x000D_ SDTM variables are populated on new records coming from other single records.  
		# Otherwise, SDTM variables are left blank.
"""
