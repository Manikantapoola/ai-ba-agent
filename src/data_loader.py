import pandas as pd
import streamlit as st

def load_file(uploaded_file):
    if uploaded_file is None:
        return None
    filename = uploaded_file.name.lower()
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif filename.endswith(".xls"):
            df = pd.read_excel(uploaded_file, engine="xlrd")
        else:
            st.error("Please upload a CSV or Excel file.")
            return None
        if df.empty:
            st.error("The file is empty.")
            return None
        return df
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return None