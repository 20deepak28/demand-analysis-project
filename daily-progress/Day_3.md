# Day 3 — Feature Engineering

## 1. Objective

The objective of Day 3 was to develop and validate time-series features for the Retail Demand Forecasting & Inventory Optimization System using the Walmart M5 Forecasting dataset.

These features will help a forecasting model learn from historical sales patterns, calendar information, and special events.

## 2. Dataset Sampling

Initially, we tested our feature-engineering logic on 100 product-store combinations.

After reviewing the sample, we identified that using only the first 100 rows did not provide sufficient coverage of the dataset's different categories, stores, and states.

We then selected a random sample of 1,000 product-store combinations using `random_state=42`.

```python
sample = sales.sample(n=1000, random_state=42).copy()
```

The sample covered all three product categories:

* FOODS
* HOUSEHOLD
* HOBBIES

It also included all 10 stores and all three states: California, Texas, and Wisconsin.

## 3. Data Transformation

The sampled sales data was originally in wide format, with each daily sales observation stored in a separate column.

We converted it into long format using Pandas `melt()`.

```python
sample_long2 = sample.melt(
    id_vars=[
        "id", "item_id", "dept_id",
        "cat_id", "store_id", "state_id"
    ],
    value_vars=daily_columns,
    var_name="d",
    value_name="sales"
)
```

We then extracted the numerical day identifier and sorted the data by product-store combination and day number.

```python
sample_long2["day_number"] = (
    sample_long2["d"]
    .str.replace("d_", "", regex=False)
    .astype("int16")
)

sample_long2 = sample_long2.sort_values(
    ["id", "day_number"]
).reset_index(drop=True)
```

### Result

* Product-store combinations: 1,000
* Daily observations per combination: 1,913
* Total observations: 1,913,000

## 4. Historical Sales Features

We created lag features to provide the forecasting model with information about previous sales.

```python
sample_long2["lag_1"] = (
    sample_long2.groupby("id")["sales"].shift(1)
)

sample_long2["lag_7"] = (
    sample_long2.groupby("id")["sales"].shift(7)
)

sample_long2["lag_28"] = (
    sample_long2.groupby("id")["sales"].shift(28)
)
```

The features represent:

* `lag_1`: Sales from the previous day.
* `lag_7`: Sales from seven days earlier.
* `lag_28`: Sales from 28 days earlier.

These features were calculated separately for each product-store combination.

## 5. Rolling Average Features

We created seven-day and 28-day rolling averages to represent recent sales patterns.

```python
sample_long2["rolling_mean_7"] = (
    sample_long2.groupby("id")["sales"]
    .transform(lambda x: x.shift(1).rolling(7).mean())
)

sample_long2["rolling_mean_28"] = (
    sample_long2.groupby("id")["sales"]
    .transform(lambda x: x.shift(1).rolling(28).mean())
)
```

Using `shift(1)` ensures that the rolling averages use historical sales rather than including the current day's target value.

This helps prevent target leakage when preparing forecasting features.

## 6. Calendar Feature Engineering

We merged the calendar dataset with the sampled sales data using the day identifier `d`.

The merge included:

* Actual date
* Weekday
* Event names and event types
* SNAP indicators for California, Texas, and Wisconsin

We used a many-to-one merge validation because multiple product-store observations can correspond to the same calendar day.

### Numerical weekday feature

We mapped weekday names to numerical values:

| Weekday   | Value |
| --------- | ----: |
| Monday    |     0 |
| Tuesday   |     1 |
| Wednesday |     2 |
| Thursday  |     3 |
| Friday    |     4 |
| Saturday  |     5 |
| Sunday    |     6 |

The resulting feature is called `day_of_week`.

### Month feature

We converted the date column to Pandas datetime format and extracted the month.

```python
sample_long2["date"] = pd.to_datetime(
    sample_long2["date"]
)

sample_long2["month"] = (
    sample_long2["date"].dt.month
)
```

### Event indicator

We created a binary feature to identify dates with at least one recorded event.

```python
sample_long2["is_event"] = (
    sample_long2["event_name_1"].notna()
    | sample_long2["event_name_2"].notna()
).astype("int8")
```

* `1`: At least one event name is recorded.
* `0`: Neither event name is recorded.

The dataset contained 154,000 product-store-day observations marked with an event and 1,759,000 without one.

These counts refer to observations, not unique event dates.

## 7. Feature Validation

We checked missing values in the engineered features.

| Feature           | Missing Values |
| ----------------- | -------------: |
| `lag_1`           |          1,000 |
| `lag_7`           |          7,000 |
| `lag_28`          |         28,000 |
| `rolling_mean_7`  |          7,000 |
| `rolling_mean_28` |         28,000 |
| `day_of_week`     |              0 |
| `month`           |              0 |
| `is_event`        |              0 |

The missing values in the lag and rolling features are expected because the earliest observations do not have enough historical data.

For example, each product-store combination has no previous-day observation for its first day, resulting in 1,000 missing values in `lag_1`.

We also inspected the feature values for individual product-store combinations and reviewed category, store, and state coverage.

## 8. Current Dataset Status

The feature-engineered sample contains:

* **Rows:** 1,913,000
* **Columns:** 26
* **Product-store combinations:** 1,000
* **Unique dates:** Expected to be 1,913 across the sample's historical period

The sample covers all three product categories, all 10 stores, and all three states represented in the original sales dataset.

The dataset was prepared for saving in Parquet format under the processed-data directory.

## 9. Work Remaining

The feature-engineering workflow has been developed and partially validated. The following tasks remain:

1. Complete the remaining validation checks.
2. Decide how to handle initial observations with missing historical features.
3. Prepare chronological training and testing datasets.
4. Establish a baseline forecasting method.
5. Train and evaluate forecasting models.
6. Use forecast results for inventory planning.

## 10. Day 3 Summary

Day 3 focused on transforming sampled retail sales data into a time-series format and creating historical and calendar-based features.

The work established the initial feature-engineering pipeline for the Retail Demand Forecasting & Inventory Optimization System.

**Status:** Feature engineering developed; final validation and model preparation remain in progress.
