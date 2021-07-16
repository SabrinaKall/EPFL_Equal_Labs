import webbrowser
from dash.exceptions import PreventUpdate
from lab_data import LabData
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(
    __name__, title='EPFL Labs by Gender')
server = app.server

lab_data = LabData()

app.layout = html.Div(children=[

    html.Div(
        className="app-header",
        children=[
            html.Div(
                'Gender in research at EPFL Labs',
                className="app-header--title")
        ]),

    html.Div(
        children=html.Div([
            html.H5('General'),
            html.P('Our data was collected from the official lab websites, which may be incomplete or out-of-date. Non-technical staff, guests and project students are not considered EPFL research staff.'),
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
    html.Footer(['For questions, comments, contributions or ideas for expansion, feel free to contact us at epfl.labs.gender.update@protonmail.com.'],
        style={'font-size':'small'}
    ),
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
                     "women": faculty_labs["number_women"],
                 },
                 labels={"acronym": "lab", "value": "research staff breakdown"},
                 custom_data=['lab_url']
                 )

    return fig


@app.callback(
    Output('bar-chart-graph', 'children'),
    [Input('bar-chart-graph', 'clickData')])
def open_source_url(clickData):
    if clickData:
        url = clickData['points'][0]['customdata'][0]
        webbrowser.open_new_tab(url)
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=False)
