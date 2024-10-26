"""
Manage all configurations and connections
"""

import streamlit as st

class ConnectionConfig:
    openai_url: str = st.secrets["OPENAI_URL"]
    openai_sec_key: str = st.secrets["OPENAI_SEC_KEY"]

settings = ConnectionConfig()
