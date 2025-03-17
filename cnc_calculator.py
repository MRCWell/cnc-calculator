import streamlit as st
import pandas as pd

# IRS National Standards for allowable living expenses (example values, should be updated with latest IRS data)
IRS_NATIONAL_STANDARDS = {
    "food": 800,  # Example value
    "housing": 1500,  # Example value
    "transportation": 500,  # Example value
    "healthcare": 300,  # Example value
    "misc": 200  # Example value
}

def calculate_cnc_eligibility(income, expenses, irs_debt):
    # Apply IRS national standards for allowable living expenses
    allowable_expenses = sum(IRS_NATIONAL_STANDARDS.values())
    
    # Calculate disposable income
    disposable_income = income - max(expenses, allowable_expenses)
    
    # Calculate IRS monthly payment threshold
    irs_monthly_payment = irs_debt / 72
    
    # Determine CNC eligibility
    if disposable_income <= 0:
        result = "Eligible for Currently Not Collectible (CNC) status"
    else:
        result = f"Must pay ${max(disposable_income, irs_monthly_payment):.2f} monthly to the IRS"
    
    return {
        "Disposable Income": f"${disposable_income:.2f}",
        "IRS Monthly Payment Threshold": f"${irs_monthly_payment:.2f}",
        "Result": result
    }

# Streamlit UI
st.title("IRS CNC Eligibility Calculator")

income = st.number_input("Enter your monthly income:", min_value=0.0, format="%.2f")
expenses = st.number_input("Enter your total monthly expenses:", min_value=0.0, format="%.2f")
irs_debt = st.number_input("Enter your total IRS debt:", min_value=0.0, format="%.2f")

if st.button("Calculate Eligibility"):
    result = calculate_cnc_eligibility(income, expenses, irs_debt)
    df = pd.DataFrame([result])
    st.dataframe(df)
