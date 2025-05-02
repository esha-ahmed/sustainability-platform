import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load the datasets
aps_df = pd.read_csv('./data/IEA-EV-dataEV-salesProjection-APSCars.csv')
steps_df = pd.read_csv('./data/IEA-EV-dataEV-salesProjection-STEPSCars.csv')

# Add scenario column
aps_df['scenario'] = 'APS'
steps_df['scenario'] = 'STEPS'

# Combine datasets
combined_df = pd.concat([aps_df, steps_df])

# Clean and prepare data
def clean_data(df):
    # Convert values to appropriate types
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Create a clean year column
    df['year'] = df['year'].astype(int)
    
    # Create a clean region column
    df['region'] = df['region'].str.strip()
    
    # Create powertrain categories
    df['powertrain'] = df['powertrain'].str.strip()
    
    return df

combined_df = clean_data(combined_df)

# Helper functions for analysis
def filter_data(df, regions=None, parameters=None, years=None, powertrains=None, scenarios=None):
    if regions is not None:
        if not isinstance(regions, list):
            regions = [regions]
        df = df[df['region'].isin(regions)]
    
    if parameters is not None:
        if not isinstance(parameters, list):
            parameters = [parameters]
        df = df[df['parameter'].isin(parameters)]
    
    if years is not None:
        if not isinstance(years, list):
            years = [years]
        df = df[df['year'].isin(years)]
    
    if powertrains is not None:
        if not isinstance(powertrains, list):
            powertrains = [powertrains]
        df = df[df['powertrain'].isin(powertrains)]
    
    if scenarios is not None:
        if not isinstance(scenarios, list):
            scenarios = [scenarios]
        df = df[df['scenario'].isin(scenarios)]
    
    return df

# 1. EV Adoption Trends by Region
def plot_ev_adoption_trends():
    # Get EV sales share data
    sales_share = filter_data(combined_df, parameters='EV sales share', powertrains='EV')
    
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=sales_share, x='year', y='value', hue='region', style='scenario')
    plt.title('EV Sales Share Projections by Region and Scenario')
    plt.ylabel('EV Sales Share (%)')
    plt.xlabel('Year')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# 2. Powertrain Mix Comparison
def plot_powertrain_mix(region='China', scenario='APS'):
    # Get sales data for the selected region and scenario
    sales_data = filter_data(
        combined_df, 
        regions=region, 
        parameters='EV sales', 
        scenarios=scenario,
        powertrains=['BEV', 'PHEV', 'FCEV']
    )
    
    # Pivot to get values by year and powertrain
    pivot_df = sales_data.pivot_table(
        index='year', 
        columns='powertrain', 
        values='value', 
        aggfunc='sum'
    ).fillna(0)
    
    # Calculate percentages
    pivot_df = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100
    
    plt.figure(figsize=(12, 6))
    pivot_df.plot(kind='bar', stacked=True, width=0.8)
    plt.title(f'EV Powertrain Mix - {region} ({scenario} Scenario)')
    plt.ylabel('Percentage of Sales')
    plt.xlabel('Year')
    plt.legend(title='Powertrain', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# 3. Electricity Demand Projections
def plot_electricity_demand():
    elec_demand = filter_data(combined_df, parameters='Electricity demand')
    
    fig = px.line(
        elec_demand, 
        x='year', 
        y='value', 
        color='region', 
        line_dash='scenario',
        title='Electricity Demand Projections for EVs by Region and Scenario',
        labels={'value': 'Electricity Demand (GWh)', 'year': 'Year'},
        log_y=True
    )
    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    fig.show()

# 4. Oil Displacement Comparison
def plot_oil_displacement():
    oil_disp = filter_data(combined_df, parameters='Oil displacement Mbd')
    
    fig = px.line(
        oil_disp, 
        x='year', 
        y='value', 
        color='region', 
        line_dash='scenario',
        title='Oil Displacement Projections (Million Barrels per Day)',
        labels={'value': 'Oil Displacement (Mbd)', 'year': 'Year'}
    )
    fig.update_layout(
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    fig.show()

# 5. Scenario Comparison Dashboard
def create_dashboard(region='World'):
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'EV Sales Share - {region}',
            f'Electricity Demand - {region}',
            f'Oil Displacement - {region}',
            f'EV Stock - {region}'
        )
    )
    
    # EV Sales Share
    sales_share = filter_data(combined_df, parameters='EV sales share', regions=region)
    for scenario in ['APS', 'STEPS']:
        df = sales_share[sales_share['scenario'] == scenario]
        fig.add_trace(
            go.Scatter(
                x=df['year'], y=df['value'],
                name=f'Sales Share {scenario}',
                line=dict(dash='solid' if scenario == 'APS' else 'dash')
            ),
            row=1, col=1
        )
    
    # Electricity Demand
    elec_demand = filter_data(combined_df, parameters='Electricity demand', regions=region)
    for scenario in ['APS', 'STEPS']:
        df = elec_demand[elec_demand['scenario'] == scenario]
        fig.add_trace(
            go.Scatter(
                x=df['year'], y=df['value'],
                name=f'Electricity {scenario}',
                line=dict(dash='solid' if scenario == 'APS' else 'dash'),
                showlegend=False
            ),
            row=1, col=2
        )
    
    # Oil Displacement
    oil_disp = filter_data(combined_df, parameters='Oil displacement Mbd', regions=region)
    for scenario in ['APS', 'STEPS']:
        df = oil_disp[oil_disp['scenario'] == scenario]
        fig.add_trace(
            go.Scatter(
                x=df['year'], y=df['value'],
                name=f'Oil Disp. {scenario}',
                line=dict(dash='solid' if scenario == 'APS' else 'dash'),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # EV Stock
    ev_stock = filter_data(
        combined_df, 
        parameters='EV stock', 
        regions=region,
        powertrains=['BEV', 'PHEV', 'FCEV']
    )
    for scenario in ['APS', 'STEPS']:
        for powertrain in ['BEV', 'PHEV', 'FCEV']:
            df = ev_stock[
                (ev_stock['scenario'] == scenario) & 
                (ev_stock['powertrain'] == powertrain)
            ]
            fig.add_trace(
                go.Scatter(
                    x=df['year'], y=df['value'],
                    name=f'{powertrain} {scenario}',
                    line=dict(dash='solid' if scenario == 'APS' else 'dash'),
                    showlegend=(powertrain == 'BEV')  # Only show legend for BEV to reduce clutter
                ),
                row=2, col=2
            )
    
    fig.update_layout(
        height=800,
        title_text=f"EV Adoption Metrics - {region}",
        hovermode='x unified'
    )
    fig.show()

# 6. Carbon Footprint Calculator (Simplified)
def calculate_carbon_footprint(ev_type='BEV', annual_miles=12000, region='USA'):
    """
    Simplified carbon footprint calculator for EVs vs ICE vehicles
    
    Parameters:
    - ev_type: 'BEV' or 'PHEV'
    - annual_miles: miles driven per year
    - region: region for electricity grid emissions factor
    
    Returns:
    - Dictionary with carbon footprint comparison
    """
    # Emission factors (grams CO2 per mile)
    # Source: EPA estimates and regional grid averages
    emission_factors = {
        'ICE': 404,  # Average gasoline car
        'BEV': {
            'USA': 200,
            'Europe': 150,
            'China': 250,
            'India': 300,
            'World': 220
        },
        'PHEV': {
            'USA': 250,
            'Europe': 180,
            'China': 300,
            'India': 350,
            'World': 240
        }
    }
    
    # Calculate annual emissions
    ice_emissions = annual_miles * emission_factors['ICE']
    ev_emissions = annual_miles * emission_factors[ev_type][region]
    
    # Calculate savings
    savings = ice_emissions - ev_emissions
    savings_percent = (savings / ice_emissions) * 100
    
    return {
        'vehicle_type': ev_type,
        'annual_miles': annual_miles,
        'region': region,
        'ice_emissions_kg': ice_emissions / 1000,
        'ev_emissions_kg': ev_emissions / 1000,
        'savings_kg': savings / 1000,
        'savings_percent': savings_percent
    }

# Run visualizations
plot_ev_adoption_trends()
plot_powertrain_mix(region='China', scenario='APS')
plot_electricity_demand()
plot_oil_displacement()
create_dashboard(region='World')

# Example carbon footprint calculation
carbon_footprint = calculate_carbon_footprint(ev_type='BEV', annual_miles=15000, region='Europe')
print("\nCarbon Footprint Comparison:")
for k, v in carbon_footprint.items():
    print(f"{k.replace('_', ' ').title()}: {v}")