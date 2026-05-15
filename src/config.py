from dotenv import load_dotenv
import os

try:
    import streamlit as st
    API_KEY = st.secrets.get("ANTHROPIC_API_KEY", None)
    MODEL   = st.secrets.get("MODEL", None)
except Exception:
    API_KEY = None
    MODEL   = None

if not API_KEY:
    load_dotenv()
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL   = os.getenv("MODEL", "claude-sonnet-4-20250514")