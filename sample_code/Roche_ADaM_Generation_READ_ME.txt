(c) 2007-2020 NIHPO, ,Inc.   http://NIHPO.com   Contact: Jose.Lacal@NIHPO.com
Filename: Roche_ADaM_Generation_READ_ME.txt
Purpose: Instructions for using the 'Roche_ADaM_Generation.py' Python script to generate realistic yet fake ADaM data using Roche's sample spreadsheet.
Version: Tuesday 07 July 2020.

License:
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
* You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
 



User-configured variables.

You can manually configure these variables in the Python script to best fit your analysis:

These variables are configured at run time:
* Number of Subjects.
* Date of enrollment start
* Date when the files are generated (used for estimating visit and death dates).


These variables are defined in the script itself:
* Percentage Female / Male split.
* Minimum and maximum inclusion ages.
* Race splits : 'AMERICAN INDIAN OR ALASKA NATIVE', 'ASIAN', 'BLACK OR AFRICAN AMERICAN', 'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER', 'WHITE', 'NOT REPORTED', 'UNKNOWN'.
* Ethnicity split ('Hispanic' or 'Non-Hispanic').

Structure of trial:
* Define number of Visits.
  * For each Visit, define number of Analysis.
    * For each Analysis, define number of Parameters.
      * For each Parameter: define Lower value, Upper value, and Fuzz factor.

* Arm identifiers. Assign Subjects by percentage of total enrollment to each arm. 
* Group identifiers. Assign Subjects by percentage of total enrollment to each group. 
* Site identifiers. Assign Subjects by percentage of total enrollment to each site.
* Investigator identifiers. Assign Subjects by percentage of total enrollment to each investigator.

* Percentage deaths.
* Causes of death (by percentages).
* Percentage of subjects that do not finish all phases of the trial.
* Percentage of subjects that experience at least 01 adverse event.
* Country enrollment. Assign Subjects by percentage of total enrollment to each country.




The SQLite3 database file contains the following "Controlled Terms" used throughout the output files.

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
C102580 | "Laboratory Test Standard Character Result" | 06
C124296 | "Subject Trial Status" | 03




Files generated:
* ADSL: 01 record per Subject.
* ADAE: 01 record if Subject suffers and Adverse Event.
* ADLB: 01 record per subject per parameter per analysis visit per analysis date.
* ADHY: 01 record per subject per parameter per analysis visit per analysis date.
* ADSAFTTE: 01 record per subject per parameter per analysis visit per analysis date.


Pending Work:
* Fields where the content looks like "-LBDY-" need work (I'm not sure how to populate this field yet).



Open Questions

01. Do I need to generate a "Baseline" record for each Subject? Including (random) starting values for all Parameters addressed in each Analysis.
Then, during each Visit, Parameters are randomly generated for the visit and compared against the Baseline.

02. Create an in-memory dictionary:
Dates
* Enrollment
* Each Visit
* Date results are available
* Relative Day (since start of participation)

Parameter:
* Baseline value
* Measure (each Visit)
* Compare measure with Baseline
