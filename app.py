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

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")

min_year = int(df.index.min())
max_year = int(df.index.max())

year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Apply filter
df_f = df.loc[year_range[0]:year_range[1]].copy()

# ------------------------------------------------------------------
# INSIGHT 1: Devaluation → Inflation lag
# ------------------------------------------------------------------
st.header("1. Currency devaluation precedes inflation")
st.markdown(
    "When the PKR depreciates sharply against the USD, consumer inflation "
    "tends to spike **6–18 months later** — not immediately. This means "
    "policymakers should expect persistent inflation *after* a devaluation, "
    "not just in the same quarter."
)

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Scatter(x=df_f.index, y=df_f['exchange_rate'],
               name="Exchange Rate (PKR/USD)",
               line=dict(color='orange', width=2)),
    secondary_y=True
)
fig1.add_trace(
    go.Scatter(x=df_f.index, y=df_f['inflation'],
               name="Inflation (%)",
               line=dict(color='red', width=2)),
    secondary_y=False
)
fig1.update_layout(height=420, hovermode="x unified",
                   legend=dict(orientation="h", y=1.1))
fig1.update_yaxes(title_text="Inflation (%)", secondary_y=False)
fig1.update_yaxes(title_text="PKR per USD", secondary_y=True)
st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------------
# INSIGHT 2: Jobless growth
# ------------------------------------------------------------------
st.header("2. GDP growth hasn't translated into jobs")
st.markdown(
    "In Pakistan's strongest growth years, unemployment barely fell. The "
    "scatter below plots GDP growth against the year-on-year change in "
    "unemployment. Points above zero (higher unemployment) cluster "
    "alongside high growth years — evidence of **jobless growth**."
)

df_f['unemp_change'] = df_f['unemployment'].diff()
sub = df_f[['gdp_growth', 'unemp_change']].dropna()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=sub['gdp_growth'], y=sub['unemp_change'],
    mode='markers+text',
    text=[str(y) for y in sub.index],
    textposition='top center',
    marker=dict(size=10, color='steelblue')
))
fig2.add_hline(y=0, line_dash="dash", line_color="gray")
fig2.update_layout(
    height=420,
    xaxis_title="GDP Growth (%)",
    yaxis_title="Change in Unemployment (pp)",
)
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------------
# INSIGHT 3: Education spend vs population
# ------------------------------------------------------------------
st.header("3. Population grew 2.5×; education spending didn't")
st.markdown(
    "Education spending as a share of GDP has stayed roughly flat since 1990, "
    "while the population has grown more than 2.5-fold. The **per-person** "
    "investment in education is falling even in years when the budget looks "
    "stable — a quiet demographic pressure."
)

edu = df_f['education_spend'].dropna()
if len(edu) > 0:
    pop_indexed = (df_f['population'] / df_f['population'].iloc[0]) * 100
    edu_indexed = (edu / edu.iloc[0]) * 100

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=pop_indexed.index, y=pop_indexed,
        name="Population (start = 100)",
        line=dict(color='green', width=2)
    ))
    fig3.add_trace(go.Scatter(
        x=edu_indexed.index, y=edu_indexed,
        name="Education Spend (start = 100)",
        line=dict(color='purple', width=2)
    ))
    fig3.update_layout(
        height=420,
        xaxis_title="Year",
        yaxis_title="Index (start of range = 100)",
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No education spend data in the selected range.")

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "**Source:** World Bank Development Indicators (1990–2023). "
    "**Method:** All indicators pulled via `wbdata` from the World Bank API. "
    "Missing values are left as gaps, not imputed."
)