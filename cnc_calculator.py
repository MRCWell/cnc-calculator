import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def parse_standard_values(text, keyword):
    """Extract numerical values based on specific keywords from extracted text."""
    lines = text.split("\n")
    for line in lines:
        if keyword in line:
            values = [float(x) for x in line.split() if x.replace('.', '').isdigit()]
            return values
    return []

def main():
    st.title("IRS Form 433-F Qualification Calculator")
    
    housing_text = extract_text_from_pdf("/mnt/data/all-states-housing-standards.pdf")
    transportation_text = extract_text_from_pdf("/mnt/data/transportation-standards.pdf")
    healthcare_text = extract_text_from_pdf("/mnt/data/out-of-pocket-health-care.pdf")
    national_text = extract_text_from_pdf("/mnt/data/national-standards.pdf")
    
    household_size = st.number_input("Household size:", min_value=1, step=1)
    state = st.text_input("State:")
    county = st.text_input("County:")
    region = st.selectbox("Region:", ["Northeast", "Midwest", "South", "West"])
    age = st.number_input("Age:", min_value=18, step=1)
    monthly_income = st.number_input("Total monthly income:", min_value=0.0, step=100.0)
    tax_debt = st.number_input("Total tax debt:", min_value=0.0, step=100.0)
    
    real_estate_expense = st.number_input("Real estate expense (rent/mortgage):", min_value=0.0, step=50.0)
    utilities = st.number_input("Utilities (electricity, water, internet, etc.):", min_value=0.0, step=50.0)
    credit_card_payment = st.number_input("Credit card minimum payments:", min_value=0.0, step=10.0)
    child_care = st.number_input("Child/dependent care expense:", min_value=0.0, step=50.0)
    student_loans = st.number_input("Student loan payments:", min_value=0.0, step=50.0)
    insurance = st.number_input("Health and life insurance expense:", min_value=0.0, step=50.0)
    transportation = st.number_input("Actual transportation expense:", min_value=0.0, step=50.0)
    
    if st.button("Calculate Eligibility"):
        housing_exp = parse_standard_values(housing_text, state)
        transport_exp = parse_standard_values(transportation_text, region)
        healthcare_exp = parse_standard_values(healthcare_text, "Under 65" if age < 65 else "65 and Older")
        national_standard = parse_standard_values(national_text, str(household_size))
        
        total_expenses = (sum(housing_exp) + sum(transport_exp) + sum(healthcare_exp) + sum(national_standard) +
                          real_estate_expense + utilities + credit_card_payment +
                          child_care + student_loans + insurance + transportation)
        
        disposable_income = monthly_income - total_expenses
        eligibility = "CNC Eligible" if disposable_income <= 0 else ("Online Installment Agreement" if tax_debt < 50000 else "Full Installment Agreement")
        
        st.write(f"### Disposable Income: ${disposable_income:.2f}")
        st.write(f"### IRS Eligibility: {eligibility}")

if __name__ == "__main__":
    main()
