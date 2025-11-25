# PII NER System – Short Report

## 1. Model Overview
Key components modified:
- **model.py** – switched to a stronger, lightweight model with tuned dropout.
- **train.py** – tuned epochs, batch size, and learning rate.
- **predict.py** – replaced entity span decoding with a robust BIO-to-span algorithm.

---

## 2. Data Preparation
Four JSONL files were provided:
- `train.jsonl`  
- `dev.jsonl`  
- `test.jsonl`  
- `stress.jsonl`  

The development set was expanded to match approximate target counts:
- train: ~850  
- dev: ~185  
- test: 175  
- stress: 100  

This was done using the gen.py script to generate additional synthetic PII examples - however the generated data was not very realistic.

---

## 3. Model Architecture
Model used: **bert-base-cased**  
- Fast, reliable, no protobuf dependencies  
- Good NER performance on small datasets

Additional tuning for overfitting:
- `hidden_dropout_prob = 0.2`
- `attention_probs_dropout_prob = 0.2`

---

## 4. Training Details
Set the Hyperparameters to:
- **Epochs:** 5  
- **Batch Size:** 16  
- **Learning Rate:** 3e-5  
---

## 5. Performance

### Baseline Results:

#### Per-Entity Metrics

| Entity        | Precision | Recall | F1 Score |
|---------------|-----------|--------|----------|
| CITY          | **1.000** | 0.645  | 0.784    |
| CREDIT_CARD   | 0.103     | 0.120  | 0.111    |
| DATE          | 0.784     | **1.000** | 0.879 |
| EMAIL         | 0.774     | 0.857  | 0.814    |
| LOCATION      | 0.462     | 0.222  | 0.300    |
| PERSON_NAME   | **0.971** | **0.971** | **0.971** |
| PHONE         | 0.234     | 0.500  | 0.319    |

---

#### Macro-F1

**Macro-F1:** `0.597`

---

#### PII-Only Metrics

| Metric     | Value |
|------------|--------|
| Precision  | 0.544  |
| Recall     | 0.726  |
| F1 Score   | 0.622  |

---

#### Non-PII Metrics

| Metric     | Value |
|------------|--------|
| Precision  | 0.788  |
| Recall     | 0.448  |
| F1 Score   | 0.571  |


The new model couldn't finish it's training before the deadline for the new results. It is expected to perform better than the baseline. Will show the final results in the loom submission.

Average loss Epoch 1: 1.0024
Average loss Epoch 2: 0.0276
Average loss Epoch 3: 0.0096

---