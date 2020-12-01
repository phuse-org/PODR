![PHUSE PODR Logo Logo](/PODR.jpeg)
# PODR - Sample Code

Here you can find sample code to use with the PODR platform.

## C

## C#
[C# sample - NOT finished yet.](/sample_code/PHUSE_PODR.csharp)

## Java
[Java sample](/sample_code/PHUSE_PODR.java)

## Python
[Python3 sample](/sample_code/PHUSE_PODR.py)

## R
Hanming Tu at Frontage Labs has created (November 2020) a R Shiny app for accessing PODR: 
[Live demo](https://geotiger.shinyapps.io/01_podr/) {Please contact [Jose C. Lacal](mailto:Jose.Lacal@NIHPO.com) for a username and password.
[CRAN package] (https://cran.rstudio.com/web/packages/podr/index.html) and available for everyone to download. 
[About podr package] (https://cran.rstudio.com/web/packages/podr/vignettes/about-podr.html)


## SAS

## CDISC ADaM
These files contain Synthetic Data that matches the specifications of CDISC's ADaM format:

[Synthetic Data for 10 subjects](/sample_code/ADaM_SyntData_10.csv)

[Synthetic Data for 100 subjects](/sample_code/ADaM_SyntData_100.csv)

[Synthetic Data for 300 subjects](/sample_code/ADaM_SyntData_300.csv)

## SQLite3 file to generate Synthetic Health Data
This [SQLite3 file](/sample_code/Synthetic_Health_Data_NIHPO.sqlite3) includes data from the following sources:

a.) "Therapeutic Area User Guide TA Specifications" from CDISC's website [https://www.cdisc.org/standards/therapeutic-areas]. 
The following Excel files were processed and records from these sheets were extracted: 'Domains' and 'Variables'.
* Breast Cancer
* CDAD
* Colorectal Cancer
* Diabetic Kidney Disease
* Duchenne Muscular Dystrophy
* Dyslipidemia
* Ebola
* Hepatitis C
* HIV
* Huntington's Disease
* Influenza
* Kidney Transplant
* Lung Cancer
* Major Depressive Disorder
* Malaria
* Multiple Sclerosis
* Nutrition
* Pain
* Post Traumatic Stress Disorder
* Prostate Cancer
* Rheumatoid Arthritis
* Schizophrenia
* Traditional Chinese Medicine - Coronary Artery Disease-Angina
* Tuberculosis
* Vaccines
* Virology


b.) CDISC Terminology files. Downloaded from Source: https://www.cancer.gov/research/resources/terminology/cdisc

This SQLite3 file can be used to programmatically generate Synthetic Health Data that complies with CDISC's specifications.

## Contact
Please contact [Jose C. Lacal](mailto:Jose.Lacal@NIHPO.com) if you'd like to contribute your own code snippets for other PHUSE members to use.