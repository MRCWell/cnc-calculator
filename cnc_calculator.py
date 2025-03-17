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

def get_local_standard(region, household_size):
    base_standard = LOCAL_HOUSING_UTILITIES.get(region, 0)
    return base_standard + (household_size - 1) * 200  # Example adjustment per additional household member

def calculate_cnc_eligibility(income, expenses, irs_debt, region, household_size):
    # Apply IRS national standards for allowable living expenses
    allowable_expenses = sum(IRS_NATIONAL_STANDARDS.values()) + get_local_standard(region, household_size)
    
    # Ensure expenses do not exceed national/local standards
    total_expenses = min(expenses, allowable_expenses)
    
    # Calculate disposable income
    disposable_income = income - total_expenses
    
    # Calculate IRS monthly payment threshold
    irs_monthly_payment = irs_debt / 72
    
    # Determine CNC eligibility and explanation
    if disposable_income < irs_monthly_payment:
        if disposable_income > 0:
            result = (f"Your disposable income (${disposable_income:.2f}) is less than the IRS monthly payment threshold (${irs_monthly_payment:.2f}).\n\n"
                      "You may qualify for a lower monthly payment equal to your disposable income.\n\n"
                      "Complete Form 433-F and call the IRS to discuss a reduced payment option.")
        else:
            result = (f"Your disposable income (${disposable_income:.2f}) is zero or negative.\n\n"
                      "You are eligible for Currently Not Collectible (CNC) status.\n\n"
                      "Complete Form 433-F and call the IRS to request CNC status.")
    else:
        result = (f"Your disposable income (${disposable_income:.2f}) is more than the IRS required payment (${irs_monthly_payment:.2f}).\n\n"
                  f"You must pay at least ${max(disposable_income, irs_monthly_payment):.2f} monthly to the IRS.")
    
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

st.header("Household Information")
household_size = st.number_input("Enter the number of people in your household:", min_value=1, step=1)

irs_debt = st.number_input("Enter your total IRS debt:", min_value=0.0, format="%.2f")
region = st.selectbox("Select your region:", ["Midwest", "West", "South", "Northeast"])

if st.button("Calculate Eligibility"):
    result = calculate_cnc_eligibility(total_income, total_expenses, irs_debt, region, household_size)
    df = pd.DataFrame([result])
    st.write(result["Result"])
