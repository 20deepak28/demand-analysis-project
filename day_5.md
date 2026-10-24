# Day 5 — Model Evaluation & Forecast Error Analysis

## Project Overview

* **Project:** Retail Demand Forecasting & Inventory Optimization
* **Dataset:** M5 Walmart Retail Sales Dataset
* **Modeling Scope:** Sample of 1,000 item-store series
* **Test Observations:** 383,000

---

## 1. Day 5 Objectives

* Compare baseline models with price-aware models.
* Ensure all models use the same training and test observations.
* Select the primary project model.
* Analyze forecasting errors by direction and demand level.

---

## 2. Data Alignment Issue — Found and Fixed

During model comparison, the baseline and price-aware models were found to be using mismatched data matrices.

### Initial Diagnostics

* Baseline `X_train`: 1,857,000 rows
* `y_train`: 1,502,000 rows
* Baseline `X_test`: 28,000 rows
* `y_test`: 383,000 rows

These mismatches meant the earlier baseline results were not suitable for a fair comparison.

### Resolution

The baseline matrices were rebuilt using the same training and test datasets as the price-aware models.

```python
X_train_base = train_model[base_features].copy()
y_train_base = train_model[target].copy()

X_test_base = test_model[base_features].copy()
y_test_base = test_model[target].copy()
```

The baseline models were then retrained using these aligned matrices.

### Final Matrix Shapes

| Dataset           |       Baseline |    Price-Aware |
| ----------------- | -------------: | -------------: |
| Training features | 1,502,000 × 11 | 1,502,000 × 15 |
| Training target   |      1,502,000 |      1,502,000 |
| Test features     |   383,000 × 11 |   383,000 × 15 |
| Test target       |        383,000 |        383,000 |

All six model configurations were evaluated on the same 383,000 test observations. Predictions were clipped at zero to ensure non-negative sales forecasts.

---

## 3. Model Comparison Results

| Rank | Model                     |    MAE | WAPE (%) |
| ---: | ------------------------- | -----: | -------: |
|    1 | Random Forest             | 0.8817 |    75.95 |
|    2 | LightGBM                  | 0.8838 |    76.13 |
|    3 | Random Forest + Price     | 0.8845 |    76.19 |
|    4 | LightGBM + Price          | 0.8851 |    76.25 |
|    5 | Linear Regression         | 0.9029 |    77.77 |
|    6 | Linear Regression + Price | 0.9078 |    78.19 |

### Model Selection Decision

* **Best-performing model:** Random Forest, with a WAPE of 75.95%.
* **Selected primary project model:** LightGBM, with a WAPE of 76.13%.
* **Benchmark model:** Random Forest.

LightGBM was selected as the primary model because it is specified in the project instructions, not because it achieved the lowest error.

Random Forest performed marginally better in this experiment and will remain the benchmark for future comparisons.

---

## 4. Price Feature Analysis

| Algorithm         | Without Price | With Price |             WAPE Change |
| ----------------- | ------------: | ---------: | ----------------------: |
| Random Forest     |        75.95% |     76.19% | +0.24 percentage points |
| LightGBM          |        76.13% |     76.25% | +0.12 percentage points |
| Linear Regression |        77.77% |     78.19% | +0.42 percentage points |

### Key Finding

Adding the current price features did not improve WAPE in this experiment.

This does not prove that price is irrelevant to demand. It only describes the result obtained with the current features, data sample, and modeling setup.

Further experimentation may help determine whether different price-related features improve forecasting performance.

---

## 5. LightGBM Forecast Error Analysis

The selected LightGBM model was evaluated on 383,000 test observations.

### Overall Error Metrics

| Metric                    |           Result |
| ------------------------- | ---------------: |
| Mean Absolute Error (MAE) |           0.8838 |
| Median Absolute Error     |           0.4652 |
| Maximum Absolute Error    |       92.0 units |
| Overpredictions           | 263,826 (68.88%) |
| Underpredictions          | 110,974 (28.97%) |
| Exact Predictions         |    8,200 (2.14%) |

### Error Definition

The error was calculated as:

`error = actual_sales - predicted_sales`

* **Negative error:** Overprediction — predicted sales are higher than actual sales.
* **Positive error:** Underprediction — predicted sales are lower than actual sales.
* **Zero error:** Exact prediction.

### Initial Findings

1. LightGBM overpredicted more often than it underpredicted.
2. The maximum absolute error indicates that some observations need closer investigation.
3. These aggregate statistics do not establish the reasons behind the errors.

---

## 6. Error Analysis by Actual Demand Level

Actual sales were divided into five demand groups:

* Zero sales
* 1 unit
* 2–5 units
* 6–10 units
* Above 10 units

### Key Observations

#### 1. Zero-Sales Observations

* Observations: 231,349
* Average actual sales: 0.000 units
* Average predicted sales: 0.505 units
* Total actual sales: 0 units
* Total predicted sales: 116,745.801 units

The model predicted positive sales for many observations where actual sales were zero.

#### 2. Positive-Demand Observations

Average predictions were below average actual sales in the positive-demand groups.

#### 3. Higher-Demand Observations

For the group with actual sales above 10 units:

* Average actual sales: 18.153 units
* Average predicted sales: 7.518 units

This indicates substantial underprediction in the higher-demand group.

#### 4. Demand Distribution

Zero-sales observations represented approximately 60.4% of the 383,000 test observations.

These findings describe the current test sample. They do not, by themselves, explain why the model behaves this way.

---

## 7. Visualizations Created

The following visualizations were created during the analysis.

| File Name                                    | Description                                                            |
| -------------------------------------------- | ---------------------------------------------------------------------- |
| `day5_model_comparison_linkedin.png`         | WAPE comparison across six model configurations                        |
| `day5_error_direction_linkedin.png`          | Comparison of overpredictions, underpredictions, and exact predictions |
| `lightgbm_actual_vs_predicted_by_demand.png` | Average actual versus predicted sales across demand levels             |

Keep these images in the project's reports or visuals folder.

---

## 8. Day 5 Conclusions

1. Identified and fixed the baseline data alignment issue.
2. Retrained baseline models using correctly aligned data.
3. Compared six model configurations on the same 383,000 test observations.
4. Random Forest achieved the lowest WAPE at 75.95%.
5. Selected LightGBM as the primary project model according to the project instructions.
6. Retained Random Forest as the benchmark model.
7. Price features did not improve WAPE in the current experiment.
8. LightGBM overpredicted more frequently overall.
9. Average predictions were below actual sales in the positive-demand groups.
10. Identified forecasting error patterns that require further investigation.

---

## 9. Day 6 — Next Steps

### Task 1: Investigate Large Errors

* Examine the 10 observations with the largest absolute forecasting errors.
* Identify the items, stores, dates, and actual versus predicted sales associated with those errors.

### Task 2: Analyze Errors by Item and Store

* Identify items with consistently high forecasting errors.
* Compare model performance across stores.
* Check whether errors are concentrated in particular item-store series.

### Task 3: Visualize Actual vs. Predicted Sales

* Plot actual versus predicted sales.
* Examine selected item-store series over time.
* Look for systematic overprediction or underprediction.

### Task 4: Investigate Error Patterns

* Investigate overprediction on zero-sales days.
* Investigate underprediction on higher-demand days.
* Explore potential improvements to features and model settings.

### Task 5: Improve and Evaluate the Model

* Test targeted LightGBM improvements.
* Use the same chronological test period for fair comparisons.
* Compare each experiment against the current LightGBM benchmark.
* Record the results and explain the final model selection.

---

## Important Scope Note

These results are based on a sample of **1,000 item-store series**, not all 30,490 item-store series in the full M5 dataset.
