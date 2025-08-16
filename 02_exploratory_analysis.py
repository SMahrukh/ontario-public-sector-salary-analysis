#!/usr/bin/env python
# coding: utf-8

# In[83]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[84]:


df = pd.read_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\clean\salary_clean")


# In[85]:


df.info()


# In[86]:


df.describe().T


# In[87]:


df['salary_text'] = df['salary'].astype(str)


# In[88]:


df['salary_text']


# In[89]:


df['salary'] = (df['salary_text']
                  .str.replace(r'[\$,]', '', regex=True)
                  .str.replace('\u00A0','')     # non-breaking space (sometimes sneaks in)
                  .str.replace('\u202F',''))    # narrow non-breaking space
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
df['salary']


# In[90]:


df['total_comp'] = df['salary'] + df['benefits']
df['total_comp']


# In[91]:


print("Rows, Cols:", df.shape)
print(list(df.columns))
df[['salary','benefits','total_comp']].describe(percentiles=[.1,.25,.5,.75,.9,.95,.99]).T


# # Salary Percentiles

# In[92]:


percentiles = [0.1,0.25,0.5,0.75,0.9,0.95,0.99]
pd.DataFrame({
    "percentile": [int(p*100) for p in percentiles],
    "salary": np.quantile(df['salary'], percentiles),
    "total_comp": np.quantile(df['total_comp'], percentiles)
})


# # Sector Overview

# In[93]:


sector_agg = (df.groupby('sector', as_index=False)
                .agg(emp_count=('sector','size'),
                     median_salary=('salary','median'),
                     mean_salary=('salary','mean'),
                     median_benefits=('benefits','median'),
                     total_payroll=('salary','sum'))
                .sort_values('emp_count', ascending=False))
sector_agg.head(15)


# # Employers Organisation

# In[94]:


employer_agg = (df.groupby('employer', as_index=False)
                  .agg(emp_count=('employer','size'),
                       median_salary=('salary','median'),
                       mean_salary=('salary','mean'),
                       total_payroll=('salary','sum')))

top_emp_by_count = employer_agg.sort_values('emp_count', ascending=False).head(20)
top_emp_by_count[['employer','emp_count','median_salary','total_payroll']]

top_emp_by_payroll = employer_agg.sort_values('total_payroll', ascending=False).head(20)
top_emp_by_payroll[['employer','emp_count','median_salary','total_payroll']]


# # Job titles (role-level view)

# In[95]:


df['job_title_norm'] = df['job_title'].str.strip()

title_agg = (df.groupby('job_title_norm', as_index=False)
               .agg(emp_count=('job_title_norm','size'),
                    median_salary=('salary','median'),
                    p90_salary=('salary', lambda s: np.percentile(s,90)),
                    mean_benefits=('benefits','mean'))
               .sort_values('emp_count', ascending=False))

# Most common roles
title_agg.head(25)

# Highest median salary among “material” titles (avoid tiny groups)
title_agg[title_agg['emp_count']>=30].sort_values('median_salary', ascending=False).head(25)


# # Individuals at the top (total comp)

# In[96]:


top_people = df.sort_values('total_comp', ascending=False).head(25)
top_people[['full_name','employer','job_title','salary','benefits','total_comp']]


# # Outliers

# In[97]:


salary_z = (df['salary'] - df['salary'].mean()) / df['salary'].std()
outliers = df.loc[salary_z > 4].sort_values('salary', ascending=False)[
    ['full_name','employer','job_title','salary','benefits']]
outliers.head(10)


# # Saving the tables

# In[98]:


sector_agg.to_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\outputs\sector_summary.csv", index=False)
employer_agg.to_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\outputs\employer_summary.csv", index=False)
title_agg.to_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\outputs\title_summary.csv", index=False)
top_people.to_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\outputs\top_people.csv", index=False)


# # Import library for visualization

# In[99]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

get_ipython().run_line_magic('matplotlib', 'inline')


# In[100]:


fig, ax = plt.subplots()
sns.histplot(df["salary"], bins=60, kde=True, ax=ax)
ax.set_title("Salary Distribution (2024)")
ax.set_xlabel("Salary"); ax.set_ylabel("Count")


# # Salary buckets

# In[101]:


bins = [100_000,125_000,150_000,200_000,250_000,300_000,400_000,500_000,1_000_000, df["salary"].max()]
labels = ["100–125k","125–150k","150–200k","200–250k","250–300k","300–400k","400–500k","500k–1M",">1M"]
df["salary_bucket"] = pd.cut(df["salary"], bins=bins, labels=labels, include_lowest=True)

bucket_counts = df["salary_bucket"].value_counts().sort_index()
fig, ax = plt.subplots()
bucket_counts.plot(kind="bar", ax=ax)
ax.set_title("Employees by Salary Bucket")
ax.set_xlabel("Salary bucket"); ax.set_ylabel("Employees")


# # Benefits & Benefits Share

# In[102]:


df["benefit_share"] = np.where(df["salary"] > 0, df["benefits"]/df["salary"], np.nan)

fig, ax = plt.subplots()
sns.histplot(df["benefits"], bins=60, kde=True, ax=ax)
ax.set_title("Benefits Distribution")
ax.set_xlabel("Benefits"); ax.set_ylabel("Count")

fig, ax = plt.subplots()
sns.histplot(df["benefit_share"].clip(upper=1), bins=50, kde=True, ax=ax)
ax.set_title("Benefit Share of Salary (clipped at 1)")
ax.set_xlabel("Benefits / Salary"); ax.set_ylabel("Count")


# # Sectors — who’s big, who pays what

# In[103]:


sector_agg = (df.groupby("sector", as_index=False)
                .agg(emp_count=("sector","size"),
                     median_salary=("salary","median"),
                     mean_salary=("salary","mean"),
                     total_payroll=("salary","sum"))
                .sort_values("emp_count", ascending=False))

# Top sectors by headcount
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(data=sector_agg.head(15), x="emp_count", y="sector", ax=ax)
ax.set_title("Top Sectors by Employee Count")
ax.set_xlabel("Employees"); ax.set_ylabel("Sector")

# Median salary by sector (limit to largest 15 for readability)
top15 = sector_agg.head(15).sort_values("median_salary", ascending=False)
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(data=top15, x="median_salary", y="sector", ax=ax)
ax.set_title("Median Salary by Sector (Top 15 by Count)")
ax.set_xlabel("Median salary"); ax.set_ylabel("Sector")


# # Employers — biggest and spendiest

# In[104]:


employer_agg = (df.groupby("employer", as_index=False)
                  .agg(emp_count=("employer","size"),
                       median_salary=("salary","median"),
                       total_payroll=("salary","sum")))

# Top 20 by headcount
top_emp_count = employer_agg.sort_values("emp_count", ascending=False).head(20)
fig, ax = plt.subplots(figsize=(8,8))
sns.barplot(data=top_emp_count, x="emp_count", y="employer", ax=ax)
ax.set_title("Top 20 Employers by Employee Count")
ax.set_xlabel("Employees"); ax.set_ylabel("Employer")


# Top 20 by total payroll
top_emp_payroll = employer_agg.sort_values("total_payroll", ascending=False).head(20)
fig, ax = plt.subplots(figsize=(8,8))
sns.barplot(data=top_emp_payroll, x="total_payroll", y="employer", ax=ax)
ax.set_title("Top 20 Employers by Total Payroll")
ax.set_xlabel("Total salary spend"); ax.set_ylabel("Employer")


# # Job titles — common and high-paying

# In[105]:


df["job_title_norm"] = df["job_title"].str.strip()

title_agg = (df.groupby("job_title_norm", as_index=False)
               .agg(emp_count=("job_title_norm","size"),
                    median_salary=("salary","median"))
               .sort_values("emp_count", ascending=False))

# Most common titles
fig, ax = plt.subplots(figsize=(8,10))
sns.barplot(data=title_agg.head(25), x="emp_count", y="job_title_norm", ax=ax)
ax.set_title("Top 25 Job Titles by Count")
ax.set_xlabel("Employees"); ax.set_ylabel("Job Title")

# Highest median salary among titles with at least 30 records
material_titles = title_agg[title_agg["emp_count"] >= 30].sort_values("median_salary", ascending=False).head(25)
fig, ax = plt.subplots(figsize=(8,10))
sns.barplot(data=material_titles, x="median_salary", y="job_title_norm", ax=ax)
ax.set_title("Top Titles by Median Salary (min 30 employees)")
ax.set_xlabel("Median salary"); ax.set_ylabel("Job Title")


# # Salary by Sector

# In[106]:


top10_sectors = sector_agg.sort_values("emp_count", ascending=False)["sector"].head(10)
fig, ax = plt.subplots(figsize=(10,6))
sns.boxplot(data=df[df["sector"].isin(top10_sectors)], x="sector", y="salary", ax=ax)
ax.set_title("Salary by Sector (Top 10 by Count)")
ax.set_xlabel("Sector"); ax.set_ylabel("Salary")
plt.xticks(rotation=45, ha="right")


# # Total Individuals by Compensation

# In[107]:


top_people = df.sort_values("total_comp", ascending=False).head(25)
fig, ax = plt.subplots(figsize=(8,10))
sns.barplot(data=top_people, x="total_comp", y="full_name", ax=ax)
ax.set_title("Top 25 Total Compensation (Individuals)")
ax.set_xlabel("Total compensation"); ax.set_ylabel("Name")


# In[ ]:




