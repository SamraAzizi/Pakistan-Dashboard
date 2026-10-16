import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("data/pakistan_clean.csv")
df['year'] = df['year'].astype(int)
df = df.set_index('year')

# ---------------------------------------------------------------
# CHART 1: Devaluation → Inflation (dual axis)
# ---------------------------------------------------------------
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(
    go.Scatter(x=df.index, y=df['exchange_rate'],
               name="Exchange Rate (PKR/USD)",
               line=dict(color='orange', width=2)),
    secondary_y=True
)
fig1.add_trace(
    go.Scatter(x=df.index, y=df['inflation'],
               name="Inflation (%)",
               line=dict(color='red', width=2)),
    secondary_y=False
)
fig1.update_layout(
    title="Insight 1: Devaluation Precedes Inflation Spikes",
    xaxis_title="Year",
    hovermode="x unified"
)
fig1.update_yaxes(title_text="Inflation (%)", secondary_y=False)
fig1.update_yaxes(title_text="PKR per USD", secondary_y=True)
fig1.write_html("charts/insight1.html")
print("Saved charts/insight1.html")

# ---------------------------------------------------------------
# CHART 2: Jobless growth (scatter)
# ---------------------------------------------------------------
df['unemp_change'] = df['unemployment'].diff()
sub = df[['gdp_growth', 'unemp_change']].dropna()

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
    title="Insight 2: Jobless Growth — GDP Up, Unemployment Didn't Fall",
    xaxis_title="GDP Growth (%)",
    yaxis_title="Change in Unemployment (pp)",
)
fig2.write_html("charts/insight2.html")
print("Saved charts/insight2.html")

# ---------------------------------------------------------------
# CHART 3: Education spend vs population (indexed)
# ---------------------------------------------------------------
edu = df['education_spend'].dropna()
pop_indexed = (df['population'] / df['population'].iloc[0]) * 100
edu_indexed = (edu / edu.iloc[0]) * 100

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=pop_indexed.index, y=pop_indexed,
    name="Population (1990 = 100)",
    line=dict(color='green', width=2)
))
fig3.add_trace(go.Scatter(
    x=edu_indexed.index, y=edu_indexed,
    name="Education Spend (1990 = 100)",
    line=dict(color='purple', width=2)
))
fig3.update_layout(
    title="Insight 3: Population Grew ~2.5x, Education Spend Barely Moved",
    xaxis_title="Year",
    yaxis_title="Index (1990 = 100)",
)
fig3.write_html("charts/insight3.html")
print("Saved charts/insight3.html")