# JPMorgan Chase & Co. - Credit Risk Modeling

## 📊rop ect Overview
This repository contains a quantitative finance prototype developed for a personal loan portfolio. The script uses machine learning to evaluate whether a borrower should be approved for a loan by analyzing their financial profile and predicting the bank's exposure risk.

## 🧮 Core Analytics Logic
The application automatically calculates **Expected Loss (EL)** using an industry-standard risk framework:
* **Probability of Default (PD):** Predicted dynamically using a Logistic Regression model trained on a 10,000-row loan dataset.
* **Loss Given Default (LGD):** Calculated at **90%** assuming a historical recovery rate of 10%.
* **Formula:** Expected Loss = PD × Outstanding Loan Amount × 0.90

## 🛠️ Interactive Features
* **Live CLI Console:** Takes real-time terminal inputs (Income, FICO score, Debt, etc.) to immediately output the bank's financial risk in clean currency formatting.
