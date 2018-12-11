# Bios8366 Final Project: Data Cleaning, Pre-Processing, & Analysis Pipeline  

**Group Members:** Alvin Jeffery, Kim Kondratieff, Patrick Wu  

Student name in parentheses indicates the student who took primary responsibility for the notebook.  

## 1. Create Cohort (Kim)  
> We removed pediatric and psychiatric patients because they are not eligible for the CMS readmission penalty.  

Code File: `base_table_creation.ipynb`  

| Input                                 | Output(s)                 |
| ---                                   | ---                       |
| `FONNESBECK_ADT_20151202.csv`         | `adt_cms_final.pkl`       |
| `FONNESBECK_phenotype_20151202.csv`   |                           |
| `FONNESBECK_CPT_20151202.csv`         |                           |  

## 2. Clean Phenotype, Medications, ICD, and CPT (Alvin)  
> Major cleaning steps include mapping medications to medication classes with RxNorm API calls through helper functions and counted for each day.  ICD and CPT codes were rolled up to chapters (categories) and counted for each day.  

Code File: `descriptives_cpt_icd_meds_phenotype.ipynb`  

| Input                                   | Output(s)                         |
| ---                                     | ---                               |
| `FONNESBECK_phenotype_20151202.csv`     | `phenotype.pkl`                   |
| `FONNESBECK_ICD9_20151202.csv`          | `icd_wide.pkl`                    |
| `FONNESBECK_CPT_20151202.csv`           | `cpt_wide.pkl`                    |
| `FONNESBECK_MED_20151202.csv`           | `med_classes_final_ruids.pkl`     |  


## 3. Clean Labs and BMI (Patrick)  
> `adt_cms_final.pkl` = output from `base_table_creation.ipynb` that contains cohort information. `labs_cleaned.csv` = has columns ['ruid','lab_name','lab_date','lab_value','visit_id','hospital_day'] for 19 top labs by total count. I identified outliers in the original labs contained in `FONNESBECK_LAB_20151202.csv` by looking at the 1%, 99% of values, distribution, and looking at normal values in adults. Outliers were converted to 'NaN' for imputation in `impute.ipynb`.    

Code File: `bios8366_fp_pw_120518.ipynb`   
  
| Input                                         | Output(s)                 |
| ---                                           | ---                       |
| `FONNESBECK_LAB_20151202.csv`                 | `labs.csv`                |
| `adt_cms_final.pkl`                           |                           |

Code File: `bios8366_fp_pw_120518.ipynb`

## 4. Merge All Predictors onto Cohort (Alvin)  
> Thie notebook combines the work from (1), (2), and (3) above into a single flat-file for descriptive statistics, imputation, and analysis.  

Code File: `merging.ipynb`  
  
| Input                             | Output(s)                 |
| ---                               | ---                       |
| `adt_cms_final.pkl`               | `merged.csv`              |
| `phenotype.pkl`                   |                           |
| `icd_wide.pkl`                    |                           |
| `cpt_wide.pkl`                    |                           |
| `med_classes_final_ruids.pkl`     |                           |
| `labs.csv`                        |                           |  

## 5. Descriptive Statistics (Patrick)  
> Description goes here  

Code File: `description.ipynb`

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `merged.csv`                      | Report Only               |  


## 6. Imputation (Alvin)  
> This R-based notebook uses `Hmisc::transcan()` to provide a single imputation of the data.  There is also a review of potentially redundant variables that could be exluded in the regression analysis.  

Code File: `impute.ipynb`

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `merged.csv`                      | `train_imputed.csv`       |
|                                   | `valid_imputed.csv`       |  
|                                   | `test_imputed.csv`        |  

## 7. Analysis-Bayesian Regression (Kim)  
> Description goes here  

Code File: `bayesian_regression.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| INSERT HERE                     | Report Only               |  


## 8. Analysis-Machine Learning (Alvin)  
> Using hyperopt to explore the ideal classification algorithm(s) and best hyperparameters, this notebook identifies potential machine learning approaches for predicting 30-day readmissions.  

Code File: `machine_learning.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| `train_imputed.csv`             | Report Only               |
| `valid_imputed.csv`             |                           |
| `test_imputed.csv`              |                           |  


