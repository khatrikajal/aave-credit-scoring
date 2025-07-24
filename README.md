# aave-credit-scoring

## Problem Statement

I was provided with raw transaction-level data from the Aave V2 protocol. Each record corresponds to a wallet interacting with the protocol through actions like `deposit`, `borrow`, `repay`, `redeemunderlying`, and `liquidationcall`.

**Goal**: Build a robust machine learning model that assigns a credit score between **0 and 1000** to each wallet, based on historical transaction behavior. Higher scores indicate trustworthy wallets, while lower scores flag risky or bot-like behavior.

---

## Project Folder Structure

This project follows a modular and production-grade folder structure:

```
aave-credit-scoring/
├── analysis/                            # Analysis reports and plots
│   ├── analysis.md                      # Score distribution analysis 
│   ├── plot_score_distribution.py       # Script to generate score_distribution.png
│   └── score_distribution.png           # Score distribution graph embedded in analysis.md
│
├── data/                                # Input and output data
│   ├── sample_transactions.json         # Raw transaction data (input)
│   └── wallet_score.csv                 # Scored wallet data (output)
│
├── model_training/                      # Model training code and artifacts
│   ├── training_notebook.ipynb          # Model training notebook (Google Colab)
│   ├── rf_credit_model.pkl              # Trained RandomForestClassifier
│   └── credit_scaler.pkl                # Trained MinMaxScaler
│
├── streamlit_app/                       # Streamlit frontend application
│   └── app.py                           # Main UI script
│
├── README.md                            # Project documentation and setup guide
├── .gitignore                           # Git ignore file
├── LICENSE                              # License information
└── .gitattributes                       # Git attributes
```

---

## Architecture & Workflow

1. **Input**: JSON file containing wallet transaction history.
2. **Feature Engineering**:
   - Total deposit, borrow, and repay amounts
   - Repay-to-borrow and borrow-to-deposit ratios
   - Liquidation count
   - Transaction count
3. **Preprocessing**:
   - Handled missing values
   - Converted and aggregated numeric features by wallet
4. **Handling Imbalanced Data**:
   - Applied **SMOTE (Synthetic Minority Oversampling Technique)**
5. **Modeling**:
   - Trained a **Random Forest Classifier** on resampled and scaled features
   - Mapped labels to fixed credit scores:
     - 0 → 200 (High Risk)
     - 1 → 400 (Low Risk)
     - 2 → 600 (Moderate Risk)
     - 3 → 800 (Average Standing)
     - 4 → 900 (Safe)
6. **Output**:
   - CSV with each wallet’s credit score and risk label
   - Streamlit UI for interaction

---

## Why I Chose This Approach

The dataset lacked predefined labels, so I couldn't directly train a supervised model.

### Challenges Faced:
- **KMeans clustering** was unstable and produced inconsistent credit scores.
- No ground truth made it hard to justify the score logic.
- Some clusters were too small, indicating poor separation.
- I needed to **define custom risk labels manually**.

### My Solution:
- I designed a **rule-based labeling system** using domain insights (e.g., repay ratio, liquidation count).
- Used **SMOTE** to balance class distribution.
- Trained a **Random Forest Classifier** and fixed the score mapping to produce deterministic results.
- This way, I ensured consistency in scoring both known and unseen wallets.

---

## Testing

I tested the pipeline with:
- JSON files via the Streamlit interface
- Edge cases: wallets with single or missing transactions
- Ensured robust handling of malformed data

---

## How to Use

1. Run: `streamlit run app.py`
2. Upload your JSON wallet transaction file
3. Download the output CSV with credit scores

---

## For Analysis

Refer to `analysis/analysis.md` to explore:
- Credit score distribution
- SMOTE impact on class balance
- Risk segment behavior insights



---

##  Sample Transaction Data Included

To demonstrate the pipeline and ensure the code is testable without sensitive data, a **sample transaction dataset** is provided in:

data/sample_transactions.json


This file contains **15 mock DeFi transactions** across different wallets, representing typical actions such as:

- Deposits
- Borrows
- Repayments
- Liquidation calls

These synthetic transactions are crafted to simulate realistic wallet behaviors and ensure functionality even without proprietary data.

---

##  Tested on Sample and Provided Data

- The complete pipeline has been tested and validated using both:
  - The **provided transaction data** from Zeru (not committed due to confidentiality).
  - The **included sample data** (`sample-wallet-transactions.json`) to make the project independently testable.

- The output credit scores, model behavior, and reports are based on the provided data.

- The visualization (`plot_score_distribution.png`) shown in the `analysis.md` is generated **based on the actual transaction data supplied by Zeru**.

---

##  Note

If you'd like to test on your own dataset, You can upload the sample file in frontend and re-run the pipeline to generate new outputs.

---
