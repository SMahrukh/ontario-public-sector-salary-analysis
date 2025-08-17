# Ontario Public Sector Salary Analysis  

## Overview  
This project analyzes Ontario’s public sector salary disclosure dataset (the “Sunshine List”).  
The dataset contains compensation information for employees earning $100,000 or more.  
The goal of this project is to explore salary distribution, sector-level patterns, employer payroll costs, and highlight top roles by headcount and pay.  

**Data source:** [Ontario Public Sector Salary Disclosure, 2024](https://www.ontario.ca/public-sector-salary-disclosure/2024/all-sectors-and-seconded-employees/)  

### Note on Data and Columns  
This repository does not include the full Ontario dataset due to size constraints.  
The analysis expects fields such as `sector`, `employer`, `job_title`, `salary`, `benefits`, and `year`.  

⚠️ Some code cells reference a `full_name` column built from first and last names.  
If you use a reduced dataset without employee names, those specific cells will not run unless you load the full dataset from the [Ontario Government site](https://www.ontario.ca/public-sector-salary-disclosure/2024/all-sectors-and-seconded-employees/).  

---

## Tools & Libraries  
- Python: pandas, numpy, matplotlib  
- Data Cleaning: removal of `$` and commas, trimming text fields, handling missing values  
- Analysis: percentiles, sector/employer/job title aggregations, outlier detection  
- Visualizations: histograms, salary buckets, bar charts, line charts, and boxplots  

---

## Process  

1. **Data Preparation**  
   - Converted salary and benefits to numeric values  
   - Created a `total_comp` field (`salary + benefits`)  
   - Built derived fields like `full_name`  
   - Cleaned employer, sector, and job title text fields  
   - Checked for nulls and negative values  

2. **Exploratory Analysis**  
   - Salary and benefits distributions  
   - Salary percentiles (10th–95th)  
   - Bucketing of employees into compensation ranges  
   - Sector-level aggregation: headcount, payroll, medians, 90th percentile  
   - Employer-level aggregation: top 20 by headcount, payroll, and median pay  
   - Job title analysis: most common roles, and top-paying roles with at least 30 employees  
   - Outlier analysis with sector-wise boxplots  

3. **Yearly Trends (optional extension)**  
   - Headcount, payroll, and median pay summarized by year  
   - Line charts to show how compensation shifts over time  

---

## Key Insights  

1. **Most employees earn just above the threshold**  
   - The majority fall between $100k and $150k.  
   - Very few cross $200k, and only a handful exceed $500k.  

2. **Education and healthcare dominate the list**  
   - School boards, colleges, and universities have the largest headcounts.  
   - Hospitals and school boards also have the biggest payrolls.  

3. **Who earns the most (typical pay)**  
   - Judges, doctors, and energy executives show the highest median salaries.  
   - These roles pull up the median pay in their sectors.  

4. **Two kinds of job titles**  
   - Large groups: teachers, professors, nurses, and police officers — many people with moderate pay.  
   - Smaller groups: surgeons, judges, executives — fewer people but very high pay.  

5. **Outliers matter**  
   - A small number of individuals earn more than $1M.  
   - They are rare, but they skew average pay upward.  
   - Using the median gives a clearer view of what’s “normal.”  

   - Adding sector-level yearly charts highlights which areas are growing fastest.  

---
