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

tabtitle = 'Virginia Vs US Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/vharkar/305-virginia-census-data'
varlist=['TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'RUCC_2013']

census=pd.read_csv('resources/acs2017_county_data.csv')
fips=pd.read_excel('resources/ruralurbancodes2013.xls')
fips.groupby('RUCC_2013')[['RUCC_2013','Description']].max()
us=pd.merge(census, fips, left_on='CountyId', right_on='FIPS', how='left')
va=us.loc[us['State_y']=='CA']
us=us.dropna()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H2('Virginia and US Census Data Comparision for 2017'),
    
    # Dropdown 
    # VA MAP
    html.Div([
           html.H6('Select census variable:'),
           dcc.Dropdown(
               id='stats-drop1',
               options=[{'label': i, 'value': i} for i in varlist],
               value='MeanCommute'
           ),
           html.Br(),
           dcc.Graph(id='va-map'),
           html.Br()
    ], className='five columns'),
    
    # US MAP
    html.Div([
            dcc.Graph(id='us-map')
    ], className='ten columns'),
    
    # Footer
    html.Div([
       html.Br(),
       html.A('Code on Github', href=githublink),
       html.Br(),
       html.A("Data Source", href=sourceurl)
    ], className='three columns'),
  ]
)

############ Callbacks
@app.callback(Output('va-map', 'figure'),
              Output('us-map', 'figure'),
              [Input('stats-drop1', 'value')])
def display_results1(selected_value):
    valmin1=va[selected_value].min()
    valmax1=va[selected_value].max()
    fig1 = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=va['FIPS'],
                                    z=va[selected_value],
                                    colorscale='Magma',
                                    text=va['County'],
                                    zmin=valmin1,
                                    zmax=valmax1,
                                    marker_opacity=0.5,
                                    marker_line_width=0))
    fig1.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.8,
                      mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    valmin2=us[selected_value].min()
    valmax2=us[selected_value].max()
    fig2 = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=us['FIPS'],
                                    z=us[selected_value],
                                    colorscale='Magma',
                                    text=us['County'],
                                    zmin=valmin2,
                                    zmax=valmax2,
                                    marker_opacity=0.5,
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
