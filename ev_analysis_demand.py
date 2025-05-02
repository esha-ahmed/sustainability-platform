import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# Load the datasets
aps_df = pd.read_csv('./data/IEA-EV-dataElectricity-demandProjection-APSCars.csv')
steps_df = pd.read_csv('./data/IEA-EV-dataElectricity-demandProjection-STEPSCars.csv')

# Add scenario identifier
aps_df['scenario'] = 'APS'
steps_df['scenario'] = 'STEPS'

# Combine datasets
combined_df = pd.concat([aps_df, steps_df])

# Clean column names and data types
combined_df.columns = combined_df.columns.str.strip().str.lower()
combined_df['value'] = pd.to_numeric(combined_df['value'], errors='coerce')

# Data Exploration
print(f"Total records: {len(combined_df)}")
print(f"Unique regions: {combined_df['region'].unique()}")
print(f"Unique parameters: {combined_df['parameter'].unique()}")

# Helper function to filter and pivot data - FINAL CORRECTED VERSION
def filter_pivot_data(df, parameter, regions=None, years=None):
    # Use .isin() properly for array comparisons
    mask = df['parameter'] == parameter
    filtered = df[mask]
    
    if regions is not None:
        filtered = filtered[filtered['region'].isin(regions)]
    if years is not None:
        filtered = filtered[filtered['year'].isin(years)]
        
    if filtered.empty:
        return pd.DataFrame()
        
    return filtered.pivot_table(index=['year', 'scenario'], columns='region', values='value')

# 1. Data Visualization Dashboard - FINAL CORRECTED VERSION
def create_dashboard():
    # Set up the dashboard layout
    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "scatter"}],
               [{"colspan": 2}, None]],
        subplot_titles=("EV Sales Share by Region", 
                       "EV Stock Share by Region",
                       "Electricity Demand (GWh)",
                       "Oil Displacement (Mbd)",
                       "Comparison of APS vs STEPS Scenarios (China)")
    )
    
    # Define regions to analyze
    regions = ['China', 'Europe', 'USA', 'India', 'Rest of the world']
    
    # Plot EV Sales Share - FIXED BOOLEAN OPERATIONS
    sales_share = filter_pivot_data(combined_df, 'EV sales share', regions)
    if not sales_share.empty:
        for region in regions:
            for scenario in ['APS', 'STEPS']:
                try:
                    data = sales_share.xs(scenario, level='scenario')[region].dropna()
                    if not data.empty:
                        fig.add_trace(
                            go.Scatter(x=data.index, y=data, name=f"{region} - {scenario}",
                                     legendgroup=region, showlegend=(scenario=='APS')),
                            row=1, col=1
                        )
                except (KeyError, TypeError):
                    continue
    
    # Plot EV Stock Share
    stock_share = filter_pivot_data(combined_df, 'EV stock share', regions)
    if not stock_share.empty:
        for region in regions:
            for scenario in ['APS', 'STEPS']:
                try:
                    data = stock_share.xs(scenario, level='scenario')[region].dropna()
                    if not data.empty:
                        fig.add_trace(
                            go.Scatter(x=data.index, y=data, name=f"{region} - {scenario}",
                                     legendgroup=region, showlegend=False),
                            row=1, col=2
                        )
                except (KeyError, TypeError):
                    continue
    
    # Plot Electricity Demand
    elec_demand = filter_pivot_data(combined_df, 'Electricity demand', regions)
    if not elec_demand.empty:
        for region in regions:
            for scenario in ['APS', 'STEPS']:
                try:
                    data = elec_demand.xs(scenario, level='scenario')[region].dropna()
                    if not data.empty:
                        fig.add_trace(
                            go.Scatter(x=data.index, y=data, name=f"{region} - {scenario}",
                                     legendgroup=region, showlegend=False),
                            row=2, col=1
                        )
                except (KeyError, TypeError):
                    continue
    
    # Plot Oil Displacement
    oil_disp = filter_pivot_data(combined_df, 'Oil displacement Mbd', regions)
    if not oil_disp.empty:
        for region in regions:
            for scenario in ['APS', 'STEPS']:
                try:
                    data = oil_disp.xs(scenario, level='scenario')[region].dropna()
                    if not data.empty:
                        fig.add_trace(
                            go.Scatter(x=data.index, y=data, name=f"{region} - {scenario}",
                                     legendgroup=region, showlegend=False),
                            row=2, col=2
                        )
                except (KeyError, TypeError):
                    continue
    
    # Scenario comparison for China - PROPERLY HANDLED BOOLEAN FILTERS
    china_mask = (combined_df['region'] == 'China')
    china_data = combined_df[china_mask]
    
    params_to_compare = ['EV sales share', 'EV stock share', 'Electricity demand', 'Oil displacement Mbd']
    
    for param in params_to_compare:
        param_mask = (china_data['parameter'] == param)
        param_data = china_data[param_mask]
        
        if param_data.empty:
            continue
            
        aps_mask = (param_data['scenario'] == 'APS')
        steps_mask = (param_data['scenario'] == 'STEPS')
        
        aps_data = param_data[aps_mask]
        steps_data = param_data[steps_mask]
        
        if not aps_data.empty:
            fig.add_trace(
                go.Scatter(x=aps_data['year'], y=aps_data['value'], 
                         name=f"APS - {param}", line=dict(dash='dash')),
                row=3, col=1
            )
        
        if not steps_data.empty:
            fig.add_trace(
                go.Scatter(x=steps_data['year'], y=steps_data['value'], 
                         name=f"STEPS - {param}", line=dict(dash='dot')),
                row=3, col=1
            )
    
    # Update layout
    fig.update_layout(
        height=1200,
        title_text="Electric Vehicle Data Analysis Dashboard",
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text="Percentage", row=1, col=1)
    fig.update_yaxes(title_text="Percentage", row=1, col=2)
    fig.update_yaxes(title_text="GWh", row=2, col=1)
    fig.update_yaxes(title_text="Million barrels per day", row=2, col=2)
    fig.update_yaxes(title_text="Value", row=3, col=1)
    
    return fig

# Show dashboard
dashboard = create_dashboard()
dashboard.show()

# 2. Predictive Models - FINAL CORRECTED VERSION
def create_predictive_models():
    # Prepare data for China's electricity demand (APS scenario)
    china_mask = (
        (combined_df['region'] == 'China') & 
        (combined_df['parameter'] == 'Electricity demand') &
        (combined_df['scenario'] == 'APS')
    )
    china_elec = combined_df[china_mask][['year', 'value']].dropna().sort_values('year')
    
    if len(china_elec) < 3:
        print("Insufficient data for electricity demand forecasting")
    else:
        # Time-series forecasting with ARIMA
        ts_data = china_elec.set_index('year')['value']
        
        try:
            model = ARIMA(ts_data, order=(1,1,1))
            model_fit = model.fit()
            
            # Forecast next 5 years
            forecast_years = list(range(ts_data.index.max()+1, ts_data.index.max()+6))
            forecast = model_fit.forecast(steps=5)
            
            # Plot actual vs forecast
            plt.figure(figsize=(10,6))
            plt.plot(ts_data.index, ts_data, label='Actual')
            plt.plot(forecast_years, forecast, label='Forecast', linestyle='--')
            plt.title('China Electricity Demand Forecast (APS Scenario)')
            plt.xlabel('Year')
            plt.ylabel('Electricity Demand (GWh)')
            plt.legend()
            plt.grid()
            plt.show()
        except Exception as e:
            print(f"ARIMA modeling failed: {str(e)}")
    
    # Regression model for oil displacement vs EV stock
    # Prepare masks first to avoid chained indexing
    china_mask = (combined_df['region'] == 'China')
    stock_mask = combined_df['parameter'].str.contains('EV stock', na=False)
    aps_mask = (combined_df['scenario'] == 'APS')
    oil_mask = (combined_df['parameter'] == 'Oil displacement Mbd')
    
    china_ev_stock = combined_df[china_mask & stock_mask & aps_mask]
    china_oil_disp = combined_df[china_mask & oil_mask & aps_mask]
    
    if len(china_ev_stock) == 0 or len(china_oil_disp) == 0:
        print("Insufficient data for regression model")
        return
    
    try:
        # Merge with proper handling
        regression_data = pd.merge(
            china_ev_stock[['year', 'powertrain', 'value']],
            china_oil_disp[['year', 'value']],
            on='year',
            suffixes=('_stock', '_oil'),
            how='inner'
        )
        
        if regression_data.empty:
            print("No overlapping data for regression")
            return
            
        # Pivot with proper aggregation
        regression_data = regression_data.pivot_table(
            index='year', 
            columns='powertrain', 
            values='value_stock',
            aggfunc='sum'
        ).join(china_oil_disp.set_index('year')['value'])
        
        regression_data = regression_data.fillna(0)
        
        if len(regression_data) < 2:
            print("Insufficient data points for regression")
            return
            
        # Fit linear regression
        X = regression_data[['BEV', 'PHEV', 'FCEV']].values  # Convert to numpy array
        y = regression_data['value'].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        print("\nRegression Model for Oil Displacement vs EV Stock:")
        print(f"Coefficients - BEV: {model.coef_[0]:.6f}, PHEV: {model.coef_[1]:.6f}, FCEV: {model.coef_[2]:.6f}")
        print(f"Intercept: {model.intercept_:.6f}")
        print(f"R-squared: {model.score(X_test, y_test):.4f}")
        
        # Plot actual vs predicted
        y_pred = model.predict(X)
        plt.figure(figsize=(10,6))
        plt.scatter(y, y_pred)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--')
        plt.title('Actual vs Predicted Oil Displacement')
        plt.xlabel('Actual Oil Displacement (Mbd)')
        plt.ylabel('Predicted Oil Displacement (Mbd)')
        plt.grid()
        plt.show()
        
    except Exception as e:
        print(f"Regression modeling failed: {str(e)}")

# Run predictive models
create_predictive_models()