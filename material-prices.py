import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the data
df = pd.read_csv('sustainability_platform/data/price-of-selected-battery-materials-and-lithium-ion-batteries-2015-2024.csv', sep=';', skiprows=3)

# Clean column names
df.columns = ['Timestamp'] + list(df.columns[1:])

# Convert Unix timestamps (milliseconds) to datetime
df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')

# Melt the dataframe for better plotting
melted_df = df.melt(id_vars=['Date'], 
                    value_vars=['Cobalt sulfate', 'Lithium carbonate', 'Nickel sulphate',
                               'Manganese flake', 'Phosphoric acid', 'Battery pack price'],
                    var_name='Material',
                    value_name='Price Index')

# Create the interactive plot
fig = px.line(melted_df, 
              x='Date', 
              y='Price Index',
              color='Material',
              title='<b>Battery Materials Price Trends (2015-2024)</b><br><i>Index: January 2017 = 100</i>',
              labels={'Price Index': 'Price Index (Jan 2017=100)'},
              template='plotly_white',
              line_shape='spline',
              render_mode='svg')

# Customize the layout
fig.update_layout(
    hovermode='x unified',
    legend_title_text='Material',
    xaxis_title='Date',
    yaxis_title='Price Index',
    height=600,
    width=1000,
    font=dict(family="Arial", size=12)
)

# Add range slider and buttons
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=5, label="5y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# Highlight key events
events = [
    ("2018-06", "Chinese subsidy changes", 300),
    ("2020-03", "COVID-19 pandemic", 250),
    ("2022-03", "Russia-Ukraine war", 350)
]

for date, text, y_pos in events:
    fig.add_vline(
        x=pd.to_datetime(date),
        line_width=1,
        line_dash="dash",
        line_color="grey"
    )
    fig.add_annotation(
        x=pd.to_datetime(date),
        y=y_pos,
        text=text,
        showarrow=True,
        arrowhead=1,
        bgcolor="white"
    )

# Save and show
fig.write_html("battery_materials_prices.html")
fig.show()