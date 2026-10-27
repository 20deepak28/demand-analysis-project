# Day 8: Inventory Simulation & Optimization

## Objective

Develop and evaluate a historical inventory replenishment simulation using item-store demand patterns, reorder points, safety stock, and lead-time assumptions.

## 1. Dataset

* **Simulation period:** April 8, 2015 – April 24, 2016
* **Item-store combinations:** 1,000
* **Simulation observations:** 383,000 daily records
* **Lead time:** 7 days
* **Target coverage:** 14 additional days beyond lead time

## 2. Inventory Policy

Historical demand statistics were calculated using data through April 7, 2015.

The inventory policy calculated:

* Average daily demand
* Daily demand standard deviation
* Safety stock
* Reorder point
* Target stock level
* Recommended order quantity

Replenishment orders were placed when inventory position reached or fell below the reorder point. Orders were scheduled to arrive after the assumed 7-day lead time.

## 3. Simulation Results

| Metric                                     |        Result |
| ------------------------------------------ | ------------: |
| Item-store combinations                    |         1,000 |
| Total demand                               | 444,626 units |
| Fulfilled demand                           | 375,062 units |
| Unmet demand                               |  69,564 units |
| Overall demand-weighted fill rate          |        84.35% |
| Total units ordered                        |       372,058 |
| Total replenishment orders                 |        62,778 |
| Average inventory across item-store series |   10.68 units |

### Established-Demand Products

| Metric                    |        Result |
| ------------------------- | ------------: |
| Product combinations      |           982 |
| Total demand              | 434,924 units |
| Fulfilled demand          | 375,062 units |
| Unmet demand              |  59,862 units |
| Demand-weighted fill rate |        86.24% |

### Zero-History Products

* 18 combinations had zero historical demand through April 7, 2015.
* These combinations experienced 9,702 units of demand during the simulation.
* None of this demand was fulfilled because the historical policy assigned zero initial and target stock.
* These products require a separate cold-start or intermittent-demand policy.

## 4. Deliverables

* `day8_inventory_simulation_results.csv`
* `day8_inventory_simulation_summary.csv`
* `day8_inventory_evaluation.csv`
* `day8_inventory_performance.png`

## 5. Limitations

* This is a historical backtest using observed sales as demand, not a live deployment.
* Lead time is assumed to be a fixed seven days.
* Initial inventory is set to the historically calculated target stock.
* The policy has not yet been compared against alternative inventory policies.
* No procurement costs, holding costs, or lost-sales costs are included.
* Zero-history products are reported separately because the current policy cannot handle their later demand.
* Fill rate measures fulfilled units divided by total demand; it does not establish profitability or optimal inventory cost.

## 6. Next Steps

1. Compare the current policy with a baseline inventory strategy.
2. Investigate service-level improvements and inventory costs.
3. Develop an interactive dashboard for forecasts and inventory KPIs.
4. Document the project workflow and results in the repository README.

**Status:** Inventory simulation completed; further policy comparison and optimization remain.
