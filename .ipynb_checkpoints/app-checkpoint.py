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

def fipsStr(fips):
    if fips < 10000:
        return "0" + str(fips)
    else:
        return str(fips)
    
########### Define a few variables ######

tabtitle = 'US Counties Census Info'
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
census['FIPSSTR'] = census['CountyId'].apply(fipsStr)

fips=pd.read_excel('resources/ruralurbancodes2013.xls')
fips.groupby('RUCC_2013')[['RUCC_2013','Description','County_Name','Population_2010','State']].max()
fips['FIPSSTR'] = fips['FIPS'].apply(fipsStr)

statesList = []
for i in census['State'].unique():
    statesList.append(i)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
        
    html.H2('2017 US Census Data - by State', style = {'text-align':'center'}),
      
    # Dropdown for state
    html.Div([
       html.H6('Select State:'),
       dcc.Dropdown(
           id='state-drop',
           options=[{'label': i, 'value': i} for i in statesList],
            value='Virginia'
       ),
       html.Br()
    ], className='three columns'),
    
    # Dropdown for attribute
    html.Div([
       html.H6('Select census variable:'),
       dcc.Dropdown(
           id='attr-drop',
           options=[{'label': i, 'value': i} for i in varlist],
           value='MeanCommute'
       ),
       html.Br()
    ], className='three columns'),
    
    # US MAP
    html.Div([
        html.Br(),
        dcc.Graph(id='county-map')
    ], className='eight columns'),
    
    # Footer
    html.Div([
       html.Br(),
       html.A('Code on Github', href=githublink),
       html.Br(),
       html.A("Data Source", href=sourceurl)
    ], className='three columns')
  ]
)
    
############ Callbacks
@app.callback(Output('county-map', 'figure'),
              Input('state-drop', 'value'),
              Input('attr-drop', 'value'))
def display_results1(state, attribute):
    
    statedf=census.loc[census['State']==state]
    county=pd.merge(statedf, fips, left_on='FIPSSTR', right_on='FIPSSTR', how='left')

    valmin=county[attribute].min()
    valmax=county[attribute].max()
    
    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=county['FIPSSTR'],
                                    z=county[attribute],
                                    colorscale='Magma',
                                    text=county['County'],
                                    zmin=valmin,
                                    zmax=valmax,
                                    marker_opacity=0.5,
                                    marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3.0,
                      mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=1000)

    return fig
    
# https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
