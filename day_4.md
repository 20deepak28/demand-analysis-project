# Day 4: Price Feature Engineering, Demand Analysis & Model Development

## 1. Objective

The primary objective of Day 4 was to enrich our retail demand forecasting dataset with product pricing information and investigate how price changes coincide with sales behavior.

Until now, our forecasting work had primarily relied on historical sales, lag features, rolling averages, calendar information, weekdays, events, and SNAP indicators.

However, retail demand is influenced by more than historical sales patterns. Product prices can change over time, and understanding how those changes relate to demand is an important step toward building a more informative forecasting system.

Today's work focused on integrating price data, engineering price-related features, handling missing values, developing price-aware models, and exploring the relationship between detected price changes and observed sales.

---

## 2. Integrating the Price Dataset

We used the M5 Forecasting dataset, which provides daily unit sales, calendar information, and weekly selling prices for individual products across Walmart stores.

The relevant datasets were:

* **Sales data:** Historical daily unit sales for each item-store combination.
* **Calendar data:** Dates, weekdays, events, and SNAP-related indicators.
* **Selling-price data:** Weekly selling prices for individual products in specific stores.

The sales dataset contained 30,490 item-store time series, while our development dataset contained 1,000 sampled series.

We retained this sample for development rather than immediately processing every available series into a much larger daily dataset.

### Integration process

We first connected the daily sales observations to the calendar using the day identifier.

We then connected the resulting data to the selling-price dataset using three keys:

* `store_id`
* `item_id`
* `wm_yr_wk`

The calendar's week identifier allowed us to associate each daily sales observation with the corresponding weekly product price.

We used merge validation to verify the expected relationships between the datasets and checked that the number of rows remained unchanged after merging.

### Result

The merged dataset contained **1,913,000 rows**, matching the number of observations in our sampled daily sales dataset.

This was an important validation step: the price merge did not unexpectedly increase the number of sales observations.

---

## 3. Investigating Missing Price Data

One of the first challenges was the presence of missing selling prices.

After merging, we found:

* Total observations: 1,913,000
* Observations with missing selling prices: 420,812
* Approximate missing-price rate: 22%

Initially, missing prices could have appeared to indicate a problem with the merge. However, further investigation showed that price coverage was incomplete in earlier weeks for some item-store combinations.

For example, an inspected FOODS product at a California store had no recorded price in an early week, while prices were available in subsequent weeks.

This suggested that at least some missing values reflected the historical availability of price records rather than a failed merge.

### Missing prices by category

| Category  | Missing-price percentage |
| --------- | -----------------------: |
| FOODS     |                   21.70% |
| HOBBIES   |                   22.74% |
| HOUSEHOLD |                   21.97% |

Missing-price rates were relatively similar across the three categories.

### Missing prices by state

We also investigated the number of missing-price observations across California, Texas, and Wisconsin.

| State      | Missing-price observations |
| ---------- | -------------------------: |
| California |                    178,787 |
| Texas      |                    120,001 |
| Wisconsin  |                    122,024 |

These counts describe our sampled dataset, not the entire M5 dataset.

### Key finding

Missing price information was substantial enough that it could not simply be ignored.

We needed a consistent strategy for handling these values before using price information in our machine-learning models.

---

## 4. Engineering Price-Related Features

After validating the merged data, we created additional features to represent product pricing and price changes.

### 4.1 Selling price — `sell_price`

This feature represents the recorded selling price for an item in a particular store and week.

It provides the model with information about the product's price level.

### 4.2 Previous price — `previous_price`

We sorted the observations chronologically within each item-store series and calculated the selling price from seven daily rows earlier.

Because prices are recorded weekly and repeated across daily observations, this shift generally compares the current price with the corresponding weekday in the previous week when both prices are available.

This feature helped us investigate whether the recorded price had changed relative to the previous week.

### 4.3 Percentage price change — `price_change_pct`

We calculated the percentage difference between the current selling price and the previous price.

This represents the relative price movement rather than simply the absolute difference between two prices.

Missing or unavailable previous prices were handled as missing values rather than being treated as genuine price changes.

### 4.4 Price-change indicator — `price_changed`

We created a binary feature:

* `1`: Both current and previous prices were available and differed.
* `0`: Otherwise, including cases where a valid comparison was unavailable.

The feature helped identify observations with a detected price change.

An important limitation is that a value of zero does not always mean the price remained stable. It can also indicate insufficient price history.

### 4.5 Log price change — `log_price_change`

We also calculated the logarithm of the ratio between the current price and the previous price.

Log price changes provide a mathematically useful representation of relative price movements.

The calculation was performed only when both prices were positive.

We inspected the resulting distribution and observed that some products experienced large recorded price movements. These observations were not automatically removed because extreme values require investigation before deciding whether they represent errors or genuine price changes.

### Price-feature summary

| Feature            | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| `sell_price`       | Represents the recorded product price                     |
| `previous_price`   | Provides a reference price from seven daily rows earlier  |
| `price_change_pct` | Measures percentage price movement                        |
| `log_price_change` | Represents relative price movement on a logarithmic scale |
| `price_changed`    | Identifies detected price changes                         |
| `price_missing`    | Identifies observations without a recorded current price  |

These features expanded the information available to our forecasting models beyond historical sales and calendar variables.

---

## 5. Handling Missing Values Without Data Leakage

Missing prices required special attention because replacing them indiscriminately could introduce misleading information.

We used a training-derived imputation strategy.

### Imputation procedure

1. Calculated the global median selling price from the training period.
2. Calculated the median selling price for each item-store series using training data.
3. Filled missing prices with the corresponding item-store median where available.
4. Used the training-period global median as a fallback.
5. Filled missing log-price changes using the training-period median.
6. Retained a separate `price_missing` indicator so the model could distinguish originally missing prices from recorded prices.

The global median selling price in our training data was **3.34**.

Importantly, we calculated these imputation values from the training period rather than using the full dataset, which would have allowed information from the test period to influence preprocessing.

After imputation, the model-ready datasets contained no missing values in the imputed price features.

### Why this matters

Imputation allows models to process observations that would otherwise contain missing values.

However, an imputed price is not an observed historical price. Retaining the missingness indicator helps preserve this distinction.

---

## 6. Developing Price-Aware Forecasting Models

After creating the additional features, we trained three regression models using the price-enriched dataset.

The models were:

1. Random Forest Regressor
2. LightGBM Regressor
3. Linear Regression

The models used our existing historical-sales and calendar features, supplemented by the price-related features.

### Existing forecasting features

Our base feature set included:

* `lag_1`
* `lag_7`
* `lag_28`
* `rolling_mean_7`
* `rolling_mean_28`
* `day_of_week`
* `month`
* `is_event`
* `snap_CA`
* `snap_TX`
* `snap_WI`

The additional price features were:

* `sell_price_imputed`
* `log_price_change_imputed`
* `price_changed`
* `price_missing`

The target variable remained `sales`.

### Evaluation split

We used a chronological train-test split rather than randomly assigning individual observations to the training and test sets.

The split was:

| Dataset  | Period                       | Rows before feature-based filtering |
| -------- | ---------------------------- | ----------------------------------: |
| Training | Before April 8, 2015         |                           1,530,000 |
| Testing  | April 8, 2015–April 24, 2016 |                             383,000 |

After excluding training observations with missing lag or rolling features, the model-training dataset contained 1,502,000 rows.

The test dataset retained 383,000 rows.

This split preserved chronological ordering and gave us a consistent test period for evaluating the price-aware models.

---

## 7. Price-Aware Model Results

We evaluated the models using Mean Absolute Error (MAE) and Weighted Absolute Percentage Error (WAPE).

### Results

| Model                              |    MAE |   WAPE |
| ---------------------------------- | -----: | -----: |
| Random Forest + Price Features     | 0.8845 | 76.19% |
| LightGBM + Price Features          | 0.8851 | 76.25% |
| Linear Regression + Price Features | 0.9078 | 78.19% |

Lower values indicate better performance for both metrics.

### Interpretation

**Random Forest** achieved the lowest MAE and WAPE among the three price-aware models, although its advantage over LightGBM was small.

**LightGBM** delivered very similar performance to Random Forest, making it another strong candidate for further experimentation.

**Linear Regression** performed less accurately than the two tree-based models on this evaluation.

These results provide a preliminary comparison of the three models using the same price-aware feature set and test period.

However, we had already trained baseline models before integrating price data. Those original results came from a different evaluation setup.

Consequently, we cannot use the original baseline metrics to claim that price features improved or worsened performance. A fair assessment requires baseline predictions on the same test observations and under the same evaluation methodology.

---

## 8. Investigating Sales Behavior on Price-Change Days

After model development, we explored the relationship between detected price changes and observed sales.

Our first analysis compared average sales for observations with and without a detected price change.

### Results

| Metric                 | No detected price change | Price changed |
| ---------------------- | -----------------------: | ------------: |
| Number of observations |                1,896,355 |        16,645 |
| Average sales          |                   0.9869 |        1.6364 |
| Median sales           |                        0 |             0 |
| Total units sold       |                1,871,424 |        27,238 |

### Finding 1: Higher average sales on detected price-change days

Average sales were approximately 1.6364 units on detected price-change days, compared with 0.9869 units in the other group.

That is an approximately 65.8% difference in average sales.

However, the groups were not balanced: detected price-change observations accounted for only about 0.87% of all observations.

Furthermore, the group without a detected price change also included observations where sufficient price history was unavailable.

The difference is therefore an exploratory finding, not evidence that price changes caused higher demand.

### Finding 2: Zero sales remained common

The median sales value was zero for both groups.

This indicates that zero-sales observations were common even when a price change was detected.

Average sales alone do not fully describe the distribution, especially in intermittent-demand retail data.

### Finding 3: The groups had very different sample sizes

The analysis included far more observations without a detected price change than observations with one.

This imbalance matters when interpreting the results and reinforces the need for more careful comparisons.

---

## 9. Comparing Sales With the Previous Day

Next, we compared sales on detected price-change days with sales on the previous day for the same item-store series.

We classified each observation into one of three groups:

* Sales increased
* Sales decreased
* Sales remained unchanged

### Results

| Sales behavior  | Observations | Percentage |
| --------------- | -----------: | ---------: |
| Sales unchanged |        7,955 |     47.79% |
| Sales increased |        4,826 |     28.99% |
| Sales decreased |        3,864 |     23.22% |
| **Total**       |   **16,645** |   **100%** |

### Finding 4: Unchanged sales were the most common outcome

Approximately 47.79% of observations showed no change in sales relative to the previous day.

This is important because a detected price change did not necessarily coincide with a change in daily unit sales.

### Finding 5: Sales increases were more frequent than sales decreases

Sales increased in 4,826 observations and decreased in 3,864.

Thus, increases were more frequent than decreases in this sample of detected price-change days.

However, this comparison does not establish whether the price change itself influenced sales. Daily demand naturally fluctuates, and other variables may explain the observed differences.

---

## 10. Category-Level Price Analysis

We then investigated whether the observed sales patterns differed across the three product categories.

The categories were FOODS, HOBBIES, and HOUSEHOLD.

For each category, we calculated:

* Number of detected price-change observations
* Average sales on those observations
* Average sales on the previous day
* Average change in sales relative to the previous day

### Results

| Category  | Price-change observations | Average sales | Previous-day average sales | Average sales change |
| --------- | ------------------------: | ------------: | -------------------------: | -------------------: |
| FOODS     |                    10,932 |        1.9705 |                     1.7003 |              +0.2701 |
| HOBBIES   |                     2,484 |        1.1981 |                     1.0491 |              +0.1490 |
| HOUSEHOLD |                     3,229 |        0.8427 |                     0.7070 |              +0.1356 |

### Finding 6: FOODS had the largest average sales difference

FOODS showed the largest difference between current sales and previous-day sales, at approximately 0.2701 units.

It also had the highest average sales level among the three categories.

This identifies FOODS as a useful candidate for more detailed investigation. It does not establish that FOODS demand is more sensitive to price changes.

### Finding 7: HOBBIES showed a smaller positive difference

HOBBIES recorded an average sales difference of approximately 0.1490 units.

Although the difference was smaller than that of FOODS, average sales were still higher on detected price-change days than on the previous day.

### Finding 8: HOUSEHOLD had the lowest average sales

HOUSEHOLD recorded an average sales difference of approximately 0.1356 units.

Its average sales were also the lowest among the three categories.

These results reflect differences in observed sales levels across categories. They should not be interpreted as a ranking of price sensitivity.

---

## 11. Visualizing the Category-Level Results

We created a grouped bar chart titled:

**Average Sales Before and on Price-Change Days**

The chart compared previous-day average sales with average sales on detected price-change days for FOODS, HOBBIES, and HOUSEHOLD.

### What the chart showed

* FOODS had the highest average sales in both groups.
* HOBBIES occupied the middle position.
* HOUSEHOLD had the lowest average sales.
* All three categories showed higher average sales on detected price-change days than on the previous day.

The visualization made the category differences easier to interpret than a table alone.

It also provided a clear summary of the exploratory analysis completed during Day 4.

---

## 12. Technical Challenges and Lessons Learned

Day 4 involved more than simply adding features to a dataset.

### Challenge 1: Understanding multi-table joins

We had to understand how daily sales, calendar dates, weekly identifiers, and item-store prices fit together.

Choosing the correct merge keys was essential to avoid incorrectly matching prices or multiplying sales observations.

### Challenge 2: Investigating missing values

The large number of missing prices initially required investigation.

We checked missingness across categories, states, and historical weeks instead of assuming every missing value represented a coding error.

This reinforced an important data-science principle: missing values should be investigated before being handled.

### Challenge 3: Creating meaningful features

We transformed raw selling prices into additional features describing relative price changes and whether a change had been detected.

This helped turn raw source data into information that could be used for modeling and exploratory analysis.

### Challenge 4: Preventing preprocessing leakage

We calculated price-imputation values from the training period.

This helped prevent the test period from influencing the preprocessing statistics.

### Challenge 5: Interpreting model metrics correctly

We recognized that model metrics from different evaluation setups cannot be compared directly.

A model can appear better or worse because of differences in the test period or evaluation methodology, rather than because of the feature engineering itself.

### Challenge 6: Interpreting observed relationships carefully

Higher average sales on detected price-change days do not demonstrate that price changes caused those sales outcomes.

This distinction between an observed association and a causal explanation is essential when working with real-world data.

### Challenge 7: Learning through debugging and explanation

Understanding the code was an important part of the process. The work required following how data moved through merges, feature engineering, imputation, model training, and analysis.

Using AI assistance to explain unfamiliar sections helped support the learning process, but the findings still needed to be checked against the actual outputs.

---

## 13. Day 4: Final Summary

By the end of Day 4, we had:

* Integrated weekly selling prices into the daily sales dataset.
* Validated that the merge preserved the number of observations.
* Investigated missing prices across categories, states, and historical weeks.
* Engineered multiple price-related features.
* Implemented training-derived price imputation.
* Created a chronological train-test split.
* Trained Random Forest, LightGBM, and Linear Regression with price features.
* Evaluated the price-aware models using MAE and WAPE.
* Examined sales behavior on detected price-change days.
* Compared sales changes across FOODS, HOBBIES, and HOUSEHOLD.
* Created a visualization of category-level results.
* Identified evaluation limitations that must be addressed before making definitive model comparisons.

## 14. Conclusion

Day 4 expanded our demand forecasting work from historical sales and calendar features to include product pricing information.

The most important outcome was not simply that we trained three additional models. We also investigated the quality and availability of price data, developed features from raw pricing records, handled missing values, and explored how observed sales differed around detected price changes.

Our exploratory analysis showed higher average sales on detected price-change days across all three categories. However, these findings remain descriptive and require more rigorous analysis before we can draw conclusions about price sensitivity.

The price-aware models also provided a useful benchmark for future experiments, although their performance must be compared with baseline models under identical evaluation conditions.

**The next stage is to build on this foundation, improve the evaluation methodology, and continue developing a more reliable retail demand forecasting system.**
