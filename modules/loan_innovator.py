# modules/loan_innovator.py
import streamlit as st
import pandas as pd
import random
import os

CSV_PATH = "loan_applications.csv"

def save_application(data):
    """Save approved applications to CSV"""
    df = pd.DataFrame([{
        'timestamp': data['timestamp'],
        'name': data['name'],
        'income': data['income'],
        'loan_amount': data['loan_amount'],
        'status': data['status'],
        'risk_score': data['risk_score']
    }])
    
    # Write header only if file doesn't exist
    header = not os.path.exists(CSV_PATH)
    df.to_csv(CSV_PATH, mode='a', header=header, index=False)

def check_loan_eligibility(income, loan_amount):
    try:
        income = float(income.replace('$','').replace(',',''))
        loan = float(loan_amount.replace('$','').replace(',',''))
    except:
        return False, "Invalid financial data"
    
    if loan <= income * 5:
        return True, "Congratulations! Loan approved"
    return False, "Loan amount exceeds 5x annual income"

def display_calculator():
    col1, col2 = st.columns(2)
    with col1:
        amount = st.slider("Loan Amount ($)", 1000, 100000, 25000)
        rate = st.select_slider("Interest Rate (%)", [3.5, 4.0, 4.5, 5.0])
    with col2:
        term = st.radio("Term (months)", [12, 24, 36, 60])
    
    monthly_pmt = (amount * (rate/100/12)) / (1 - (1 + rate/100/12)**-term)
    st.subheader(f"💸 Monthly Payment: ${monthly_pmt:,.2f}")
    
    with st.expander("📅 Payment Schedule"):
        data = {
            'Month': list(range(1, term+1)),
            'Principal': [monthly_pmt * 0.8] * term,
            'Interest': [monthly_pmt * 0.2] * term
        }
        df = pd.DataFrame(data)
        st.dataframe(df.head(10).style.highlight_max(axis=0))

def predict_default_risk(income, loan_amount):
    risks = ["Low Risk (10%)", "Moderate Risk (25%)", "High Risk (45%)"]
    return random.choice(risks)

def display_admin_analytics():
    st.title("🔍 Bank Analytics Hub")
    
    try:
        df = pd.read_csv(CSV_PATH)
        
        st.subheader("📊 Recent Applications")
        st.dataframe(df.tail(10), height=300)
        
        st.subheader("📈 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Applications", len(df))
            st.metric("Approval Rate", 
                     f"{(df[df.status == 'approved'].shape[0]/len(df)*100):.1f}%")
        
        with col2:
            avg_loan = df.loan_amount.astype(float).mean()
            st.metric("Avg. Loan Amount", f"${avg_loan:,.2f}")
            
        with col3:
            avg_risk = df.risk_score.mean()
            st.metric("Average Risk Score", f"{avg_risk:.0f}")
            
        st.subheader("📅 Approval Trends")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df.timestamp.dt.date
        daily_stats = df.groupby('date').agg({
            'status': [('total', 'count'), ('approved', lambda x: (x == 'approved').sum())]
        }).reset_index()
        
        daily_stats.columns = ['Date', 'Total Applications', 'Approved']
        st.line_chart(daily_stats.set_index('Date'))
        
    except FileNotFoundError:
        st.warning("No applications data found")
