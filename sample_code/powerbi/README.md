# POWER BI demonstration using Beat 19 COVID-19 data

Details of the Beat19 study can be found on [here](https://clinicaltrials.gov/ct2/show/NCT04321811).

* [Required software](#required-software)
* [Data import](#data-import)
* [Dashboard](#dashboard)

## Required software
* Microsoft PowerBI Desktop
* R: required for [correlation coefficient visual](https://appsource.microsoft.com/en-us/product/power-bi-visuals/WA104380814?tab=Overview)

### [Power BI Desktop](https://powerbi.microsoft.com/en-us/downloads/)

![powerbi](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/powerbi_installation.PNG)

### [R](https://cran.r-project.org/bin/windows/base/)

![R](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/R.PNG)

### Check if R is installed

![R_installed](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/check_r_version.gif)

## Data import

* connect to PHUSE Open Data Respository ([PODR](https://github.com/phuse-org/PODR/blob/master/documentation/power_bi/NIHPO_PHUSE_PowerBI.pdf)). Note: the walkthrough below doesn't require PODR credentials as they have previously been entered.

![data_import](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/data_import.gif)

## Dashboard

* details of each variable can be found [here](https://github.com/beat19-org/beat19-public-data).

### Number of subjects
* variable: _id

![n_subjs](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_nsubj.gif)

### Number of entries stratified by gender
* variable: gender (Female, Male, Other/Decline to Answer)
* should be labelled sex.

![gender](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_gender.gif)

### Number of entries stratified by hospitalization status
* variable: ble_care_hospitalized (answer to the question: "Have you been or are you currently hospitalized for COVID-19 related symptoms?") renamed to Hospitalized (0/1)
* new column added: Hospitalized (Y/N)

![hosp_status](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_hosp_status.gif)
