# Day 7 — Model Improvement & Inventory Optimization

**Project:** Retail Demand Forecasting & Inventory Optimization
**Notebook:** `05_model_improvement.ipynb`
**Status:** Completed

Today, I worked on improving the demand forecasting model and started inventory optimization. Both activities are included in **Day 7**.

---

## 1. Model Improvement

### Dataset and Evaluation

I evaluated a LightGBM model using a time-based train/test split.

* **Training rows before cleanup:** 1,530,000
* **Training rows after cleanup:** 1,502,000
* **Test rows:** 383,000
* **Zero-sales observations:** 231,349
* **Percentage of zero-sales observations:** 60.40%

### Model Results

| Experiment                        | Adjustment Factor |    MAE |   WAPE |
| --------------------------------- | ----------------: | -----: | -----: |
| LightGBM Baseline                 |              1.00 | 0.8830 | 76.06% |
| LightGBM + 10% Reduction          |              0.90 | 0.8670 | 74.68% |
| LightGBM + Best Tested Adjustment |              0.80 | 0.8625 | 74.30% |

### Key Observations

* The model initially produced 8,275 negative predictions.
* I clipped negative predictions to zero because demand cannot be negative.
* Reducing predictions improved overall MAE and WAPE on the test set.
* The adjustment reduced errors on zero-sales observations but increased errors on positive-sales observations.

> **Important limitation:** I selected the adjustment factor after examining test-set results. Therefore, the adjusted results are exploratory, not an unbiased final evaluation. A validation set should be used to select the adjustment before evaluating on an untouched test set.

---

## 2. Demand Analysis

I analyzed demand across **1,000 item-store combinations** using the prepared dataset:

`Data/processed/price_model_df.parquet`

### Features Analyzed

* Total sales
* Active sales days
* Observation days
* Average daily demand
* Maximum daily demand
* Zero-sales percentage
* Daily demand standard deviation
* Median daily demand
* Demand coefficient of variation (CV)

### Example Findings

| Item-Store Combination | Average Daily Demand | Zero-Sales Days |
| ---------------------- | -------------------: | --------------: |
| `FOODS_3_318_WI_3`     |                28.63 |          29.43% |
| `FOODS_3_723_CA_3`     |                23.41 |          21.75% |
| `FOODS_3_288_CA_2`     |                11.47 |          49.66% |

The average of the item-store average daily demand values was approximately **0.99 units**, while the median was approximately **0.41 units**.

### Learning

Different products have different demand patterns. Some products sell consistently, while others experience frequent zero-sales days.

Demand variability must be interpreted carefully, particularly for products with very low average demand.

---

## 3. Inventory Optimization

I created an initial inventory policy to calculate reorder points, safety stock, target stock, and recommended order quantities.

### Assumptions

* **Lead time:** 7 days
* **Target service level:** 95%
* **Z-score:** 1.645
* **Additional target coverage:** 14 days

### Calculations

**1. Lead-Time Demand**

`Lead-Time Demand = Average Daily Demand × Lead Time`

**2. Safety Stock**

`Safety Stock = Z-score × Daily Demand Standard Deviation × √Lead Time`

**3. Reorder Point**

`Reorder Point = Lead-Time Demand + Safety Stock`

**4. Target Stock**

`Target Stock = Average Daily Demand × (Lead Time + Additional Coverage Days)`

**5. Recommended Order Quantity**

`Recommended Order Quantity = max(Target Stock - Reorder Point, 0)`

The calculated quantities were rounded up where appropriate.

### Inventory Policy Results

| Metric                     |     Average |   Maximum |
| -------------------------- | ----------: | --------: |
| Safety Stock               |  6.58 units | 156 units |
| Reorder Point              | 14.04 units | 357 units |
| Target Stock               | 21.33 units | 602 units |
| Recommended Order Quantity |  7.52 units | 245 units |

### Example

For `FOODS_3_318_WI_3`:

* **Average daily demand:** 28.63 units
* **Safety stock:** 156 units
* **Reorder point:** 357 units
* **Target stock:** 602 units
* **Recommended order quantity:** 245 units

These recommendations are illustrative and depend on the assumptions used.

### Important Limitation

The initial inventory policy was calculated using the full prepared dataset, including the test period. This introduces potential data leakage.

For a more reliable evaluation, the inventory policy should be recalculated using only the appropriate historical training period.

The current policy also does not account for:

* Actual stock on hand
* Existing purchase orders
* Supplier constraints
* Product pack sizes
* Inventory holding costs
* Stockout records

The safety-stock calculation also assumes approximately independent daily demand. Products with intermittent demand may require a specialized approach.

---

## 4. Files Created

* `05_model_improvement.ipynb` — model improvement and inventory analysis
* `reports/day7_model_improvement_results.csv` — model experiment results
* `reports/day8_inventory_policy.csv` — initial inventory policy

**Note:** Although the inventory optimization work was originally planned for the next stage, I started it early and counted it as part of Day 7.

---

## 5. Key Learnings

1. Evaluated a LightGBM model using a time-based split.
2. Compared prediction adjustment factors using MAE and WAPE.
3. Investigated the difference between zero-sales and positive-sales prediction errors.
4. Analyzed demand patterns across 1,000 item-store combinations.
5. Calculated safety stock, reorder points, target stock, and recommended order quantities.
6. Identified data leakage and evaluation limitations that need to be addressed.

---

## 6. Next Steps

* Recalculate inventory policy using historical training data only.
* Build a simple inventory simulation.
* Develop a decision-focused dashboard.
* Document the methodology, assumptions, limitations, and results in the project README.
* Commit the completed work to GitHub.

---

## Day 7 Summary

**Day 7 combined demand forecasting improvement with the first stage of inventory optimization.** I evaluated the model, analyzed product-level demand patterns, and developed an initial inventory replenishment policy.

The next priority is to validate the inventory logic and build a practical demonstration of how forecasting can support inventory decisions.
