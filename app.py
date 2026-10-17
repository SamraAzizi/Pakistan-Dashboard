import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Pakistan Insights",
    page_icon="🇵🇰",
    layout="wide"
)

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/pakistan_clean.csv")
    df['year'] = df['year'].astype(int)
    return df

df = load_data().set_index('year')

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("🇵🇰 Pakistan Insights Dashboard")
st.markdown(
    "Three non-obvious patterns in Pakistan's economic data, 1990–2023. "
    "Source: World Bank Development Indicators."
)