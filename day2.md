# Day 2 — Data Preparation & Demand Analysis

## 1. Objective

The objective of Day 2 was to transform the raw sales dataset into a time-series-friendly format, connect sales observations with calendar information, and investigate demand patterns across weekdays.

## 2. Work Completed

### Task 1: Memory Management

Checked the memory usage of the sales dataset and available system RAM before transforming the data.

- Initial sales dataset memory usage: approximately 455 MB.
- Available RAM before cleanup: approximately 5.03 GB.
- Available RAM after cleanup: approximately 9.08 GB.

This helped ensure sufficient memory was available for data processing.

### Task 2: Wide-to-Long Transformation

The original sales dataset stored daily sales in separate columns named `d_1`, `d_2`, `d_3`, and so on.

Used Pandas `melt()` to transform the dataset into long format.

```python
sales_columns = [
    col for col in sales.columns
    if col.startswith("d_")
]

sales_long = sales.melt(
    id_vars=[
        "id",
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id"
    ],
    value_vars=sales_columns,
    var_name="d",
    value_name="sales"
)
```

### Task 3: Understanding `melt()`

The `melt()` function converts data from wide format to long format.

**Important parameters:**
- `id_vars`: Columns that remain unchanged.
- `value_vars`: Columns converted into rows.
- `var_name`: Name of the column containing the original column names.
- `value_name`: Name of the column containing the corresponding values.


#### This transformation makes the dataset easier to work with for time-series analysis.

### Task 4: Calendar Data Integration

###### Merged the sales dataset with calendar information.

###### Added the actual date, weekday, and selected event information to each sales observation.

###### The merge used a left join to preserve all existing sales records.

### Task 5: Weekday Demand Analysis

###### Calculated average sales for each weekday.

```python
weekday_demand = (
    sales_long.groupby("weekday")["sales"]
    .mean()
    .sort_values(ascending=False)
)
```

### Weekday Average Sales Results

| Weekday | Average Sales |
|---|---:|
| Saturday | 1.363 |
| Sunday | 1.349 |
| Friday | 1.123 |
| Monday | 1.078 |
| Tuesday | 0.996 |
| Thursday | 0.991 |
| Wednesday | 0.984 |

**Observation:**
- Saturday recorded the highest average sales at 1.363 units.
- Sunday followed at 1.349 units.
- Wednesday recorded the lowest average sales at 0.984 units.
- Weekend sales were higher than weekday sales in this dataset.

*Note: These figures represent average units sold per product-store combination for each weekday.*
These values represent average units sold per product-store combination for each weekday.

### Task 6: Demand Visualization

- Created a bar chart to visualize average sales by weekday.

- The visualization helps compare demand across the seven days of the week.

- Observation: Saturday and Sunday showed the highest average sales, while Wednesday showed the lowest.

- This is an initial observation and requires further investigation across stores and product categories.

## 3. Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Walmart M5 Forecasting Dataset

## 4. Concepts Learned
- Data Transformation

- Converting wide-format data into long-format data using melt().

- Data Merging

- Combining sales records with calendar information using a left join.

- Grouping and Aggregation

- Using groupby() and mean() to calculate average demand by weekday.

- Data Visualization

- Using bar charts to compare demand patterns across weekdays.

- Memory Management

- Monitoring RAM usage when processing large datasets.

## 5. Challenges Encountered
- The full dataset expanded to more than 58 million rows.
- The transformed DataFrame required approximately 3.5 GB of memory.
- Additional RAM was needed to safely process the dataset.
- Understanding how daily identifiers map to actual calendar dates required careful inspection.
## 6. Business Insights
- Average sales differed across weekdays.
- Weekend demand was higher than weekday demand in the overall dataset.
- These differences may help improve demand forecasting.
- Further analysis is needed to determine whether the patterns remain consistent across products, categories, and stores.
## 7. Next Steps
- Investigate demand patterns across product categories and stores.
- Prepare time-series features for forecasting.
- Explore lag features and rolling averages.
- Train baseline forecasting models.
- Evaluate model performance.
- Develop inventory optimization logic.
## 8. Day 2 Summary

- Day 2 focused on transforming the sales dataset, integrating calendar information, managing memory usage, and analyzing weekday demand.

- The resulting dataset connects individual product-store sales observations with calendar information, establishing a foundation for subsequent feature engineering and demand forecasting.


**Save location:** Your project root folder.

**Filename:** `DAY_02_NOTES.md`

