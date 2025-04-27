# app.py
import streamlit as st
import json
import time
import random
import re
from datetime import datetime
import pandas as pd
from modules.ui_enhancer import dark_mode, inject_animation_css
from modules.enhanced_processor import process_uploaded_file, extract_fields
from modules.loan_innovator import check_loan_eligibility, display_calculator, predict_default_risk, display_admin_analytics
from modules.pdf_generator import create_loan_agreement

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    inject_animation_css()
    st.title("🌟 SmartLoan")
    
    # Dark mode toggle
    with st.sidebar:
        st.session_state.dark_mode = dark_mode()
        if st.button("🌀 Toggle Premium View"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.experimental_rerun()
            
        # Admin access
        if st.checkbox("🔐 Bank Staff Access"):
            if st.text_input("Enter access code:", type="password") == "bank123":
                show_admin_dashboard()
                return

    # Chat interface
    with st.expander("💬 Loan Assistant Chat", expanded=False):
        user_input = st.text_input("Ask about loans:", key="chat_input")
        if user_input:
            handle_chat_query(user_input)
        for msg in st.session_state.chat_history[-3:]:
            st.markdown(f"`{'🤖' if msg['is_bot'] else '👤'}` {msg['content']}")

    # Document processing
    extracted_data = {}
    with st.status("📁 Document Processing Zone", expanded=True) as status:
        uploaded_file = st.file_uploader("Drag financial docs here", type=['pdf', 'png', 'jpg', 'jpeg'])
        if uploaded_file:
            status.update(label="⚡ Processing Document...", state="running")
            time.sleep(1)
            full_text = process_uploaded_file(uploaded_file)
            extracted_data = extract_fields(full_text)
            status.update(label="✅ Document Analyzed!", state="complete")

    # Editable fields AFTER status block
    if uploaded_file:
        with st.expander("✏️ Verify Extracted Data", expanded=True):
            extracted_data = {key: st.text_input(key.capitalize(), value=value) 
                            for key, value in extracted_data.items()}

    # Loan calculator
    if st.checkbox("🧮 Show Smart Loan Calculator"):
        display_calculator()

    # Main form
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", extracted_data.get('name', ''))
            income = st.text_input("Annual Income", extracted_data.get('income', ''))
        with col2:
            address = st.text_input("Address", extracted_data.get('address', ''))
            loan_amount = st.text_input("Loan Amount", extracted_data.get('loan_amount', ''))
        
        if st.checkbox("📊 Include AI Risk Assessment"):
            st.write(f"*Default Risk Prediction:* {predict_default_risk(income, loan_amount)}")
        
        if st.form_submit_button("🚀 Submit Application", use_container_width=True):
            handle_application(name, address, income, loan_amount)
    if 'pdf_data' in st.session_state:
        print(st.session_state.pdf_data)
        with st.expander("📄 Download Loan Agreement"):
            st.download_button(
                "⬇️ Get PDF Contract",
                data=open(st.session_state.pdf_data, "rb").read(),
                file_name=f"loan_contract_{st.session_state.pdf_data.split('/')[-1].split('.')[0]}.pdf",
                mime="application/pdf",
                key="download_contract"
            )
        del st.session_state.pdf_data
def calculate_risk_score(income, loan_amount):
    try:
        income = float(income.replace('$','').replace(',',''))
        loan = float(loan_amount.replace('$','').replace(',',''))
    except:
        return 650  # Default risk score if parsing fails

    risk_score = 700 - (loan / income) * 100
    return max(300, min(850, int(risk_score)))

def handle_application(name, address, income, loan_amount):
    with st.spinner("🤖 Analyzing financial patterns..."):
        time.sleep(1.5)
        is_eligible, message = check_loan_eligibility(income, loan_amount)
        
        app_data = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'status': 'approved' if is_eligible else 'rejected',
            'risk_score': calculate_risk_score(income, loan_amount),
            'income': income.replace('$','').replace(',',''),
            'loan_amount': loan_amount.replace('$','').replace(',',''),
            'address': address
        }
        
        if is_eligible:
            from modules.loan_innovator import save_application
            save_application(app_data)  # Save to CSV
            pdf_data = create_loan_agreement(app_data)
            st.session_state.pdf_data = pdf_data
            st.success(f"✅ {message} Loan approved! Check your email for details.")


def show_admin_dashboard():
    display_admin_analytics()

def handle_chat_query(query):
    response = "Ask about application status, documents needed, or interest rates!"
    query = query.lower()
    
    patterns = {
        r'status|progress': "Check your application status in your dashboard.",
        r'document|required': "Required: ID proof, income statements, and address verification.",
        r'contact|help': "Support: support@smartloanpro.com | Phone: 555-1234",
        r'rate|interest': "Current rates: 3.5% - 5.0% based on credit assessment."
    }
    
    for pattern, reply in patterns.items():
        if re.search(pattern, query):
            response = reply
            break
    
            
    st.session_state.chat_history.append({'content': query, 'is_bot': False})
    st.session_state.chat_history.append({'content': response, 'is_bot': True})

if __name__ == "__main__":
    main()