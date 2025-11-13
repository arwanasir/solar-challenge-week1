"""
Utility functions for dashboard
"""
import pandas as pd
import plotly.express as px


def load_data(uploaded_file, country_name):
    """Load CSV file and add country"""
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['Country'] = country_name
        return df
    return None
