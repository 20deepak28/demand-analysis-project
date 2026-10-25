# Day 6: Forecast Error Analysis

## 1. Objective

The objective of Day 6 was to investigate the forecasting errors produced by the baseline LightGBM model for the Retail Demand Forecasting & Inventory Optimization project.

The analysis focused on identifying patterns in forecast errors across demand levels, stores, individual items, weekdays, and product categories. The findings will guide the next stage of model improvement.

## 2. Dataset and Evaluation Setup

* **Dataset:** Walmart M5 retail sales dataset
* **Model:** Baseline LightGBM Regressor
* **Test observations:** 383,000
* **Forecast horizon:** Test period beginning April 8, 2015
* **Evaluation metrics:** Mean Absolute Error (MAE) and Weighted Absolute Percentage Error (WAPE)

The same test observations were used to analyze different aspects of forecast performance.

## 3. Overall Model Performance

| Metric                                    |           Result |
| ----------------------------------------- | ---------------: |
| Test observations                         |          383,000 |
| Total actual sales                        |          444,626 |
| Total predicted sales                     |       444,722.11 |
| Mean Absolute Error (MAE)                 |           0.8838 |
| Weighted Absolute Percentage Error (WAPE) |           76.13% |
| Total underprediction                     | 169,197.63 units |
| Total overprediction                      | 169,293.74 units |
| Observations with overprediction          |           68.88% |
| Observations with underprediction         |           28.97% |

The model's total predicted sales were close to total actual sales. However, this aggregate agreement does not mean individual forecasts were accurate.

The WAPE of 76.13% indicates substantial absolute forecast error relative to total actual sales.

The model overpredicted approximately 68.88% of observations and underpredicted approximately 28.97%. The remaining observations were exact matches.

## 4. Forecast Errors by Demand Level

The predictions were evaluated across five demand groups.

| Actual Demand Group | Observations | Average Actual Sales | Average Predicted Sales |   MAE |
| ------------------- | -----------: | -------------------: | ----------------------: | ----: |
| Zero sales          |      231,349 |                0.000 |                   0.505 | 0.505 |
| 1 unit              |       68,502 |                1.000 |                   0.977 | 0.626 |
| 2–5 units           |       66,099 |                2.831 |                   1.997 | 1.475 |
| 6–10 units          |       11,177 |                7.374 |                   5.079 | 3.328 |
| Above 10 units      |        5,873 |               18.153 |                  12.301 | 7.518 |

### Key observations

* The model predicted positive demand on many days when actual sales were zero.
* Predictions were relatively close to actual averages for observations with one unit of demand.
* The model increasingly underpredicted average sales in the higher-demand groups.
* The above-10-units group had the highest MAE, at 7.518 units.

These findings suggest two distinct challenges: overprediction during zero-sales periods and underprediction during high-demand periods.

## 5. Forecast Errors by Store

Store-level evaluation showed differences in forecasting performance.

| Store |  MAE |   WAPE |
| ----- | ---: | -----: |
| CA_4  | 0.73 | 96.44% |
| TX_1  | 0.73 | 86.48% |
| WI_1  | 0.82 | 82.17% |
| TX_2  | 0.83 | 80.30% |
| TX_3  | 0.81 | 76.97% |
| WI_2  | 0.92 | 76.73% |
| WI_3  | 0.76 | 75.20% |
| CA_2  | 1.08 | 70.53% |
| CA_1  | 0.98 | 70.31% |
| CA_3  | 1.23 | 64.16% |

CA_4 had the highest WAPE, while CA_3 had the highest MAE.

This difference demonstrates why both metrics are useful: MAE measures average absolute error per observation, while WAPE measures total absolute error relative to total actual sales.

CA_4 was selected for further investigation because of its high WAPE.

## 6. Store-Level Demand Analysis

The CA_4 and TX_1 analyses revealed similar patterns.

For CA_4:

* Zero-sales observations had average predicted sales of approximately 0.44 units.
* Average actual sales in the 2–5-unit group were 2.75, compared with predicted sales of 1.78.
* Average actual sales above 10 units were 17.74, compared with predicted sales of 5.53.

For TX_1:

* Zero-sales observations had average predicted sales of approximately 0.43 units.
* Average actual sales in the 2–5-unit group were 2.76, compared with predicted sales of 1.72.
* Average actual sales above 10 units were 15.79, compared with predicted sales of 10.74.

The model struggled with both zero-sales observations and higher-demand observations in these stores.

## 7. Item-Level Investigation: HOBBIES_1_178 at CA_4

A detailed investigation was conducted for item `HOBBIES_1_178` at store `CA_4`.

| Metric                |   Result |
| --------------------- | -------: |
| Test observations     |      383 |
| Total actual sales    |    2,500 |
| Total predicted sales | 2,336.74 |
| MAE                   |     6.22 |
| Total absolute error  | 2,380.56 |

The item experienced several demand spikes that the model substantially underpredicted.

### Largest missed demand spikes

| Date       | Actual Sales | Predicted Sales | Underprediction |
| ---------- | -----------: | --------------: | --------------: |
| 2015-07-27 |           49 |            3.35 |           45.65 |
| 2016-01-16 |           51 |            6.11 |           44.89 |
| 2015-10-10 |           50 |            7.11 |           42.89 |
| 2015-09-26 |           49 |            7.06 |           41.94 |
| 2016-03-02 |           43 |            3.12 |           39.88 |

These observations show that the model sometimes produced low predictions despite actual sales being unusually high.

### Changes in demand over time

The test period was divided into four periods.

Period 3 had the highest average actual sales and the highest MAE. In Period 4, 62.5% of observations had zero sales, and average predictions exceeded average actual sales.

This suggests that demand patterns can change over time, making a single forecasting approach challenging for intermittent products.

## 8. Weekday Analysis

For `HOBBIES_1_178` at CA_4, Saturday had the largest average absolute error among weekdays.

| Weekday   | Observations |  MAE | Mean Signed Error |
| --------- | -----------: | ---: | ----------------: |
| Monday    |           54 | 5.51 |             -1.11 |
| Tuesday   |           54 | 5.45 |              1.55 |
| Wednesday |           55 | 6.80 |              1.97 |
| Thursday  |           55 | 5.12 |             -0.14 |
| Friday    |           55 | 5.16 |             -0.66 |
| Saturday  |           55 | 9.54 |              4.87 |
| Sunday    |           55 | 5.90 |             -3.51 |

**Mean signed error = actual sales − predicted sales.**

Positive values indicate average underprediction, while negative values indicate average overprediction.

Saturday's average absolute error was 9.54 units, compared with 5.66 units across the other weekdays.

A one-sided Mann–Whitney U test comparing Saturday errors with other weekdays returned a p-value of approximately 0.0134. This provides evidence of larger Saturday errors in this particular item-store sample, although the finding should not be generalized to every product or store.

The five largest Saturday errors accounted for approximately 37.01% of total Saturday absolute error. This suggests that a small number of large demand spikes contributed substantially to Saturday's error.

## 9. Recent Sales Features

Feature importance analysis showed that the model relied heavily on recent sales history.

The most important features included:

* `rolling_mean_7`
* `lag_1`
* `lag_7`
* `lag_28`
* `rolling_mean_28`

These features describe recent and historical sales patterns.

An additional analysis compared error magnitude with recent sales activity.

| Error Group     | Observations | Average Actual Sales | Average Predicted Sales | Average Absolute Error |
| --------------- | -----------: | -------------------: | ----------------------: | ---------------------: |
| Low (≤1)        |      290,185 |                0.486 |                   0.626 |                  0.362 |
| Moderate (1–5)  |       85,206 |                2.500 |                   2.346 |                  1.971 |
| High (5–10)     |        5,925 |                9.151 |                   7.162 |                  6.644 |
| Very high (>10) |        1,684 |               21.661 |                  12.385 |                 15.434 |

The rolling averages for the very-high-error group were initially missing because of a row-alignment issue. These values must be rechecked before drawing conclusions about the relationship between recent sales features and very large errors.

The broader pattern is clear: large errors are associated with higher actual demand, and the model frequently predicts less than the actual sales during high-demand observations.

## 10. Underprediction by Item

An item-level investigation identified products with the largest cumulative positive underprediction.

Examples included:

* `HOBBIES_1_178`
* `FOODS_3_723`
* `HOBBIES_1_371`
* `FOODS_3_288`
* `HOUSEHOLD_1_465`

`HOBBIES_1_178` had the largest total underprediction in this analysis, approximately 2,294.95 units.

These totals are calculated across the available item-store observations. Items appearing in multiple stores may have more observations, so total underprediction should not be interpreted as a fair standalone ranking of item difficulty without considering observation counts and demand volume.

## 11. Main Findings

The Day 6 investigation identified the following issues:

1. **Zero-sales overprediction:** The model frequently predicts positive sales when actual demand is zero.
2. **Demand-spike underprediction:** Large increases in demand are often underestimated.
3. **Higher error at higher demand:** MAE increases across the higher actual-demand groups.
4. **Store-level differences:** Forecast performance varies across stores, with CA_4 having the highest WAPE in this evaluation.
5. **Weekday variation:** Saturday errors were significantly larger than errors on other weekdays for the investigated item-store sample.
6. **Dependence on recent sales history:** Lag and rolling-average features are among the model's most important features, but historical averages do not always anticipate sudden spikes.

The analysis is descriptive. It identifies patterns associated with forecast errors but does not establish the cause of every error.

## 12. Conclusion

The baseline LightGBM model achieved an MAE of 0.8838 units and a WAPE of 76.13% across 383,000 test observations.

Although total predicted sales were close to total actual sales, the model made substantial errors at the individual observation level. The most important challenges identified were zero-sales overprediction and high-demand underprediction.

The Day 6 findings provide a clear direction for the next phase: test targeted model improvements and evaluate them against the baseline using the same test observations and metrics.

## 13. Next Steps: Day 7

The next phase will focus on model improvement.

Planned activities:

1. Establish baseline metrics by actual demand group.
2. Investigate approaches for reducing overprediction on zero-sales days.
3. Test an improvement designed to better capture demand spikes.
4. Compare the improved model with the baseline on the same evaluation data.
5. Retain an improvement only if the measured results justify it.

The existing baseline results will be preserved so that any improvement can be measured fairly.
