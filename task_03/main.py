import pandas as pd
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')

# 1. the dataframe
df = pd.read_csv('tasks.csv') 

# 2. spliting into Clues (X) and Answer (y)
X = df[['income', 'years_employed', 'fico_score', 'credit_lines_outstanding', 'total_debt_outstanding']]
y = df['default']

# 3. creating and training the model
model = LogisticRegression()
model.fit(X, y)

# 4. defining the requested function
def calculate_expected_loss(income, years_employed, fico_score, credit_lines_outstanding, total_debt_outstanding, loan_amt_outstanding):
    # preparing the input data for the model
    borrower_data = [[income, years_employed, fico_score, credit_lines_outstanding, total_debt_outstanding]]
    
    # to predict the probability of default (PD)
    # .predict_proba outputs [chance of 0, chance of 1]. We want index 1 (chance of default)
    pd_probability = model.predict_proba(borrower_data)[0][1]
    
    # calculating expected loss (LGD is 0.90 because recovery is 10%)
    expected_loss = pd_probability * loan_amt_outstanding * 0.90
    
    return expected_loss

# 5. Interactive Risk Console
print("\n--- JPMorgan Credit Risk Terminal ---")

user_income = float(input("Enter annual income ($): "))
user_years = float(input("Enter years employed: "))
user_fico = int(input("Enter FICO score (300-850): "))
user_lines = int(input("Enter outstanding credit lines: "))
user_debt = float(input("Enter total debt outstanding ($): "))
user_loan = float(input("Enter active loan amount ($): "))

# runing the calculation
loss_result = calculate_expected_loss(
    income=user_income,
    years_employed=user_years,
    fico_score=user_fico,
    credit_lines_outstanding=user_lines,
    total_debt_outstanding=user_debt,
    loan_amt_outstanding=user_loan
)

print(f"\n💰 Calculated Expected Loss: ${loss_result:,.2f}")
