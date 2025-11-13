# solar-challenge-week1

## Project Overview

Comprehensive analysis of solar farm data from Benin, Sierra Leone, and Togo to identify high-potential regions for solar investments for MoonLight Energy Solutions. This project provides data-driven recommendations through statistical analysis and interactive visualization.

## Note on Dashboard Screenshots

_The dashboard screenshots in this repository were taken using sample datasets (1,000 records per country) to ensure optimal performance. All analysis in notebooks and final report uses complete datasets._

## Tasks Completed

### Task 1: Git & Environment Setup

- Professional GitHub repository with CI/CD pipeline
- Virtual environment and dependency management
- Git workflow with feature branching (`setup-task`, `eda-*`, `compare-countries`, `dashboard-dev`)
- GitHub Actions for continuous integration

### Task 2: Data Profiling, Cleaning & EDA

- Comprehensive data analysis for all three countries
- Missing value analysis and outlier detection using Z-scores (|Z| > 3)
- Data cleaning with median imputation for key columns
- Time series analysis of solar radiation patterns
- Correlation analysis and distribution visualization
- Export of cleaned datasets for further analysis

### Task 3: Cross-Country Comparison

- Statistical comparison of solar potential (GHI, DNI, DHI)
- ANOVA testing revealing significant differences (p = 2.14e-21)
- Country ranking based on solar performance metrics
- Strategic investment recommendations with data-driven insights

### Bonus: Interactive Dashboard

- Streamlit application with multi-file upload functionality
- Advanced visualizations: wind rose, bubble charts, statistical testing
- Cleaning impact analysis and maintenance insights
- Automated recommendations based on comprehensive data analysis

## Environment Setup

### Local Development

```bash
git clone https://github.com/arwanasir/solar-challenge-week1.git
cd solar-challenge-week1


python -m venv .venv

.venv\Scripts\activate

source .venv/bin/activate

pip install -r requirements.txt
```
