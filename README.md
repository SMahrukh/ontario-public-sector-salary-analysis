# Ontario Public Sector Salary Analysis  

## Overview  
This project analyzes Ontario’s public sector salary disclosure dataset (the “Sunshine List”).  
The dataset is publicly available and contains compensation information for employees earning $100,000 or more.  
The goal of this project is to explore salary distribution, sector-level patterns, and highlight top roles and employers by headcount and pay.  

**Data source:** [Ontario Public Sector Salary Disclosure, 2024](https://www.ontario.ca/public-sector-salary-disclosure/2024/all-sectors-and-seconded-employees/)  

### Note on Data and Columns
This repository does not include the full Ontario dataset because of GitHub size limits.  
Only a reduced version (with key fields such as employer, job title, sector, salary, and benefits) is included.  

⚠️ Some formulas or code cells in the notebook reference columns like `full_name`.  
Since the reduced dataset does not include employee names, those specific cells will not run unless you load the full dataset from the [Ontario Government site](https://www.ontario.ca/public-sector-salary-disclosure/2024/all-sectors-and-seconded-employees/).  

## Tools & Libraries  
- Python: pandas, numpy, matplotlib, seaborn  
- Data Cleaning: handled currency formatting, spacing issues, and missing values  
- Analysis: salary percentiles, sector/employer/job title aggregations, outlier detection  
- Visualizations: histograms, salary buckets, bar charts, and boxplots  

## Process  
1. **Data Preparation**  
   - Converted salary text to numeric  
   - Created total compensation field (`salary + benefits`)  
   - Built salary buckets and calculated benefit share  
   - Checked outliers

2. **Exploratory Analysis**  
   - Salary and benefits distributions  
   - Salary percentiles (10th–99th)  
   - Sector-level aggregation: headcount, median salary, total payroll  
   - Employer-level aggregation: top 20 by headcount and payroll  
   - Job title analysis: most common, highest median salary (min 30 employees)  
   - Top individuals by compensation  

3. **Visualizations**  
   - Employees by salary bucket  
   - Top employers by headcount and payroll  
   - Top job titles by count and by median salary  
   - Salary distribution across sectors (boxplots)  
   - Top 25 individuals by total compensation  

## Key Insights  
- Most employees earn between **$100k–$150k**; very few exceed $200k.  
- **Teachers, professors, and nurses** dominate employee counts.  
- **School boards** are the largest employers and payroll spenders.  
- **Judiciary, power generation, and medical specialists** show the highest median salaries.  
- A handful of executives and physicians earn **>$1M**, but they are clear outliers. 
