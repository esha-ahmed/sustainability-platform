import pandas as pd
import plotly.express as px
import webbrowser
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load the data
df = pd.read_csv('sustainability_platform/data/IEA-EV-dataElectricity-demandHistoricalCars.csv')

# Filter for EV sales and stock data
sales_df = df[(df['parameter'] == 'EV sales') & (df['mode'] == 'Cars')]
stock_df = df[(df['parameter'] == 'EV stock') & (df['mode'] == 'Cars')]

# Aggregate data
sales_agg = sales_df.groupby(['year', 'region', 'powertrain'])['value'].sum().reset_index()
stock_agg = stock_df.groupby(['year', 'region', 'powertrain'])['value'].sum().reset_index()

# Create subplots
fig = make_subplots(rows=2, cols=1, 
                   subplot_titles=('<b>EV Sales by Region and Powertrain</b>', 
                                  '<b>EV Stock by Region and Powertrain</b>'),
                   vertical_spacing=0.15)

# Add sales data
for region in sales_agg['region'].unique():
    for powertrain in sales_agg['powertrain'].unique():
        subset = sales_agg[(sales_agg['region'] == region) & (sales_agg['powertrain'] == powertrain)]
        fig.add_trace(
            go.Scatter(
                x=subset['year'],
                y=subset['value'],
                name=f"{region} - {powertrain}",
                mode='lines+markers',
                legendgroup=region,
                line=dict(width=2)
            ),
            row=1, col=1
        )

# Add stock data
for region in stock_agg['region'].unique():
    for powertrain in stock_agg['powertrain'].unique():
        subset = stock_agg[(stock_agg['region'] == region) & (stock_agg['powertrain'] == powertrain)]
        fig.add_trace(
            go.Scatter(
                x=subset['year'],
                y=subset['value'],
                name=f"{region} - {powertrain}",
                mode='lines+markers',
                legendgroup=region,
                showlegend=False,
                line=dict(width=2)
            ),
            row=2, col=1
        )

# Customize layout
fig.update_layout(
    height=1200,
    width=1400,
    template='plotly_dark',
    title_text="<b>Global EV Adoption Trends (2010-2023)</b>",
    title_font_size=24,
    hovermode='x unified',
    legend=dict(
        title='<b>Region - Powertrain</b>',
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=10)
)
)

# Update axes
fig.update_yaxes(title_text="<b>Number of Vehicles</b>", row=1, col=1)
fig.update_yaxes(title_text="<b>Number of Vehicles</b>", row=2, col=1)
fig.update_xaxes(title_text="<b>Year</b>", row=2, col=1)

# Add range slider
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=5, label="5y", step="year", stepmode="backward"),
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ),
    row=2, col=1
)

# Add annotations
fig.add_annotation(
    x=0.5, y=1.08,
    xref='paper', yref='paper',
    text="<i>Data Source: IEA Global EV Outlook</i>",
    showarrow=False,
    font=dict(size=10, color="grey")
)

# Save to HTML file
html_file = 'ev_trends_enhanced.html'
fig.write_html(html_file)

# Open in browser
webbrowser.open ('file://' + os.path.realpath(html_file))