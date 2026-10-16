# EconoCausal — Day 5 Model Validation and Sensitivity Analysis

## 1. Objective
The objective of Day 5 was to examine how stable the Double Machine Learning (DML) price-effect estimate is under different model configurations and data samples.

## 2. Model Configuration Sensitivity

The Random Forest model was tested with different `min_samples_leaf` values while keeping the number of trees at 100.

| Number of Trees | Minimum Samples per Leaf | Estimated Price Effect |
|---:|---:|---:|
| 100 | 5 | 0.935336 |
| 100 | 10 | 0.921526 |
| 100 | 20 | 0.896581 |

**Observation:** The estimated effect decreased as the minimum leaf size increased. This indicates that the estimate is sensitive to the model configuration.

## 3. Sample Stability Analysis

The model was evaluated on the full dataset and two reproducible random samples.

| Sample | Observations | Estimated Price Effect |
|---|---:|---:|
| Full dataset | 76,000 | 0.921526 |
| Sample 80% A | 60,800 | 0.910325 |
| Sample 80% B | 60,800 | 0.906925 |

**Observation:** The estimates from the two 80% samples were relatively close to each other and to the full-dataset estimate, suggesting some stability under these sample changes.

## 4. Model Evaluation Metrics

| Model | Test Observations | MAE | RMSE | R² |
|---|---:|---:|---:|---:|
| Demand model | 15,200 | 27.0728 | 34.9450 | 0.4471 |
| Price model | 15,200 | 6.1089 | 8.0114 | 0.9587 |

The price model achieved a higher R² than the demand model on the evaluation set. The demand model's performance indicates that demand prediction still has room for improvement.

## 5. Outputs Created

- `reports/results/model_sensitivity.csv`
- `reports/results/effect_stability.csv`
- `reports/results/combined_sensitivity_report.csv`
- `reports/figures/price_effect_sensitivity.png`

## 6. Conclusion and Limitations

The sensitivity checks show that the estimated price effect changes with model settings and data samples. These results are useful for assessing robustness, but they do not independently establish a causal relationship.

The interpretation of the DML estimate depends on assumptions such as adequate control of confounding, suitable model specification, and sufficient treatment variation. Further validation is required before using the estimate to make real pricing decisions.

## 7. Next Steps

- Review the sensitivity chart and saved CSV outputs.
- Investigate ways to improve demand prediction.
- Continue validating the DML estimate and its assumptions.
- Prepare the model for integration with a dashboard.