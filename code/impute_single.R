# send to ACCRE
# scp /Volumes/AlvinSD/Bios8366_project/data/merged.csv jeffead1@login.accre.vanderbilt.edu:/home/jeffead1/Bios8366_project/data/
# scp /Volumes/AlvinSD/Bios8366_project/code/impute_single.R jeffead1@login.accre.vanderbilt.edu:/home/jeffead1/Bios8366_project/code/

# performa a single imputation using Hmisc::transcan()

library(Hmisc); library(dplyr); library(stringr)

#### Load Data ####

# local directory
dir <- '/Volumes/AlvinSD/Bios8366_project/'

# ACCRE directory
#dir <- '/home/jeffead1/Bios8366_project/'

df = read.csv(paste(dir, 'data/merged.csv', sep=''))

df <- select(df, -ruid, -visit_id, -admit_date, -discharge_date,
                 -readmit_time, -total_encounters, -dob, -dod)

train <- filter(df, group=='train') %>% select(-group)
valid <- filter(df, group=='valid') %>% select(-group)
test <- filter(df, group=='test') %>% select(-group)

#### VALIDATION set ####

# ensure all variables have appropriate R structures
valid$sex <- as.factor(valid$sex)
valid$race <- as.factor(valid$race)
#valid$pregnancy_indicator <- as.factor(valid$pregnancy_indicator)
valid$readmit_30d <- as.factor(valid$readmit_30d)

# function to vectorize median imputation 
med_imp <- function(x) {
  if (is.numeric(x)) {
    x <- as.numeric(impute(x, fun=median))
  }
  else {
    x <- as.factor(x)
  }
}

valid_imp <- data.frame(lapply(valid, FUN=med_imp))

#### TEST set ####

# ensure all variables have appropriate R structures
test$sex <- as.factor(test$sex)
test$race <- as.factor(test$race)
#test$pregnancy_indicator <- as.factor(test$pregnancy_indicator)
test$readmit_30d <- as.factor(test$readmit_30d)

test_imp <- data.frame(lapply(test, FUN=med_imp))


#### TRAINING set ####

# ensure all variables have appropriate R structures
train$sex <- as.factor(train$sex)
train$race <- as.factor(train$race)
#train$pregnancy_indicator <- as.factor(train$pregnancy_indicator)

# include outcome variable in imputation
train$readmit_30d <- as.factor(train$readmit_30d)


# convert all predictors into R formula
vars <- paste(names(train), collapse=' + ')
formula <- as.formula(paste('~', vars))

# perform single imputation using transformed variables & canonical correlation
single_imp <- transcan(formula,
                       categorical=c('readmit_30d', 'sex', 'race'), #, 'pregnancy_indicator'),
                       
                       eps=0.2, # increase to speed up convergence (default=0.1)
                       iter.max=1000, # prevent early stopping
                       #rhsImp='random', # as opposed to 'mean' only runs 5 iterations
                       
                       # variables with fewer than 3 unique knots
                       asis=c('icd_dx_perinatal', 'icd_dx_skin'),
                       transformed=TRUE, 
                       imputed=TRUE, 
                       # if wanting multiple imputations rather than a single:
                       #n.impute=5, 
                       show.na=TRUE, 
                       pl=F, 
                       data=train)

# save transcan object due to long run-time
save(single_imp, file=paste(dir, 'data/single_imputation_training.RData', sep=''))

# impute train data with transcan() object
train_imp <- data.frame(impute.transcan(single_imp, data=train, list.out=T))

#### Save Imputed Datasets ####
write.csv(train_imp, file=paste(dir, 'data/train_imputed.csv', sep=''))
write.csv(valid_imp, file=paste(dir, 'data/valid_imputed.csv', sep=''))
write.csv(test_imp, file=paste(dir, 'data/test_imputed.csv', sep=''))

# retrieve from ACCRE
# scp jeffead1@login.accre.vanderbilt.edu:/home/jeffead1/Bios8366_project/data/train_imputed.csv /Volumes/AlvinSD/Bios8366_project/data/
# scp jeffead1@login.accre.vanderbilt.edu:/home/jeffead1/Bios8366_project/data/valid_imputed.csv /Volumes/AlvinSD/Bios8366_project/data/
# scp jeffead1@login.accre.vanderbilt.edu:/home/jeffead1/Bios8366_project/data/test_imputed.csv /Volumes/AlvinSD/Bios8366_project/data/
