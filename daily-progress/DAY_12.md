# Day 12 --- Multivariate LSTM Training & Model Selection

## Project

**Retail Demand Forecasting & Inventory Optimization using the M5
Walmart dataset**

## 1. Objective

Develop, train and evaluate a multivariate LSTM on the complete M5
training sequence set, compare it with the full-dataset LightGBM
baseline, and select a model candidate for the next stage.

## 2. Compute environment

-   Platform: Google Colab
-   GPU: NVIDIA Tesla T4 (14.56 GB reported GPU memory)
-   System RAM: approximately 12.67 GB
-   PyTorch: 2.11.0+cu130
-   CUDA: available
-   Input data: 31 Parquet feature chunks

## 3. Dataset and sequence preparation

The dataset contains 30,490 product-store time series, each with 1,941
daily observations (59,181,090 long-format rows before sequence
filtering).

**Sequence design** - Historical window: 28 days - Historical input: 14
features - Target-day known inputs: 8 features - Target:
`sales_log = log1p(sales)`

Historical features: `sales_log`, `sell_price_filled`, `price_missing`,
`lag_1`, `lag_7`, `lag_28`, `rolling_mean_7`, `rolling_mean_28`,
`day_of_week`, `month`, `is_event`, `snap_CA`, `snap_TX`, `snap_WI`.

Target-day known features: `sell_price_filled`, `price_missing`,
`day_of_week`, `month`, `is_event`, `snap_CA`, `snap_TX`, `snap_WI`.

The model uses the previous 28 days as historical input and target-day
known price/calendar/SNAP/event information through a separate branch.

**Chronological split** - Training target dates: through 2015-04-07 -
Validation target dates: from 2015-04-08 - Training sequences per
series: 1,502 - Validation sequences per series: 411 - Expected training
sequences: 45,795,980 - Expected validation sequences: 12,531,390

Validation is rolling one-step-ahead: each validation prediction uses
the preceding 28 days of observed history. It is not a fixed-origin
recursive forecast across the whole validation horizon.

**Preprocessing** - Numerical features standardized using a
`StandardScaler` fitted incrementally on training-period data only. -
Binary features left unscaled. - `sales_log` calculated using
`log1p(sales)`. - Missing lag/rolling values at series starts filled
with zero. - Missing prices represented by `price_missing`;
`sell_price_filled` filled with zero. - Scaler saved as
`models/lstm_feature_scaler.pkl`. - Historical window, target-day
feature and target alignment checks passed.

## 4. LSTM architecture

Two-input multivariate LSTM:

**Historical branch** - Input: `(batch, 28, 14)` - 2 LSTM layers -
Hidden size: 128 - Dropout: 0.2 - Final hidden state used as historical
representation

**Future-known branch** - Input: 8 features - Linear layer: 8 → 32 -
ReLU activation

**Regression head** - Concatenated representation: 128 + 32 = 160 -
Linear: 160 → 64 - ReLU, dropout 0.2 - Output: 64 → 1

Total trainable parameters: **216,481**.

## 5. Training configuration

  Setting                                            Value
  ------------------------------------ -------------------
  Batch size                                         2,048
  Shuffle buffer                                    65,536
  Optimizer                                          AdamW
  Initial learning rate                              0.001
  Weight decay                                     0.00001
  Loss                                          Huber Loss
  Gradient clipping                                    1.0
  Mixed precision                                     FP16
  Scheduler                              ReduceLROnPlateau
  Scheduler factor / patience                      0.5 / 1
  Minimum learning rate                            0.00001
  Maximum planned epochs                                 8
  Early-stopping patience configured                     3

Data was streamed from Parquet chunks instead of materializing all
sequences in memory. Recovery checkpoints were saved after each
completed Parquet chunk.

Batch-size benchmark: - Batch 512: about 9,174 samples/sec - Batch
2,048: about 36,401 samples/sec

## 6. Training results

All five epochs processed 45,795,980 training sequences.

  Epoch     Training loss            Training time
  ------- --------------- ------------------------
  1              0.162225                 8.05 min
  2              0.160747                 7.58 min
  3              0.160228   approximately 7--8 min
  4              0.160008                 7.57 min
  5              0.159743                 8.21 min

Training loss decreased gradually, but lower training loss did not
always mean better validation performance.

## 7. Full validation results

Each epoch was evaluated on all 12,531,390 validation sequences. Metrics
were calculated in original sales units after inverse transformation
from standardized log-sales. Negative predicted log-sales were clipped
at zero before inverse transformation.

  Epoch     Validation loss            MAE           RMSE         WAPE
  ------- ----------------- -------------- -------------- ------------
  1                0.220980       0.919404       2.325085       70.79%
  2            **0.215800**       0.889473       2.137365       68.49%
  3                0.217135       0.902027       2.315459       69.45%
  4                0.217465       0.893776       2.162783       68.82%
  5                0.216647   **0.887903**   **2.149717**   **68.37%**

**Interpretation** - Epoch 2 achieved the best validation Huber loss and
RMSE. - Epoch 5 achieved the best MAE and WAPE. - The learning-rate
scheduler reduced the learning rate from 0.001 to 0.0005 after
validation stopped improving. - Epoch 5 was selected as the project
candidate based on the priority given to MAE and WAPE. Epoch 2 is
retained as an important alternative.

## 8. Comparison with full-dataset LightGBM

Both models were evaluated on the same validation observations.

  Metric         LightGBM   LSTM Epoch 5
  -------- -------------- --------------
  MAE            0.930733   **0.887903**
  RMSE       **2.006124**       2.149717
  WAPE             71.66%     **68.37%**

LSTM Epoch 5 has approximately 4.6% lower MAE and a 3.29
percentage-point lower WAPE than LightGBM. LightGBM has lower RMSE, so
the LSTM has not won every metric. This trade-off should be reported
transparently.

## 9. Model artifacts

Google Drive project root:
`/content/drive/MyDrive/Retail-Demand-Forecasting`

Relevant artifacts: - `models/lstm_feature_scaler.pkl` -
`models/lstm_best.pt` --- best validation-loss checkpoint (Epoch 2) -
`models/lstm_best_wape.pt` --- Epoch 5 WAPE candidate -
`models/retail_demand_lstm_final.pt` --- selected Epoch 5 candidate -
`models/lstm_last.pt` --- latest recovery checkpoint -
`models/model_comparison.json` --- comparison summary

The selected Epoch 5 checkpoint was saved with the model/training state
and configuration.

## 10. Limitations and evaluation notes

1.  M5 does not provide actual inventory on hand or supplier lead times.
    Inventory outputs are recommendations based on assumptions, not live
    stockout alerts or actual purchase orders.
2.  The seven-day lead time in the inventory calculations is
    illustrative, not an observed M5 field.
3.  The safety-stock calculation assumes independent daily demand.
4.  Validation is rolling one-step-ahead using actual preceding
    observations. It is not a recursive multi-week forecast that feeds
    predictions back as future history.
5.  Epoch 5 was selected by MAE and WAPE, not by the lowest validation
    loss or RMSE.
6.  Store-, category-, demand-level and date-level error analysis is
    still pending.
7.  Final dashboard/service integration and production validation are
    still pending.

## 11. Day 13 --- Next steps

1.  Load and verify the selected Epoch 5 checkpoint.
2.  Generate predictions while retaining product-store identifiers and
    target dates.
3.  Analyze errors by store, product category and demand level.
4.  Compare LSTM and LightGBM with visualizations on identical
    validation observations.
5.  Create actual-versus-predicted and residual/error plots.
6.  Inspect large-error cases and intermittent/zero-demand series.
7.  Connect forecasting outputs to inventory optimization analysis.
8.  Save charts, metrics, model artifacts and documentation.
9.  Update the GitHub README with methodology, results, limitations and
    reproducibility instructions.

## Day 12 conclusion

A two-input multivariate LSTM was developed and trained on the full M5
training sequence set using a Tesla T4 GPU. Five full epochs were
completed and evaluated against all 12.53 million validation sequences.

Epoch 5 was selected as the final project candidate because it achieved
the best observed MAE (**0.887903**) and WAPE (**68.37%**). Epoch 2
achieved the best validation loss and RMSE and is retained for
comparison.

The next stage is error analysis, model comparison, visualization and
integration with the inventory optimization work.
