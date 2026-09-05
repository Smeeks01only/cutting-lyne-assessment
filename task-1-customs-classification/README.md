# Task 1: Customs Classification

This repository contains the solution for the Customs Classification task.

## Usage

You can use the `classify_product` function to classify cargo or product descriptions.

```python
from src.predictor import classify_product

result = classify_product("stainless steel automotive screw")
print(result)
```

## Model Metrics

The following metrics evaluate the performance of our Linear SVM model:

```json
{
    "model": "Linear SVM",
    "accuracy": 0.8730910633484162,
    "macro_f1": 0.9271317509153356,
    "weighted_f1": 0.8680780287285997,
    "top_3_accuracy": 0.907310520361991,
    "top_5_accuracy": 0.919612556561086,
    "training_records": 56572,
    "testing_records": 14144,
    "hs_classes": 5621
}
```
