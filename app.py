"""
Turkey Earthquake Analysis - Interactive Dashboard
Member 2: Geographical and Spatial Analysis

Charts:
1. Interactive Earthquake Map (Advanced)
2. Regional Distribution Treemap (Advanced)
3. Depth-Location Scatter Plot
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import re

# Page Configuration
st.set_page_config(
    page_title="Turkey Earthquake Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# DATA LOADING AND PREPROCESSING
# =============================================================================
@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv("turkey_earthquakes(1915-2024_feb).csv")

    # Rename Turkish columns to English
    df = df.rename(columns={
        "Olus tarihi": "Date",
        "Enlem": "Latitude",
        "Boylam": "Longitude",
        "Derinlik": "Depth",
        "Yer": "Location"
    })

    # Date conversion
    df["Date"] = pd.to_datetime(df["Date"], format="%Y.%m.%d", errors="coerce")
    df["Year"] = df["Date"].dt.year

    # Clean missing values
    df["Location"] = df["Location"].fillna("Unknown")

    # Coordinate filtering (Turkey boundaries)
    df = df[
        (df["Latitude"].between(35, 43)) &
        (df["Longitude"].between(25, 45)) &
        (df["Latitude"].notna()) &
        (df["Longitude"].notna())
    ]

    # Outlier cleaning
    df = df[df["Depth"] >= 0]
    df = df[df["xM"] > 0]

    # Region extraction
    def extract_region(loc):
        if pd.isna(loc):
            return "Unknown"
        match = re.search(r'\(([^)]+)\)', str(loc))
        if match:
            return match.group(1).strip()
        parts = str(loc).split('-')
        if len(parts) > 1:
            return parts[-1].strip().split()[0]
        return str(loc).split()[0] if loc else "Unknown"

    df["Region"] = df["Location"].apply(extract_region)
    return df

df = load_and_preprocess_data()

# =============================================================================
# HEADER
# =============================================================================
st.title("Turkey Earthquake Analysis")
st.caption("Geographical and Spatial Analysis | Member 2")

# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.header("Filters")

    year_range = st.slider(
        "Year Range:",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(2000, int(df["Year"].max()))
    )

    mag_range = st.slider(
        "Magnitude Range (xM):",
        min_value=float(df["xM"].min()),
        max_value=float(df["xM"].max()),
        value=(3.5, float(df["xM"].max())),
        step=0.1
    )

    depth_range = st.slider(
        "Depth Range (km):",
        min_value=0.0,
        max_value=min(200.0, float(df["Depth"].max())),
        value=(0.0, 100.0)
    )

    show_large_only = st.checkbox("Large Earthquakes Only (xM >= 5.0)")

# Apply filters
df_filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["xM"] >= mag_range[0]) &
    (df["xM"] <= mag_range[1]) &
    (df["Depth"] >= depth_range[0]) &
    (df["Depth"] <= depth_range[1])
]

if show_large_only:
    df_filtered = df_filtered[df_filtered["xM"] >= 5.0]

# =============================================================================
# CHART 1: INTERACTIVE EARTHQUAKE MAP (ADVANCED)
# =============================================================================
st.markdown("---")
st.subheader("1. Turkey Earthquake Map (Advanced)")

map_col1, map_col2 = st.columns(2)
with map_col1:
    map_type = st.selectbox("Map Type:", ["Density Map", "Scatter Map"])
with map_col2:
    map_style = st.selectbox("Map Style:", ["open-street-map", "carto-positron", "carto-darkmatter"])

if map_type == "Density Map":
    fig_map = px.density_map(
        df_filtered,
        lat="Latitude",
        lon="Longitude",
        z="xM",
        radius=15,
        center={"lat": 39.0, "lon": 35.0},
        zoom=5,
        map_style=map_style,
        color_continuous_scale="Hot"
    )
else:
    df_map = df_filtered.copy()
    df_map["size"] = (df_map["xM"] ** 2) * 2
    fig_map = px.scatter_map(
        df_map,
        lat="Latitude",
        lon="Longitude",
        color="xM",
        size="size",
        hover_name="Location",
        hover_data={"xM": ":.1f", "Depth": ":.1f", "size": False},
        color_continuous_scale="Turbo",
        zoom=5,
        center={"lat": 39.0, "lon": 35.0},
        map_style=map_style,
        opacity=0.7
    )

fig_map.update_layout(height=550, margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

st.info("This map shows earthquake distribution across Turkey. The North Anatolian Fault and East Anatolian Fault regions show the highest seismic activity.")

# =============================================================================
# CHART 2: TREEMAP - REGIONAL DISTRIBUTION (ADVANCED)
# =============================================================================
st.markdown("---")
st.subheader("2. Regional Earthquake Distribution - Treemap (Advanced)")

treemap_metric = st.selectbox(
    "Color Metric:",
    ["Earthquake Count", "Average Magnitude", "Maximum Magnitude"]
)

# Regional statistics
df_region_stats = df_filtered.groupby("Region").agg({
    "xM": ["count", "mean", "max"],
    "Depth": "mean"
}).reset_index()
df_region_stats.columns = ["Region", "Count", "Avg_Mag", "Max_Mag", "Avg_Depth"]
df_region_stats = df_region_stats[df_region_stats["Count"] >= 10]

if treemap_metric == "Earthquake Count":
    color_col = "Count"
elif treemap_metric == "Average Magnitude":
    color_col = "Avg_Mag"
else:
    color_col = "Max_Mag"

fig_treemap = px.treemap(
    df_region_stats.nlargest(25, "Count"),
    path=["Region"],
    values="Count",
    color=color_col,
    color_continuous_scale="RdYlBu_r",
    hover_data={"Count": True, "Avg_Mag": ":.2f", "Max_Mag": ":.1f"}
)
fig_treemap.update_layout(height=500, margin={"r": 10, "t": 10, "l": 10, "b": 10})
fig_treemap.update_traces(textinfo="label+value")
st.plotly_chart(fig_treemap, use_container_width=True)

st.info("Treemap displays earthquake counts by region. Box size represents frequency, color indicates the selected metric. Eastern Anatolia (Van, Malatya) and Aegean regions show high activity.")

# =============================================================================
# CHART 3: DEPTH-LOCATION SCATTER PLOT
# =============================================================================
st.markdown("---")
st.subheader("3. Depth Distribution by Geography")

scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    color_by = st.selectbox("Color By:", ["Depth", "Magnitude"])
with scatter_col2:
    sample_pct = st.slider("Data Sample %:", 10, 100, 50, 10)

if sample_pct < 100:
    df_scatter = df_filtered.sample(frac=sample_pct/100, random_state=42)
else:
    df_scatter = df_filtered

color_col = "Depth" if color_by == "Depth" else "xM"

fig_scatter = px.scatter(
    df_scatter,
    x="Longitude",
    y="Latitude",
    color=color_col,
    size="xM",
    hover_name="Location",
    hover_data={"xM": ":.1f", "Depth": ":.1f"},
    color_continuous_scale="Viridis" if color_by == "Depth" else "Turbo",
    opacity=0.6
)
fig_scatter.update_layout(
    height=500,
    xaxis_title="Longitude",
    yaxis_title="Latitude"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.info("Scatter plot shows earthquake locations colored by depth or magnitude. Most earthquakes occur at shallow depths (0-30 km). Deep earthquakes cluster in eastern Turkey (Van-Hakkari region).")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Data Source: Kaggle - Turkey Earthquakes Dataset (1915-2024) | Technologies: Python, Streamlit, Plotly, Pandas")
