# -*- coding: utf-8 -*-
"""Final_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GRmrdX79p_XgiI16jf0SpQuWP3DGn1lj

# **Corporate Employee Attrition Analytics**
**Team ID : PNT2022TMID21456**

Project Development Phase - Sprint - 4




**AIM :**


> Explore , Visualise and Analyse the Dataset.

**ABOUT NOTEBOOK:**

**NOTEBOOK SECTIONS:**

> 1) DATA LOADING AND DATA INSIGHTS(SHAPE , COLUMNS ,INFORMATION),


> 2) DATA CLEANING (HANDLING NULL ,DROPPING IRRELEVANT FEATURES),


> 3) DATA VISUALISATION & PLOTTING CORRELATION HEATMAP.


> 4) FEATURE ENGINEERING (HANDING OUTLIERS ,REMOVING IRRELEVANT FEATURES)



> 5) CATEGORICAL VARIABLES ENCODING


> 6) HANDLING DATA IMBALANCE (SMOTE)

> 7) SPLITTING DATA INTO TRAINING AND TESTING SETS

> 8) SCALING DATA USING STANDARDSCALER


> 9) MODEL SELECTION BASED ON CROSS VAL SCORES (SCORING - NEG MEAN SQ ERROR) USING  LOGISTIC REGRESSION , RANDOM FOREST , SUPPORT VECTOR MACHINE ,DECISION TREE


> 10) MODEL OPTIMAL PARAMETER SELECTION USING GRIDCV

> 11) MODEL BUILDING USING ABOVE RESULTS

> 12) ESTIMATING CLASSIFICATION REPORT AND PLOTTING CONFUSION MATRIX

> 13) FINDING MOST IMPORTANT FEATURES OF CLASSIFICATION 



**IMPORTING THE LIBRARIES**
"""

from google.colab import drive
drive.mount('/content/drive')

#GENERAL
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

#FEATURE ENGINEERING
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#MODEL SELECTION
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

#MODEL
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

#MODEL SCORES
from sklearn.metrics import confusion_matrix , accuracy_score ,classification_report

#FEATURE IMPORTANCE
from sklearn.inspection import permutation_importance

path  = '/content/drive/MyDrive/Colab Notebooks/HR-Employee-Attrition.csv'

df =pd.read_csv(path)
df

"""# **Exploratory Data Analysis**"""

df.shape

df.info()

df.select_dtypes('int64' ,'float64').columns

cat_cols = df.select_dtypes('object').columns
cat_cols

df.describe().T

df

"""# ALL CATEGORICAL COLUMNS"""

for cat in cat_cols:
    print(cat ,'-> ' , df[cat].unique())
    print()

print("All columns Unique values count")
for col in df:
    print(col, len(df[col].unique()), sep=': ')

"""# DATA VISUALISATION:

VIEWING AND ANALYSING DATA INSIGHT
"""

plt.figure(figsize =(14,5))
plt.subplot(1,2,1)
sns.countplot(df['Attrition'] ,color ='b' ,hue =df['Gender'])
plt.title('Attrition by Gender')
plt.subplot(1,2,2)
plt.pie(df['Attrition'].value_counts() ,colors =['r' ,'c'] ,explode =[0,0.1]  ,autopct = '%.2f' ,labels =['No' ,'Yes'])

plt.title('Attrition')

"""We observe a very high data imbalance here so we'll use Sampling technique to balance it,"""

plt.figure(figsize =(16 ,4))
plt.subplot(1,3,1)
sns.distplot(df['Age'] ,color ='m')
plt.title('Age')
plt.subplot(1 , 3 ,2)
sns.stripplot(x = 'Gender' ,y = 'Age' ,data = df ,palette="Set2")
plt.title('Gender vs Age')
plt.subplot(1,3,3)
sns.countplot('Gender' ,data = df ,color ='c')
plt.title('Gender')
plt.tight_layout()

plt.figure(figsize = (14 , 13))
plt.subplot(2 ,1,1)
sns.countplot(y= 'JobRole' ,data = df ,palette='winter_r')
plt.title('JOB ROLE')
plt.subplot(2,1,2)
sns.countplot(y= 'JobRole' ,data = df ,palette='winter_r'  ,hue =df['Attrition'])

plt.figure(figsize =(14,5))
plt.subplot(1,2,1)
sns.countplot('Department' ,data = df ,hue ='Attrition' ,palette='gist_rainbow_r')
plt.subplot(1,2,2)
plt.pie(df['Department'].value_counts() ,autopct ='%.2f' ,colors = ['r' ,'c' ,'g'],labels =['Research & Development','Sales', 'Human Resources'] ,explode =[0 ,0.1,0])

#HANDLING CATEGORICAL OUTPUT VARIABLE
df['Attrition'].replace({'Yes':1 ,'No':0} ,inplace = True)
df['Attrition'].head()

plt.figure(figsize =(14 ,10))
plt.subplot(2,2,1)
sns.countplot(df['JobSatisfaction'] ,hue =df['Attrition'] ,palette='Accent_r')
plt.subplot(2,2,2)
sns.countplot(df['EnvironmentSatisfaction'] ,hue =df['Attrition'] ,palette='Accent')
plt.subplot(2,2,3)
sns.countplot(df['JobInvolvement'] ,hue =df['Attrition'] ,palette='brg_r')
plt.subplot(2,2,4)
sns.countplot(df['PerformanceRating'] ,hue =df['Attrition'] ,palette='twilight_r')

plt.figure(figsize =(20 ,8))
sns.boxplot(x ='JobRole', y = 'MonthlyIncome' ,data = df ,hue ='Attrition' ,color ='red')

plt.figure(figsize =(12,10))
plt.subplot(2,1,1)
sns.boxplot(x = 'MaritalStatus' ,y ='RelationshipSatisfaction' ,data = df ,hue = 'Attrition', color = 'g')
plt.subplot(2,1,2)
sns.boxplot(df['JobLevel'],df['MonthlyIncome'] ,hue = df['Attrition'] ,palette='Reds_r')

col = ['YearsInCurrentRole' ,'YearsSinceLastPromotion' ,'YearsWithCurrManager' ,'YearsAtCompany']
plt.figure(figsize = (10 ,10))
for i,c in enumerate(col):
    plt.subplot(2 ,2,i+1)
    sns.distplot(df[c] ,color ='b')

"""# CORRELATION MATRIX"""

plt.figure(figsize = (16 ,16))
sns.heatmap(df.corr() ,cmap = 'ocean' , cbar = True , annot = True)

"""# FEATURE ENGINEERING
REMOVING IRRELEVANT FEATURES
"""

no_use = []
for col in df.columns:
    if(len(df[col].unique()) ==1):
        no_use.append(col)
no_use

df.drop(columns = no_use , axis = 1 , inplace = True)

df.columns

"""### BINARY FEATURES ENCODING"""

y_n_type = []
others =[]
for col in df.select_dtypes('object').columns:
    if(len(df[col].unique()) ==2):
        y_n_type.append(col)
        
y_n_type

df['Gender'].replace({'Male':1 ,'Female':0} ,inplace = True)
df['OverTime'].replace({'Yes':1 ,'No':0} ,inplace = True)

"""CATEGORICAL FEATURES ENCODING"""

others = df.select_dtypes('object').columns
others

le = LabelEncoder()
for col in others:
    df[col] = le.fit_transform(df[col])

df.select_dtypes('object').columns

"""SPLITTING DATASET INTO FEATURES -> X AND TARGET -> Y"""

x = df.drop('Attrition' ,axis =1)
y = df['Attrition']

print(x.shape ,y.shape)

"""HANDLING CLASS IMBALANCE

> About 84 % of data are of class label 0 and only 16 % of data are of class label 1.
This creates Class Imbalance.
It is necessary to remove because even if we create a classifier which everytime predicts Attrition as 'No' will also achieve an overall accuracy of 84%, which is meaningless.
"""

sns.countplot(df['Attrition'])

(df.Attrition.value_counts()/1470)*100

smote = SMOTE(sampling_strategy='minority')
x ,y = smote.fit_resample(x ,y)

print(x.shape ,y.shape)

#now balanced
y.value_counts()
sns.countplot(y ,palette='viridis')
plt.title('Now Class is Balanced')

"""**SPLITTING DATA INTO TRAINING AND TESTING SETS**"""

x_train , x_test , y_train ,y_test = train_test_split(x , y, test_size=0.2 , random_state= 52)
print(x_train.shape)

"""**SCALING THE DATA**"""

#scaling the data 
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


x_train

"""## **MODEL SELECTION**

**CROSS VALIDATION**
"""

k = KFold(n_splits = 5)

"""**LOGISTIC REGRESSION**"""

lr_model = LogisticRegression()
lr_score = cross_val_score(lr_model , x_train , y_train ,cv = k ,scoring = 'neg_mean_squared_error')
lr_score.mean()

"""**RANDOM FOREST CLASSIFIER**"""

rf_model = RandomForestClassifier()
rf_score = cross_val_score(rf_model , x_train , y_train ,cv = k ,scoring = 'neg_mean_squared_error')
rf_score.mean()

"""**SUPPORT VECTOR MACHINE CLASSIFIER**"""

svm_model = SVC()
svm_score = cross_val_score(svm_model , x_train , y_train ,cv = k ,scoring = 'neg_mean_squared_error')
svm_score.mean()

"""**DECISION TREE CLASSIFIER**"""

dt_model = DecisionTreeClassifier()
dt_score = cross_val_score(dt_model , x_train , y_train ,cv = k ,scoring = 'neg_mean_squared_error')
dt_score.mean()

plt.figure(figsize = (14 , 6))
plt.subplot(1,2,1)
x = ['Logistic Regression','Random Forest' ,'Support Vector' ,'Decision Tree']
y = [lr_score.mean() , rf_score.mean() ,svm_score.mean() , dt_score.mean()]
plt.title('Neg Mean square error for Models')
sns.barplot(y,x,palette="viridis")

plt.subplot(1,2,2)
plt.plot(x ,y,marker = 'o' ,color = 'r',mfc ='b' ,ms =8 )
plt.title('Neg Mean square error')

"""**OBSERVATIONS**

> WE OBTAINED LESS -VE MEAN SQ ERROR FOR BOTH RFC AND SVC (NEARLY SAME)
LETS TRY OPTIMAL PARAMETER TEST FOR BOTH

**MODEL OPTIMAL PARAMETER SELECTION USING GRID SEARCH CV**
"""

#we obtained less less -ve mena sq error for SVC and random forest 
#lets try building model with both of them

model_params ={
    'RandomForestClassifier':
    {
        'model':RandomForestClassifier(),
        'param':
        {
         'n_estimators':[10 ,50 ,100,130],
         'criterion':['gini' ,'entropy'],
         'max_depth':range(4,8,1),
         'max_features':['auto' ,'log2']
        }
    },
    'SVC':
    {
        'model':SVC(),
        'param':
        {
            'C':[1,20],
            'gamma':[1,0.1],
            'kernel':['rbf']     
        }
    }
}

scores =[]
for model_name , mp in model_params.items():
    model_sel = GridSearchCV(estimator= mp['model'] ,param_grid= mp['param'] ,cv = 4 ,return_train_score=False)
    model_sel.fit(x_train,y_train)
    
    scores.append({
        'model':model_name,
        'best_score':model_sel.best_score_,
        'best_params':model_sel.best_params_
    })
scores

"""# ***MODEL BUILIDNG***

**SELECTED MODEL -> SVC MODEL**
"""

svm_model = SVC(C=20 ,gamma=0.1 ,kernel='rbf')
svm_model.fit(x_train ,y_train)
ytest_pred = svm_model.predict(x_test)
ytrain_pred = svm_model.predict(x_train)
accuracy_score(y_test ,ytest_pred)

"""**MODEL SCORES REPORT**"""

print(classification_report(y_test , ytest_pred))

print(classification_report(y_train , ytrain_pred))

"""# ***CONFUSION MATRIX***"""

sns.heatmap(confusion_matrix(y_test ,ytest_pred) ,annot = True ,cmap ='ocean')

sns.heatmap(confusion_matrix(y_train ,ytrain_pred) ,annot = True ,cmap ='Spectral_r')

"""# ***DETERMINING FEATURE IMPORTANCE***"""

from sklearn.inspection import permutation_importance
perm_importance = permutation_importance(svm_model, x_test, y_test)

perm_importance

perm_importance.importances_mean

df.columns

cols = ['Age', 'BusinessTravel', 'DailyRate', 'Department',
       'DistanceFromHome', 'Education', 'EducationField', 'EmployeeNumber',
       'EnvironmentSatisfaction', 'Gender', 'HourlyRate', 'JobInvolvement',
       'JobLevel', 'JobRole', 'JobSatisfaction', 'MaritalStatus',
       'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'OverTime',
       'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
       'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
       'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
       'YearsSinceLastPromotion', 'YearsWithCurrManager']
    
features = np.array(cols)
plt.figure(figsize = (14 ,10))    
sorted_idx = perm_importance.importances_mean.argsort()
sns.barplot( perm_importance.importances_mean[sorted_idx] ,features[sorted_idx] )
plt.xlabel("Permutation Importance")

plt.title('FEATURE IMPORTANCE')
