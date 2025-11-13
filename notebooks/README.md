# Solar Challenge EDA Notebooks

## Analysis Workflow

### 1. Country-Specific Analysis

- **benin_eda.ipynb**: Benin solar data exploration
- **sierra_leone_eda.ipynb**: Sierra Leone solar data exploration
- **togo_eda.ipynb**: Togo solar data exploration

### 2. Comparative Analysis

- **compare_countries.ipynb**: Cross-country statistical comparison

## Analysis Framework

Each country notebook follows this structure:

### Data Loading & Validation

- Load raw CSV data
- Basic data quality assessment
- Column validation and type checking

### Data Cleaning

- Missing value analysis and imputation
- Outlier detection using Z-scores (|Z| > 3)
- Temporal consistency validation

### Exploratory Analysis

- Summary statistics for all numeric columns
- Time series analysis of solar radiation
- Correlation analysis between variables
- Distribution analysis and histogram plots

### Advanced Visualizations

- Heatmaps for correlation analysis
- Scatter plots for relationship exploration
- Box plots for outlier identification
- Wind pattern analysis where available

### Insights & Export

- Key findings and observations
- Data quality assessment
- Export cleaned dataset for further analysis

## Usage

Run notebooks in numerical order for complete analysis:

1. Start with individual country analysis
2. Proceed to cross-country comparison
3. Review statistical significance testing
4. Generate final recommendations

## Dependencies

All notebooks require:

- pandas >= 2.0.3
- numpy >= 1.24.3
- matplotlib >= 3.7.2
- seaborn >= 0.12.2
- scipy >= 1.11.1
