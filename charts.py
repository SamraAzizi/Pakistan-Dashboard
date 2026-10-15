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
