import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data with proper parsing
def load_data():
    csv_path = Path(__file__).parent.parent / "data" / "battery-price-index-by-selected-region-2020-2023.csv"
    return pd.read_csv(csv_path)

df = load_data()

# Clean data - remove any trailing empty columns
df = df.dropna(axis=1, how='all')

# Ensure Year column is properly formatted
df.columns = ['Year'] + list(df.columns[1:])

# Create interactive line chart
fig = px.line(df, 
              x='Year', 
              y=df.columns[1:],
              title='Battery Price Index by Region (2020-2023)<br><sup>Index: China = 100</sup>',
              labels={'value': 'Price Index', 'variable': 'Region'},
              markers=True)

# Customize layout
fig.update_layout(
    yaxis_range=[80, 180],
    hovermode='x unified',
    plot_bgcolor='white',
    xaxis_title='Year',
    legend_title='Region'
)

# Add horizontal line at China=100 reference
fig.add_hline(y=100, line_dash="dot", 
              annotation_text="China Baseline", 
              annotation_position="bottom right")

# Show plot
fig.show()