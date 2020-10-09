#!/usr/bin/python3
# Author: Jose.Lacal@NIHPO.com
# Filename: Generate_SDTM.py
# Purpose: This Python script generates realistic yet fake CDISC SDTM data using guidance from PHUSE's TDF working group.
# Version: Tue 06 October 2020.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
#
# From the SDTM Implementation Guide v 3.3 Final, pages 361 and forward:
CT_TA_EXAMPLE_TRIAL = 1
# Avaailable Trial Design Matrix examples: 1; 2; 3
#
# Constants:
CT_STUDYID = 'XYZ'
#
CT_DEBUG = [1, 2, 'TD', 'TE', 'TI', 'TM', 'TS', 'TV']
# Set to 0 (digit zero) to avoid debug messages. 
# 	1 for DataFrame creation
# 	2 for JSON parsing
#	Use the Domain Code to see processing steps for each Domain.
#
# Trial Design Matrix:
# The columns of a Trial Design Matrix are the Epochs of the trial, the rows are the Arms of the trial, and the cells of the matrix (the Study Cells) contain Elements.
#
# >> Validate JSON here: https://jsonlint.com/?code=
#
# Trial Design Matrix for Example Trial 1 (page 361 in SDTMIG):
if (CT_TA_EXAMPLE_TRIAL == 1):
	CT_STUDYID = 'EX1'
	CT_TRIAL_DESIGN_MATRIX = {"domain": "TA", "tdm": [
		{"arm" : "Placebo", "armcd": "P", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "RI", "element": "Run-in", "tabranch": "Randomized to Placebo", "tatrans": "", "epoch": "RUN-IN"},
			{"etcd": "P", "element": "Placebo", "tabranch": "", "tatrans": "", "epoch": "TREATMENT"}
			]},
		{"arm" : "A", "armcd": "A", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "RI", "element": "Run-in", "tabranch": "Randomized to Drug A", "tatrans": "", "epoch": "RUN-IN"},
			{"etcd": "A", "element": "Drug A", "tabranch": "", "tatrans": "", "epoch": "TREATMENT"}
			]},
		{"arm" : "B", "armcd": "B", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "RI", "element": "Run-in", "tabranch": "Randomized to Drub B", "tatrans": "", "epoch": "RUN-IN"},
			{"etcd": "B", "element": "Drug B", "tabranch": "", "tatrans": "", "epoch": "TREATMENT"}
			]}
	]}
#
# Trial Design Matrix for Example Trial 2 (page 363 in SDTMIG):
if (CT_TA_EXAMPLE_TRIAL == 2):
	CT_STUDYID = 'EX2'
	CT_TRIAL_DESIGN_MATRIX = {"domain": "TA", "tdm": [
		{"arm" : "Placebo - 5mg - 10mg", "armcd": "P-5-10", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to Placebo - 5 mg - 10 mg", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "P", "element": "Placebo", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 1"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 1"},
			{"etcd": "5", "element": "5 mg", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 2"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 2"},
			{"etcd": "10", "element": "10 mg", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 3"},
			{"etcd": "FU", "element": "Follow-up", "tabranch": "", "tatrans": "", "epoch": "FOLLOW-UP"}
			]},
		{"arm" : "5mg - Placebo - 10mg", "armcd": "5-P-10", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to 5 mg - Placebo - 10 mg", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "5", "element": "5 mg", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 1"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 1"},
			{"etcd": "P", "element": "Placebo", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 2"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 2"},
			{"etcd": "10", "element": "10 mg", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 3"},
			{"etcd": "FU", "element": "Follow-up", "tabranch": "", "tatrans": "", "epoch": "FOLLOW-UP"}
			]},
		{"arm" : "5mg - 10mg - Placebo", "armcd": "5-10-P", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to 5 mg - 10 mg - Placebo", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "5", "element": "5 mg", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 1"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 1"},
			{"etcd": "10", "element": "10 mg.", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 2"},
			{"etcd": "REST", "element": "Rest", "tabranch": "", "tatrans": "", "epoch": "WASHOUT 2"},
			{"etcd": "P", "element": "Placebo", "tabranch": "", "tatrans": "", "epoch": "TREATMENT 3"},
			{"etcd": "FU", "element": "Follow-up", "tabranch": "", "tatrans": "", "epoch": "FOLLOW-UP"}
			]}

	]}
#
# Trial Design Matrix for Example Trial 3 (page 366 in SDTMIG):
if (CT_TA_EXAMPLE_TRIAL == 3):
	CT_STUDYID = 'EX3'
	CT_TRIAL_DESIGN_MATRIX = {"domain": "TA", "tdm": [
		{"arm" : "A-Open A", "armcd": "AA", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to Treatment A", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "DBA", "element": "Treatment A", "tabranch": "Assigned to Open Drug A on basis of response evaluation", "tatrans": "", "epoch": "BLINDED TREATMENT"},
			{"etcd": "OA", "element": "Open Drug A", "tabranch": "", "tatrans": "", "epoch": "OPEN LABEL TREATMENT"}
			]},
		{"arm" : "A-Rescue", "armcd": "AR", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to Treatment A", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "DBA", "element": "Treatment A", "tabranch": "Assigned to Rescue on basis of response evaluation", "tatrans": "", "epoch": "BLINDED TREATMENT"},
			{"etcd": "RSC", "element": "Rescue", "tabranch": "", "tatrans": "", "epoch": "OPEN LABEL TREATMENT"}
			]},
		{"arm" : "B-Open A", "armcd": "BA", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to Treatment B", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "DBB", "element": "Treatment B", "tabranch": "Assigned to Open Drug A on basis of response evaluation", "tatrans": "", "epoch": "BLINDED TREATMENT"},
			{"etcd": "OA", "element": "Open Drug A", "tabranch": "", "tatrans": "", "epoch": "OPEN LABEL TREATMENT"}
			]},
		{"arm" : "B-Rescue", "armcd": "BR", "epochs": [
			{"etcd": "SCRN", "element": "Screen", "tabranch": "Randomized to Treatment B", "tatrans": "", "epoch": "SCREENING"},
			{"etcd": "DBB", "element": "Treatment B", "tabranch": "Assigned to Rescue on basis of response evaluation", "tatrans": "", "epoch": "BLINDED TREATMENT"},
			{"etcd": "RSC", "element": "Rescue", "tabranch": "", "tatrans": "", "epoch": "OPEN LABEL TREATMENT"}
			]}
	]}
#
#
# Trial Visit Matrix:
# Source: Example Trial 1, Parallel Design Planned Visits. Page 383 in SDTMIG.
CT_TRIAL_VISIT_MATRIX = {"domain": "TV", "visits": [
	{"visitnum": "1", "visit": "Visit 01", "visitdy": "1", "armcd": "Arm code 01", "arm": "Arm 01", "tvstrl": "Start of Screen Epoch", "tvenrl": "1 hour after start of Visit"},
	{"visitnum": "2", "visit": "Visit 02", "visitdy": "2", "armcd": "Arm code 02", "arm": "Arm 02", "tvstrl": "30 minutes before end of Screen Epoch", "tvenrl": "30 minutes after start of Run-in Epoch"},
	{"visitnum": "3", "visit": "Visit 03", "visitdy": "3", "armcd": "Arm code 03", "arm": "Arm 03", "tvstrl": "30 minutes before end of Run-in Epoch", "tvenrl": "1 hour after start of Treatment Epoch"},
	{"visitnum": "4", "visit": "Visit 04", "visitdy": "4", "armcd": "Arm code 04", "arm": "Arm 04", "tvstrl": "1 week after start of Treatment Epoch", "tvenrl": "1 hour after start of Visit"},
	{"visitnum": "5", "visit": "Visit 05", "visitdy": "5", "armcd": "Arm code 05", "arm": "Arm 05", "tvstrl": "2 weeks after start of Treatment Epoch", "tvenrl": "1 hour after start of Visit"}
]}
"""
Pending [Thu 10/08/2020]
* Design mechanism to encode both TVSTRL and TVENRL to allow for computing dates below.
Possible parameters:
	Time unit [hour | day | week | month] after [start | end] Epoch.
	Time unit [hour | day | week | month] after [start | end] Visit.
"""
#
#
# Trial Disease Assessments Matrix:
# Source: TD Example 1, (page 387 in SDTMIG):
CT_TRIAL_DISEASE_ASSESSMENT_MATRIX = {"domain": "TD", "assessments": [
	{"tdorder": "1", "tdancvar": "ANCH1DT", "tdstoff": "P0D", "tdtgtpai": "P8W", "tdminpai": "P53D", "tdmaxpai": "P9W", "tdnumrpt": "6"},
	{"tdorder": "2", "tdancvar": "ANCH1DT", "tdstoff": "P60W", "tdtgtpai": "P12W", "tdminpai": "P11W", "tdmaxpai": "P13W", "tdnumrpt": "4"},
	{"tdorder": "3", "tdancvar": "ANCH1DT", "tdstoff": "P120W", "tdtgtpai": "P24W", "tdminpai": "P23W", "tdmaxpai": "P25W", "tdnumrpt": "12"}
]}
#
#
# Trial Disease Milestones Matrix:
# Source: TM Example 1, (page 389 in SDTMIG):
CT_TRIAL_DISEASE_MILESTONE_MATRIX = {"domain": "TM", "milestones": [
	{"midstype": "DIAGNOSIS", "tmdef": "Initial diagnosis of diabetes, the first time a physician told the subject they had diabetes", "tmrpt": "N"},
	{"midstype": "HYPOGLYCEMIC EVENT", "tmdef": "Hypoglycemic Event, the occurrence of a glucose level below (threshold level)", "tmrpt": "Y"}
]}
#
#
# Trial Inclusion/Exclusion Criteria Matrix
# Source: TI Example 1, (page 391 in SDTMIG):
CT_TRIAL_INCLUSION_EXCLUSION_MATRIX = {"domain": "TI", "criteria": [
	{"ietestcd": "INCL01", "ietest": "Has disease under study", "iecat": "INCLUSION", "iescat": "", "tirl": "..", "tivers": "1"},
	{"ietestcd": "INCL02", "ietest": "Age 21 or greater", "iecat": "INCLUSION", "iescat": "", "tirl": "..", "tivers": "1"},
	{"ietestcd": "EXCL01", "ietest": "Pregnant or lactating", "iecat": "EXCLUSION", "iescat": "", "tirl": "..", "tivers": "1"},
	{"ietestcd": "INCL01", "ietest": "Has disease under study", "iecat": "INCLUSION", "iescat": "", "tirl": "..", "tivers": "2.2"},
	{"ietestcd": "INCL02A", "ietest": "Age 18 or greater", "iecat": "INCLUSION", "iescat": "", "tirl": "..", "tivers": "2.2"},
	{"ietestcd": "EXCL01", "ietest": "Pregnant or lactating", "iecat": "EXCLUSION", "iescat": "", "tirl": "..", "tivers": "2.2"}
]}
#
#
# Trial Summary
CT_TRIAL_SUMMARY_MATRIX = {"domain": "TS", "item": [
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "ADDON", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "AGEMAX", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "AGEMIN", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "LENGTH", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "PLANSUB", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "RANDOM", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "SEXPOP", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "STOPRULE", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "2", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "2", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "2", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "2", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "2", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "3", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "DateDesc1", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "DateDesc1", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""},
	{"tsseq": "1", "tsgrpid": "", "tsparmcd": "", "tsparm": "", "tsval": "", "tsvalnf": "", "tsvalcd": "", "tsvcdref": "", "tsvcdver": ""}
]}

# = = = = Warning! = = = =
# = = = = You should not need to make any changes below this line. = = = = =
#
# Imports Section
import csv
import datetime
import json
import os
import random
import sqlite3
import sys
import uuid
#
try:
	import numpy as np
except ImportError:
	print("Install NumPy: pip3 install numpy")
	sys.exit(1)
#
try:
	import pandas as pd
except ImportError:
	print("Install Pandas: pip3 install pandas")
	print("https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html")
	sys.exit(1)
#
try:
	import xport
	import xport.v56
except ImportError:
	print("Install xport: pip3 install xport")
	print("Source: https://github.com/selik/xport")
	sys.exit(1)
#
def validateJSON(jsonData):
	"""
	This function validates that a JSON string is well-formed.
	Source: https://pynative.com/python-json-validation/
	"""
	try:
		json.loads(jsonData)
	except ValueError as err:
		return False
	return True
#

#
# QA: Validate JSON is well-formed first. <<
if not validateJSON(json.dumps(CT_TRIAL_DESIGN_MATRIX)):
	print ("There is an error in the JSON definition of the Trial Design Matrix.")
	print ("Please validate your JSON code here: https://jsonlint.com/?code=")
	sys.exit(1)
#
elif not validateJSON(json.dumps(CT_TRIAL_VISIT_MATRIX)):
	print ("There is an error in the JSON definition of the Trial Visit Matrix.")
	print ("Please validate your JSON code here: https://jsonlint.com/?code=")
	sys.exit(1)
#
elif not validateJSON(json.dumps(CT_TRIAL_DISEASE_ASSESSMENT_MATRIX)):
	print ("There is an error in the JSON definition of the Trial Assessment Matrix.")
	print ("Please validate your JSON code here: https://jsonlint.com/?code=")
	sys.exit(1)
#
elif not validateJSON(json.dumps(CT_TRIAL_DISEASE_MILESTONE_MATRIX)):
	print ("There is an error in the JSON definition of the Trial Disease Milestone Matrix.")
	print ("Please validate your JSON code here: https://jsonlint.com/?code=")
	sys.exit(1)
#
elif not validateJSON(json.dumps(CT_TRIAL_INCLUSION_EXCLUSION_MATRIX)):
	print ("There is an error in the JSON definition of the Trial Inclusion / Exclusion Matrix.")
	print ("Please validate your JSON code here: https://jsonlint.com/?code=")
	sys.exit(1)




#
# = = Create base Pandas DataFrames. = =
# TA - Trial Arms
TA_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'ARMCD': [], 'ARM': [], 'TAETORD': [], 'ETCD': [], 'ELEMENT': [], 'TABRANCH': [], 'TATRANS': [], 'EPOCH': []}
TA_df = pd.DataFrame(data=TA_data)
TA_df.astype(dtype={'TAETORD': np.int32})
if ('TA' in CT_DEBUG):  print (TA_df)
#
# TE - Trial Elements
TE_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'ETCD': [], 'ELEMENT': [], 'TESTRL': [], 'TEENRL': [], 'TEDUR': []}
TE_df = pd.DataFrame(data=TE_data)
if ('TE' in CT_DEBUG):  print (TE_df)
#
# TV - Trial Visits
TV_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'VISITNUM': [], 'VISIT': [], 'VISITDY': [], 'ARMCD': [], 'ARM': [], 'TVSTRL': [], 'TVENRL': []}
TV_df = pd.DataFrame(data=TV_data)
if ('TV' in CT_DEBUG):  print (TV_df)
#
# TD - Trial Disease Assessments
TD_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'TDORDER': [], 'TDANCVAR': [], 'TDSTOFF': [], 'TDTGTPAI': [], 'TDMINPAI': [], 'TDMAXPAI': [], 'TDNUMRPT': []}
TD_df = pd.DataFrame(data=TD_data)
if ('TD' in CT_DEBUG):  print (TD_df)
#
# TM - Trial Disease Milestones
TM_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'MIDSTYPE': [], 'TMDEF': [], 'TMRPT': []}
TM_df = pd.DataFrame(data=TM_data)
if ('TM' in CT_DEBUG):  print (TM_df)
#
# TI - Trial Inclusion/Exclusion Criteria
TI_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'IETESTCD': [], 'IETEST': [], 'IECAT': [], 'IESCAT': [], 'TIRL': [], 'TIVERS': []}
TI_df = pd.DataFrame(data=TI_data)
if ('TI' in CT_DEBUG):  print (TI_df)
#
# TS - Trial Summary
TS_data = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'TSSEQ': [], 'TSGRPID': [], 'TSPARMCD': [], 'TSPARM': [], 'TSVAL': [], 'TSVALNF': [], 'TSVALCD': [], 'TSVCDREF': [], 'TSVCDVER': []}
TS_df = pd.DataFrame(data=TS_data)
if ('TS' in CT_DEBUG):  print (TS_df)





# = = Process TA = =
var_domain_ta = CT_TRIAL_DESIGN_MATRIX['domain']
var_number_arms = len(CT_TRIAL_DESIGN_MATRIX['tdm'])
if (2 in CT_DEBUG):
	print ("\n\nThere is(are) %d Arm(s) defined for this trial." % (var_number_arms))
#
# Loop through each available Arm:
var_counter_rows = 1
var_counter_arms = 0			# Reset counter.
while var_counter_arms < var_number_arms:
	var_ta_arm = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['arm']
	var_ta_armcd = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['armcd']
	if (2 in CT_DEBUG):
		print ("\n\tProcessing Arm [%s] : [%s]" % (var_ta_arm, var_ta_armcd))
	#
	var_counter_epochs = 0
	var_number_epochs = len(CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'])
	if (2 in CT_DEBUG):
		print ("\n\t\tThere is(are) %d Epoch(s) defined for this Arm [%s]" % (var_number_epochs, var_ta_arm))


	# For each Arm, generate a record for each Epoch:
	while var_counter_epochs < var_number_epochs:
		if (2 in CT_DEBUG):
			print ("\n\t\t\tInside Arm [%d] and Epoch [%d]." % (var_counter_arms, var_counter_epochs))
		#
		var_ta_taetord = var_counter_epochs + 1
		#
		var_ta_etcd = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'][var_counter_epochs]['etcd']
		var_ta_element = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'][var_counter_epochs]['element']
		var_ta_tabranch = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'][var_counter_epochs]['tabranch']
		var_ta_tatrans = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'][var_counter_epochs]['tatrans']
		var_ta_epoch = CT_TRIAL_DESIGN_MATRIX['tdm'][var_counter_arms]['epochs'][var_counter_epochs]['epoch']
		#
		# Insert rows to DataFrame:
		TA_new_row = {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_ta, 'ARMCD': var_ta_armcd, 'ARM': var_ta_arm, 'TAETORD': var_ta_taetord, 'ETCD': var_ta_etcd, 'ELEMENT': var_ta_element, 'TABRANCH': var_ta_tabranch, 'TATRANS': var_ta_tatrans, 'EPOCH': var_ta_epoch}
		TA_df = TA_df.append(TA_new_row, ignore_index=True)
		#
		var_counter_rows += 1
		#
		var_counter_epochs += 1
	
	var_counter_arms += 1


# = = Process TE = =
# TE – Description/Overview
# A trial design domain that contains the element code that is unique for each element, the element description, and the rules for starting and ending an element.
# The Trial Elements (TE) dataset contains the definitions of the Elements that appear in the Trial Arms (TA) dataset. An Element may appear multiple times in the Trial Arms table because it appears either 1) in multiple Arms, 2) multiple times within an Arm, or 3) both. However, an Element will appear only once in the Trial Elements table."
#
# Process
# a.) Identify distinct Elements in the Trial Design Matrix
# 	* Make a copy of the TA_df DataFrame.
temp_TA_df = TA_df.copy(deep=True)
# 	* Drop a few columns: 
# 	TA = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'ARMCD': [], 'ARM': [], 'TAETORD': [], 'ETCD': [], 'ELEMENT': [], 'TABRANCH': [], 'TATRANS': [], 'EPOCH': []}
# 	TE = {'Row': [], 'STUDYID': [], 'DOMAIN': [], 'ETCD': [], 'ELEMENT': [], 'TESTRL': [], 'TEENRL': [], 'TEDUR': []}
temp_TA_df = temp_TA_df.drop(columns=['DOMAIN', 'ARMCD', 'ARM', 'TAETORD', 'TABRANCH', 'TATRANS', 'EPOCH'])

# 	* Identify unique rows
temp_TA_df = temp_TA_df.drop_duplicates(subset=['ETCD', 'ELEMENT'], keep='last')
#
var_number_temp_TA_rows = len(temp_TA_df)	# Number of distinct rows in Data Frame.
#
if ('TE' in CT_DEBUG): print(temp_TA_df)
#
# 	* Collect new values, transfer to TE DataFrame.
# 	Now, cycle through each distinct TA row:
var_counter_temp_TA = 1
while var_counter_temp_TA < var_number_temp_TA_rows:
	#
	var_te_etcd = temp_TA_df.iloc[var_counter_temp_TA]['ETCD']
	var_te_element = temp_TA_df.iloc[var_counter_temp_TA]['ELEMENT']
	#
	# b.) For each unique Element, ask User to enter additional fields:
	print ("\nPlease enter the following values for ETCD = [%s] and ELEMENT = [%s]:" % (var_te_etcd, var_te_element))
	var_TESTRL = input('Rule for Start of Element: ')	# Expresses rule for beginning Element.
	var_TEENRL = input('Rule for End of Element: ')		# Expresses rule for ending Element. Either TEENRL or TEDUR must be present for each Element.
	var_TEDUR = input('Planned Duration of Element: ')	# Planned Duration of Element in ISO 8601 format. Used when the rule for ending the Element is applied after a fixed duration.
	#
	# c.) Write row to DataFrame:
	TE_new_row = {'Row': var_counter_temp_TA, 'STUDYID': CT_STUDYID, 'DOMAIN': 'TE', 'ETCD': var_te_etcd, 'ELEMENT': var_te_element, 'TESTRL': var_TESTRL, 'TEENRL': var_TEENRL, 'TEDUR': var_TEDUR}
	TE_df = TE_df.append(TE_new_row, ignore_index=True)
	#
	var_counter_temp_TA += 1


# = = Process TV = =
# Although the general structure of the Trial Visits dataset is "One Record per Planned Visit per Arm", for many clinical trials, particularly blinded clinical trials, the schedule of Visits is the same for all Arms, and the structure of the Trial Visits dataset will be "One Record per Planned Visit"
var_domain_tv = CT_TRIAL_VISIT_MATRIX['domain']
var_number_visits = len(CT_TRIAL_VISIT_MATRIX['visits'])
if (2 in CT_DEBUG):
	print ("\n\nThere is(are) %d Visit(s) defined for this trial." % (var_number_visits))
#
# Loop through each available Visit:
var_counter_rows = 1
var_counter_visits = 0
while var_counter_visits < var_number_visits:
	var_tv_visitnum = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['visitnum']
	var_tv_visit = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['visit']
	var_tv_visitdy = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['visitdy']
	var_tv_armcd = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['armcd']
	var_tv_arm = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['arm']
	var_tv_tvstrl = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['tvstrl']
	var_tv_tvenrl = CT_TRIAL_VISIT_MATRIX['visits'][var_counter_visits]['tvenrl']
	#
	if ('TV' in CT_DEBUG):
		print ("\n\tProcessing Visit [%s] : [%s]" % (var_tv_visitnum, var_tv_visit))
	#
	# Insert rows to DataFrame:
	TV_new_row =  {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_tv, 'VISITNUM': var_counter_visits, 'VISIT': var_tv_visit, 'VISITDY': var_tv_visitdy, 'ARMCD': var_tv_armcd, 'ARM': var_tv_arm, 'TVSTRL': var_tv_tvstrl, 'TVENRL': var_tv_tvenrl}
	TV_df = TV_df.append(TV_new_row, ignore_index=True)
	#
	var_counter_visits += 1
	var_counter_rows += 1


# = = Process TD = =
var_domain_td = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['domain']
var_number_assessments = len(CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'])
if (2 in CT_DEBUG):
	print ("\n\nThere is(are) %d Assessment(s) defined for this trial." % (var_number_assessments))
#
# Loop through each available Assesment:
var_counter_rows = 1
var_counter_assessments = 0
while var_counter_assessments < var_number_assessments:
	var_tv_tdorder = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdorder']
	var_tv_tdancvar = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdancvar']
	var_tv_tdstoff = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdstoff']
	var_tv_tdtgtpai = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdtgtpai']
	var_tv_tdminpai = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdminpai']
	var_tv_tdmaxpai = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdmaxpai']
	var_tv_tdnumrpt = CT_TRIAL_DISEASE_ASSESSMENT_MATRIX['assessments'][var_counter_assessments]['tdnumrpt']
	#
	if ('TD' in CT_DEBUG):
		print ("\n\tProcessing Assessment [%s] : [%s]" % (var_tv_visitnum, var_tv_visit))
	#
	# Insert rows to DataFrame:
	TD_new_row =  {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_td, 'TDORDER': var_tv_tdorder, 'TDANCVAR': var_tv_tdancvar, 'TDSTOFF': var_tv_tdstoff, 'TDTGTPAI': var_tv_tdtgtpai, 'TDMINPAI': var_tv_tdminpai, 'TDMAXPAI': var_tv_tdmaxpai, 'TDNUMRPT': var_tv_tdnumrpt}
	TD_df = TD_df.append(TD_new_row, ignore_index=True)
	#
	var_counter_assessments += 1
	var_counter_rows += 1


# = = Process TM = =
var_domain_tm = CT_TRIAL_DISEASE_MILESTONE_MATRIX['domain']
var_number_milestones = len(CT_TRIAL_DISEASE_MILESTONE_MATRIX['milestones'])
if ('TM' in CT_DEBUG):
	print ("\n\nThere is(are) %d Milestone(s) defined for this trial." % (var_number_milestones))
#
# Loop through each available Milestone:
var_counter_rows = 1
var_counter_milestones = 0
while var_counter_milestones < var_number_milestones:
	var_tm_midstype = CT_TRIAL_DISEASE_MILESTONE_MATRIX['milestones'][var_counter_milestones]['midstype']
	var_tm_tmdef = CT_TRIAL_DISEASE_MILESTONE_MATRIX['milestones'][var_counter_milestones]['tmdef']
	var_tm_tmrpt = CT_TRIAL_DISEASE_MILESTONE_MATRIX['milestones'][var_counter_milestones]['tmrpt']
	#
	if ('TM' in CT_DEBUG):
		print ("\n\tProcessing Disease Milestone [%s]" % (var_tm_midstype))
	#
	# Insert rows to DataFrame:
	TM_new_row =  {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_tm, 'MIDSTYPE': var_tm_midstype, 'TMDEF': var_tm_tmdef, 'TMRPT': var_tm_tmrpt}
	TM_df = TM_df.append(TM_new_row, ignore_index=True)
	#
	var_counter_milestones += 1
	var_counter_rows += 1


# = = Process TI = =
var_domain_ti = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['domain']
var_number_criteria = len(CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'])
if ('TI' in CT_DEBUG):
	print ("\n\nThere is(are) %d Inclusion / Exclusion Criteria defined for this trial." % (var_number_criteria))
#
# Loop through each available Inclusion / Exclusion Criteria:
var_counter_rows = 1
var_counter_criteria = 0
while var_counter_criteria < var_number_criteria:
	var_ti_ietestcd = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['ietestcd']
	var_ti_ietest = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['ietest']
	var_ti_iecat = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['iecat']
	var_ti_iescat = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['iescat']
	var_ti_tirl = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['tirl']
	var_ti_tivers = CT_TRIAL_INCLUSION_EXCLUSION_MATRIX['criteria'][var_counter_criteria]['tivers']
	#
	if ('TD' in CT_DEBUG):
		print ("\n\tProcessing Inclusion / Exclusion Criteria [%s] : [%s]" % (var_tv_visitnum, var_tv_visit))
	#
	# Insert rows to DataFrame:
	TI_new_row =  {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_ti, 'IETESTCD': var_ti_ietestcd, 'IETEST': var_ti_ietest, 'IECAT': var_ti_iecat, 'IESCAT': var_ti_iescat, 'TIRL': var_ti_tirl, 'TIVERS': var_ti_tivers}
	TI_df = TI_df.append(TI_new_row, ignore_index=True)
	#
	var_counter_criteria += 1
	var_counter_rows += 1


# = = Process TS = =
"""
TSSEQ
TSGRPID
TSPARMCD
TSPARM
TSVAL
TSVALNF
TSVALCD
TSVCDREF
TSVCDVER
"""





"""

var_domain_<..> = CT_<..>_MATRIX['domain']
var_number_<..> = len(CT_<..>_MATRIX['visits'])
if ('<Domain>' in CT_DEBUG):
	print ("\n\nThere is(are) %d <..> (s) defined for this trial." % (var_number_<..>))
#
# Loop through each available <..>:
var_counter_rows = 1
var_counter_<..> = 0
while var_counter_<..> < var_number_<..>:
	var_<Domain>_<..> = CT_<..>_MATRIX['assessments'][var_counter_<..>]['<..>']
	#
	if ('TD' in CT_DEBUG):
		print ("\n\tProcessing Visit [%s] : [%s]" % (var_tv_visitnum, var_tv_visit))
	#
	# Insert rows to DataFrame:
	TD_new_row =  {'Row': var_counter_rows, 'STUDYID': CT_STUDYID, 'DOMAIN': var_domain_<..>, ...}
	TD_df = TV_df.append(TD_new_row, ignore_index=True)
	#
	var_counter_<..> += 1
	var_counter_rows += 1

"""


#
# = Generate SAS files: = =
# Source: https://github.com/selik/xport
# The SAS Transport (XPORT) format only supports two kinds of data. Each value is either numeric or character, so xport.load decodes the values as either str or float.
#
# TA:
TA_ds = xport.Dataset(TA_df, name='TA', label='Trial Arms (TA) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TA_ds = TA_ds.rename(columns={k: k.upper()[:8] for k in TA_ds})
# Libraries can have multiple datasets.
TA_library = xport.Library({'TA': TA_ds})
#
with open('TA.xpt', 'wb') as f:
	xport.v56.dump(TA_library, f)
#
# TE:
TE_ds = xport.Dataset(TE_df, name='TE', label='Trial Elements (TE) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TE_ds = TE_ds.rename(columns={k: k.upper()[:8] for k in TE_ds})
# Libraries can have multiple datasets.
TE_library = xport.Library({'TE': TE_ds})
#
with open('TE.xpt', 'wb') as f:
	xport.v56.dump(TE_library, f)
#
# TV:
TV_ds = xport.Dataset(TV_df, name='TV', label='Trial Visits (TV) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TV_ds = TV_ds.rename(columns={k: k.upper()[:8] for k in TV_ds})
# Libraries can have multiple datasets.
TV_library = xport.Library({'TV': TV_ds})
#
with open('TV.xpt', 'wb') as f:
	xport.v56.dump(TV_library, f)
#
# TD:
TD_ds = xport.Dataset(TD_df, name='TD', label='Trial Disease Assessments (TD) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TD_ds = TD_ds.rename(columns={k: k.upper()[:8] for k in TD_ds})
# Libraries can have multiple datasets.
TD_library = xport.Library({'TD': TD_ds})
#
with open('TD.xpt', 'wb') as f:
	xport.v56.dump(TD_library, f)
#
# TM:
TM_ds = xport.Dataset(TM_df, name='TM', label='Trial Disease Milestones (TM) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TM_ds = TM_ds.rename(columns={k: k.upper()[:8] for k in TM_ds})
# Libraries can have multiple datasets.
TM_library = xport.Library({'TM': TM_ds})
#
with open('TM.xpt', 'wb') as f:
	xport.v56.dump(TM_library, f)
#
# TI:
TI_ds = xport.Dataset(TI_df, name='TI', label='Trial Inc/Exc Criteria (TI) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TI_ds = TI_ds.rename(columns={k: k.upper()[:8] for k in TI_ds})
# Libraries can have multiple datasets.
TI_library = xport.Library({'TI': TI_ds})
#
with open('TI.xpt', 'wb') as f:
	xport.v56.dump(TI_library, f)
#
# TS:
TS_ds = xport.Dataset(TS_df, name='TS', label='Trial Summary (TS) data')
# SAS variable names are limited to 8 characters. As with Pandas dataframes, you must change the name on the dataset rather than the column directly.
TS_ds = TS_ds.rename(columns={k: k.upper()[:8] for k in TS_ds})
# Libraries can have multiple datasets.
TS_library = xport.Library({'TS': TS_ds})
#
with open('TS.xpt', 'wb') as f:
	xport.v56.dump(TS_library, f)

#
# = = Clean up. = =
print("\n\nThis is the end, Beautiful friend. This is the end. My only friend, the end")