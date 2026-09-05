Customs Classification AI

An NLP-based customs classification system that predicts Harmonized System (HS) codes from cargo/product descriptions. The system combines a TF-IDF text representation with a Linear Support Vector Machine (SVM), input validation, alternative predictions, and a human-review pathway for ambiguous or insufficient descriptions.

The project was developed as part of the Cutting Lyne Freight & Logistics AI Technical Assessment.

1. Problem Statement

Customs classification requires mapping imported and exported goods to appropriate Harmonized System (HS) codes.

In practical logistics environments, cargo descriptions may be:

incomplete
abbreviated
poorly formatted
misspelled
overly generic
ambiguous
internally contradictory

A classification system therefore needs to do more than simply return an HS code. It should also identify descriptions where the model may not have enough information to make a reliable classification.

This project implements a machine-learning decision-support system that predicts likely HS codes while providing alternative candidates and routing problematic inputs for manual review.

Important: The system is intended to assist customs classification workflows. It should not be treated as an autonomous replacement for qualified customs professionals or official tariff classification procedures.

2. Solution Overview

The system follows this pipeline:

                    Cargo Description
                           │
                           ▼
                  Input Validation
                           │
                           ▼
                  Text Preprocessing
                           │
                           ▼
                    TF-IDF Vectorizer
                           │
                           ▼
                     Linear SVM
                           │
                           ▼
                  Top HS Code Candidates
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
             Valid Input       Risk/Uncertainty
                  │                 │
                  ▼                 ▼
          Classification       Manual Review

The application exposes the trained classifier through a lightweight FastAPI backend and provides a browser-based interface for testing predictions.

3. Model
Selected Model

The final classification model is a:

Linear Support Vector Machine (Linear SVM)

using:

TF-IDF (Term Frequency-Inverse Document Frequency) for text representation.

Pipeline
Product Description
        ↓
Text Cleaning
        ↓
TF-IDF Vectorization
        ↓
Linear SVM
        ↓
HS Code Prediction

A lightweight SGD Classifier was also evaluated as a baseline.

The Linear SVM outperformed the baseline across the primary evaluation metrics and was therefore selected as the final model.

4. Model Performance

The model was evaluated on a held-out test set.

Metric	Linear SVM
Accuracy	87.31%
Macro F1	92.71%
Weighted F1	86.81%
Top-3 Accuracy	90.73%
Top-5 Accuracy	91.96%
Dataset split used
Dataset	Records
Training	56,572
Testing	14,144
Total	70,716

The model covers:

5,621 HS classes

Interpretation

The model correctly identifies the exact HS class approximately 87% of the time on the held-out test set.

The higher Top-3 and Top-5 accuracy demonstrates that the model can often place the correct classification among its highest-ranked alternatives even when it does not select it as the first prediction.

This is particularly useful for a customs decision-support workflow where alternative classifications can be reviewed by a human.

5. Handling Messy Real-World Descriptions

A major requirement of the assessment was consideration of incomplete and contradictory tariff descriptions.

The system therefore includes an input-validation layer before classification.

Examples
Valid description
100% cotton men's short sleeve t-shirt

The system attempts classification and returns:

predicted HS code
official/associated description
alternative candidates
risk flags
Generic description
machine

The system identifies the description as too general and can route it to:

MANUAL REVIEW

rather than blindly trusting the model.

Empty description

The system rejects the request as invalid rather than attempting classification.

Potentially ambiguous description
stainless steel automotive screw

The system can return multiple candidate HS codes, allowing the user to review the alternatives.

6. Prediction Output

The classifier returns structured information such as:

{
    "input": "stainless steel automotive screw",
    "status": "classified",
    "hs_code": "731813",
    "description": "Iron or steel; threaded screw hooks and screw rings",
    "risk_flags": [],
    "alternatives": [
        {
            "hs_code": "851220",
            "description": "Lighting or visual signalling equipment; electrical, of a kind used on motor vehicles",
            "decision_score": -0.6917
        },
        {
            "hs_code": "731814",
            "description": "Iron or steel; threaded self-tapping screws",
            "decision_score": -0.7474
        }
    ]
}
Decision scores

The decision_score returned by the Linear SVM is a ranking score, not a probability.

Therefore, negative values are valid. The important factor is the relative ranking of the candidate classes rather than whether the score itself is positive or negative.

7. Human-in-the-Loop Design

The system is intentionally designed as a decision-support tool.

Rather than assuming every prediction is correct:

Model Prediction
      │
      ▼
Risk / Input Validation
      │
 ┌────┴─────┐
 ▼          ▼
Reliable   Uncertain
 ▼          ▼
Return     Manual
Result     Review

This approach reduces the risk of automatically acting on classifications generated from insufficient or ambiguous product descriptions.

Future versions can improve this further using calibrated confidence scores and validation thresholds derived from a dedicated validation set.

8. Web Application

A lightweight web interface was built to make the classifier directly testable.

Backend

The backend is implemented using:

FastAPI

The API loads the trained model artifacts and exposes a classification endpoint:

POST /api/classify

The endpoint accepts a product/cargo description and returns the predicted HS classification and related risk information.

Frontend

The interface uses:

HTML
CSS
JavaScript
FastAPI static/template serving

No large frontend framework is required.

The interface provides:

cargo description input
classification action
loading state
predicted HS code
HS description
alternative classifications
risk flags
manual-review feedback
validation feedback

The interface was intentionally kept lightweight so that the focus remains on the underlying classification workflow.

9. Web Interface Walkthrough

The application can be started locally and accessed through:

http://127.0.0.1:8000/
Test Case 1 — Valid Description

Enter:

100% cotton men's short sleeve t-shirt

Expected behaviour:

Classification
      ↓
HS Code
      ↓
HS Description
      ↓
Alternative Candidates
Test Case 2 — Generic Description

Enter:

machine

Expected behaviour:

Input Validation
      ↓
Risk Detected
      ↓
Manual Review

The interface displays the appropriate warning rather than treating the prediction as fully reliable.

Test Case 3 — Empty Description

Leave the description empty and select Classify.

Expected behaviour:

Empty Input
     ↓
Validation Error
     ↓
Classification rejected
10. Project Structure
task-1-customs-classification/
│
├── notebook/
│   └── customs_classification.ipynb
│
├── models/
│   ├── tfidf_vectorizer.joblib
│   ├── classifier.joblib
│   ├── hs_description_lookup.joblib
│   └── metrics.json
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── validation.py
│   └── predictor.py
│
├── templates/
│   └── index.html
│
├── app.py
│
├── tests/
│   └── test_predictor.py
│
├── requirements.txt
├── .gitignore
└── README.md
11. Installation

Clone the repository:

git clone <repository-url>

Navigate to the Task 1 directory:

cd cutting-lyne-ai-assessment/task-1-customs-classification

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
12. Running the Application

Start the FastAPI server:

uvicorn app:app --reload

The application will be available at:

http://127.0.0.1:8000/

The API endpoint is:

POST /api/classify

Example request:

{
    "description": "100% cotton men's short sleeve t-shirt"
}
13. Using the Model Programmatically

The trained model can also be used without the web interface.

from src.predictor import classify_product

result = classify_product(
    "stainless steel automotive screw"
)

print(result)

The model artifacts are loaded from:

models/

This separates the trained machine-learning artifacts from the application logic.

14. Model Artifacts

The trained system consists of:

tfidf_vectorizer.joblib

The TF-IDF vectorizer fitted during training.

classifier.joblib

The trained Linear SVM classifier.

hs_description_lookup.joblib

Mapping between HS codes and their associated descriptions.

metrics.json

Stored evaluation metrics for the final model.

Example:

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
15. Testing

The project includes tests covering the main prediction workflow.

Tests should verify:

valid descriptions can be classified
missing descriptions are rejected
generic descriptions can trigger manual review
top candidate predictions are returned
model artifacts can be loaded successfully
returned responses contain the expected fields

Run the test suite with:

pytest
16. Limitations

The current implementation has several limitations.

Dataset limitations

The training dataset does not represent the full complexity of real-world customs declarations. Model performance on operational customs data may therefore differ from the reported test-set performance.

Ambiguous products

Some products cannot be accurately classified without additional information such as:

material
intended use
composition
dimensions
manufacturing method
technical specifications
Rare classes

HS classification contains many classes with varying amounts of training data. Classes with limited examples can be more difficult for a supervised classifier to learn reliably.

Model confidence

Linear SVM decision scores are ranking scores rather than calibrated probabilities. Future versions should introduce probability calibration or another validated uncertainty-estimation approach.

Human verification

The system should remain a decision-support tool. Final customs classification should be verified according to the applicable tariff rules and by an appropriately qualified professional.

17. Future Improvements

Potential improvements include:

Confidence calibration
Calibrate model outputs to provide more interpretable confidence estimates.
Better handling of rare HS classes
Investigate class imbalance and hierarchical classification strategies.
Semantic models
Evaluate transformer-based embeddings or domain-specific language models against the current TF-IDF baseline.
Hierarchical HS classification
Predict chapter → heading → subheading rather than treating all 5,621 classes as independent classes.
Multilingual classification
Extend the model to descriptions in additional languages.
Customs-domain data
Evaluate and retrain using larger collections of real, appropriately anonymized customs declarations.
Human feedback loop
Store reviewed classifications and use them as additional training data.
Explainability
Provide users with the terms/features contributing most strongly to a prediction.
18. Key Design Decision

The primary design principle of this project is:

Automate classification where the model has sufficient evidence, and escalate uncertain cases rather than forcing an unreliable prediction.

This makes the system more appropriate for a logistics/customs environment where incorrect classifications can have financial and compliance consequences.

19. Assessment Summary

This implementation demonstrates:

Natural Language Processing for product descriptions
Supervised machine learning for HS-code classification
TF-IDF feature engineering
Linear SVM classification
Multi-class evaluation
Top-K prediction
Input validation
Messy-data handling
Human-in-the-loop design
FastAPI integration
Web-based model interface
Model serialization
Software testing
Reproducible model deployment

The final system achieves 87.31% accuracy, 92.71% Macro F1, 90.73% Top-3 accuracy, and 91.96% Top-5 accuracy on the held-out test set.