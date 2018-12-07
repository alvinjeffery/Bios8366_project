# Bios8366 Final Project: Data Cleaning, Pre-Processing, & Analysis Pipeline  

**Group Members:** Alvin Jeffery, Kim Kondratieff, Patrick Wu  

Student name in parentheses indicates the student who took primary responsibility for the notebook.  

## 1. Create Cohort (Kim)  
> We removed pediatric and psychiatric patients because they are not eligible for the CMS readmission penalty.  

Code File: `base_table_creation.ipynb`  

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `FONNESBECK_ADT_20151202.csv`     | `adt_cms_final.pkl`       |  

## 2. Clean Phenotype, Medications, ICD, and CPT (Alvin)  
> Major cleaning steps include mapping medications to medication classes with RxNorm API calls through helper functions and counted for each day.  ICD and CPT codes were rolled up to chapters (categories) and counted for each day.  

Code File: `descriptives_cpt_icd_meds_phenotype.ipynb`  

| Input                                   | Output(s)                         |
| ---                                     | ---                               |
| `FONNESBECK_phenotype_20151202.csv`     | `phenotype.pkl`                   |
| `FONNESBECK_ICD9_20151202.csv`          | `icd_wide.pkl`                    |
| `FONNESBECK_CPT_20151202.csv`           | `cpt_wide.pkl`                    |
| `FONNESBECK_MED_20151202.csv`           | `med_classes_final_ruids.pkl`     |  


3. **Clean Labs and BMI** (Patrick)  
  * Code: `bios8366_fp_pw_120518.ipynb`  
  * Input:  `FONNESBECK_LAB2_20151202.csv # note "LAB2" instead of original "LAB"`, `FONNESBECK_EGFR_20151202.csv`, `FONNESBECK_BMI_20151202.csv`  
  * Output: `labs.csv`  

4. **Merge All Predictors onto Cohort** (Alvin)  
  * Code: `merging.ipynb`  
  * Input:  `adt_cms_final.pkl`, `phenotype.pkl`, `icd_wide.pkl`, `cpt_wide.pkl`, `med_classes_final_ruids.pkl`, `labs.csv`  
  * Output: `merged.csv`  

5. **Imputation** (Alvin)  
  * Code: `impute.ipynb`  
  * Input: `merged.csv`  
  * Output: `data.pkl`  

6. **Analysis-Bayesian Regression** (Kim)  
  * Code: `bayesian_regression.ipynb`  
  * Input: `data.pkl`  
  * Output: Report only  

7. **Analysis-Random Forest** (Alvin)  
  * Code: `random_forest.ipynb`  


