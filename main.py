import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide", page_title="Battery Market Intelligence")

# Custom CSS for better styling
st.markdown("""
<style>
    .main {padding: 2rem;}
    .stPlotlyChart {border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .stTabs [data-baseweb="tab-list"] {gap: 8px;}
    .stTabs [data-baseweb="tab"] {padding: 8px 16px; border-radius: 4px 4px 0 0;}
</style>
""", unsafe_allow_html=True)

# ---- Data Loading Functions ----
@st.cache_data
def load_data(file):
    return pd.read_csv(file, sep=';')

# ---- Dashboard Header ----
st.title("🔋 Global Battery Market Dashboard")
st.markdown("""
*Visualizing lithium-ion battery production, pricing, and demand trends*  
*Data source: [IEA](https://www.iea.org)*
""")

# ---- Tab Layout ----
tab3, tab4, tab5, tab7 = st.tabs([ 
    "🏭 Capacity", 
    "💰 Materials", 
    "🚗 Demand", 
    "🌱 Emissions"
])

with tab3:
    st.header("Manufacturing Capacity by HQ")
    df = pd.read_csv('/home/esha/sustainability_platform/data/regional-ev-lithium-ion-battery-manufacturing-capacity-by-manufacturer-headquarters-2023.csv')
    df = df.melt(id_vars=['Unnamed: 0'], var_name='Headquarters', value_name='Capacity')
    fig = px.treemap(df, path=['Unnamed: 0', 'Headquarters'], values='Capacity',
                    title="2023 Production Capacity (GWh)")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Battery Material Prices")
    df = pd.read_csv('/home/esha/sustainability_platform/data/price-of-selected-battery-materials-and-lithium-ion-batteries-2015-2024.csv')
    df['Date'] = pd.to_datetime(df['Unnamed: 0']//1000, unit='s')
    materials = ['Cobalt sulfate', 'Lithium carbonate', 'Nickel sulphate', 'Battery pack price']
    fig = px.line(df, x='Date', y=[m for m in materials if m in df.columns],
                title="Material Price Trends (Index: Jan 2017=100)")
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Regional Battery Demand")
    df = pd.read_csv('/home/esha/sustainability_platform/data/electric-vehicle-battery-demand-by-region-2016-2023.csv')
    df.columns = ['Year'] + list(df.columns[1:])
    fig = px.bar(df, x='Year', y=df.columns[1:], 
                title="EV Battery Demand Growth (GWh/year)")
    st.plotly_chart(fig, use_container_width=True)

with tab7:
    st.header("Battery Lifecycle Emissions")
    df = pd.read_csv('/home/esha/sustainability_platform/data/battery-lifecycle-emissions-by-chemistry-in-the-announced-pledges-scenario-2023-2035.csv')
    chem_types = df.iloc[::2, 0].reset_index(drop=True)
    df = pd.concat([chem_types, df.iloc[1::2].reset_index(drop=True)], axis=1)
    fig = px.bar(df, x=df.columns[0], y=df.columns[1:-1],
                title="CO2 Emissions by Production Stage (kg/kWh)")
    st.plotly_chart(fig, use_container_width=True)

# ---- Footer ----
st.markdown("---")
st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d"))