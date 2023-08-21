# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
#spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df = pd.read_csv("spacex.csv")
df = spacex_df
max_payload = spacex_df['PAYLOAD_MASS__KG_'].max()
min_payload = spacex_df['PAYLOAD_MASS__KG_'].min()

landing_outcomes = df['Landing_Outcome'].value_counts()
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])

Landing_class = []
Landing_class_str = []
for i in range(len(df)):
    if df['Landing_Outcome'] [i] in bad_outcomes:
        Landing_class.append(1) 
        Landing_class_str.append('0') 
    else:
        Landing_class.append(1)
        Landing_class_str.append('1')
spacex_df['Class']=Landing_class
spacex_df['Class_str']=Landing_class_str

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                               
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCSFS LC-40', 'value': 'CCSFS LC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                               
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                    100: '100'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='Class', 
        names='Launch_Site', 
        title='Success rate for ALL Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        indexes = []
        #print(entered_site)
        for i in range(len(spacex_df)):
            #print(spacex_df['Launch_Site'][i])
            if (spacex_df['Launch_Site'][i] != entered_site):
                #print('ok')
                indexes.append(i)

        # Delete Rows by Index numbers
        df1 = spacex_df
        df1=df1.drop(df1.index[indexes])
        print(len(df1))
        print(df1)
        succ = 0
        found = 0
        #print(df1['Class'])
        #for i in range(len(df1)):
        #    for j in range(len(indexes)):
        #        if indexes[j]==i:
        #            found = 1
        #    if found==0:
        #        succ = succ + df1['Class'][i]
                #print('ok')
        #print(succ)
        
        fig = px.pie(df1, values='Class', 
        names='Class_str', 
        title='Success rate for individual Site')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload_value):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='PAYLOAD_MASS__KG_', y='Class_str', 
        color = 'Booster_Version', 
        title='Scatter plot for ALL sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
