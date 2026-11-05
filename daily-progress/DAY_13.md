# Day 13 – LSTM Forecast Evaluation & Inventory Risk Analysis

## Project
**Retail Demand Forecasting & Inventory Optimization**  
**Dataset:** Walmart M5 Forecasting dataset

## 1. Objectives
- Load the selected final LSTM model (Epoch 5).
- Generate validation predictions while preserving product, store, category, and date identifiers.
- Evaluate model performance across the full validation dataset.
- Compare LSTM with the previously recorded full-dataset LightGBM metrics.
- Analyze errors by category, store, and product-store combination.
- Connect forecasting errors with inventory recommendations.
- Visualize and save analysis outputs.

## 2. Final LSTM Model & Prediction Coverage

Selected checkpoint: `models/retail_demand_lstm_final.pt` (Epoch 5).

Inference was performed chunk-wise across all 31 feature Parquet files.

| Validation detail | Result |
|---|---:|
| Product-store series | 30,490 |
| Validation observations | 12,531,390 |
| Validation start | 2015-04-08 |
| Validation end | 2016-05-22 |
| Prediction chunks processed | 31 |
| Missing predictions | 0 |

Predictions preserve identifiers and actual values, including `id`, `item_id`, `dept_id`, `cat_id`, `store_id`, `state_id`, `date`, `sales`, and `lstm_prediction`.

## 3. Overall LSTM Performance

| Metric | LSTM Epoch 5 |
|---|---:|
| MAE | 0.887898 |
| RMSE | 2.149657 |
| WAPE | 68.36% |

Metrics are calculated on the original sales scale after reversing target scaling and the log transformation.

## 4. LSTM vs. LightGBM

| Metric | Full LightGBM | LSTM Epoch 5 | Better result |
|---|---:|---:|---|
| MAE | 0.930733 | **0.887903** | LSTM |
| RMSE | **2.006124** | 2.149717 | LightGBM |
| WAPE | 71.66% | **68.37%** | LSTM |

LSTM has lower MAE and WAPE, while LightGBM has lower RMSE. LSTM therefore does not outperform LightGBM on every metric.

**Artifact note:** The full-dataset LightGBM model was not saved. Its metrics were recorded during the earlier modeling run. `models/sample_lightgbm.pkl` is a sample-trained model, not the full-dataset model.

## 5. Error Analysis by Product Category

| Category | Validation observations | MAE | WAPE |
|---|---:|---:|---:|
| FOODS | 5,906,070 | 1.1320 | 62.46% |
| HOBBIES | 2,322,150 | 0.6446 | 93.41% |
| HOUSEHOLD | 4,303,170 | 0.6842 | 74.19% |

### Findings
- FOODS has the highest MAE.
- HOBBIES has the highest WAPE despite its lower MAE.
- WAPE is normalized by actual sales volume, so it can tell a different story from MAE.
- Category RMSE should be observation-weighted when aggregating chunk-level squared errors.

## 6. Error Analysis by Store

| Store | Validation observations | MAE | RMSE | WAPE |
|---|---:|---:|---:|---:|
| CA_4 | 1,253,139 | 0.6720 | 1.4276 | 82.41% |
| TX_1 | 1,253,139 | 0.7516 | 1.7853 | 71.73% |
| CA_2 | 1,253,139 | 0.9106 | 1.9755 | 71.66% |
| WI_1 | 1,253,139 | 0.8430 | 1.7029 | 71.21% |
| WI_3 | 1,253,139 | 0.7935 | 2.0440 | 68.37% |
| TX_2 | 1,253,139 | 0.8628 | 2.0606 | 68.19% |
| TX_3 | 1,253,139 | 0.8377 | 1.9968 | 67.65% |
| CA_1 | 1,253,139 | 0.9815 | 2.1973 | 67.05% |
| WI_2 | 1,253,139 | 0.9806 | 2.7151 | 66.15% |
| CA_3 | 1,253,139 | 1.2457 | 3.0938 | 60.49% |

### Findings
- CA_4 has the highest store-level WAPE.
- CA_3 has the highest store-level MAE and RMSE.
- CA_3 is a candidate for deeper error investigation.
- WAPE and MAE provide different perspectives because WAPE is normalized by actual sales.

## 7. Worst-Performing Product-Store Combinations

The analysis covered all 30,490 product-store combinations. Selected high-MAE examples:

| Product-store ID | Category | Store | MAE | RMSE | WAPE |
|---|---|---|---:|---:|---:|
| FOODS_3_090_CA_3_evaluation | FOODS | CA_3 | 34.5854 | 50.1735 | 34.88% |
| HOBBIES_1_234_CA_3_evaluation | HOBBIES | CA_3 | 27.9986 | 42.5972 | 86.01% |
| FOODS_3_120_CA_3_evaluation | FOODS | CA_3 | 25.5264 | 32.8420 | 31.47% |
| FOODS_3_586_TX_2_evaluation | FOODS | TX_2 | 25.4833 | 30.8912 | 27.93% |
| FOODS_3_090_WI_3_evaluation | FOODS | WI_3 | 21.8000 | 32.4795 | 33.92% |
| FOODS_3_070_WI_2_evaluation | FOODS | WI_2 | 21.2122 | 31.3950 | 66.43% |
| FOODS_3_234_WI_2_evaluation | FOODS | WI_2 | 20.0650 | 39.1257 | 80.73% |
| FOODS_3_586_TX_3_evaluation | FOODS | TX_3 | 19.5166 | 23.9201 | 26.93% |
| FOODS_3_586_CA_3_evaluation | FOODS | CA_3 | 18.4993 | 22.2866 | 25.42% |
| FOODS_3_090_TX_3_evaluation | FOODS | TX_3 | 17.5088 | 26.9455 | 29.96% |

### Findings
- FOODS_3 products are prominent among the highest-error combinations.
- CA_3 appears repeatedly among high-MAE combinations.
- FOODS_3_090_CA_3_evaluation has the highest MAE in the displayed top-20 results.
- HOBBIES_1_234_CA_3_evaluation has WAPE of 86.01%.

## 8. Inventory Optimization Connection

Forecast error results were joined to the existing inventory recommendations using the product-store `id`.

Available inventory fields:
- `avg_daily_demand`
- `demand_std`
- `safety_stock`
- `reorder_point`

The inventory recommendations use the previously documented illustrative assumptions:
- Lead time: 7 days.
- Service level: 95% (z = 1.645).
- Safety stock: `z × demand_std × sqrt(lead_time)`.
- Reorder point: `avg_daily_demand × lead_time + safety_stock`.

These are planning recommendations, not actual stock levels or confirmed stockout alerts. The M5 dataset does not provide actual on-hand inventory or supplier lead times.

## 9. Project-Defined Inventory Risk Score

The project-defined relative risk score combines percentile ranks of product-store MAE and safety stock:

`inventory_risk_score = (0.5 × error_rank + 0.5 × safety_stock_rank) × 100`

| Risk level | Score range |
|---|---:|
| Low | 0–50 |
| Medium | >50–75 |
| High | >75–90 |
| Critical | >90–100 |

### Risk distribution

| Risk level | Product-store combinations |
|---|---:|
| Low | 15,681 |
| Medium | 7,801 |
| High | 4,282 |
| Critical | 2,726 |
| **Total** | **30,490** |

### Highest-ranked examples

| Product-store ID | Store | MAE | WAPE | Safety stock | Reorder point | Risk score |
|---|---|---:|---:|---:|---:|---:|
| FOODS_3_090_CA_3_evaluation | CA_3 | 34.5854 | 34.88% | 507 | 1,482 | 100.000 |
| FOODS_3_090_WI_3_evaluation | WI_3 | 21.8000 | 33.92% | 253 | 697 | 99.990 |
| FOODS_3_120_CA_3_evaluation | CA_3 | 25.5264 | 31.47% | 189 | 450 | 99.987 |
| FOODS_3_090_TX_3_evaluation | TX_3 | 17.5088 | 29.96% | 222 | 646 | 99.979 |
| FOODS_3_090_CA_1_evaluation | CA_1 | 16.4790 | 32.67% | 269 | 764 | 99.979 |
| FOODS_3_090_TX_2_evaluation | TX_2 | 15.8871 | 30.50% | 252 | 709 | 99.974 |
| FOODS_3_234_WI_2_evaluation | WI_2 | 20.0650 | 80.73% | 156 | 343 | 99.974 |
| FOODS_3_586_TX_2_evaluation | TX_2 | 25.4833 | 27.93% | 137 | 859 | 99.962 |

**Limitation:** This is a project-defined prioritization score, not a statistically validated stockout probability or calibrated business risk measure. It combines relative forecast error and safety-stock rankings with equal weights.

## 10. Visualizations

Generated and saved:
- `category_wape.png`
- `store_wape.png`
- `store_mae.png`

Directory: `notebooks/day13_analysis/`

## 11. Saved Day 13 Outputs

All analysis outputs were saved in:

`Data/processed/full_dataset/day13_analysis/`

- `product_forecast_errors.parquet`
- `inventory_risk_analysis.parquet`
- `inventory_risk_analysis.csv`
- `category_error_summary.csv`
- `store_error_summary.csv`

LSTM prediction chunks remain in:

`Data/processed/full_dataset/predictions/`

## 12. Completion Checklist

- [x] Loaded selected Epoch 5 LSTM checkpoint.
- [x] Generated predictions for all 30,490 product-store series.
- [x] Processed all 31 feature chunks.
- [x] Verified 12,531,390 predictions with no missing predictions.
- [x] Calculated full validation MAE, RMSE, and WAPE.
- [x] Compared LSTM with recorded full-dataset LightGBM metrics.
- [x] Analyzed errors by category and store.
- [x] Identified high-error product-store combinations.
- [x] Joined forecast errors with inventory recommendations.
- [x] Created project-defined inventory risk score and risk bands.
- [x] Generated category and store visualizations.
- [x] Saved Day 13 analysis outputs.

## 13. Day 14 Preview – Interactive Dashboard

Next phase: build a Streamlit dashboard with:
1. Executive Overview
2. Demand Forecast Analysis
3. Model Performance Comparison
4. Store & Category Analysis
5. Inventory Optimization
6. High-Risk Product Monitoring

---

**Day 13 Status: COMPLETE**
