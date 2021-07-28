import webbrowser
from dash.exceptions import PreventUpdate
from dash_html_components.H6 import H6
from dash_html_components.Table import Table
from dash_html_components.Td import Td
from dash_html_components.Th import Th
from dash_html_components.Tr import Tr
from dash_html_components.Ul import Ul
from data.lab_data import LabData
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(
    __name__, title='EPFL Labs by Gender')
server = app.server

lab_data = LabData()

sample_entry = lab_data.get_random_lab()
sample_url = sample_entry['lab_url'].iloc[0]


app.layout = html.Div(children=[

    html.Div(
        className="app-header",
        children=[
            html.Div(
                'Gender in Research at EPFL Labs',
                className="app-header--title")
        ]),

    html.Div(
        children=html.Div([
            html.H5("Overview"),
            html.Label([html.Div(['''Filter by faculty''']),
                        dcc.Dropdown(
                        id='faculty-select',
                        options=[{'label': i, 'value': i}
                                 for i in lab_data.faculties],
                        value='ALL',
                        placeholder='Select a lab',
                        searchable=True,
                        )],
                       ),

            html.Label([html.Div(['''Sort by''']),
                        dcc.Dropdown(
                        id='sort-select',
                        options=[{'label': i, 'value': i}
                                 for i in ["total", "women", "men"]],
                        value='total',
                        placeholder='Sort by...',
                        )],
                       ),
        ],
        )
    ),

    html.Div([dcc.Graph('bar-chart-graph', config={'displayModeBar': False})]),
    html.H5("Lab details"),
    html.Table(children=[
        html.Tr([
                html.Th("Name"),
                html.Th("Acronym"),
                html.Th("Faculty"),
                html.Th("Institute"),
                html.Th("Source"),
                html.Th("Number of men"),
                html.Th("Number of women"),
                ]),
        html.Tr([
                html.Td(id='lab_name', children=[
                        sample_entry['name'].iloc[0]]),
                html.Td(id='lab_acronym', children=[
                        sample_entry['acronym'].iloc[0]]),
                html.Td(id='lab_faculty', children=[
                        sample_entry['faculty'].iloc[0]]),
                html.Td(id='lab_institute', children=[
                        sample_entry['institute'].iloc[0]]),
                html.Td([
                    html.A(id='lab_url', children=[
                           sample_url], href=sample_url)
                ]),
                html.Td(id='lab_number_men', children=[
                        sample_entry['number_men'].iloc[0]]),
                html.Td(id='lab_number_women', children=[
                        sample_entry['number_women'].iloc[0]]),
                ]),
    ]),
    html.P(" ", style={'width': '100%', 'font-size': 'small'}),
    html.Footer(['Our data was collected from the official lab websites, which may be incomplete or out-of-date. Non-technical staff, guests and project students are not considered EPFL research staff. For questions, comments, contributions or ideas for expansion, feel free to contact us at epfl.labs.gender.update@protonmail.com.'],
                style={'font-size': 'small'}
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
                     "total researchers": faculty_labs["total"],
                     "men": faculty_labs["number_men"],
                     "women": faculty_labs["number_women"],
                 },
                 labels={"acronym": "lab", "value": "number of research staff"},
                 custom_data=['lab_url', 'name',
                              'acronym', 'faculty', 'institute']
                 )

    return fig


@app.callback(
    [
        Output('lab_url', 'href'),
        Output('lab_url', 'children'),
        Output('lab_name', 'children'),
        Output('lab_acronym', 'children'),
        Output('lab_faculty', 'children'),
        Output('lab_institute', 'children'),
        Output('lab_number_men', 'children'),
        Output('lab_number_women', 'children')
    ],
    [Input('bar-chart-graph', 'clickData')])
def open_source_url(clickData):
    if clickData:
        custom_data = clickData['points'][0]['customdata']
        url = custom_data[0]
        name = custom_data[1]
        acronym = custom_data[2]
        faculty = custom_data[3]
        institute = custom_data[4]
        number_men = custom_data[7]
        number_women = custom_data[8]

        return [url, url, name, acronym, faculty, institute, number_men, number_women]
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=False)
