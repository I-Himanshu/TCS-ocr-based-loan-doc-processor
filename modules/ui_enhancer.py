# modules/ui_enhancer.py
import streamlit as st

def dark_mode():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp { background-color: #1a1a1a; color: #ffffff; }
            .stTextInput>div>div>input { color: #fff !important; }
            .css-1d391kg { background-color: #2d2d2d; }
        </style>
        """, unsafe_allow_html=True)
    return st.session_state.dark_mode

def inject_animation_css():
    st.markdown("""
    <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .stApp > div { animation: fadeIn 0.5s ease-out; }
        .stButton>button { transition: all 0.3s ease; }
        .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)