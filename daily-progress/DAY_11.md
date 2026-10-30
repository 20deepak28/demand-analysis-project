# Day 11 --- Inventory Optimization, Full-Dataset Modeling & LSTM Preparation

**Project:** Retail Demand Forecasting & Inventory Optimization\
**Dataset:** M5 Forecasting (Walmart)\
**Status:** Inventory optimization and LightGBM modeling completed;
multivariate LSTM preparation completed; LSTM training pending.

## 1. Inventory Optimization

### Objective

Generate product-store-level inventory recommendations from historical
demand.

### Assumptions

-   Calculations used all 31 engineered Parquet chunks and training data
    through **2015-04-07**.
-   Total product-store combinations: **30,490**.
-   Assumed lead time: **7 days** (illustrative; actual supplier lead
    times are not available in M5).
-   Target service level: **95%**, z-score **1.645**.
-   Safety-stock calculation assumes independent daily demand.

### Formulas

``` python
safety_stock = z_score * demand_std * sqrt(lead_time)
reorder_point = avg_daily_demand * lead_time + safety_stock
```

Values were rounded up to whole units.

### Priority classification

``` python
inventory_df["priority"] = pd.cut(
    inventory_df["reorder_point"],
    bins=[-1, 10, 50, 150, float("inf")],
    labels=["Low", "Medium", "High", "Critical"]
)
```

  Priority      Product-store combinations
  ----------- ----------------------------
  Low                               19,905
  Medium                             9,091
  High                               1,280
  Critical                             214
  **Total**                     **30,490**

### Example recommendations

  -----------------------------------------------------------------------------------------
  Product-store ID                  Avg. daily    Demand std.   Safety stock  Reorder point
                                        demand           dev.                
  ----------------------------- -------------- -------------- -------------- --------------
  FOODS_3_090_CA_3_evaluation          139.286        116.293            507          1,482

  FOODS_3_586_TX_2                     103.017         31.460            137            859

  FOODS_3_090_CA_1                      70.669         61.740            269            764
  -----------------------------------------------------------------------------------------

### Saved outputs

Directory: `Data/processed/full_dataset/inventory/`

-   `inventory_recommendations.parquet`
-   `inventory_recommendations.csv`
-   `final_inventory_analysis.parquet`
-   `final_inventory_analysis.csv`

**Limitation:** M5 does not provide actual inventory-on-hand levels or
supplier lead times. These outputs are recommended thresholds, not live
stockout alerts or confirmed replenishment orders.

------------------------------------------------------------------------

## 2. Full-Dataset LightGBM Model

### Features and target

``` python
FEATURES = [
    "lag_1", "lag_7", "lag_28",
    "rolling_mean_7", "rolling_mean_28",
    "day_of_week", "month", "is_event",
    "snap_CA", "snap_TX", "snap_WI"
]
TARGET = "sales"
```

### Chronological split

-   Training: through **2015-04-07**
-   Validation: from **2015-04-08**
-   Training rows: **46,649,700**
-   Validation rows: **12,531,390**
-   Total: **59,181,090**

### Parameters

``` python
params = {
    "objective": "regression",
    "metric": ["mae", "rmse"],
    "learning_rate": 0.05,
    "num_leaves": 63,
    "max_depth": -1,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "max_bin": 127,
    "verbosity": -1,
    "num_threads": 4,
    "seed": 42
}
```

### Results

Best iteration: **286**

  Metric     Full validation result
  -------- ------------------------
  MAE                      0.930733
  RMSE                     2.006124
  WAPE                   71.662936%

Saved model: `models/full_dataset_lightgbm.pkl`\
Sample-trained model: `models/sample_lightgbm.pkl`

------------------------------------------------------------------------

## 3. Sample vs Full-Dataset LightGBM

Both models were evaluated on the same full validation rows.

  Metric     Sample-trained model   Full-dataset model
  -------- ---------------------- --------------------
  MAE                    0.939400             0.930733
  RMSE                   2.095643             2.006124
  WAPE                 72.330259%           71.662936%

The full-data model improved MAE by approximately **0.92%**, RMSE by
**4.27%**, and WAPE by **0.67 percentage points**.

**Evaluation protocol:** Rolling one-step-ahead validation. Each
validation prediction uses actual preceding observations. This is not a
fixed-origin recursive forecast over the full validation horizon.

------------------------------------------------------------------------

## 4. Multivariate LSTM --- Data Preparation

### Why multivariate?

The dataset already contains engineered demand, price, calendar, event,
and SNAP features. The LSTM preparation therefore uses a multivariate
sequence instead of historical sales alone.

### Environment and data

-   Google Colab with **NVIDIA Tesla T4**.
-   PyTorch GPU support verified.
-   Google Drive project directory:
    `/content/drive/MyDrive/Retail-Demand-Forecasting`
-   31 Parquet chunks.
-   30,490 product-store time series.
-   First 30 chunks contain 1,000 series each; the final chunk contains
    490.
-   Each complete series contains 1,941 daily observations.

### Input features

``` python
FEATURES = [
    "sales_log",
    "sell_price_filled",
    "price_missing",
    "lag_1",
    "lag_7",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_28",
    "day_of_week",
    "month",
    "is_event",
    "snap_CA",
    "snap_TX",
    "snap_WI"
]
TARGET = "sales_log"
```

Sales was transformed using `log1p`.

### Missing-price handling

In the first tested chunk: - 392,504 prices were missing (approximately
20.22%). - All missing-price rows in that chunk had zero sales. - No
positive-sales rows in that chunk had missing prices.

Created `price_missing` as an indicator and `sell_price_filled` by
filling missing prices with zero. This specific verification was
performed on the first chunk.

### Missing lag and rolling values

Initial missing values in the first chunk:

  Feature             Missing rows
  ----------------- --------------
  lag_1                      1,000
  lag_7                      7,000
  lag_28                    28,000
  rolling_mean_7             7,000
  rolling_mean_28           28,000

These values were filled with zero to retain the initial history rows.

### Scaling

A single `StandardScaler` was fitted incrementally across
training-period data from all 31 chunks. Validation data was not used to
fit the scaler.

Scaled features:

``` python
SCALED_FEATURES = [
    "sales_log",
    "sell_price_filled",
    "lag_1",
    "lag_7",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_28",
    "day_of_week",
    "month"
]
```

Unscaled binary features:

``` python
BINARY_FEATURES = [
    "price_missing",
    "is_event",
    "snap_CA",
    "snap_TX",
    "snap_WI"
]
```

Scaler saved at: `models/lstm_feature_scaler.pkl`

### Sequence generation

-   Sequence length: **28 days**
-   Input shape: **(28, 14)**
-   Target: next-day `sales_log`
-   Training ends: **2015-04-07**
-   Validation starts: **2015-04-08**

First tested product-store series:

  Split        X shape          y shape
  ------------ ---------------- ---------
  Training     (1502, 28, 14)   (1502,)
  Validation   (411, 28, 14)    (411,)

Each target is predicted using the preceding 28 days; the target day is
excluded from its input window.

### Streaming and GPU test

A streaming generator was created to process Parquet chunks and
product-store series without holding all generated sequences in memory
simultaneously.

PyTorch batch transfer test: - X device: `cuda:0` - y device: `cuda:0` -
X shape: `[512, 28, 14]` - y shape: `[512]` - Data type: `float32`

The first prepared chunk contained 1,941,000 rows and its 14 model
features had no missing values after preprocessing.

------------------------------------------------------------------------

## 5. LSTM --- Checks Required Before Training

The LSTM has **not yet been trained**. The following design points
remain:

1.  **Batch mixing and shuffling:** The current generator yields batches
    series-by-series. Improve batch mixing so training does not process
    long consecutive runs from only one product-store series.
2.  **Future-known covariates:** Current sequences contain historical
    calendar and price features. LightGBM also uses target-day calendar
    features. Consider passing target-day known features (day of week,
    month, event, SNAP, and price) separately to the LSTM for a more
    comparable and useful setup.
3.  **Target inverse scaling:** `sales_log` is standardized as an input
    feature, and the sequence function currently takes its target from
    that standardized column too. Before calculating sales-unit metrics,
    reverse the scaling using the `sales_log` scaler mean and scale,
    then apply `expm1`.
4.  **Consistent validation:** Preserve the chronological split and
    rolling one-step-ahead evaluation protocol when comparing LSTM with
    LightGBM.

These are pending implementation checks, not completed model results.

------------------------------------------------------------------------

## 6. Day 11 --- Final Status

### Completed

-   Product-store demand statistics calculated.
-   Safety stock and reorder points calculated.
-   Inventory priority categories assigned.
-   Inventory recommendation files saved.
-   Full-dataset LightGBM trained and evaluated.
-   Sample-trained and full-dataset models compared on identical
    validation rows.
-   Colab Tesla T4 environment configured.
-   Multivariate LSTM features prepared and shared scaler fitted.
-   Sequence generation tested on a product-store series.
-   Streaming pipeline tested on the first Parquet chunk.
-   PyTorch GPU batch transfer verified.

### Pending

-   Finalize LSTM batch sampling and future-known covariate design.
-   Implement and train the multivariate LSTM.
-   Convert predictions back to original sales units and calculate
    metrics.
-   Compare LSTM against the full-dataset LightGBM model.

**Day 11 concludes with inventory optimization and full-dataset LightGBM
completed. The multivariate LSTM data pipeline is prepared, with final
design checks and model training remaining.**
