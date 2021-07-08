from dash_html_components.Div import Div
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import plotly.express as px


labs = pd.read_csv('db/labs.csv').sort_values(by="number_women")

app = dash.Dash(__name__)
server = app.server
faculties = list(labs["faculty"].unique())
faculties.insert(0, "ALL")
app.layout = html.Div([
    html.Div([
        
        dcc.Dropdown(id='faculty-select', options=[{'label': i, 'value': i}
                     for i in faculties], value='ALL', style={'width': '140px'}, ),
        dcc.Dropdown(id='sort-select', options=[{'label': i, 'value': i} for i in [
                     "total", "women", "men"]], value='total', style={'width': '140px'})
    ]),
    dcc.Graph('bar-chart-graph', config={'displayModeBar': False})
])


@app.callback(
    Output('bar-chart-graph', 'figure'),
    [Input('faculty-select', 'value'), Input('sort-select', 'value')]
)
def update_graph(faculty, sort_type):
    if faculty == 'ALL':
        faculty_labs = labs
    else:
        faculty_labs = (labs[labs['faculty'] == faculty]
                        ).sort_values(by="number_women")

    if sort_type == 'women':
        faculty_labs = faculty_labs.sort_values(by="number_women")
    elif sort_type == 'men':
        faculty_labs = faculty_labs.sort_values(by="number_men")
    else:
        faculty_labs["total"] = faculty_labs['number_women'] + \
            faculty_labs['number_men']
        faculty_labs = faculty_labs.sort_values(by='total')

    fig = px.bar(faculty_labs,
                 x="acronym",
                 y=["number_women", "number_men"],
                 title="Faculty: " + faculty,
                 hover_name="name",
                 hover_data={
                     "acronym": False,
                     "variable": False,
                     "value": False,
                     "total researchers": faculty_labs["number_men"] + faculty_labs["number_women"],
                     "men": faculty_labs["number_men"],
                     "women": faculty_labs["number_women"]
                 }
                 )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
