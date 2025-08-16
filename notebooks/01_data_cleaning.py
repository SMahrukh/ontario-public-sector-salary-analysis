#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Data handling
import pandas as pd
import numpy as np


# In[4]:


# Load the unclean dataset 
df = pd.read_csv(r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\raw\salary_disclosure_raw.csv")


# # 1.0. Data Cleaning

# # 1.1. Data Structure

# In[5]:


df.info()
df.shape
df.describe()


# In[6]:


df.head()


# # 1.1. Data handling

# In[7]:


#convert benefits to numeric
df['Benefits']=df['Benefits'].str.replace(',','').astype(float)


# In[8]:


#standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')


# In[9]:


# add full name column
df['full_name']=df['first_name']+ ' '+ df['last_name']


# In[10]:


df.head()


# In[11]:


#save file
df.to_csv("C:\Mahrukh\Data Analytics\hr-attrition-project\data\clean\salary_clean", index=False)


# In[12]:


# compressed file
# Keep only the columns you actually need
keep_cols = ['employer','job_title','sector','salary','benefits']
df_small = df[keep_cols]

# Save compressed version
df_small.to_csv(
    r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\clean\salary_reduced.csv.gz",
    index=False,
    compression="gzip"
)


# In[ ]:




