# 📊 Demand Analysis & Forecasting

**Analyzing product demand patterns and improving inventory decisions using Python and Machine Learning.**

## 📌 Project Overview

This project explores historical product-level demand data to identify patterns, understand demand behavior, and develop machine learning models that can support better inventory planning.

The workflow covers the complete data science process, from exploratory data analysis and preprocessing to feature engineering, baseline modeling, model improvement, and inventory policy analysis.

The goal is to turn historical sales data into actionable insights that can help businesses make more informed demand and inventory decisions.

## 🎯 Business Problem

Businesses need to understand how demand changes over time to make effective inventory decisions.

Poor demand planning can contribute to:

* Overstocking and unnecessary inventory costs.
* Stockouts and missed sales opportunities.
* Difficulty identifying demand trends and irregular patterns.
* Inefficient inventory replenishment decisions.

This project investigates historical demand data and applies data science techniques to support more informed forecasting and inventory planning.

## 🎯 Project Objectives

* Explore historical demand patterns and data quality.
* Prepare and transform data for analysis and modeling.
* Engineer meaningful features from historical demand data.
* Develop a baseline machine learning model.
* Improve model performance through experimentation.
* Compare model results and analyze prediction errors.
* Explore inventory policies using demand analysis and model outputs.

## 🗂️ Dataset Overview

The processed dataset contains approximately **1.91 million rows and 26 columns**, representing **1,000 unique products**.

| Attribute          | Details                              |
| ------------------ | ------------------------------------ |
| Dataset type       | Historical product-level demand data |
| Number of records  | 1,913,000                            |
| Number of features | 26                                   |
| Unique products    | 1,000                                |
| Date range         | January 29, 2011 – April 24, 2016    |
| Data format        | Parquet and CSV                      |

These figures describe the dataset inspected during the project. The exact dataset source and original column definitions can be documented separately as they are verified.

## 🛠️ Technologies Used

* **Python** — Core programming language
* **Pandas** — Data manipulation and analysis
* **NumPy** — Numerical computing
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical visualization
* **Scikit-learn** — Machine learning and model evaluation
* **Jupyter Notebook** — Interactive experimentation
* **Git & GitHub** — Version control and project documentation

## 🔄 Project Workflow

### 1. Exploratory Data Analysis

* Examined the dataset's structure and dimensions.
* Investigated product-level demand patterns.
* Checked for duplicate product-date records.
* Explored data quality and demand behavior.
* Investigated zero-sales days and demand variability.

### 2. Data Preprocessing

* Prepared data for downstream analysis.
* Examined data quality issues.
* Organized the dataset for feature engineering and model development.

### 3. Feature Engineering

* Developed a feature-engineered dataset for machine learning.
* Prepared relevant features for demand prediction.
* Organized the processed data for subsequent modeling experiments.

### 4. Baseline Modeling

* Established an initial machine learning baseline.
* Evaluated model predictions using appropriate performance metrics.
* Saved baseline results for comparison.

### 5. Model Improvement

* Experimented with model improvements.
* Compared model performance against the baseline.
* Investigated prediction errors and opportunities for improvement.

### 6. Inventory Policy Analysis

* Explored inventory-related decisions using demand analysis and model outputs.
* Examined inventory policy results.
* Worked toward translating model outputs into practical inventory planning insights.

## 📈 Results & Evaluation

The project includes baseline model results, model comparison outputs, prediction-error visualizations, and inventory policy analysis.

The following artifacts are available in the repository:

* `baseline_results.csv` — Baseline evaluation results.
* `model_comparison.csv` — Model comparison results.
* `day5_error_direction.png` — Prediction-error analysis visualization.
* `day5_model_comparison.png` — Model comparison visualization.
* `day7_inventory_policy.csv` — Inventory policy analysis output.
* `day7_model_improvement_results.csv` — Model improvement results.

**Note:** Quantitative performance improvements and final conclusions should be reported after verifying the actual evaluation metrics and comparing the baseline with the improved model.

## 📁 Repository Structure

```text
demand-analysis-project/
│
├── README.md
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
│   └── feature_engineered_sample.parquet
│
├── reports/
│   ├── baseline_results.csv
│   ├── model_comparison.csv
│   ├── day5_error_direction.png
│   ├── day5_model_comparison.png
│   ├── day7_inventory_policy.csv
│   └── day7_model_improvement_results.csv
│
├── daily-progress/
│   ├── README.md
│   └── Daily progress logs
│
└── requirements.txt
```

*The structure above summarizes the intended organization. Keep the filenames aligned with the files actually present in your repository.*

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or a compatible version for your installed dependencies.
* Jupyter Notebook or JupyterLab.
* Git, if you want to clone the repository.

### Installation

Clone the repository:

```bash
git clone https://github.com/20deepak28/demand-analysis-project.git
```

Navigate to the project directory:

```bash
cd demand-analysis-project
```

Create and activate a virtual environment if desired, then install the dependencies:

```bash
pip install -r requirements.txt
```

Launch Jupyter:

```bash
jupyter lab
```

Open the notebooks in numerical order to follow the project workflow.

**Important:** Some notebooks may require the original dataset or additional processed files. Check their data-loading paths and obtain any required data before running them.

## 🔮 Future Improvements

* Evaluate additional forecasting approaches.
* Improve model performance through systematic hyperparameter tuning.
* Compare prediction accuracy across different products and demand patterns.
* Investigate intermittent and highly variable demand.
* Evaluate inventory policies using appropriate business cost assumptions.
* Add clearer visualizations of forecast accuracy and inventory outcomes.
* Document final model metrics and business recommendations.

## 👨‍💻 Author

**Deepak Kumar Shukla**

Aspiring Data Scientist | Python | SQL | Machine Learning | Data Analysis

* **GitHub:** [20deepak28](https://github.com/20deepak28)
* **LinkedIn:** [Deepak Kumar Shukla](https://www.linkedin.com/in/deepak-kumar-shukla-474ab922a/)

---

*This project is part of my hands-on journey in data science, focused on applying data analysis and machine learning techniques to practical business problems.*
