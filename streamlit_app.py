import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="J.P. Morgan - Credit Risk Analyzer", layout="centered")
st.title("🏦 J.P. Morgan Credit Risk Assessment")
st.markdown("**Predict Probability of Default & Expected Loss**")

# Load the model (we'll train and save it first)
@st.cache_resource
def load_model():
    return joblib.load('credit_risk_model.pkl')

model = load_model()

# Input fields
st.header("Borrower Information")

col1, col2 = st.columns(2)

with col1:
    credit_lines = st.number_input("Credit Lines Outstanding", min_value=0, value=2)
    loan_amount = st.number_input("Loan Amount Outstanding ($)", min_value=0.0, value=5000.0)
    total_debt = st.number_input("Total Debt Outstanding ($)", min_value=0.0, value=15000.0)
    income = st.number_input("Annual Income ($)", min_value=0.0, value=80000.0)

with col2:
    years_employed = st.number_input("Years Employed", min_value=0, value=5)
    fico_score = st.number_input("FICO Score", min_value=300, max_value=850, value=650)

if st.button("Calculate Risk & Expected Loss", type="primary"):
    # Prepare input
    input_data = pd.DataFrame({
        'credit_lines_outstanding': [credit_lines],
        'loan_amt_outstanding': [loan_amount],
        'total_debt_outstanding': [total_debt],
        'income': [income],
        'years_employed': [years_employed],
        'fico_score': [fico_score]
    })

    # Predict probability of default
    prob_default = model.predict_proba(input_data)[0][1]
    expected_loss = prob_default * loan_amount * 0.90  # 10% recovery rate

    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Probability of Default", f"{prob_default:.1%}")
    with col2:
        st.metric("Expected Loss", f"${expected_loss:,.2f}")
    with col3:
        if prob_default < 0.15:
            st.success("✅ LOW RISK - Approve")
        elif prob_default < 0.35:
            st.warning("⚠️ MEDIUM RISK - Review")
        else:
            st.error("❌ HIGH RISK - Decline")

    st.info(f"Recommendation: {'Approve with caution' if prob_default < 0.25 else 'High risk - Consider declining or higher interest'}")

st.caption("J.P. Morgan Forage Virtual Experience | Built with Streamlit")

# the website is live here: https://jpmorgan-credit-risk.onrender.com/
