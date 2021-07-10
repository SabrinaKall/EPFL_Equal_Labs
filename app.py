from dash_html_components.Label import Label
from dash_html_components.P import P
from lab_data import LabData
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


app = dash.Dash(
    __name__, title='HireHer: gender equality in hiring at EPFL Labs')
server = app.server

lab_data = LabData()

app.layout = html.Div(children=[

    html.Div(
        className="app-header",
        children=[
            html.Div(
                'Gender distribution of research staff at EPFL Labs',
                className="app-header--title")
        ]),

    html.Div(
        children=html.Div([
            html.H5('General'),
            html.Label([html.Div(['''Filter by faculty''']),
                        dcc.Dropdown(
                        id='faculty-select',
                        options=[{'label': i, 'value': i}
                                 for i in lab_data.faculties],
                        value='ALL',
                        placeholder='Select a lab',
                        searchable=True,
                        )],
                       style={'width': '25%',
                              'display': 'inline-block', 'margin': '1%'},
                       ),

            html.Label([html.Div(['''Sort by''']),
                        dcc.Dropdown(
                        id='sort-select',
                        options=[{'label': i, 'value': i}
                                 for i in ["total", "women", "men"]],
                        value='total',
                        placeholder='Sort by...',
                        )],
                       style={'width': '25%',
                              'display': 'inline-block', 'margin': '1%'},
                       ),
        ],

        )
    ),

    html.Div([dcc.Graph('bar-chart-graph', config={'displayModeBar': False})]),
    html.Div([
        html.P(['* Does not include non-technical staff, guests or project students']),
        html.P(['** If you feel any of the lab information is inaccurate or out-of-date, feel free to send me the correct information, including a source, at "". )'])
    ],
        style={'font-size':'small'})
])


@app.callback(
    Output('bar-chart-graph', 'figure'),
    [Input('faculty-select', 'value'), Input('sort-select', 'value')]
)
def update_graph(faculty, sort_type):
    faculty_labs = lab_data.sort_labs_by(faculty, sort_type)
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
                 },
                 labels={"acronym":"lab", "value": "research staff breakdown"}
                 )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
