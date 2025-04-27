import streamlit as st
import json
from modules.document_processor import process_uploaded_file, extract_fields
from modules.loan_eligibility import check_loan_eligibility

def main():
    st.title("Automated Loan Document Processing")
    
    uploaded_file = st.file_uploader("Upload Document (PDF/Image)", 
                                    type=['pdf', 'png', 'jpg', 'jpeg'])
    
    extracted_data = {}
    
    if uploaded_file:
        full_text = process_uploaded_file(uploaded_file)
        extracted_data = extract_fields(full_text)
        st.text_area("Extracted Text", full_text, height=300)
        st.json(extracted_data)
        st.success("Text extraction complete!")
    
    with st.form("data_form"):
        name = st.text_input("Name", extracted_data.get('name', ''))
        address = st.text_input("Address", extracted_data.get('address', ''))
        income = st.text_input("Annual Income", extracted_data.get('income', ''))
        loan_amount = st.text_input("Loan Amount", extracted_data.get('loan_amount', ''))
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            errors = []
            income_clean = income.replace('$', '').replace(',', '').strip()
            loan_clean = loan_amount.replace('$', '').replace(',', '').strip()
            
            if not name.strip():
                errors.append("Name is required")
            if not address.strip():
                errors.append("Address is required")
            if not income_clean.isdigit():
                errors.append("Income must be a valid number")
            if not loan_clean.isdigit():
                errors.append("Loan amount must be a valid number")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Check eligibility
                is_eligible, message = check_loan_eligibility(income, loan_amount)
                
                application_data = {
                    'name': name,
                    'address': address,
                    'income': income_clean,
                    'loan_amount': loan_clean,
                    'eligible': is_eligible
                }
                
                if is_eligible:
                    with open('loan_applications.json', 'a') as f:
                        json.dump(application_data, f)
                        f.write('\n')
                    st.success("Application submitted successfully!")
                    st.balloons()
                else:
                    st.error(f"Application rejected: {message}")
                
                # Display eligibility result
                st.subheader("Eligibility Check Result")
                st.write(f"**Status:** {'Eligible' if is_eligible else 'Not Eligible'}")
                st.write(f"**Details:** {message}")

if __name__ == "__main__":
    main()