# DAY 14 --- Future Forecasting & Final Dashboard Preparation

**Project:** Retail Demand Forecasting & Inventory Optimization\
**Work covered:** Previous Day 14 dashboard work + Day 15 future
forecasting\
**Documentation convention:** Combined and recorded as Day 14.

------------------------------------------------------------------------

## 1. Objectives

-   Complete a 28-day recursive future-demand forecasting run for all
    product-store combinations.
-   Generate forecast outputs and product-level forecast summaries.
-   Prepare a separate notebook for the final client-facing Streamlit
    dashboard.
-   Keep final dashboard work separate from model training and
    forecasting notebooks.

## 2. Existing Dashboard Work

A Streamlit dashboard had already been developed in `dashboard/app.py`,
using Streamlit, Plotly, and Pandas.

Its six sections were: 1. Executive Overview 2. Demand Forecast Analysis
3. Model Performance Comparison 4. Store & Category Analysis 5.
Inventory Optimization 6. High-Risk Product Monitoring

Client-facing requirements: - Do not expose backend chunk labels or
chunk selectors. - Allow product and store exploration across the
complete dataset. - Use business-friendly labels such as Demand
Forecast, Inventory Risk, Sales Trends, and Product Performance. - Keep
the dashboard application separate from modelling notebooks.

## 3. Future Forecasting --- 28-Day Horizon

### Forecast setup

-   Model: trained Retail Demand LSTM checkpoint
    `retail_demand_lstm_final.pt`, selected Epoch 5.
-   Historical input window: 28 days.
-   Forecast horizon: 28 days.
-   Product-store series: 30,490.
-   Forecast dates: **23 May 2016 -- 19 June 2016**.
-   Approach: recursive, day-by-day inference. Each predicted day is
    added to the rolling history used for the next prediction.
-   Future calendar and sell-price information were prepared for the
    forecast horizon.
-   SNAP features were aligned to the corresponding state (CA, TX, or
    WI).

### First forecasting run

The first full run generated 853,720 predictions. Some forecasts were
implausibly large; for example, the highest-demand series had a forecast
average near 940 units/day. This exposed a target-scale handling issue
in the inference code. The first run was retained as an earlier
experiment and was not treated as the final forecast output.

### Corrected-scale forecasting run

A second full run applied an inverse transformation to the model output
before converting `sales_log` back to sales units.

**Important limitation:** The original training target construction and
the discrepancy between saved validation predictions and reconstructed
inference had not been conclusively reconciled. This run is therefore a
corrected-scale forecasting candidate, not a fully validated business
forecast.

### Corrected run results

  Metric                                             Result
  -------------------------------------------- ------------
  Product-store combinations                         30,490
  Forecast days                                          28
  Total predictions                                 853,720
  Forecast start                                 2016-05-23
  Forecast end                                   2016-06-19
  Mean predicted sales per product-store-day       0.858323
  Standard deviation                               1.687794
  Median                                           0.342938
  75th percentile                                  0.832202
  Maximum daily prediction                        73.081833

### Top 10 forecast totals

  Product-store series            Forecast total   Average daily demand
  ----------------------------- ---------------- ----------------------
  FOODS_3_090_CA_3_evaluation           1,253.03                  44.75
  FOODS_3_586_TX_2_evaluation           1,204.27                  43.01
  FOODS_3_090_WI_3_evaluation           1,054.17                  37.65
  FOODS_3_586_CA_3_evaluation           1,025.28                  36.62
  FOODS_3_090_TX_3_evaluation             984.51                  35.16
  FOODS_3_586_TX_3_evaluation             962.96                  34.39
  FOODS_3_090_TX_2_evaluation             909.98                  32.50
  FOODS_3_586_TX_1_evaluation             892.29                  31.87
  FOODS_3_681_CA_3_evaluation             832.75                  29.74
  FOODS_3_090_CA_1_evaluation             811.40                  28.98

The series `FOODS_3_090_CA_3_evaluation` had recent 28-day historical
sales totalling 3,357 units (about 119.89 units/day), while its
corrected-scale forecast averaged 44.75 units/day. This is a substantial
decrease and must be investigated before presenting the forecast as
reliable.

## 4. Forecast Output Files

The corrected run was saved separately under:

`Data/processed/full_dataset/future_forecasts_corrected_v2/`

Expected outputs: - `future_forecasts.parquet` -
`future_forecasts.csv` - `forecast_summary.parquet` -
`forecast_summary.csv`

The earlier, uncorrected run was kept in a separate forecast folder.
Neither run should overwrite validation prediction files or trained
model checkpoints.

## 5. Validation and Modelling Limitations

The saved validation prediction files contained 411 days per
product-store series, covering 8 April 2015 through 22 May 2016.

For `FOODS_1_001_CA_1_evaluation`, saved validation predictions
produced: - MAE: 0.752824 - RMSE: 1.084536 - WAPE: 109.33% - Actual
total: 283 - Predicted total: 161.986

A separate reconstructed one-step inference for 22 May 2016 did not
reproduce the saved prediction: the saved value was approximately
0.621495, while reconstructed inference produced approximately 0.189140.
Historical engineered feature values and scaler values were checked and
matched, but the original validation sequence/inference pipeline was not
recovered.

**Conclusion:** The corrected-scale forecast output is generated and
stored, but forecast accuracy is not established. Do not describe the
future forecasts as validated or production-ready until the target
transformation and validation inference mismatch are resolved and
backtesting is completed.

## 6. Final Dashboard Notebook Preparation

A new notebook was planned:

`notebooks/08_final_dashboard.ipynb`

Its purpose is to create the final client-facing Streamlit + Plotly
dashboard, separate from the modelling workflow.

Planned sections: 1. Executive Overview 2. Demand Forecasting 3.
Historical vs Forecast 4. Model Performance 5. Store & Category Analysis
6. Inventory Optimization 7. High-Risk Products

The dashboard should provide product/store filtering and must not expose
technical chunking details.

### Dashboard data-loading issue

During setup of Notebook 08, the expected project path was:

`/content/drive/MyDrive/Retail-Demand-Forecasting`

However, the currently mounted Drive showed only a `dashboard` folder
inside that project directory. The expected `Data`, `models`, and
`notebooks` folders were not visible. Searches did not locate the
forecast Parquet files, inventory-risk Parquet file, model checkpoint,
or feature Parquet chunks.

The dashboard notebook therefore could not load its datasets from the
expected location. No forecasting rerun or destructive file operation
was performed during this troubleshooting.

**Current status:** The data-location/recovery issue must be resolved
before dashboard integration can continue.

## 7. Technologies Used

-   Python
-   Pandas
-   NumPy
-   PyTorch
-   Scikit-learn
-   Parquet
-   Google Colab
-   Google Drive
-   Streamlit
-   Plotly

## 8. Completed Work

-   Generated a 28-day forecast for all 30,490 product-store series.
-   Produced 853,720 daily forecast records.
-   Created product-store forecast summaries.
-   Saved a separate corrected-scale forecast candidate.
-   Defined the final dashboard structure and client-facing
    requirements.
-   Started a separate Notebook 08 for final dashboard development.
-   Identified that the current mounted Drive project path does not
    contain the expected data and model folders.

## 9. Pending Work

1.  Locate or restore the original `Data`, `models`, and `notebooks`
    project folders.
2.  Recover the forecast, inventory, and model artifacts if available.
3.  Resolve the model target-scaling and validation inference mismatch.
4.  Backtest the recursive forecasting pipeline before making accuracy
    claims.
5.  Build the final Streamlit dashboard in `08_final_dashboard.ipynb`.
6.  Integrate forecast, inventory, risk, category, store, and
    model-performance data.
7.  Test the dashboard end-to-end before sharing it with clients.

------------------------------------------------------------------------

## Final Day 14 Status

**Forecast generation:** Completed for 30,490 product-store combinations
and 28 days.\
**Forecast validation:** Pending; corrected-scale outputs are not yet
confirmed reliable.\
**Final dashboard:** Structure planned; implementation is blocked by
missing project data/model folders in the currently mounted Drive
location.\
**Project files:** Earlier outputs and the corrected-scale candidate
were intended to remain separate; no existing model was retrained as
part of this work.
