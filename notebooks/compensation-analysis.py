#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 120)
pd.options.display.float_format = "{:,.2f}".format #converting float values to decimals and presenting in right format


# In[4]:


data_path = r"C:\Mahrukh\Data Analytics\hr-attrition-project\data\raw\salary_disclosure_raw.csv"

df_raw = pd.read_csv(data_path, low_memory = False)


# In[5]:


df_raw.info()


# In[6]:


df_raw.shape


# In[7]:


df_raw.head(10)


# In[8]:


df= df_raw.copy()


# In[9]:


df.columns = (df.columns
                .str.strip()
                .str.lower()
                .str.replace(r"\s+", "_", regex=True)
                .str.replace(r"[^0-9a-zA-Z_]", "", regex=True))


# In[10]:


df.columns


# In[11]:


df["salary"] = df["salary"].str.replace("$","",regex = False) \
                .str.replace(",","",regex = False) \
            .astype(float)


# In[12]:


df["benefits"] = df["benefits"].str.replace("$","",regex = False) \
                .str.replace(",","",regex = False) \
                .astype(float)


# In[13]:


df.info()


# In[14]:


# adding total compensation to the table

df["total_comp"]=df["salary"]+df["benefits"]


# In[15]:


df["full_name"]=df["first_name"]+" "+df["last_name"]


# In[16]:


df.head()


# In[17]:


df[["sector","last_name","first_name","salary","benefits","employer","job_title","year","total_comp","full_name"]].isna().sum()


# In[18]:


(df[["salary","benefits","total_comp","year"]]<0).sum()


# In[19]:


#checking percentage of null values
(df.isna().mean().sort_values(ascending=False)*100).round(2).head(10)


# In[20]:


df.columns


# In[21]:


#cleaning text columns

text_cols = ["sector","last_name", "first_name","employer","job_title","full_name"]

df[text_cols] = df[text_cols].astype(str).apply(lambda s:s.str.strip()).replace({"nan":np.nan})


# In[22]:


#descriptive statistics

num_summary = df[["salary","benefits","total_comp"]].describe(percentiles=[0.1,0.25,0.50,0.75,0.90,0.95]).T
num_summary


# # Bucketing Salaries and Analysing the Percentage of employees in each

# In[23]:


bins = [100000,125000,150000,175000,200000,225000,250000,275000,300000,400000,500000,1000000,df["total_comp"].max()]
labels = ["100k-125k","125k-150k","150k-175k","175k-200k","200k-225k","225k-250k","250k-275k","275k-300k","300k-400k","400k-500k","500k-1mio",">1mio"]

bucket_summary = (
    pd.cut(df["total_comp"], bins=bins, labels=labels, include_lowest=True)
      .value_counts(normalize=True)    
      .sort_index()                    
      .mul(100)                        
      .round(2)                        
      .to_frame("percent")
)

# If you also want the raw counts alongside:
bucket_summary["count"] = (
    pd.cut(df["total_comp"], bins=bins, labels=labels, include_lowest=True)
      .value_counts()
      .sort_index()
)

bucket_summary


# In[24]:


bucket_counts = pd.cut(df["total_comp"],bins = bins, labels = labels, include_lowest = True). value_counts().sort_index()


# In[25]:


ax = bucket_counts.plot(kind="bar", figsize = (10,6), color = "lightcoral")
plt.title("Employee Count by Total Compensation Bucket")
plt.xlabel("Compensation Range")
plt.ylabel("Number of Employees")
plt.xticks(rotation=90, ha="right")
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.show()


# In[26]:


bucket_percent = pd.cut(df["total_comp"], bins = bins, labels = labels, include_lowest = True).value_counts(normalize = True)\
.sort_index()\
.mul(100)\
.round(2)\
.to_frame("percent")


# In[27]:


ax=bucket_percent.plot(kind = "bar", figsize = (10,6), color = "lightgreen")
plt.title("Employee % by Total Compensation Bucket"),
plt.xlabel("Compensation Range")
plt.ylabel("Number of Employees")
plt.xticks(rotation = 90, ha = "right")
ax.bar_label(ax.containers[0], fmt="%.1f%%")
plt.show()


# # Sector Level KPI

# In[28]:


sec = df[df["sector"].notna() & df["total_comp"].notna()].copy()

g = sec.groupby("sector")

headcount = g["total_comp"].count()
median = g["total_comp"].median()
p90 = g["total_comp"].quantile(0.9)
payroll = g["total_comp"].sum()

sector_summary = pd.DataFrame({"headcount": headcount, "median_total_comp": median, "p90_total_comp": p90, "payroll": payroll}).reset_index()

sector_summary = sector_summary.sort_values("median_total_comp", ascending = False)

sector_summary


# In[29]:


ax = payroll.plot(kind = "barh", figsize = (10,7), color = "lightgreen")
plt.title("Payroll by Sector")
plt.xlabel("Sector")
plt.ylabel("Total Payroll (Billions)")
plt.xticks(rotation = 90, ha = "right")

ax.bar_label(ax.containers[0], labels=[f"{v/1e9:.1f}B" for v in payroll.values])

plt.show()


# In[30]:


data_filtered = df[df["full_name"].notna() & df["sector"].notna()]

headcount_by_sector = data_filtered["sector"].value_counts().sort_index()

ax = headcount_by_sector.plot(kind = "bar", figsize = (10,6), color = "blue")

plt.title("Headcount by Sector")
plt.xlabel("Sector")
plt.ylabel("Headcount")

plt.xticks(rotation = 90, ha = "right")
    
ax.bar_label(ax.containers[0])
plt.show()


# # Employer headcount / payroll leaders

# In[31]:


emp = df.loc[df["employer"].notna() & df["total_comp"].notna()].copy()


# In[32]:


emp_headcount = (emp.groupby("employer", as_index = False)["employer"]
                .value_counts()
                .sort_values("count", ascending = False))
                 
emp_headcount.head(20)


# In[38]:


top20 = emp_headcount.head(20)

ax = top20.plot(kind = "barh", x = "employer", y = "count",figsize = (10,6), color = "coral")

plt.title("Top 20 Employers by Headcount")
plt.xlabel("Employers")
plt.ylabel("Headcount")

plt.xticks(rotation = 90)
ax.bar_label(ax.containers[0], labels = [f"{int(v):,}" for v in top20["count"]])

plt.show()


# In[39]:


emp_payroll = (
                emp.groupby("employer", as_index=False)["total_comp"]
                .sum()
                .rename(columns={"total_comp": "total_payroll"})
                .sort_values("total_payroll", ascending = False)
                       )
emp_payroll.head(20)


# In[40]:


emp_payroll=emp_payroll.head(20).sort_values("total_payroll", ascending = True)

top20payroll = emp_payroll.head(20)

ax = top20payroll.plot(kind = "barh", x = "employer", y = "total_payroll",figsize = (10,6), color = "coral")

plt.title("Top 20 Employers by Payroll")
plt.xlabel("Employers")
plt.ylabel("Payroll(Billions)")

plt.xticks(rotation = 90)
labels = [f"{v/1e9:.1f}B" for v in top20payroll["total_payroll"]]
ax.bar_label(ax.containers[0], labels=labels)
plt.show()


# In[41]:


emp_median = (
    emp.groupby("employer", as_index=False)["total_comp"]
       .median()
       .rename(columns={"total_comp": "median_total_comp"})
       .sort_values("median_total_comp", ascending=False)
)
emp_median.head(20)


# In[42]:


top20_median = emp_median.head(20).sort_values("median_total_comp", ascending = True).head(20)

ax = top20_median.plot(kind = "barh", figsize = (10,6), color = "coral")

plt.title("Top 20 Employers by Median Pay")
plt.xlabel("Median Total Compensation ($)")
plt.ylabel("Employer")

# Format labels as $ with commas
labels = [f"${int(v):,}" for v in top20_median["median_total_comp"]]
ax.bar_label(ax.containers[0], labels=labels)

plt.tight_layout()
plt.show()


# # Outlier Analysis

# In[60]:


# Pick the 20 largest sectors by employee count
top20_sectors = (
    df["sector"]
    .value_counts()
    .head(20)
    .index
)

df_sector = df[df["sector"].isin(top20_sectors) & df["total_comp"].notna()]


# In[62]:


order = (
    df_sector.groupby("sector")["total_comp"]
    .median()
    .sort_values(ascending=False)
    .index
)

plt.figure(figsize=(12,6))

# Boxplot per sector (matplotlib auto-detects outliers)
df_sector.boxplot(
    column="total_comp",
    by="sector",
    grid=False,
    vert=True
)

plt.title("Total Compensation Distribution (Top 20 Sectors)")
plt.suptitle("")  # remove default grouped title
plt.xlabel("Sector")
plt.ylabel("Total Compensation")
plt.xticks(rotation=90, ha="right")
plt.show()


# # Analysis by Job Title

# In[47]:


job_summary = (
    df.groupby("job_title", as_index=False)
      .agg(
          headcount=("total_comp", "size"),
          avg_total_comp=("total_comp", "mean"),
          median_total_comp=("total_comp", "median")
      )
      .sort_values("headcount", ascending=False)
)

job_summary.head(20)


# In[75]:


title_pay = (
    df.groupby("job_title", as_index=False)
      .agg(
          n=("total_comp", "size"),
          median_total_comp=("total_comp", "median")
      )
)


title_pay_30 = title_pay.loc[title_pay["n"] >= 30]

top10_median = (
    title_pay_30
    .sort_values("median_total_comp", ascending=False)
    .head(10)
)


plt.figure(figsize=(8,5))
plt.barh(top10_median["job_title"][::-1], top10_median["median_total_comp"][::-1])
plt.title("Top 10 Job Titles by Median Total Compensation (n ≥ 30)")
plt.xlabel("Median Total Compensation")
plt.ylabel("Job Title")
plt.tight_layout()
plt.show()


# # Outliers - Sector-wise

# In[68]:


# Top 10 sectors by headcount
top10_sectors = df["sector"].value_counts().head(10).index

# Subset just those rows
sub = df.loc[df["sector"].isin(top10_sectors) & df["total_comp"].notna(), ["sector", "total_comp"]]


# In[72]:


plt.figure(figsize=(10,6))

# Build the data list in the right order
data = [sub.loc[sub["sector"] == s, "total_comp"].values for s in order]

# Boxplot (showfliers=True means we keep outliers)
plt.boxplot(data, labels=order, showfliers=True)

plt.title("Total Compensation by Sector (Top 10 Sectors, Outliers Shown)")
plt.xlabel("Sector")
plt.ylabel("Total Compensation")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.show()


# In[ ]:




