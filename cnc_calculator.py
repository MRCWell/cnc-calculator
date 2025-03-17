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

st.header("Income Information")
employment_income = st.number_input("Enter monthly wages/salary:", min_value=0.0, format="%.2f")
self_employment_income = st.number_input("Enter monthly self-employment income:", min_value=0.0, format="%.2f")
investment_income = st.number_input("Enter monthly investment income:", min_value=0.0, format="%.2f")
social_security = st.number_input("Enter monthly Social Security income:", min_value=0.0, format="%.2f")
other_income = st.number_input("Enter any other monthly income:", min_value=0.0, format="%.2f")

total_income = employment_income + self_employment_income + investment_income + social_security + other_income

st.header("Expense Information")
rent_mortgage = st.number_input("Enter monthly rent/mortgage payment:", min_value=0.0, format="%.2f")
utility_bills = st.number_input("Enter monthly utilities (electric, gas, water, etc.):", min_value=0.0, format="%.2f")
transportation = st.number_input("Enter monthly transportation cost:", min_value=0.0, format="%.2f")
groceries = st.number_input("Enter monthly grocery and food expenses:", min_value=0.0, format="%.2f")
medical = st.number_input("Enter monthly medical expenses:", min_value=0.0, format="%.2f")
other_expenses = st.number_input("Enter any other monthly necessary expenses:", min_value=0.0, format="%.2f")

total_expenses = rent_mortgage + utility_bills + transportation + groceries + medical + other_expenses

irs_debt = st.number_input("Enter your total IRS debt:", min_value=0.0, format="%.2f")
region = st.selectbox("Select your region:", ["Midwest", "West", "South", "Northeast"])

if st.button("Calculate Eligibility"):
    result = calculate_cnc_eligibility(total_income, total_expenses, irs_debt, region)
    df = pd.DataFrame([result])
    st.dataframe(df)
