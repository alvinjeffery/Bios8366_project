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
> Description goes here  

Code File: `bios8366_fp_pw_120518.ipynb`   
  
| Input                                         | Output(s)                 |
| ---                                           | ---                       |
| `FONNESBECK_LAB2_20151202.csv` # note LAB2    | `labs.csv`       |
| `FONNESBECK_EGFR_20151202.csv`                |                           |
| `FONNESBECK_BMI_20151202.csv`                 |                           |  

## 4. Merge All Predictors onto Cohort (Alvin)  
> Descriptions goes here  

Code File: `merging.ipynb`  
  
| Input                             | Output(s)                 |
| ---                               | ---                       |
| `adt_cms_final.pkl`               | `merged.csv`              |
| `phenotype.pkl`                   |                           |
| `icd_wide.pkl`                    |                           |
| `cpt_wide.pkl`                    |                           |
| `med_classes_final_ruids.pkl`     |                           |
| `labs.csv`                        |                           |  

## 5. Imputation (Alvin)  
> Description goes here  

Code File: `impute.ipynb`

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `merged.csv`                      | `train_imputed.csv`       |
|                                   | `valid_imputed.csv`       |  
|                                   | `test_imputed.csv`        |  

## 6. Analysis-Bayesian Regression (Kim)  
> Description goes here  

Code File: `bayesian_regression.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| INSERT HERE                     | Report Only               |  


## 7. Analysis-Random Forest (Alvin)  
> Description goes here  

Code File: `random_forest.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| `train_imputed.csv`             | Report Only               |
| `valid_imputed.csv`             |                           |
| `test_imputed.csv`              |                           |  


