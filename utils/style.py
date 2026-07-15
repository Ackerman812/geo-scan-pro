import streamlit as st

def add_custom_css():
    st.markdown("""
    <style>
    /* Тёмный профессиональный фон */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Заголовки - голубой неон */
    h1, h2, h3, h4 {
        color: #00ffff !important;
    }
    
    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #0080ff) !important;
        color: #0f0c29 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* Метрики */
    div[data-testid="stMetric"] {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 8px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #00ffff !important;
    }
    
    /* Скрываем меню Streamlit */
    #MainMenu, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)