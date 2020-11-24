# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:31:07 2020

@author: Manika
"""

import pandas as pd

df1 = pd.read_csv("glassdoor_jobs.csv")

#-----SALARY COLUMN------------------------------------------------------------

#Remove negative salary from the salary Estimate
df1 = df1.loc[df1["Salary Estimate"]!="-1"]

#Removing the glassdoor company name from the salary column
salary = df1["Salary Estimate"].apply(lambda x: x.split("(")[0])

#Removing the "K" and "$" sign from the salary column
minus_kd = salary.map(lambda x: x.replace("K","").replace("$",""))
minus_kd_edit = minus_kd.map(lambda x: x.lower().replace("per hour", "").replace("employer provided salary:",""))

#------------------------------------------------------------------------------


#------------------ COMPANY NAME COLUMN ---------------------------------------
df1["Company name"] = df1.apply(lambda x: x["Company Name"] if x["Rating"]<0 else x["Company Name"][:-3], axis=1)
#------------------------------------------------------------------------------

#------------------ LOCATION --------------------------------------------------
df1["Company State"] = df1["Location"].apply(lambda x: x.split(",")[1])
comp_no_dict = dict(df1["Company State"].value_counts())
print(comp_no_dict)
#------------------------------------------------------------------------------


#Adding column in main dataframe
df1["Hourly"] = df1["Salary Estimate"].apply(lambda x: 1 if "Per Hour" in x else 0)
df1["Employer_provided"] = df1["Salary Estimate"].apply(lambda x: 1 if "employer provided salary:" in x.lower() else 0)
df1["Min salary"] = minus_kd_edit.apply(lambda x: x.split("-")[0]).astype('int')
df1["Max Salary"] = minus_kd_edit.apply(lambda x: x.split("-")[1]).astype("int")
df1["Average Salary"] = (df1["Min salary"] + df1["Max Salary"])/2
df1["Same state"] = df1.apply(lambda x: 1 if x["Location"]==x["Headquarters"] else 0, axis=1)
df1["Company age"] = df1["Founded"].apply(lambda x: x if x<0 else 2020-x)

df1.drop(["Unnamed: 0"], axis=1, inplace=True)

df1.to_csv("Glass")