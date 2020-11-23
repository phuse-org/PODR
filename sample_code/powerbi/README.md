# POWER BI demonstration using Beat 19 COVID-19 data

Details of the Beat19 study can be found on [here](https://clinicaltrials.gov/ct2/show/NCT04321811).

* [Required software](#required-software)
* [Data import](#data-import)
* [Step by step tutorial](#step-by-step-tutorial)
* [Exploration](#exploration)

## Required software
* Microsoft PowerBI Desktop
* R: required for visualizing heatmap of correlation coefficients

### [Power BI Desktop](https://powerbi.microsoft.com/en-us/downloads/)

![powerbi](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/powerbi_installation.PNG)

### [R](https://cran.r-project.org/bin/windows/base/)

![R](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/R.PNG)

### Check if R is installed

![R_installed](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/check_r_version.gif)

## Data import

* connect to PHUSE Open Data Respository ([PODR](https://github.com/phuse-org/PODR/blob/master/documentation/power_bi/NIHPO_PHUSE_PowerBI.pdf)). Note: the walkthrough below doesn't require PODR credentials as they have previously been entered.

![data_import](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/data_import.gif)

## Step by step tutorial

* walkthroughs of a few visual can be found below. The completed dashboard can be found in the [.pbix file](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/beat19_dashboard.pbix).
* details of each variable can be found [here](https://github.com/beat19-org/beat19-public-data).

### 1) Number of subjects
* variable: _id

![n_subjs](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_nsubj.gif)

### 2) Number of entries stratified by gender
* variable: gender (Female, Male, Other/Decline to Answer)
* should be labelled sex?

![gender](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_gender.gif)

### 4) Number of entries stratified by hospitalization status
* variable: ble_care_hospitalized (answer to the question: "Have you been or are you currently hospitalized for COVID-19 related symptoms?") renamed to Hospitalized (0/1)
* new column added: Hospitalized (Y/N)

![hosp_status](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_hosp_status.gif)

### 5) Average symptom severity based on symptom-type

![symptoms](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_symptoms.gif)

### 6) Age groups

![age](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_age.gif)

### 7) Correlation between symptom severities

![corr](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_corr.gif)

### 8) Edit interactions
* filter visualizations based on selection on other visuals

![interactions](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_edit_interactions.gif)

## Exploration

1. Explore hospitalization status by gender.

![demo1](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_demo1.gif)

2. Visual correlation between symptoms based on age group per hospitalization group.

![demo2](https://github.com/singha53/PODR/blob/master/sample_code/powerbi/screenshots/dashboard_demo2.gif)
