import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('sustainability_platform/data/electric-vehicle-battery-demand-by-region-2016-2023.csv', sep=';', skiprows=3)

# Clean column names
df.columns = ['Year'] + list(df.columns[1:])

# Create stacked area chart
fig = px.area(df, 
              x='Year', 
              y=['China', 'Europe', 'United States', 'Rest of world'],
              title='<b>EV Battery Demand by Region (2016-2023)</b><br><i>Units: GWh/year</i>',
              labels={'value': 'Battery Demand (GWh)', 'variable': 'Region'},
              color_discrete_map={
                  'China': '#1F77B4',
                  'Europe': '#FF7F0E',
                  'United States': '#2CA02C',
                  'Rest of world': '#9467BD'
              },
              template='plotly_white')

# Add line traces for better visibility
for region in ['China', 'Europe', 'United States', 'Rest of world']:
    fig.add_scatter(x=df['Year'], 
                   y=df[region], 
                   mode='lines',
                   line=dict(width=0.5, color='white'),
                   name='',
                   showlegend=False,
                   hoverinfo='skip')

# Customize layout
fig.update_layout(
    hovermode='x unified',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    yaxis=dict(
        rangemode='tozero'
    ),
    height=600,
    width=900
)

# Add annotations for growth rates
growth_text = []
for region in ['China', 'Europe', 'United States', 'Rest of world']:
    growth = (df[region].iloc[-1] / df[region].iloc[0] - 1) * 100
    growth_text.append(f"{region}: {growth:.0f}% growth")

fig.add_annotation(
    x=0.05,
    y=0.95,
    xref='paper',
    yref='paper',
    text="<br>".join(growth_text),
    showarrow=False,
    bgcolor='white',
    bordercolor='black',
    borderwidth=1
)

# Add range slider
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=5, label="5y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# Save and show
fig.write_html("ev_battery_demand.html")
fig.show()