from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
spacex_df = pd.read_csv('spacex_launch_dash.csv')
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Initialize app
app = Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

# TASK 1&3: Add a dropdown component and add a Range Slider
    dcc.Dropdown(id='site-dropdown',
                 options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
    ), 
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),  
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]
    ),    
    html.Br(),
    dcc.Graph(id='success-payload-scatter-chart')
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown.
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df_grouped = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        print(df_grouped)  # Debug: see output in terminal
        fig = px.pie(df_grouped, values='class', names='Launch Site',
                     title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
            filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
            filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
            fig = px.pie(filtered_df, values='class count',
                    names='class',
                    title=f'Total Success Launched for site {entered_site}')
    return fig

# TASK 4- Add a callback function to render the scatter plot.
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def get_scatter_plot(entered_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                           (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            title='Payload vs. Launch Outcome (All Sites)',
            labels={'class': 'Launch Outcome (1=Success, 0=Failure)'}
        )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            title=f'Payload vs. Launch Outcome for {entered_site}',
            labels={'class': 'Launch Outcome (1=Success, 0=Failure)'}
        )
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)