import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import os

# First define the CAGR calculation function
def calculate_cagr(start_value, end_value, years):
    """Calculate Compound Annual Growth Rate"""
    return (end_value/start_value)**(1/years) - 1

# Now load and process the data
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'data', 'lithium-production.csv')
df = pd.read_csv(data_path)

# Prepare world data
world = df[df['Entity'] == 'World'][['Year', 'Lithium production - kt']].set_index('Year')
world_ts = world.asfreq('YS').sort_index()

# Time Series Decomposition
try:
    result = seasonal_decompose(world_ts['Lithium production - kt'], 
                              model='additive', 
                              period=5)
    result.plot()
    
    os.makedirs(os.path.join(script_dir, '..', 'outputs'), exist_ok=True)
    output_path = os.path.join(script_dir, '..', 'outputs', 'seasonal_decomposition.png')
    plt.savefig(output_path)
    print(f"Decomposition plot saved to {output_path}")
    plt.close()
except ValueError as e:
    print(f"Decomposition failed: {str(e)}")

# CAGR Calculation
try:
    start_val = world_ts.loc[1995, 'Lithium production - kt']
    end_val = world_ts.loc[2023, 'Lithium production - kt']
    cagr = calculate_cagr(start_val, end_val, 28)
    print(f"Global Lithium Production CAGR (1995-2023): {cagr:.2%}")
except KeyError as e:
    print(f"Missing data for CAGR calculation: {str(e)}")

# Growth Analysis
try:
    growth = df[df['Year'].isin([1995, 2023])].pivot(
        index='Entity', 
        columns='Year', 
        values='Lithium production - kt'
    ).dropna()
    
    growth['growth'] = growth[2023] / growth[1995]
    print("\nTop 5 Growth Countries (1995-2023):")
    print(growth.nlargest(5, 'growth'))
except Exception as e:
    print(f"Growth analysis failed: {str(e)}")