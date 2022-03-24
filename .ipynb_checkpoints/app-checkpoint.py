import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd

# Read in the USA counties shape files
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

########### Define a few variables ######

tabtitle = 'Virginia Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/vharkar/305-virginia-census-data'
varlist=['TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'RUCC_2013']

df=pd.read_pickle('resources/va-stats.pkl')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Virginia Census Data 2017'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select census variable:'),
                dcc.Dropdown(
                    id='stats-drop1',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='MeanCommute'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='va-map1')
        ], className='nine columns'),
    ], className='twelve columns'),
    
    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('va-map1', 'figure'),
              Output('va-map2', 'figure'),
              [Input('stats-drop1', 'value')])
def display_results1(selected_value):
    valmin1=df[selected_value].min()
    valmax1=df[selected_value].max()
    fig1 = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=df['FIPS'],
                                    z=df[selected_value],
                                    colorscale='Blues',
                                    text=df['County'],
                                    zmin=valmin1,
                                    zmax=valmax1,
                                    marker_line_width=0))
    fig1.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.8,
                      mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    valmin2=df[selected_value].min()
    valmax2=df[selected_value].max()
    fig2 = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=df['FIPS'],
                                    z=df[selected_value],
                                    colorscale='Blues',
                                    text=df['County'],
                                    zmin=valmin2,
                                    zmax=valmax2,
                                    marker_line_width=0))
    fig2.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3,
                      mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig1, fig2
    

# https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
