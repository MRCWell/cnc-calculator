import streamlit as st
import pandas as pd

# IRS National and Local Standards for allowable living expenses (example values, should be updated with latest IRS data)
IRS_NATIONAL_STANDARDS = {
    "food": 800,  # Example value
    "housing": 1500,  # Example value
    "transportation": 500,  # Example value
    "healthcare": 300,  # Example value
    "misc": 200  # Example value
}

# Local housing and utilities standards (example values)
LOCAL_HOUSING_UTILITIES = {
    "Midwest": 1800,
    "West": 2200,
    "South": 1600,
    "Northeast": 2500
}

def get_local_standard(region):
    return LOCAL_HOUSING_UTILITIES.get(region, 0)

def calculate_cnc_eligibility(income, expenses, irs_debt, region):
    # Apply IRS national standards for allowable living expenses
    allowable_expenses = sum(IRS_NATIONAL_STANDARDS.values()) + get_local_standard(region)
    
    # Ensure expenses do not exceed national/local standards
    total_expenses = min(expenses, allowable_expenses)
    
    # Calculate disposable income
    disposable_income = income - total_expenses
    
    # Calculate IRS monthly payment threshold
    irs_monthly_payment = irs_debt / 72
    
    # Determine CNC eligibility
    if disposable_income < irs_monthly_payment:
        result = "Eligible for Currently Not Collectible (CNC) status. Complete Form 433-F and call the IRS."
    else:
        result = f"Must pay ${max(disposable_income, irs_monthly_payment):.2f} monthly to the IRS."
    
    return {
        "Total Income": f"${income:.2f}",
        "Total Allowable Expenses": f"${total_expenses:.2f}",
        "Disposable Income": f"${disposable_income:.2f}",
        "IRS Monthly Payment Threshold": f"${irs_monthly_payment:.2f}",
        "Result": result
    }

# Streamlit UI
st.title("IRS CNC Eligibility Calculator")

income = st.number_input("Enter your total monthly income:", min_value=0.0, format="%.2f")
expenses = st.number_input("Enter your total monthly expenses:", min_value=0.0, format="%.2f")
irs_debt = st.number_input("Enter your total IRS debt:", min_value=0.0, format="%.2f")
region = st.selectbox("Select your region:", ["Midwest", "West", "South", "Northeast"])

if st.button("Calculate Eligibility"):
    result = calculate_cnc_eligibility(income, expenses, irs_debt, region)
    df = pd.DataFrame([result])
    st.dataframe(df)
