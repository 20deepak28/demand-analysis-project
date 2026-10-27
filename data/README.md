# 📊 Demand Analysis & Forecasting

**Analyzing product demand patterns and improving inventory decisions using Python and Machine Learning.**

## 📌 Project Overview

This project focuses on analyzing historical product-level demand data to identify patterns, understand demand behavior, and develop machine learning models that support better inventory planning.

The project follows an end-to-end data science workflow, covering exploratory data analysis, data preprocessing, feature engineering, baseline modeling, model improvement, prediction-error analysis, and inventory policy evaluation.

The objective is to transform historical sales data into actionable insights that help businesses make more informed demand forecasting and inventory management decisions.

## 🎯 Business Problem

Businesses need reliable demand estimates to make effective inventory decisions.

Poor demand planning can lead to:

* Overstocking and increased inventory holding costs.
* Stockouts and missed sales opportunities.
* Difficulty identifying demand trends and irregular patterns.
* Inefficient inventory replenishment decisions.
* Challenges in balancing product availability with inventory costs.

This project investigates historical demand data and applies data science and machine learning techniques to support better forecasting and inventory planning.

## 🎯 Project Objectives

* Explore historical demand patterns and assess data quality.
* Prepare and transform data for analysis and modeling.
* Engineer meaningful features from historical demand data.
* Establish a baseline machine learning model.
* Experiment with model improvements and compare performance.
* Analyze prediction errors to identify opportunities for improvement.
* Investigate inventory policies using demand analysis and model outputs.
* Organize experimental results and document project progress.

## 🗂️ Dataset Overview

The processed dataset contains approximately **1.91 million rows and 26 columns**, representing **1,000 unique products**.

| Attribute         | Details                              |
| ----------------- | ------------------------------------ |
| Dataset type      | Historical product-level demand data |
| Number of records | 1,913,000                            |
| Number of columns | 26                                   |
| Unique products   | 1,000                                |
| Date range        | January 29, 2011 – April 24, 2016    |
| Data formats      | Parquet and CSV                      |

These figures describe the dataset inspected during the project. The original data source and column definitions should be documented separately once verified.

## 🛠️ Technologies Used

* **Python** — Core programming language
* **Pandas** — Data manipulation and analysis
* **NumPy** — Numerical computing
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical visualization
* **Scikit-learn** — Machine learning and model evaluation
* **PyArrow** — Parquet file processing
* **Jupyter Notebook** — Interactive experimentation
* **Git & GitHub** — Version control and project documentation

## 🔄 Project Workflow

### Day 1: Exploratory Data Analysis

* Examined dataset dimensions, structure, and data types.
* Investigated product-level demand patterns.
* Checked for duplicate product-date records.
* Explored data quality and demand behavior.
* Investigated zero-sales days and demand variability.

### Day 2: Data Preprocessing

* Prepared data for downstream analysis.
* Investigated potential data quality issues.
* Organized the dataset for feature engineering and model development.
* Prepared the foundation for subsequent modeling experiments.

### Day 3: Feature Engineering

* Developed a feature-engineered dataset for machine learning.
* Prepared relevant features for demand prediction.
* Organized processed data for subsequent modeling experiments.
* Saved processed data in reusable formats.

### Day 4: Baseline Modeling

* Established an initial machine learning baseline.
* Evaluated model predictions using appropriate performance metrics.
* Saved baseline evaluation results.
* Created a reference point for subsequent experiments.

### Day 5: Model Evaluation and Improvement

* Experimented with model improvements.
* Compared model performance against the baseline.
* Investigated prediction errors and their direction.
* Generated visualizations to compare model results.
* Organized evaluation outputs for further analysis.

### Day 6: Model Experimentation

* Continued investigating model performance.
* Reviewed experimental results and potential improvements.
* Organized outputs to support reproducible comparisons.

### Day 7: Inventory Policy Analysis

* Explored inventory-related decisions using demand analysis and model outputs.
* Examined inventory policy results.
* Investigated how demand estimates could inform inventory planning.
* Saved outputs for further evaluation.

### Day 8: Continued Analysis and Project Development

* Continued development of the demand forecasting workflow.
* Organized processed datasets and project outputs for subsequent analysis.
* Reviewed the existing modeling and inventory analysis workflow.
* Continued preparing the project for more systematic evaluation and reproducibility.

*The Day 8 description should be refined to reflect the exact implementation, experiments, and outputs completed during that session.*

## 📈 Results & Evaluation

The project includes baseline evaluation results, model comparison outputs, prediction-error visualizations, and inventory policy analysis.

### Available Results

| Artifact                             | Purpose                         |
| ------------------------------------ | ------------------------------- |
| `baseline_results.csv`               | Baseline model evaluation       |
| `model_comparison.csv`               | Comparison of model performance |
| `day5_error_direction.png`           | Prediction-error analysis       |
| `day5_model_comparison.png`          | Model comparison visualization  |
| `day7_inventory_policy.csv`          | Inventory policy analysis       |
| `day7_model_improvement_results.csv` | Model improvement evaluation    |

### Evaluation Approach

The project uses model evaluation and comparison to investigate forecasting performance.

The analysis focuses on:

* Comparing model results against the baseline.
* Examining prediction errors.
* Identifying opportunities for model improvement.
* Exploring the relationship between demand predictions and inventory decisions.

**Note:** Final performance metrics, percentage improvements, and business impact should be reported only after verifying the actual experimental results.

## 📁 Repository Structure

```text
demand-analysis-project/
│
├── README.md
├── requirements.txt
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_prep.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_baseline_model.ipynb
│   └── 05_model_improvement.ipynb
│
├── data/
│   ├── README.md
│   ├── feature_engineered_sample.parquet
│   └── sales_sample.csv
│
├── reports/
│   ├── baseline_results.csv
│   ├── model_comparison.csv
│   ├── day5_error_direction.png
│   ├── day5_model_comparison.png
│   ├── day7_inventory_policy.csv
│   └── day7_model_improvement_results.csv
│
└── daily-progress/
    └── README.md
```

*This structure is illustrative. Update it to match the files and folders actually present in the repository, including any Day 8 artifacts.*

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or a compatible version for the installed dependencies.
* Jupyter Notebook or JupyterLab.
* Git, if you want to clone the repository.

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/20deepak28/demand-analysis-project.git
```

**2. Navigate to the project directory**

```bash
cd demand-analysis-project
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Launch JupyterLab**

```bash
jupyter lab
```

Open the notebooks in numerical order to follow the project workflow.

**Important:** Some notebooks may require the original dataset or additional processed files. Verify the data-loading paths and obtain any required data before running them.

## 🔮 Future Improvements

* Evaluate additional forecasting approaches.
* Perform systematic hyperparameter tuning.
* Compare prediction accuracy across products and demand patterns.
* Investigate intermittent and highly variable demand.
* Evaluate inventory policies using realistic business cost assumptions.
* Develop clearer visualizations of forecast accuracy and inventory outcomes.
* Document verified model metrics and business recommendations.
* Improve reproducibility through consistent experiment tracking.
* Expand the project documentation as additional development days are completed.

## 👨‍💻 Author

**Deepak Kumar Shukla**

Aspiring Data Scientist | Python | SQL | Machine Learning | Data Analysis

* **GitHub:** [20deepak28](https://github.com/20deepak28)
* **LinkedIn:** [Deepak Kumar Shukla](https://www.linkedin.com/in/deepak-kumar-shukla-474ab922a/)

---

*This project is part of my hands-on data science journey, focused on applying data analysis and machine learning techniques to practical business problems.*

