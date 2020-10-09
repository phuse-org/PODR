-- Filename: TDF_SDTM.sqlite
-- Author: Jose.Lacal@NIHPO.com
-- Purpose: This SQL script creates tables in an SQLite3 file used to generate synthethic CDISC data. 
-- Version: Thu 24 September 2020.
--
-- This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
-- This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
-- You should have received a copy of the GNU General Public License along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html
/*
Reference:

Study Data Tabulation Model Implementation Guide: Human Clinical Trials Version 3.3 (Final)
https://www.cdisc.org/standards/foundational/sdtmig/sdtmig-v3-3/html

Based on TDF meeting minutes from Aug. 14, 2020
https://github.com/phuse-org/TestDataFactory/tree/master/Minutes
*/
--
-- This table defines the processing rules for each domain.
DROP TABLE IF EXISTS cdisc_sdtm_domain_rules;
CREATE TABLE cdisc_sdtm_domain_rules (
	domain_code text,
	per_trial text,
	per_subject text,
	per_arm text,
	per_visit text,
	per_visit_measurement text,
	per_adverse_event text,
	per_concomitant_prior text);
--
/*
ae.xpt, Adverse Events — Events, Version 3.3. One record per adverse event per subject, Tabulation.
cm.xpt, Concomitant/Prior Medications — Interventions, Version 3.3. One record per recorded intervention occurrence or constant-dosing interval per subject, Tabulation.
dm.xpt, Demographics — Special Purpose, Version 3.3. One record per subject, Tabulation.
ds.xpt, Disposition — Events, Version 3.3. One record per disposition status or protocol milestone per subject, Tabulation.
ex.xpt, Exposure — Interventions, Version 3.3. One record per protocol-specified study treatment, constant-dosing interval, per subject, Tabulation.
lb.xpt, Laboratory Test Results — Findings, Version 3.3. One record per lab test per time point per visit per subject, Tabulation.
mh.xpt, Medical History — Events, Version 3.3. One record per medical history event per subject, Tabulation.
ta.xpt, Trial Arms — Trial Design, Version 3.3. One record per planned Element per Arm, Tabulation.
ts.xpt, Trial Summary Information — Trial Design, Version 3.2. One record per trial summary parameter value, Tabulation.
tv.xpt, Trial Visits — Trial Design, Version 3.2. One record per planned Visit per Arm, Tabulation.
vs.xpt, Vital Signs — Findings, Version 3.3. One record per vital sign measurement per time point per visit per subject, Tabulation.
*/
#
# This table definition maps out 
INSERT INTO cdisc_sdtm_domain_rules (domain_code, per_trial, per_subject, per_arm, per_visit, per_visit_measurement, per_adverse_event, per_concomitant_prior) VALUES 
('AE', '0', '1', '0', '0', '0', '1', '0'),
('CM', '0', '1', '0', '0', '0', '0', '1'),
('DM', '0', '1', '0', '0', '0', '0', '0'),
('DS', '0', '1', '0', '0', '0', '0', '0'),
('EX', '0', '1', '1', '1', '0', '0', '0'),
('LB', '0', '1', '1', '1', '1', '0', '0'),
('MH', '0', '1', '0', '0', '0', '0', '0'),
('TA', '0', '0', '1', '0', '0', '0', '0'),
('TS', '1', '0', '0', '0', '0', '0', '0'),
('TV', '0', '1', '1', '1', '0', '0', '0'),
('VS', '0', '1', '0', '1', '1', '0', '0')
;
--
--
-- This table defines the CDISC domains of interest:
DROP TABLE IF EXISTS cdisc_sdtm_domain_definitions;
CREATE TABLE cdisc_sdtm_domain_definitions (
	domain_code text,
	variable_name text,
	variable_label text,
	type text,
	controlled_terms text,
	role text,
	cdisc_notes text,
	core text);
--
-- Domain: AE
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('AE', 'AEACN','Action Taken with Study Treatment', 'Char', '(ACN)', 'Record Qualifier', 'Describes changes to the study treatment as a result of the event. AEACN is specifically for the relationship to study treatment. AEACNOTH is for actions unrelated to dose adjustments of study treatment. Examples of AEACN values include ICH E2B values: "DRUG WITHDRAWN", "DOSE REDUCED", "DOSE INCREASED", "DOSE NOT CHANGED", "UNKNOWN" or "NOT APPLICABLE".', 'Exp'),
('AE', 'AEACNOTH','Other Action Taken', 'Char', '', 'Record Qualifier', 'Describes other actions taken as a result of the event that are unrelated to dose adjustments of study treatment. Usually reported as free text. Example: "TREATMENT UNBLINDED. PRIMARY CARE PHYSICIAN NOTIFIED".', 'Perm'),
('AE', 'AEBDSYCD','Body System or Organ Class Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary derived. Code for the body system or organ class used by the sponsor. When using a multi-axial dictionary such as MedDRA, this should contain the SOC used for the sponsor''s analyses and summary tables, which may not necessarily be the primary SOC.', 'Exp'),
('AE', 'AEBODSYS','Body System or Organ Class', 'Char', '*', 'Record Qualifier', 'Dictionary derived. Body system or organ class used by the sponsor from the coding dictionary (e.g., MedDRA). When using a multi-axial dictionary such as MedDRA, this should contain the SOC used for the sponsor''s analyses and summary tables, which may not necessarily be the primary SOC.', 'Exp'),
('AE', 'AECAT','Category for Adverse Event', 'Char', '*', 'Grouping Qualifier', 'Used to define a category of related records. Example: "BLEEDING", "NEUROPSYCHIATRIC".', 'Perm'),
('AE', 'AECONTRT','Concomitant or Additional Trtmnt Given', 'Char', '(NY)', 'Record Qualifier', 'Was another treatment given because of the occurrence of the event? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AEDECOD','Dictionary-Derived Term', 'Char', 'MedDRA', 'Synonym Qualifier', 'Dictionary-derived text description of AETERM or AEMODIFY. Equivalent to the Preferred Term (PT in MedDRA). The sponsor is expected to provide the dictionary name and version used to map the terms utilizing the external codelist element in the Define-XML document.', 'Req'),
('AE', 'AEDUR','Duration of Adverse Event', 'Char', 'ISO 8601', 'Timing', 'Collected duration and unit of an adverse event. Used only if collected on the CRF and not derived from start and end date/times. Example: "P1DT2H" (for 1 day, 2 hours).', 'Perm'),
('AE', 'AEENDTC','End Date/Time of Adverse Event', 'Char', 'ISO 8601', 'Timing', 'End date/time of the adverse event represented in ISO 8601 character format.', 'Exp'),
('AE', 'AEENDY','Study Day of End of Adverse Event', 'Num', '', 'Timing', 'Study day of end of event relative to the sponsor-defined RFSTDTC.', 'Perm'),
('AE', 'AEENRF','End Relative to Reference Period', 'Char', '(STENRF)', 'Timing', 'Describes the end of the event relative to the sponsor-defined reference period. The sponsor-defined reference period is a continuous period of time defined by a discrete starting point (RFSTDTC) and a discrete ending point (RFENDTC) of the trial. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.','Perm'),
('AE', 'AEENRTPT','End Relative to Reference Time Point', 'Char', '(STENRF)', 'Timing', 'Identifies the end of the event as being before or after the reference time point defined by variable AEENTPT. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.','Perm'),
('AE', 'AEENTPT','End Reference Time Point', 'Char', '', 'Timing', 'Description of date/time in ISO 8601 character format of the reference point referred to by AEENRTPT. Examples: "2003-12-25" or "VISIT 2".', 'Perm'),
('AE', 'AEGRPID','Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('AE', 'AEHLGT','High Level Group Term', 'Char', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived text description of the High Level Group Term for the primary System Organ Class.', 'Exp'),
('AE', 'AEHLGTCD','High Level Group Term Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived code for the High Level Group Term for the primary System Organ Class.', 'Exp'),
('AE', 'AEHLT','High Level Term', 'Char', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived text description of the High Level Term for the primary System Organ Class.', 'Exp'),
('AE', 'AEHLTCD','High Level Term Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived code for the High Level Term for the primary System Organ Class.', 'Exp'),
('AE', 'AELLT','Lowest Level Term', 'Char', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived text description of the Lowest Level Term.', 'Exp'),
('AE', 'AELLTCD','Lowest Level Term Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived code for the Lowest Level Term.', 'Exp'),
('AE', 'AELOC','Location of Event', 'Char', '(LOC)', 'Record Qualifier', 'Describes anatomical location relevant for the event (e.g., "ARM" for skin rash).', 'Perm'),
('AE', 'AEMODIFY','Modified Reported Term', 'Char', '', 'Synonym Qualifier', 'If AETERM is modified to facilitate coding, then AEMODIFY will contain the modified text.', 'Perm'),
('AE', 'AEOUT','Outcome of Adverse Event', 'Char', '(OUT)', 'Record Qualifier', 'Description of the outcome of an event.', 'Perm'),
('AE', 'AEPATT','Pattern of Adverse Event', 'Char', '*', 'Record Qualifier', 'Used to indicate the pattern of the event over time. Examples: "INTERMITTENT", "CONTINUOUS", "SINGLE EVENT".', 'Perm'),
('AE', 'AEPRESP','Pre-Specified Adverse Event', 'Char', '(NY)', 'Variable Qualifier', 'A value of "Y" indicates that this adverse event was pre-specified on the CRF. Values are null for spontaneously reported events (i.e., those collected as free-text verbatim terms).', 'Perm'),
('AE', 'AEPTCD','Preferred Term Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived code for the Preferred Term.', 'Exp'),
('AE', 'AEREFID','Reference ID', 'Char', '', 'Identifier', 'Internal or external identifier such as a serial number on an SAE reporting form.', 'Perm'),
('AE', 'AEREL','Causality', 'Char', '*', 'Record Qualifier', 'Records the investigator''s opinion as to the causality of the event to the treatment. ICH E2A and E2B examples include "NOT RELATED", "UNLIKELY RELATED", "POSSIBLY RELATED", "RELATED". Controlled Terminology may be defined in the future. Check with regulatory authority for population of this variable.', 'Exp'),
('AE', 'AERELNST','Relationship to Non-Study Treatment', 'Char', '', 'Record Qualifier', 'Records the investigator''s opinion as to whether the event may have been due to a treatment other than study drug. May be reported as free text. Example: "MORE LIKELY RELATED TO ASPIRIN USE".', 'Perm'),
('AE', 'AESCAN','Involves Cancer', 'Char', '(NY)', 'Record Qualifier', 'Was the serious event associated with the development of cancer? Valid values are "Y" and "N". This is a legacy seriousness criterion. It is not included in ICH E2A.', 'Perm'),
('AE', 'AESCAT','Subcategory for Adverse Event', 'Char', '*', 'Grouping Qualifier', 'A further categorization of adverse event. Example: "NEUROLOGIC".', 'Perm'),
('AE', 'AESCONG','Congenital Anomaly or Birth Defect', 'Char', '(NY)', 'Record Qualifier', 'Was the serious event associated with congenital anomaly or birth defect? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESDISAB','Persist or Signif Disability/Incapacity', 'Char', '(NY)', 'Record Qualifier', 'Did the serious event result in persistent or significant disability/incapacity? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESDTH','Results in Death', 'Char', '(NY)', 'Record Qualifier', 'Did the serious event result in death? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESEQ','Sequence Number', 'Num', '', 'Identifier', 'Sequence number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('AE', 'AESER','Serious Event', 'Char', '(NY)', 'Record Qualifier', 'Is this a serious event? Valid values are "Y" and "N".', 'Exp'),
('AE', 'AESEV','Severity/Intensity', 'Char', '(AESEV)', 'Record Qualifier', 'The severity or intensity of the event. Examples: "MILD", "MODERATE", "SEVERE".', 'Perm'),
('AE', 'AESHOSP','Requires or Prolongs Hospitalization', 'Char', '(NY)', 'Record Qualifier', 'Did the serious event require or prolong hospitalization? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESLIFE','Is Life Threatening', 'Char', '(NY)', 'Record Qualifier', 'Was the serious event life threatening? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESMIE','Other Medically Important Serious Event', 'Char', '(NY)', 'Record Qualifier', 'Do additional categories for seriousness apply? Valid values are "Y" and "N".', 'Perm'),
('AE', 'AESOC','Primary System Organ Class', 'Char', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived text description of the primary System Organ Class. Will be the same as AEBODSYS if the primary SOC was used for analysis.', 'Exp'),
('AE', 'AESOCCD','Primary System Organ Class Code', 'Num', 'MedDRA', 'Variable Qualifier', 'Dictionary-derived code for the primary System Organ Class. Will be the same as AEBDSYCD if the primary SOC was used for analysis.', 'Exp'),
('AE', 'AESOD','Occurred with Overdose', 'Char', '(NY)', 'Record Qualifier', 'Did the serious event occur with an overdose? Valid values are "Y" and "N". This is a legacy seriousness criterion. It is not included in ICH E2A.', 'Perm'),
('AE', 'AESPID','Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined identifier. It may be preprinted on the CRF as an explicit line identifier or defined in the sponsor''s operational database. Example: Line number on an Adverse Events page.', 'Perm'),
('AE', 'AESTDTC','Start Date/Time of Adverse Event', 'Char', 'ISO 8601', 'Timing', 'Start date/time of the adverse event represented in ISO 8601 character format.', 'Exp'),
('AE', 'AESTDY','Study Day of Start of Adverse Event', 'Num', '', 'Timing', 'Study day of start of adverse event relative to the sponsor-defined RFSTDTC.', 'Perm'),
('AE', 'AETERM','Reported Term for the Adverse Event', 'Char', '', 'Topic', 'Verbatim name of the event.', 'Req'),
('AE', 'AETOXGR','Standard Toxicity Grade', 'Char', '*', 'Record Qualifier', 'Toxicity grade according to a standard toxicity scale such as Common Terminology Criteria for Adverse Events v3.0 (CTCAE). Sponsor should specify name of the scale and version used in the metadata (see Assumption 6d). If value is from a numeric scale, represent only the number (e.g., "2" and not "Grade 2").', 'Perm'),
('AE', 'DOMAIN','Domain Abbreviation', 'Char', 'AE', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('AE', 'EPOCH','Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time of the adverse event. Examples: "SCREENING", "TREATMENT", "FOLLOW-UP".', 'Perm'),
('AE', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('AE', 'TAETORD','Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm.', 'Perm'),
('AE', 'USUBJID','Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req')
;
--
-- Domain: CM
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('CM', 'CMADJ', 'Reason for Dose Adjustment', 'Char', '', 'Record Qualifier', 'Describes reason or explanation of why a dose is adjusted. Examples: "ADVERSE EVENT", "INSUFFICIENT RESPONSE", "NON-MEDICAL REASON".', 'Perm'),
('CM', 'CMCAT', 'Category for Medication', 'Char', '', 'Grouping Qualifier', 'Used to define a category of medications/treatment. Examples: "PRIOR", "CONCOMITANT", "ANTI-CANCER MEDICATION", or "GENERAL CONMED".', 'Perm'),
('CM', 'CMCLAS', 'Medication Class', 'Char', '', 'Variable Qualifier', 'Drug class. May be obtained from coding. When coding to a single class, populate with class value. If using a dictionary and coding to multiple classes, then follow Section 4.2.8.3, Multiple Values for a Non-Result Qualifier Variable, or omit CMCLAS.', 'Perm'),
('CM', 'CMCLASCD', 'Medication Class Code', 'Char', '', 'Variable Qualifier', 'Class code corresponding to CMCLAS. Drug class. May be obtained from coding. When coding to a single class, populate with class code. If using a dictionary and coding to multiple classes, then follow Section 4.2.8.3, Multiple Values for a Non-Result Qualifier Variable, or omit CMCLASCD.', 'Perm'),
('CM', 'CMDECOD', 'Standardized Medication Name', 'Char', '', 'Synonym Qualifier', 'Standardized or dictionary-derived text description of CMTRT or CMMODIFY. Equivalent to the generic drug name in WHO Drug. The sponsor is expected to provide the dictionary name and version used to map the terms utilizing the external codelist element in the Define-XML document. If an intervention term does not have a decode value in the dictionary, then CMDECOD will be left blank.', 'Perm'),
('CM', 'CMDOSE', 'Dose per Administration', 'Num', '', 'Record Qualifier', 'Amount of CMTRT given. Not populated when CMDOSTXT is populated.', 'Perm'),
('CM', 'CMDOSFRM', 'Dose Form', 'Char', '(FRM)', 'Variable Qualifier', 'Dose form for CMTRT. Examples: "TABLET", "LOTION".', 'Perm'),
('CM', 'CMDOSFRQ', 'Dosing Frequency per Interval', 'Char', '(FREQ)', 'Variable Qualifier', 'Usually expressed as the number of repeated administrations of CMDOSE within a specific time period. Examples: "BID" (twice daily), "Q12H" (every 12 hours).', 'Perm'),
('CM', 'CMDOSRGM', 'Intended Dose Regimen', 'Char', '', 'Variable Qualifier', 'Text description of the (intended) schedule or regimen for the Intervention. Example: "TWO WEEKS ON, TWO WEEKS OFF".', 'Perm'),
('CM', 'CMDOSTOT', 'Total Daily Dose', 'Num', '', 'Record Qualifier', 'Total daily dose of CMTRT using the units in CMDOSU. Used when dosing is collected as Total Daily Dose. Total dose over a period other than day could be recorded in a separate Supplemental Qualifier variable.', 'Perm'),
('CM', 'CMDOSTXT', 'Dose Description', 'Char', '', 'Record Qualifier', 'Dosing amounts or a range of dosing information collected in text form. Units may be stored in CMDOSU. Examples: "200-400", "15-20". Not populated when CMDOSE is populated.', 'Perm'),
('CM', 'CMDOSU', 'Dose Units', 'Char', '(UNIT)', 'Variable Qualifier', 'Units for CMDOSE, CMDOSTOT, or CMDOSTXT. Examples: "ng", "mg", or "mg/kg".', 'Perm'),
('CM', 'CMDUR', 'Duration', 'Char', 'ISO 8601', 'Timing', 'Collected duration for a treatment episode. Used only if collected on the CRF and not derived from start and end date/times.', 'Perm'),
('CM', 'CMENDTC', 'End Date/Time of Medication', 'Char', 'ISO 8601', 'Timing', 'End date/time of the medication administration represented in ISO 8601 character format.', 'Perm'),
('CM', 'CMENDY', 'Study Day of End of Medication', 'Num', '', 'Timing', 'Study day of end of medication relative to the sponsor-defined RFSTDTC.', 'Perm'),
('CM', 'CMENRF', 'End Relative to Reference Period', 'Char', '(STENRF)', 'Timing', 'Describes the end of the medication relative to the sponsor-defined reference period. The sponsor-defined reference period is a continuous period of time defined by a discrete starting point and a discrete ending point (represented by RFSTDTC and RFENDTC in Demographics). If information such as "PRIOR", "ONGOING, or "CONTINUING" was collected, this information may be translated into CMENRF. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('CM', 'CMENRTPT', 'End Relative to Reference Time Point', 'Char', '(STENRF)', 'Timing', 'Identifies the end of the medication as being before or after the sponsor-defined reference time point defined by variable CMENTPT.	Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('CM', 'CMENTPT', 'End Reference Time Point', 'Char', '', 'Timing', 'Description or date/time in ISO 8601 character format of the sponsor-defined reference point referred to by CMENRTPT. Examples: "2003-12-25" or "VISIT 2".', 'Perm'),
('CM', 'CMGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('CM', 'CMINDC', 'Indication', 'Char', '', 'Record Qualifier', 'Denotes why a medication was taken or administered. Examples: "NAUSEA", "HYPERTENSION".', 'Perm'),
('CM', 'CMMODIFY', 'Modified Reported Name', 'Char', '', 'Synonym Qualifier', 'If CMTRT is modified to facilitate coding, then CMMODIFY will contain the modified text.', 'Perm'),
('CM', 'CMOCCUR', 'CM Occurrence', 'Char', '(NY)', 'Record Qualifier', 'When the use of a specific medication is solicited. CMOCCUR is used to indicate whether or not ("Y"/"N") use of the medication occurred. Values are null for medications not specifically solicited.', 'Perm'),
('CM', 'CMPRESP', 'CM Pre-specified', 'Char', '(NY)', 'Variable Qualifier', 'Used to indicate whether ("Y"/null) information about the use of a specific medication was solicited on the CRF.', 'Perm'),
('CM', 'CMREASND', 'Reason Medication Not Collected', 'Char', '', 'Record Qualifier', 'Reason not done. Used in conjunction with CMSTAT when value is "NOT DONE".', 'Perm'),
('CM', 'CMROUTE', 'Route of Administration', 'Char', '(ROUTE)', 'Variable Qualifier', 'Route of administration for the intervention. Examples: "ORAL", "INTRAVENOUS".', 'Perm'),
('CM', 'CMRSDISC', 'Reason the Intervention Was Discontinued', 'Char', '', 'Record Qualifier', 'When dosing of a treatment is recorded over multiple successive records, this variable is applicable only for the (chronologically) last record for the treatment.', 'Perm'),
('CM', 'CMSCAT', 'Subcategory for Medication', 'Char', '', 'Grouping Qualifier', 'A further categorization of medications/treatment. Examples: "CHEMOTHERAPY", "HORMONAL THERAPY", "ALTERNATIVE THERAPY".', 'Perm'),
('CM', 'CMSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence number to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('CM', 'CMSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Example: a number pre-printed on the CRF as an explicit line identifier or record identifier defined in the sponsor''s operational database. Example: line number on a concomitant medication page.', 'Perm'),
('CM', 'CMSTAT', 'Completion Status', 'Char', '(ND)', 'Record Qualifier', 'Used to indicate that a question about the occurrence of a pre-specified intervention was not answered. Should be null or have a value of "NOT DONE".', 'Perm'),
('CM', 'CMSTDTC', 'Start Date/Time of Medication', 'Char', 'ISO 8601', 'Timing', 'Start date/time of the medication administration represented in ISO 8601 character format.', 'Perm'),
('CM', 'CMSTDY', 'Study Day of Start of Medication', 'Num', '', 'Timing', 'Study day of start of medication relative to the sponsor-defined RFSTDTC.', 'Perm'),
('CM', 'CMSTRF', 'Start Relative to Reference Period', 'Char', '(STENRF)', 'Timing', 'Describes the start of the medication relative to sponsor-defined reference period. The sponsor-defined reference period is a continuous period of time defined by a discrete starting point and a discrete ending point (represented by RFSTDTC and RFENDTC in Demographics). If information such as "PRIOR" was collected, this information may be translated into CMSTRF. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('CM', 'CMSTRTPT', 'Start Relative to Reference Time Point', 'Char', '(STENRF)', 'Timing', 'Identifies the start of the medication as being before or after the sponsor-defined reference time point defined by variable CMSTTPT. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('CM', 'CMSTTPT', 'Start Reference Time Point', 'Char', '', 'Timing', 'Description or date/time in ISO 8601 character format of the sponsor-defined reference point referred to by CMSTRTPT. Examples: "2003-12-15" or "VISIT 1".', 'Perm'),
('CM', 'CMTRT', 'Reported Name of Drug, Med, or Therapy', 'Char', '', 'Topic', 'Verbatim medication name that is either pre-printed or collected on a CRF.', 'Req'),
('CM', 'DOMAIN', 'Domain Abbreviation', 'Char', 'CM', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('CM', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time of the medication administration. Null for medications that started before study participation.', 'Perm'),
('CM', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('CM', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm for the Element in which the medication administration started. Null for medications that started before study participation.', 'Perm'),
('CM', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req')
;
--
-- Domain: DM
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('DM', 'ACTARM', 'Description of Actual Arm', 'Char', '*', 'Synonym Qualifier', 'Description of actual Arm. With the exception of studies which use multi-stage Arm assignments, must be a value of ARM in the Trial Arms Dataset. If the subject was not assigned to an Arm or followed a course not described by any planned Arm, ACTARM is null and ARMNRS is populated.', 'Exp'),
('DM', 'ACTARMCD', 'Actual Arm Code', 'Char', '*', 'Record Qualifier', 'Code of actual Arm. ACTARMCD is limited to 20 characters. It is not subject to the character restrictions that apply to TESTCD. The maximum length of ACTARMCD is longer than for other short variables to accommodate the kind of values that are likely to be needed for crossover trials. With the exception of studies which use multi-stage Arm assignments, must be a value of ARMCD in the Trial Arms Dataset. If the subject was not assigned to an Arm or followed a course not described by any planned Arm, ACTARMCD is null and ARMNRS is populated.', 'Exp'),
('DM', 'ACTARMUD', 'Description of Unplanned Actual Arm', 'Char', '', 'Record Qualifier', 'A description of actual treatment for a subject who did not receive treatment described in one of the planned trial Arms.', 'Exp'),
('DM', 'AGE', 'Age', 'Num', '', 'Record Qualifier', 'Age expressed in AGEU. May be derived from RFSTDTC and BRTHDTC, but BRTHDTC may not be available in all cases (due to subject privacy concerns).', 'Exp'),
('DM', 'AGEU', 'Age Units', 'Char', '(AGEU)', 'Variable Qualifier', 'Units associated with AGE.', 'Exp'),
('DM', 'ARM', 'Description of Planned Arm', 'Char', '*', 'Synonym Qualifier', 'Name of the Arm to which the subject was assigned. If the subject was not assigned to an Arm, ARM is null and ARMNRS is populated. With the exception of studies which use multi-stage Arm assignments, must be a value of ARM in the Trial Arms Dataset.', 'Exp'),
('DM', 'ARMCD', 'Planned Arm Code', 'Char', '*', 'Record Qualifier', 'ARMCD is limited to 20 characters. It is not subject to the character restrictions that apply to TESTCD.The maximum length of ARMCD is longer than for other "short" variables to accommodate the kind of values that are likely to be needed for crossover trials. For example, if ARMCD values for a seven-period crossover were constructed using two-character abbreviations for each treatment and separating hyphens, the length of ARMCD values would be 20. If the subject was not assigned to an Arm, ARMCD is null and ARMNRS is populated. With the exception of studies which use multi-stage Arm assignments, must be a value of ARMCD in the Trial Arms Dataset.', 'Exp'),
('DM', 'ARMNRS', 'Reason Arm and/or Actual Arm is Null', 'Char', '*', 'Record Qualifier', 'A coded reason that Arm variables (ARM and ARMCD) and/or actual Arm variables (ACTARM and ACTARMCD) are null. Examples: "SCREEN FAILURE", "NOT ASSIGNED", "ASSIGNED, NOT TREATED", "UNPLANNED TREATMENT". It is assumed that if the Arm and actual Arm variables are null, the same reason applies to both Arm and actual Arm.', 'Exp'),
('DM', 'BRTHDTC', 'Date/Time of Birth', 'Char', 'ISO 8601', 'Record Qualifier', 'Date/time of birth of the subject.', 'Perm'),
('DM', 'COUNTRY', 'Country', 'Char', 'ISO 3166-1 Alpha-3', 'Record Qualifier', 'Country of the investigational site in which the subject participated in the trial.', 'Req'),
('DM', 'DMDTC', 'Date/Time of Collection', 'Char', 'ISO 8601', 'Timing', 'Date/time of demographic data collection.', 'Perm'),
('DM', 'DMDY', 'Study Day of Collection', 'Num', '', 'Timing', 'Study day of collection measured as integer days.', 'Perm'),
('DM', 'DOMAIN', 'Domain Abbreviation', 'Char', 'DM', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('DM', 'DTHDTC', 'Date/Time of Death', 'Char', 'ISO 8601', 'Record Qualifier', 'Date/time of death for any subject who died, in ISO 8601 format. Should represent the date/time that is captured in the clinical-trial database.', 'Exp'),
('DM', 'DTHFL', 'Subject Death Flag', 'Char', '(NY)', 'Record Qualifier', 'Indicates the subject died. Should be "Y" or null. Should be populated even when the death date is unknown.', 'Exp'),
('DM', 'ETHNIC', 'Ethnicity', 'Char', '(ETHNIC)', 'Record Qualifier', 'The ethnicity of the subject. Sponsors should refer to "Collection of Race and Ethnicity Data in Clinical Trials" (FDA, October, 2016) for guidance regarding the collection of ethnicity (https://www.fda.gov/downloads/regulatoryinformation/guidances/ucm126396.pdf).', 'Perm'),
('DM', 'INVID', 'Investigator Identifier', 'Char', '', 'Record Qualifier', 'An identifier to describe the Investigator for the study. May be used in addition to SITEID. Not needed if SITEID is equivalent to INVID.', 'Perm'),
('DM', 'INVNAM', 'Investigator Name', 'Char', '', 'Synonym Qualifier', 'Name of the investigator for a site.', 'Perm'),
('DM', 'RACE', 'Race', 'Char', '(RACE)', 'Record Qualifier', 'Race of the subject. Sponsors should refer to "Collection of Race and Ethnicity Data in Clinical Trials" (FDA, October, 2016) for guidance regarding the collection of race (https://www.fda.gov/downloads/regulatoryinformation/guidances/ucm126396.pdf) See Assumption below regarding RACE.', 'Exp'),
('DM', 'RFENDTC', 'Subject Reference End Date/Time', 'Char', 'ISO 8601', 'Record Qualifier', 'Reference End Date/time for the subject in ISO 8601 character format. Usually equivalent to the date/time when subject was determined to have ended the trial, and often equivalent to date/time of last exposure to study treatment. Required for all randomized subjects; null for screen failures or unassigned subjects.', 'Exp'),
('DM', 'RFICDTC', 'Date/Time of Informed Consent', 'Char', 'ISO 8601', 'Record Qualifier', 'Date/time of informed consent in ISO 8601 character format. This will be the same as the date of informed consent in the Disposition domain, if that protocol milestone is documented. Would be null only in studies not collecting the date of informed consent.', 'Exp'),
('DM', 'RFPENDTC', 'Date/Time of End of Participation', 'Char', 'ISO 8601', 'Record Qualifier', 'Date/time when subject ended participation or follow-up in a trial, as defined in the protocol, in ISO 8601 character format. Should correspond to the last known date of contact. Examples include completion date, withdrawal date, last follow-up, date recorded for lost to follow up, or death date.', 'Exp'),
('DM', 'RFSTDTC', 'Subject Reference Start Date/Time', 'Char', 'ISO 8601', 'Record Qualifier', 'Reference Start Date/time for the subject in ISO 8601 character format. Usually equivalent to date/time when subject was first exposed to study treatment. See Assumption 9 for additional detail on when RFSTDTC may be null.', 'Exp'),
('DM', 'RFXENDTC', 'Date/Time of Last Study Treatment', 'Char', 'ISO 8601', 'Record Qualifier', 'Last date/time of exposure to any protocol-specified treatment or therapy, equal to the latest value of EXENDTC (or the latest value of EXSTDTC if EXENDTC was not collected or is missing).', 'Exp'),
('DM', 'RFXSTDTC', 'Date/Time of First Study Treatment', 'Char', 'ISO 8601', 'Record Qualifier', 'First date/time of exposure to any protocol-specified treatment or therapy, equal to the earliest value of EXSTDTC.', 'Exp'),
('DM', 'SEX', 'Sex', 'Char', '(SEX)', 'Record Qualifier', 'Sex of the subject.', 'Req'),
('DM', 'SITEID', 'Study Site Identifier', 'Char', '*', 'Record Qualifier', 'Unique identifier for a site within a study.', 'Req'),
('DM', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('DM', 'SUBJID', 'Subject Identifier for the Study', 'Char', '', 'Topic', 'Subject identifier, which must be unique within the study. Often the ID of the subject as recorded on a CRF.', 'Req'),
('DM', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product. This must be a unique number, and could be a compound identifier formed by concatenating STUDYID-SITEID-SUBJID.', 'Req')
;
--
-- Domain: DS
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('DS', 'DOMAIN', 'Domain Abbreviation', 'Char', 'DS', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('DS', 'DSCAT', 'Category for Disposition Event', 'Char', '(DSCAT)', 'Grouping Qualifier', 'Used to define a category of related records.', 'Exp'),
('DS', 'DSDECOD', 'Standardized Disposition Term', 'Char', '(NCOMPLT)(PROTMLST)', 'Synonym Qualifier', 'Controlled terminology for the name of disposition event or protocol milestone. Examples of protocol milestones: "INFORMED CONSENT OBTAINED", "RANDOMIZED". There are separate codelists used for DSDECOD where the choice depends on the value of DSCAT. Codelist "NCOMPLT" is used for disposition events and codelist "PROTMLST" is used for protocol milestones. The variable may be subject to controlled terminology for other events.', 'Req'),
('DS', 'DSDTC', 'Date/Time of Collection', 'Char', 'ISO 8601', 'Timing', 'Collection date and time of the disposition observation represented in ISO 8601 character format.', 'Perm'),
('DS', 'DSDY', 'Study Day of Collection', 'Num', '', 'Timing', 'Start date/time of the disposition event in ISO 8601 character format.', 'Exp'),
('DS', 'DSGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('DS', 'DSREFID', 'Reference ID', 'Char', '', 'Identifier', 'Internal or external identifier.', 'Perm'),
('DS', 'DSSCAT', 'Subcategory for Disposition Event', 'Char', '*', 'Grouping Qualifier', 'A further categorization of DSCAT (e.g., "STUDY PARTICIPATION", "STUDY TREATMENT" when DSCAT = "DISPOSITION EVENT").', 'Perm'),
('DS', 'DSSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence Number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('DS', 'DSSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Perhaps preprinted on the CRF as an explicit line identifier or defined in the sponsor''s operational database. Example: Line number on a Disposition page.', 'Perm'),
('DS', 'DSSTDTC', 'Start Date/Time of Disposition Event', 'Char', 'ISO 8601', 'Timing', 'Start date/time of the disposition event in ISO 8601 character format.', 'Exp'),
('DS', 'DSSTDY', 'Study Day of Start of Disposition Event', 'Num', '', 'Timing', 'Study day of start of event relative to the sponsor-defined RFSTDTC.', 'Perm'),
('DS', 'DSTERM', 'Reported Term for the Disposition Event', 'Char', '', 'Topic', 'Verbatim name of the event or protocol milestone. Some terms in DSTERM will match DSDECOD, but others, such as "Subject moved" will map to controlled terminology in DSDECOD, such as "LOST TO FOLLOW-UP".', 'Req'),
('DS', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time of the event.', 'Perm'),
('DS', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('DS', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req')
;
--
-- Domain: EX
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('EX', 'DOMAIN', 'Domain Abbreviation', 'Char', 'EX', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('EX', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Trial Epoch of the Exposure record. Examples: "RUN-IN", "TREATMENT".', 'Perm'),
('EX', 'EXADJ', 'Reason for Dose Adjustment', 'Char', '*', 'Record Qualifier', 'Describes reason or explanation of why a dose is adjusted.', 'Perm'),
('EX', 'EXCAT', 'Category of Treatment', 'Char', '*', 'Grouping Qualifier', 'Used to define a category of EXTRT values.', 'Perm'),
('EX', 'EXDIR', 'Directionality', 'Char', '(DIR)', 'Variable Qualifier', 'Qualifier for anatomical location further detailing directionality. Examples: "ANTERIOR", "LOWER", "PROXIMAL", "UPPER".', 'Perm'),
('EX', 'EXDOSE', 'Dose', 'Num', '', 'Record Qualifier', 'Amount of EXTRT when numeric. Not populated when EXDOSTXT is populated.', 'Exp'),
('EX', 'EXDOSFRM', 'Dose Form', 'Char', '(FRM)', 'Variable Qualifier', 'Dose form for EXTRT. Examples: "TABLET", "LOTION".', 'Exp'),
('EX', 'EXDOSFRQ', 'Dosing Frequency per Interval', 'Char', '(FREQ)', 'Variable Qualifier', 'Usually expressed as the number of repeated administrations of EXDOSE within a specific time period. Examples: "Q2H", "QD", "BID".', 'Perm'),
('EX', 'EXDOSRGM', 'Intended Dose Regimen', 'Char', '', 'Variable Qualifier', 'Text description of the intended schedule or regimen for the Intervention. Example: "TWO WEEKS ON, TWO WEEKS OFF".', 'Perm'),
('EX', 'EXDOSTXT', 'Dose Description', 'Char', '', 'Record Qualifier', 'Amount of EXTRT when non-numeric. Dosing amounts or a range of dosing information collected in text form. Example: 200-400. Not populated when EXDOSE is populated.', 'Perm'),
('EX', 'EXDOSU', 'Dose Units', 'Char', '(UNIT)', 'Variable Qualifier', 'Units for EXDOSE, EXDOSTOT, or EXDOSTXT representing protocol-specified values. Examples: "ng", "mg", "mg/kg", "mg/m2".', 'Exp'),
('EX', 'EXDUR', 'Duration of Treatment', 'Char', 'ISO 8601', 'Timing', 'Collected duration of administration. Used only if collected on the CRF and not derived from start and end date/times.', 'Perm'),
('EX', 'EXELTM', 'Planned Elapsed Time from Time Point Ref', 'Char', 'ISO 8601', 'Timing', 'Planned elapsed time relative to the planned fixed reference (EXTPTREF). This variable is useful where there are repetitive measures. Not a clock time.', 'Perm'),
('EX', 'EXENDTC', 'End Date/Time of Treatment', 'Char', 'ISO 8601', 'Timing', 'The date/time when administration of the treatment indicated by EXTRT and EXDOSE ended. For administrations considered given at a point in time (e.g., oral tablet, pre-filled syringe injection), where only an administration date/time is collected, EXSTDTC should be copied to EXENDTC as the standard representation.', 'Exp'),
('EX', 'EXENDY', 'Study Day of End of Treatment', 'Num', '', 'Timing', 'Study day of EXENDTC relative to DM.RFSTDTC.', 'Perm'),
('EX', 'EXFAST', 'Fasting Status', 'Char', '(NY)', 'Record Qualifier', 'Indicator used to identify fasting status. Examples: "Y", "N".', 'Perm'),
('EX', 'EXGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('EX', 'EXLAT', 'Laterality', 'Char', '(LAT)', 'Variable Qualifier', 'Qualifier for anatomical location further detailing laterality of the intervention administration. Examples: "LEFT", "RIGHT".', 'Perm'),
('EX', 'EXLNKGRP', 'Link Group ID', 'Char', '', 'Identifier', 'Identifier used to link related, grouped records across domains.', 'Perm'),
('EX', 'EXLNKID', 'Link ID', 'Char', '', 'Identifier', 'Identifier used to link related records across domains.', 'Perm'),
('EX', 'EXLOC', 'Location of Dose Administration', 'Char', '(LOC)', 'Record Qualifier', 'Specifies location of administration. Examples: "ARM", "LIP".', 'Perm'),
('EX', 'EXLOT', 'Lot Number', 'Char', '', 'Record Qualifier', 'Lot number of the intervention product.', 'Perm'),
('EX', 'EXREFID', 'Reference ID', 'Char', '', 'Identifier', 'Internal or external identifier (e.g., kit number, bottle label, vial identifier).', 'Perm'),
('EX', 'EXRFTDTC', 'Date/Time of Reference Time Point', 'Char', 'ISO 8601', 'Timing', 'Date/time for a fixed reference time point defined by EXTPTREF.', 'Perm'),
('EX', 'EXROUTE', 'Route of Administration', 'Char', '(ROUTE)', 'Variable Qualifier', 'Route of administration for the intervention. Examples: "ORAL", "INTRAVENOUS".', 'Perm'),
('EX', 'EXSCAT', 'Subcategory of Treatment', 'Char', '*', 'Grouping Qualifier', 'A further categorization of EXCAT values.', 'Perm'),
('EX', 'EXSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence Number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('EX', 'EXSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Perhaps pre-printed on the CRF as an explicit line identifier or defined in the sponsor''s operational database. Example: Line number on a CRF Page.', 'Perm'),
('EX', 'EXSTDTC', 'Start Date/Time of Treatment', 'Char', 'ISO 8601', 'Timing', 'The date/time when administration of the treatment indicated by EXTRT and EXDOSE began.', 'Exp'),
('EX', 'EXSTDY', 'Study Day of Start of Treatment', 'Num', '', 'Timing', 'Study day of EXSTDTC relative to DM.RFSTDTC.', 'Perm'),
('EX', 'EXTPT', 'Planned Time Point Name', 'Char', '', 'Timing', '1. Text Description of time when administration should occur. 2. This may be represented as an elapsed time relative to a fixed reference point, such as time of last dose. See EXTPTNUM and EXTPTREF.', 'Perm'),
('EX', 'EXTPTNUM', 'Planned Time Point Number', 'Num', '', 'Timing', 'Numerical version of EXTPT to aid in sorting.', 'Perm'),
('EX', 'EXTPTREF', 'Time Point Reference', 'Char', '', 'Timing', 'Name of the fixed reference point referred to by EXELTM, EXTPTNUM, and EXTPT. Examples: PREVIOUS DOSE, PREVIOUS MEAL.', 'Perm'),
('EX', 'EXTRT', 'Name of Treatment', 'Char', '*', 'Topic', 'Name of the protocol-specified study treatment given during the dosing period for the observation.', 'Req'),
('EX', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('EX', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm.', 'Perm'),
('EX', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req')
;
--
-- Domain: LB
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('LB', 'DOMAIN', 'Domain Abbreviation', 'Char', 'LB', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('LB', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time of the observation, or the date/time of collection if start date/time is not collected.', 'Perm'),
('LB', 'LBBLFL', 'Baseline Flag', 'Char', '(NY)', 'Record Qualifier', 'Indicator used to identify a baseline value. Should be "Y" or null. Note that LBBLFL is retained for backward compatibility. The authoritative baseline for statistical analysis is in an ADaM dataset.', 'Perm'),
('LB', 'LBCAT', 'Category for Lab Test', 'Char', '*', 'Grouping Qualifier', 'Used to define a category of related records across subjects. Examples: "HEMATOLOGY", "URINALYSIS", "CHEMISTRY".', 'Exp'),
('LB', 'LBDRVFL', 'Derived Flag', 'Char', '(NY)', 'Record Qualifier', 'Used to indicate a derived record. The value should be "Y" or null. Records that represent the average of other records, or do not come from the CRF, or are not as originally received or collected are examples of records that might be derived for the submission datasets. If LBDRVFL = "Y", then LBORRES may be null, with LBSTRESC and (if numeric) LBSTRESN having the derived value.', 'Perm'),
('LB', 'LBDTC', 'Date/Time of Specimen Collection', 'Char', 'ISO 8601', 'Timing', 'Date/time of specimen collection represented in ISO 8601 character format.', 'Exp'),
('LB', 'LBDY', 'Study Day of Specimen Collection', 'Num', '', 'Timing', '1. Study day of specimen collection, measured as integer days. 2. Algorithm for calculations must be relative to the sponsor-defined RFSTDTC variable in Demographics. This formula should be consistent across the submission.', 'Perm'),
('LB', 'LBELTM', 'Planned Elapsed Time from Time Point Ref', 'Char', 'ISO 8601', 'Timing', 'Planned elapsed time (in ISO 8601) relative to a planned fixed reference (LBTPTREF). This variable is useful where there are repetitive measures. Not a clock time or a date/time variable. Represented as ISO 8601 duration. Examples: "-PT15M" to represent the period of 15 minutes prior to the reference point indicated by LBTPTREF, or "PT8H" to represent the period of 8 hours after the reference point indicated by LBTPTREF.', 'Perm'),
('LB', 'LBENDTC', 'End Date/Time of Specimen Collection', 'Char', 'ISO 8601', 'Timing', 'End date/time of specimen collection represented in ISO 8601 character format.', 'Perm'),
('LB', 'LBENDY', 'Study Day of End of Observation', 'Num', '', 'Timing', 'Actual study day of end of observation expressed in integer days relative to the sponsor-defined RFSTDTC in Demographics.', 'Perm'),
('LB', 'LBFAST', 'Fasting Status', 'Char', '(NY)', 'Record Qualifier', 'Indicator used to identify fasting status such as "Y", "N", "U", or null if not relevant.', 'Perm'),
('LB', 'LBGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('LB', 'LBLOBXFL', 'Last Observation Before Exposure Flag', 'Char', '(NY)', 'Record Qualifier', 'Operationally-derived indicator used to identify the last non-missing value prior to RFXSTDTC. The value should be "Y" or null.', 'Exp'),
('LB', 'LBLOINC', 'LOINC Code', 'Char', '*', 'Synonym Qualifier', '1. Code for the lab test from the LOINC code system. 2. The sponsor is expected to provide the dictionary name and version used to map the terms utilizing the Define-XML external codelist attributes.', 'Perm'),
('LB', 'LBMETHOD', 'Method of Test or Examination', 'Char', '(METHOD)', 'Record Qualifier', 'Method of the test or examination. Examples: "EIA" (Enzyme Immunoassay), "ELECTROPHORESIS", "DIPSTICK".', 'Perm'),
('LB', 'LBNAM', 'Vendor Name', 'Char', '', 'Record Qualifier', 'The name or identifier of the laboratory that performed the test.', 'Perm'),
('LB', 'LBNRIND', 'Reference Range Indicator', 'Char', '(NRIND)', 'Variable Qualifier', '1. Indicates where the value falls with respect to reference range defined by LBORNRLO and LBORNRHI, LBSTNRLO and LBSTNRHI, or by LBSTNRC. Examples: "NORMAL", "ABNORMAL", "HIGH", "LOW". 2. Sponsors should specify in the study metadata (Comments column in the Define-XML document) whether LBNRIND refers to the original or standard reference ranges and results. 3. Should not be used to indicate clinical significance.', 'Exp'),
('LB', 'LBORNRHI', 'Reference Range Upper Limit in Orig Unit', 'Char', '', 'Variable Qualifier', 'Upper end of reference range for continuous measurement in original units. Should be populated only for continuous results.', 'Exp'),
('LB', 'LBORNRLO', 'Reference Range Lower Limit in Orig Unit', 'Char', '', 'Variable Qualifier', 'Lower end of reference range for continuous measurement in original units. Should be populated only for continuous results.', 'Exp'),
('LB', 'LBORRES', 'Result or Finding in Original Units', 'Char', '', 'Result Qualifier', 'Result of the measurement or finding as originally received or collected.', 'Exp'),
('LB', 'LBORRESU', 'Original Units', 'Char', '(UNIT)', 'Variable Qualifier', 'Original units in which the data were collected. The unit for LBORRES. Example: "g/L".', 'Exp'),
('LB', 'LBREASND', 'Reason Test Not Done', 'Char', '', 'Record Qualifier', 'Describes why a measurement or test was not performed, e.g., "BROKEN EQUIPMENT", "SUBJECT REFUSED", or "SPECIMEN LOST". Used in conjunction with LBSTAT when value is "NOT DONE".', 'Perm'),
('LB', 'LBREFID', 'Specimen ID', 'Char', '', 'Identifier', 'Internal or external specimen identifier. Example: Specimen ID.', 'Perm'),
('LB', 'LBRFTDTC', 'Date/Time of Reference Time Point', 'Char', 'ISO 8601', 'Timing', 'Date/time of the reference time point, LBTPTREF.', 'Perm'),
('LB', 'LBSCAT', 'Subcategory for Lab Test', 'Char', '*', 'Grouping Qualifier', 'A further categorization of a test category such as "DIFFERENTIAL", "COAGULATION", "LIVER FUNCTION", "ELECTROLYTES".', 'Perm'),
('LB', 'LBSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('LB', 'LBSPCCND', 'Specimen Condition', 'Char', '(SPECCOND)', 'Record Qualifier', 'Free or standardized text describing the condition of the specimen, e.g., "HEMOLYZED", "ICTERIC", "LIPEMIC".', 'Perm'),
('LB', 'LBSPEC', 'Specimen Type', 'Char', '(SPECTYPE)', 'Record Qualifier', 'Defines the type of specimen used for a measurement. Examples: "SERUM", "PLASMA", "URINE", "DNA", "RNA".', 'Perm'),
('LB', 'LBSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Perhaps preprinted on the CRF as an explicit line identifier or defined in the sponsor''s operational database. Example: Line number on the Lab page.', 'Perm'),
('LB', 'LBSTAT', 'Completion Status', 'Char', '(ND)', 'Record Qualifier', 'Used to indicate exam not done. Should be null if a result exists in LBORRES.', 'Perm'),
('LB', 'LBSTNRC', 'Reference Range for Char Rslt-Std Units', 'Char', '', 'Variable Qualifier', 'For normal range values that are character in ordinal scale or if categorical ranges were supplied (e.g., "-1 to +1", "NEGATIVE TO TRACE").', 'Perm'),
('LB', 'LBSTNRHI', 'Reference Range Upper Limit-Std Units', 'Num', '', 'Variable Qualifier', 'Upper end of reference range for continuous measurements in standardized units. Should be populated only for continuous results.', 'Exp'),
('LB', 'LBSTNRLO', 'Reference Range Lower Limit-Std Units', 'Num', '', 'Variable Qualifier', 'Lower end of reference range for continuous measurements for LBSTRESC/LBSTRESN in standardized units. Should be populated only for continuous results.', 'Exp'),
('LB', 'LBSTREFC', 'Reference Result in Standard Format', 'Char', '', 'Variable Qualifier', 'Reference value for the result or finding copied or derived from LBORREF in a standard format.', 'Exp'),
('LB', 'LBSTRESC', 'Character Result/Finding in Std Format', 'Char', '(LBSTRESC)', 'Result Qualifier', 'Contains the result value for all findings, copied or derived from LBORRES in a standard format or standard units. LBSTRESC should store all results or findings in character format; if results are numeric, they should also be stored in numeric format in LBSTRESN. For example, if a test has results "NONE", "NEG", and "NEGATIVE" in LBORRES and these results effectively have the same meaning, they could be represented in standard format in LBSTRESC as "NEGATIVE". For other examples, see general assumptions.', 'Exp'),
('LB', 'LBSTRESN', 'Numeric Result/Finding in Standard Units', 'Num', '', 'Result Qualifier', 'Used for continuous or numeric results or findings in standard format; copied in numeric format from LBSTRESC. LBSTRESN should store all numeric test results or findings.', 'Exp'),
('LB', 'LBSTRESU', 'Standard Units', 'Char', '(UNIT)', 'Variable Qualifier', 'Standardized unit used for LBSTRESC or LBSTRESN.', 'Exp'),
('LB', 'LBTEST', 'Lab Test or Examination Name', 'Char', '(LBTEST)', 'Synonym Qualifier', 'Verbatim name of the test or examination used to obtain the measurement or finding. Note any test normally performed by a clinical laboratory is considered a lab test. The value in LBTEST cannot be longer than 40 characters. Examples: "Alanine Aminotransferase", "Lactate Dehydrogenase".', 'Req'),
('LB', 'LBTESTCD', 'Lab Test or Examination Short Name', 'Char', '(LBTESTCD)', 'Topic', 'Short name of the measurement, test, or examination described in LBTEST. It can be used as a column name when converting a dataset from a vertical to a horizontal format. The value in LBTESTCD cannot be longer than 8 characters, nor can it start with a number (e.g., "1TEST" is not valid). LBTESTCD cannot contain characters other than letters, numbers, or underscores. Examples: "ALT", "LDH".', 'Req'),
('LB', 'LBTOX', 'Toxicity', 'Char', '*', 'Variable Qualifier', 'Description of toxicity quantified by LBTOXGR. The sponsor is expected to provide the name of the scale and version used to map the terms, utilizing the external codelist element in the Define-XML document.', 'Perm'),
('LB', 'LBTOXGR', 'Standard Toxicity Grade', 'Char', '*', 'Record Qualifier', 'Records toxicity grade value using a standard toxicity scale (such as the NCI CTCAE). If value is from a numeric scale, represent only the number (e.g., "2" and not "Grade 2"). The sponsor is expected to provide the name of the scale and version used to map the terms, utilizing the external codelist element in the Define-XML document.', 'Perm'),
('LB', 'LBTPT', 'Planned Time Point Name', 'Char', '', 'Timing', '1. Text description of time when specimen should be taken. 2. This may be represented as an elapsed time relative to a fixed reference point, such as time of last dose. See LBTPTNUM and LBTPTREF. Examples: "Start", "5 min post".', 'Perm'),
('LB', 'LBTPTNUM', 'Planned Time Point Number', 'Num', '', 'Timing', 'Numerical version of LBTPT to aid in sorting.', 'Perm'),
('LB', 'LBTPTREF', 'Time Point Reference', 'Char', '', 'Timing', 'Name of the fixed reference point referred to by LBELTM, LBTPTNUM, and LBTPT. Examples: PREVIOUS DOSE, PREVIOUS MEAL.', 'Perm'),
('LB', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('LB', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm.', 'Perm'),
('LB', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req'),
('LB', 'VISIT', 'Visit Name', 'Char', '', 'Timing', '1. Protocol-defined description of clinical encounter. 2. May be used in addition to VISITNUM and/or VISITDY.', 'Perm'),
('LB', 'VISITDY', 'Planned Study Day of Visit', 'Num', '', 'Timing', 'Planned study day of the visit based upon RFSTDTC in Demographics.', 'Perm'),
('LB', 'VISITNUM', 'Visit Number', 'Num', '', 'Timing', '1. Clinical encounter number. 2. Numeric version of VISIT, used for sorting.', 'Exp')
;
--
-- Domain: MH
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('MH', 'DOMAIN', 'Domain Abbreviation', 'Char', 'MH', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('MH', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time of the medical history event.', 'Perm'),
('MH', 'MHBODSYS', 'Body System or Organ Class', 'Char', '*', 'Record Qualifier', 'Dictionary-derived. Body system or organ class that is involved in an event or measurement from a standard hierarchy (e.g., MedDRA). When using a multi-axial dictionary such as MedDRA, this should contain the SOC used for the sponsor''s analyses and summary tables which may not necessarily be the primary SOC.', 'Perm'),
('MH', 'MHCAT', 'Category for Medical History', 'Char', '*', 'Grouping Qualifier', 'Used to define a category of related records. Examples: "CARDIAC" or "GENERAL".', 'Perm'),
('MH', 'MHDECOD', 'Dictionary-Derived Term', 'Char', '*', 'Synonym Qualifier', 'Dictionary-derived text description of MHTERM or MHMODIFY. Equivalent to the Preferred Term (PT in MedDRA). The sponsor is expected to provide the dictionary name and version used to map the terms utilizing the external codelist element in the Define-XML document.', 'Perm'),
('MH', 'MHDTC', 'Date/Time of History Collection', 'Char', 'ISO 8601', 'Timing', 'Collection date and time of the medical history observation represented in ISO 8601 character format.', 'Perm'),
('MH', 'MHDY', 'Study Day of History Collection', 'Num', '', 'Timing', '1. Study day of medical history collection, measured as integer days. 2. Algorithm for calculations must be relative to the sponsor-defined RFSTDTC variable in Demographics. This formula should be consistent across the submission.', 'Perm'),
('MH', 'MHENDTC', 'End Date/Time of Medical History Event', 'Char', 'ISO 8601', 'Timing', 'End date/time of the medical history event.', 'Perm'),
('MH', 'MHENRF', 'End Relative to Reference Period', 'Char', '(STENRF)', 'Timing', 'Describes the end of the event relative to the sponsor-defined reference period. The sponsor-defined reference period is a continuous period of time defined by a discrete starting point and a discrete ending point (represented by RFSTDTC and RFENDTC in Demographics).	Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('MH', 'MHENRTPT', 'End Relative to Reference Time Point', 'Char', '(STENRF)', 'Timing', 'Identifies the end of the event as being before or after the reference time point defined by variable MHENTPT. Not all values of the codelist are allowable for this variable. See Section 4.4.7, Use of Relative Timing Variables.', 'Perm'),
('MH', 'MHENTPT', 'End Reference Time Point', 'Char', '', 'Timing', 'Description or date/time in ISO 8601 character format of the reference point referred to by MHENRTPT. Examples: "2003-12-25" or "VISIT 2".', 'Perm'),
('MH', 'MHEVDTYP', 'Medical History Event Date Type', 'Char', '(MHEDTTYP)', 'Variable Qualifier', 'Specifies the aspect of the medical condition or event by which MHSTDTC and/or the MHENDTC is defined. Examples: "DIAGNOSIS", "SYMPTOMS", "RELAPSE", "INFECTION".', 'Perm'),
('MH', 'MHGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('MH', 'MHMODIFY', 'Modified Reported Term', 'Char', '', 'Synonym Qualifier', 'If MHTERM is modified to facilitate coding, then MHMODIFY will contain the modified text.', 'Perm'),
('MH', 'MHOCCUR', 'Medical History Occurrence', 'Char', '(NY)', 'Record Qualifier', 'Used when the occurrence of specific medical history conditions is solicited, to indicate whether or not ("Y"/"N") a medical condition (MHTERM) had ever occurred. Values are null for spontaneously reported events.', 'Perm'),
('MH', 'MHPRESP', 'Medical History Event Pre-Specified', 'Char', '(NY)', 'Variable Qualifier', 'A value of "Y" indicates that this medical history event was pre-specified on the CRF. Values are null for spontaneously reported events (i.e., those collected as free-text verbatim terms).', 'Perm'),
('MH', 'MHREASND', 'Reason Medical History Not Collected', 'Char', '', 'Record Qualifier', 'Describes the reason why data for a pre-specified condition was not collected. Used in conjunction with MHSTAT when value is "NOT DONE".', 'Perm'),
('MH', 'MHREFID', 'Reference ID', 'Char', '', 'Identifier', 'Internal or external medical history identifier.', 'Perm'),
('MH', 'MHSCAT', 'Subcategory for Medical History', 'Char', '*', 'Grouping Qualifier', 'A further categorization of the condition or event.', 'Perm'),
('MH', 'MHSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence Number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('MH', 'MHSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Perhaps preprinted on the CRF as an explicit line identifier or defined in the sponsor''s operational database. Example: Line number on a Medical History page.', 'Perm'),
('MH', 'MHSTAT', 'Completion Status', 'Char', '(ND)', 'Record Qualifier', 'The status indicates that the pre-specified question was not asked/answered.', 'Perm'),
('MH', 'MHSTDTC', 'Start Date/Time of Medical History Event', 'Char', 'ISO 8601', 'Timing', 'Start date/time of the medical history event represented in ISO 8601 character format.', 'Perm'),
('MH', 'MHTERM', 'Reported Term for the Medical History', 'Char', '', 'Topic', 'Verbatim or preprinted CRF term for the medical condition or event.', 'Req'),
('MH', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('MH', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm for the Element in which the assessment was made.', 'Perm'),
('MH', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req')
;
-- 
-- Domain: TA
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('TA', 'ARM', 'Description of Planned Arm', 'Char', '*', 'Synonym Qualifier', 'Name given to an Arm or treatment group.', 'Req'),
('TA', 'ARMCD', 'Planned Arm Code', 'Char', '*', 'Topic', 'ARMCD is limited to 20 characters and does not have special character restrictions. The maximum length of ARMCD is longer than that for other "short" variables to accommodate the kind of values that are likely to be needed for crossover trials. For example, if ARMCD values for a seven-period crossover were constructed using two-character abbreviations for each treatment and separating hyphens, the length of ARMCD values would be 20.', 'Req'),
('TA', 'DOMAIN', 'Domain Abbreviation', 'Char', 'TA', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('TA', 'ELEMENT', 'Description of Element', 'Char', '*', 'Synonym Qualifier', 'The name of the Element. The same Element may occur more than once within an Arm.', 'Perm'),
('TA', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Name of the Trial Epoch with which this Element of the Arm is associated.', 'Req'),
('TA', 'ETCD', 'Element Code', 'Char', '*', 'Record Qualifier', 'ETCD (the companion to ELEMENT) is limited to 8 characters and does not have special character restrictions. These values should be short for ease of use in programming, but it is not expected that ETCD will need to serve as a variable name.', 'Req'),
('TA', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('TA', 'TABRANCH', 'Branch', 'Char', '', 'Rule', 'Condition subject met, at a "branch" in the trial design at the end of this Element, to be included in this Arm (e.g., "Randomization to DRUG X").', 'Exp'),
('TA', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the order of the Element within the Arm.', 'Req'),
('TA', 'TATRANS', 'Transition Rule', 'Char', '', 'Rule', 'If the trial design allows a subject to transition to an Element other than the next Element in sequence, then the conditions for transitioning to those other Elements, and the alternative Element sequences, are specified in this rule (e.g., "Responders go to washout").', 'Exp')
;
--
-- Domain: TS
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('TS', 'DOMAIN', 'Domain Abbreviation', 'Char', 'TS', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('TS', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('TS', 'TSGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a group of related records.', 'Perm'),
('TS', 'TSPARM', 'Trial Summary Parameter', 'Char', '(TSPARM)', 'Synonym Qualifier', 'Term for the Trial Summary Parameter. The value in TSPARM cannot be longer than 40 characters. Examples: "Planned Minimum Age of Subjects", "Planned Maximum Age of Subjects".', 'Req'),
('TS', 'TSPARMCD', 'Trial Summary Parameter Short Name', 'Char', '(TSPARMCD)', 'Topic', 'TSPARMCD (the companion to TSPARM) is limited to 8 characters and does not have special character restrictions. These values should be short for ease of use in programming, but it is not expected that TSPARMCD will need to serve as variable names. Examples: "AGEMIN", "AGEMAX".', 'Req'),
('TS', 'TSSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence number given to ensure uniqueness within a dataset. Allows inclusion of multiple records for the same TSPARMCD.', 'Req'),
('TS', 'TSVAL', 'Parameter Value', 'Char', '*', 'Result Qualifier', 'Value of TSPARM. Example: "ASTHMA" when TSPARM value is "Trial Indication". TSVAL can only be null when TSVALNF is populated. Text over 200 characters can be added to additional columns TSVAL1-TSVALn. See Assumption 8.', 'Exp'),
('TS', 'TSVALCD', 'Parameter Value Code', 'Char', '*', 'Result Qualifier', 'This is the code of the term in TSVAL. For example, "6CW7F3G59X" is the code for Gabapentin; "C49488" is the code for Y. The length of this variable can be longer than 8 to accommodate the length of the external terminology.', 'Exp'),
('TS', 'TSVALNF', 'Parameter Null Flavor', 'Char', 'ISO 21090 NullFlavor enumeration', 'Result Qualifier', 'Null flavor for the value of TSPARM, to be populated if and only if TSVAL is null.', 'Perm'),
('TS', 'TSVCDREF', 'Name of the Reference Terminology', 'Char', '', 'Result Qualifier', 'The name of the Reference Terminology from which TSVALCD is taken. For example; CDISC, SNOMED, ISO 8601.', 'Exp'),
('TS', 'TSVCDVER', 'Version of the Reference Terminology', 'Char', '', 'Result Qualifier', 'The version number of the Reference Terminology, if applicable.', 'Exp')
;
--
-- Domain: TV
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('TV', 'ARM', 'Description of Planned Arm', 'Char', '*', 'Synonym Qualifier', '1. Name given to an Arm or Treatment Group. 2. If the timing of Visits for a trial does not depend on which Arm a subject is in, then Arm should be left blank.', 'Perm'),
('TV', 'ARMCD', 'Planned Arm Code', 'Char', '*', 'Record Qualifier', '1. ARMCD is limited to 20 characters and does not have special character restrictions. The maximum length of ARMCD is longer than for other "short" variables to accommodate the kind of values that are likely to be needed for crossover trials. For example, if ARMCD values for a seven-period crossover were constructed using two-character abbreviations for each treatment and separating hyphens, the length of ARMCD values would be 20. 2. If the timing of Visits for a trial does not depend on which Arm a subject is in, then ARMCD should be null.', 'Exp'),
('TV', 'DOMAIN', 'Domain Abbreviation', 'Char', 'TV', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('TV', 'STUDYID', 'Study Identifier', 'Char', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('TV', 'TVENRL', 'Visit End Rule', 'Char', '', 'Rule', 'Rule describing when the Visit ends, in relation to the sequence of Elements.', 'Perm'),
('TV', 'TVSTRL', 'Visit Start Rule', 'Char', '', 'Rule', 'Rule describing when the Visit starts, in relation to the sequence of Elements.', 'Req'),
('TV', 'VISIT', 'Visit Name', 'Char', '', 'Synonym Qualifier', '1. Protocol-defined description of clinical encounter. 2. May be used in addition to VISITNUM and/or VISITDY as a text description of the clinical encounter.', 'Perm'),
('TV', 'VISITDY', 'Planned Study Day of Visit', 'Num', '', 'Timing', '1. Planned study day of VISIT. 2. Due to its sequential nature, used for sorting.', 'Perm'),
('TV', 'VISITNUM', 'Visit Number', 'Num', '', 'Topic', '1. Clinical encounter number 2. Numeric version of VISIT, used for sorting.', 'Req')
;
--
-- Domain: VS
INSERT INTO cdisc_sdtm_domain_definitions (domain_code, variable_name, variable_label, type, controlled_terms, role, cdisc_notes, core) VALUES 
('VS', 'DOMAIN', 'Domain Abbreviation', 'Char', 'VS', 'Identifier', 'Two-character abbreviation for the domain.', 'Req'),
('VS', 'EPOCH', 'Epoch', 'Char', '(EPOCH)', 'Timing', 'Epoch associated with the start date/time at which the assessment was made.', 'Perm'),
('VS', 'STUDYID', 'Study Identifier', 'Char	', '', 'Identifier', 'Unique identifier for a study.', 'Req'),
('VS', 'TAETORD', 'Planned Order of Element within Arm', 'Num', '', 'Timing', 'Number that gives the planned order of the Element within the Arm.', 'Perm'),
('VS', 'USUBJID', 'Unique Subject Identifier', 'Char', '', 'Identifier', 'Identifier used to uniquely identify a subject across all studies for all applications or submissions involving the product.', 'Req'),
('VS', 'VISIT', 'Visit Name', 'Char', '', 'Timing', '1. Protocol-defined description of clinical encounter. 2. May be used in addition to VISITNUM and/or VISITDY.', 'Perm'),
('VS', 'VISITDY', 'Planned Study Day of Visit', 'Num', '', 'Timing', 'Planned study day of the visit based upon RFSTDTC in Demographics.', 'Perm'),
('VS', 'VISITNUM', 'Visit Number', 'Num', '', 'Timing', '1. Clinical encounter number. 2. Numeric version of VISIT, used for sorting.', 'Exp'),
('VS', 'VSBLFL', 'Baseline Flag', 'Char', '(NY)', 'Record Qualifier', 'Indicator used to identify a baseline value. Should be "Y" or null. Note that VSBLFL is retained for backward compatibility. The authoritative baseline for statistical analysis is in an ADaM dataset.', 'Perm'),
('VS', 'VSCAT', 'Category for Vital Signs', 'Char', '*', 'Grouping Qualifier', 'Used to define a category of related records.', 'Perm'),
('VS', 'VSDRVFL', 'Derived Flag', 'Char', '(NY)', 'Record Qualifier', 'Used to indicate a derived record. The value should be "Y" or null. Records that represent the average of other records or that do not come from the CRF are examples of records that would be derived for the submission datasets. If VSDRVFL = "Y," then VSORRES may be null, with VSSTRESC and (if numeric) VSSTRESN having the derived value.', 'Perm'),
('VS', 'VSDTC', 'Date/Time of Measurements', 'Char', 'ISO 8601', 'Timing', 'Date and time of the vital signs assessment represented in ISO 8601 character format.', 'Exp'),
('VS', 'VSDY', 'Study Day of Vital Signs', 'Num', '', 'Timing', '1. Study day of vital signs measurements, measured as integer days. 2. Algorithm for calculations must be relative to the sponsor-defined RFSTDTC variable in Demographics.', 'Perm'),
('VS', 'VSELTM', 'Planned Elapsed Time from Time Point Ref', 'Char', 'ISO 8601', 'Timing', 'Planned elapsed time (in ISO 8601) relative to a planned fixed reference (VSTPTREF). This variable is useful where there are repetitive measures. Not a clock time or a date time variable. Represented as an ISO 8601 Duration. Examples: "-PT15M" to represent the period of 15 minutes prior to the reference point indicated by VSTPTREF, or "PT8H" to represent the period of 8 hours after the reference point indicated by VSTPTREF.', 'Perm'),
('VS', 'VSGRPID', 'Group ID', 'Char', '', 'Identifier', 'Used to tie together a block of related records in a single domain for a subject.', 'Perm'),
('VS', 'VSLAT', 'Laterality', 'Char', '(LAT)', 'Result Qualifier', 'Qualifier for anatomical location or specimen further detailing laterality. Examples: "RIGHT", "LEFT", "BILATERAL".', 'Perm'),
('VS', 'VSLOBXFL', 'Last Observation Before Exposure Flag', 'Char', '(NY)', 'Record Qualifier', 'Operationally-derived indicator used to identify the last non-missing value prior to RFXSTDTC. Should be "Y" or null.', 'Exp'),
('VS', 'VSLOC', 'Location of Vital Signs Measurement', 'Char', '(LOC)', 'Record Qualifier', 'Location relevant to the collection of Vital Signs measurement. Example: "ARM" for blood pressure.', 'Perm'),
('VS', 'VSORRES', 'Result or Finding in Original Units', 'Char', '', 'Result Qualifier', 'Result of the vital signs measurement as originally received or collected.', 'Exp'),
('VS', 'VSORRESU', 'Original Units', 'Char', '(VSRESU)', 'Variable Qualifier', 'Original units in which the data were collected. The unit for VSORRES. Examples: "in", "LB", "beats/min".', 'Exp'),
('VS', 'VSPOS', 'Vital Signs Position of Subject', 'Char', '(POSITION)', 'Record Qualifier', 'Position of the subject during a measurement or examination. Examples: "SUPINE", "STANDING", "SITTING".', 'Perm'),
('VS', 'VSREASND', 'Reason Not Performed', 'Char', '', 'Record Qualifier', 'Describes why a measurement or test was not performed. Examples: "BROKEN EQUIPMENT" or "SUBJECT REFUSED". Used in conjunction with VSSTAT when value is "NOT DONE".', 'Perm'),
('VS', 'VSRFTDTC', 'Date/Time of Reference Time Point', 'Char', 'ISO 8601', 'Timing', 'Date/time of the reference time point, VSTPTREF.', 'Perm'),
('VS', 'VSSCAT', 'Subcategory for Vital Signs', 'Char', '*', 'Grouping Qualifier', 'A further categorization of a measurement or examination.', 'Perm'),
('VS', 'VSSEQ', 'Sequence Number', 'Num', '', 'Identifier', 'Sequence number given to ensure uniqueness of subject records within a domain. May be any valid number.', 'Req'),
('VS', 'VSSPID', 'Sponsor-Defined Identifier', 'Char', '', 'Identifier', 'Sponsor-defined reference number. Perhaps pre-printed on the CRF as an explicit line identifier or defined in the sponsor''s operational database.', 'Perm'),
('VS', 'VSSTAT', 'Completion Status', 'Char', '(ND)', 'Record Qualifier', 'Used to indicate that a vital sign measurement was not done. Should be null if a result exists in VSORRES.', 'Perm'),
('VS', 'VSSTRESC', 'Character Result/Finding in Std Format', 'Char', '', 'Result Qualifier', 'Contains the result value for all findings, copied or derived from VSORRES in a standard format or standard units. VSSTRESC should store all results or findings in character format; if results are numeric, they should also be stored in numeric format in VSSTRESN. For example, if a test has results "NONE", "NEG", and "NEGATIVE" in VSORRES, and these results effectively have the same meaning, they could be represented in standard format in VSSTRESC as "NEGATIVE".', 'Exp'),
('VS', 'VSSTRESN', 'Numeric Result/Finding in Standard Units', 'Num', '', 'Result Qualifier', 'Used for continuous or numeric results or findings in standard format; copied in numeric format from VSSTRESC. VSSTRESN should store all numeric test results or findings.', 'Exp'),
('VS', 'VSSTRESU', 'Standard Units', 'Char', '(VSRESU)', 'Variable Qualifier', 'Standardized unit used for VSSTRESC and VSSTRESN.', 'Exp'),
('VS', 'VSTEST', 'Vital Signs Test Name', 'Char', '(VSTEST)', 'Synonym Qualifier', 'Verbatim name of the test or examination used to obtain the measurement or finding. The value in VSTEST cannot be longer than 40 characters. Examples: "Systolic Blood Pressure", "Diastolic Blood Pressure", "Body Mass Index".', 'Req'),
('VS', 'VSTESTCD', 'Vital Signs Test Short Name', 'Char', '(VSTESTCD)', 'Topic', 'Short name of the measurement, test, or examination described in VSTEST. It can be used as a column name when converting a dataset from a vertical to a horizontal format. The value in VSTESTCD cannot be longer than 8 characters, nor can it start with a number (e.g., "1TEST" is not valid). VSTESTCD cannot contain characters other than letters, numbers, or underscores. Examples: "SYSBP", "DIABP", "BMI".', 'Req'),
('VS', 'VSTPT', 'Planned Time Point Name', 'Char', '', 'Timing', '1. Text description of time when measurement should be taken. 2. This may be represented as an elapsed time relative to a fixed reference point, such as time of last dose. See VSTPTNUM and VSTPTREF. Examples: "Start", "5 min post".', 'Perm'),
('VS', 'VSTPTNUM', 'Planned Time Point Number', 'Num', '', 'Timing', 'Numerical version of VSTPT to aid in sorting.', 'Perm'),
('VS', 'VSTPTREF', 'Time Point Reference', 'Char', '', 'Timing', 'Name of the fixed reference point referred to by VSELTM, VSTPTNUM, and VSTPT. Examples: "PREVIOUS DOSE", "PREVIOUS MEAL".', 'Perm')
;
--
--