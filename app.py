import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def card_style():
    return {
        "flex": "1",
        "backgroundColor": "#1e293b",
        "padding": "20px",
        "borderRadius": "12px",
        "textAlign": "center",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.3)"
    }

# -----------------------------
# LOAD DATA
# -----------------------------
cluster_features = pd.read_csv("cluster_features.csv")
final_table = pd.read_csv("final_table.csv")

def assign_risk(score):
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

cluster_features["risk_level"] = cluster_features["PICRI"].apply(assign_risk)
cluster_features = cluster_features.sort_values("PICRI", ascending=False)

map_data = final_table.merge(
    cluster_features[["cluster", "PICRI", "risk_level"]],
    on="cluster",
    how="left"
).drop_duplicates("cluster")

# -----------------------------
# INIT APP
# -----------------------------
app = dash.Dash(__name__)

# -----------------------------
# BAR CHART
# -----------------------------
bar_fig = px.bar(
    cluster_features.head(15),
    x="cluster",
    y="PICRI",
    color="risk_level",
    title="Top Hotspots by PICRI"
)

bar_fig.update_layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white"
)

# -----------------------------
# MAP (NEW API: scatter_map)
# -----------------------------
map_fig = px.scatter_map(
    map_data,
    lat="latitude",
    lon="longitude",
    color="risk_level",
    size="PICRI",
    hover_name="cluster",
    zoom=11,
    height=600
)

map_fig.update_layout(
    map_style="open-street-map",
    paper_bgcolor="#0f172a",
    font_color="white",
    margin=dict(r=0, t=0, l=0, b=0)
)

# -----------------------------
# LAYOUT
# -----------------------------
app.layout = html.Div(style={
    "backgroundColor": "#0f172a",
    "minHeight": "100vh",
    "padding": "20px",
    "fontFamily": "Arial"
}, children=[

    # TITLE
    html.H1("🚗 Parking Congestion Intelligence Dashboard",
            style={"color": "white"}),

    html.P("AI-driven hotspot detection using PICRI clustering",
           style={"color": "#94a3b8"}),

    html.Br(),

    # KPI ROW
    html.Div([
        html.Div([
            html.H2(len(cluster_features), style={"color": "#38bdf8"}),
            html.P("Total Clusters", style={"color": "#cbd5e1"})
        ], style=card_style()),

        html.Div([
            html.H2((cluster_features["risk_level"] == "High").sum(),
                    style={"color": "#ef4444"}),
            html.P("High Risk Zones", style={"color": "#cbd5e1"})
        ], style=card_style()),

        html.Div([
            html.H2(round(cluster_features["PICRI"].mean(), 2),
                    style={"color": "#22c55e"}),
            html.P("Average PICRI", style={"color": "#cbd5e1"})
        ], style=card_style()),
    ], style={"display": "flex", "gap": "15px"}),

    html.Br(),

    # BAR CHART
    dcc.Graph(figure=bar_fig),

    html.Br(),

    # MAP
    dcc.Graph(figure=map_fig),

    html.Br(),

    # TABLE
    html.H3("Cluster Details", style={"color": "white"}),

    html.Div([
        html.Pre(map_data.head(20).to_string())
    ], style={
        "backgroundColor": "#1e293b",
        "color": "white",
        "padding": "15px",
        "borderRadius": "10px",
        "overflowX": "auto"
    })
])

# -----------------------------
# RUN APP (NEW DASH WAY)
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)