import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent.parent / "data" / "lithium-production.csv"
    return pd.read_csv(csv_path)

df = load_data()

# Dashboard
st.title("🌍 Lithium Production Intelligence")

# Filters
selected_year = st.slider("Select Year", 1995, 2023, 2023)
selected_entities = st.multiselect(
    "Select Countries/Regions",
    options=df['Entity'].unique(),
    default=['Africa', 'Argentina', 'Asia', 'Australia', 'Brazil', 'Chile', 'China', 'Europe', 'High-income countries', 'Lower-middle-income countries', 'North America', 'Oceania', 'Portugal', 'Rest of World (EI)', 'South America', 'United States', 'Upper-middle-income countries', 'World', 'Zimbabwe']
)

# Filter data
filtered_df = df[(df['Year'] == selected_year) & 
                (df['Entity'].isin(selected_entities))]

# Metrics
col1, col2, col3 = st.columns(3)
world_prod = df[(df['Entity'] == 'World') & (df['Year'] == selected_year)]['Lithium production - kt'].values[0]
col1.metric("Global Production (kt)", f"{world_prod:,.0f}")

# Visualizations
tab1, tab2 = st.tabs(["Production Map", "Historical Trends"])

with tab1:
    # Requires country codes in your data
    fig = px.choropleth(filtered_df,
                        locations="Code",
                        color="Lithium production - kt",
                        hover_name="Entity",
                        scope="world",
                        title=f"Lithium Production {selected_year}")
    st.plotly_chart(fig)

with tab2:
    trend_df = df[df['Entity'].isin(selected_entities)]
    fig = px.line(trend_df, x='Year', y='Lithium production - kt',
                 color='Entity', title='Production Over Time')
    st.plotly_chart(fig)