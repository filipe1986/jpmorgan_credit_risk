import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

print('Loading data and training model ...')

# Load the data
df = pd.read_csv('tasks.csv')

# features and target
features = ['credit_lines_outstanding', 'loan_amt_outstanding', 'total_debt_outstanding', 'income', 'years_employed', 'fico_score']

x = df[features]
y = df['default']

# training the model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(x,y)

# saving the model
joblib.dump(model, 'credit_risk_model.pkl')

print('Model trained and saved successfully as "credit_risk_model.pkl"')
print(f"Default Rate in data: {y.mean():.4f}")

