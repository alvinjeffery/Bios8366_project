# Bios8366 Final Project  

**Group Members:** Alvin Jeffery, Kim Kondratieff, Patrick Wu  

## Data Cleaning, Pre-Processing, & Analysis Pipeline  

Student name in parentheses indicates the student who took primary responsibility for the notebook.  

1. **Create Cohort** (Kim): 
  * Code File: `base_table_creation.ipynb`  

We removed pediatric and psychiatric patients because they are not eligible for the CMS readmission penalty.  

  * Input Data: `FONNESBECK_ADT_20151202.csv`  
  * Output Data: `adt_cms_final.pkl`  


2. **Clean Phenotype, Medications, ICD, and CPT** (Alvin)
  * Code File: `descriptives_cpt_icd_meds_phenotype.ipynb`  
  * Input Data: `FONNESBECK_phenotype_20151202.csv`, `FONNESBECK_ICD9_20151202.csv`, `FONNESBECK_CPT_20151202.csv`, `FONNESBECK_MED_20151202.csv`  
  * Output Data: `phenotype.pkl`, `icd_wide.pkl`, `cpt_wide.pkl`, `med_classes_final_ruids.pkl`  

3. Clean (Patrick): `bios8366_fp_pw_120518.ipynb`  
  * Input:  
```
FONNESBECK_LAB2_20151202.csv # note "LAB2" instead of original "LAB"
FONNESBECK_EGFR_20151202.csv
FONNESBECK_BMI_20151202.csv
```
  * Output: `labs.csv`  

4. Merge All Predictors onto Cohort (Alvin): `merging.ipynb`  
  * Input:  
```
adt_cms_final.pkl  
phenotype.pkl  
icd_wide.pkl  
cpt_wide.pkl  
med_classes_final_ruids.pkl
labs.csv
```
  * Output: `merged.csv`  

5. Imputation (Alvin): `impute.ipynb`  
  * Input: `merged.csv`  
  * Output: `data.pkl`  

6. Analysis-Bayesian Regression (Kim): `bayesian_regression.ipynb`  
  * Input: `data.pkl`  
  * Output: Report only  

7. Analysis-Random Forest (Alvin): `random_forest.ipynb`  


