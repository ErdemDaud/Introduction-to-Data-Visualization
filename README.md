# Turkey Earthquake Analysis - Interactive Dashboard

Interactive dashboard for exploring and visualizing Turkey earthquake data (1915-2024) using Python and Streamlit.

## Screenshots

### Interactive Earthquake Map
![Earthquake Map](Screenshots/Screenshot%202025-11-23%20170653.png)

### Regional Distribution Treemap
![Treemap](Screenshots/Screenshot%202025-11-23%20170719.png)

### Depth-Location Scatter Plot
![Scatter Plot](Screenshots/Screenshot%202025-11-23%20170730.png)

## Dataset

- **Source:** [Kaggle - Turkey Earthquakes Dataset](https://www.kaggle.com/datasets/atasaygin/turkey-earthquakes-1915-2024-feb)
- **Records:** 95,000+ earthquakes
- **Attributes:** Date, coordinates (lat/lon), depth, magnitude, location

## Visualizations

### Chart 1: Interactive Earthquake Map (Advanced)
Geographical map showing earthquake distribution with density heatmap and scatter plot modes.

### Chart 2: Regional Distribution Treemap (Advanced)
Hierarchical visualization of earthquake frequency by region with color-coded magnitude metrics.

### Chart 3: Depth-Location Scatter Plot
Scatter plot analyzing the relationship between geographical location and earthquake depth/magnitude.

## Installation

```bash
git clone https://github.com/ErdemDaud/Introduction-to-Data-Visualization.git
cd Introduction-to-Data-Visualization
pip install -r requirements.txt
streamlit run app.py
```

## Interactive Features

- Year range slider
- Magnitude filter
- Depth filter
- Large earthquakes checkbox
- Map type and style selectors
- Color metric options
- Hover tooltips with detailed information

## Technologies

- Python
- Streamlit
- Plotly
- Pandas

## Team Contributions

| Member | Task |
|--------|------|
| Member 1 | Time series analysis, magnitude distribution |
| Member 2 | Geographical analysis, map and treemap |
| Member 3 | Correlation analysis, clustering |

---

*CEN445 Introduction to Data Visualization - 2025*
