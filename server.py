import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go


labs = pd.read_csv('db/labs.csv').sort_values(by="number_women")

app = dash.Dash(__name__)
server = app.server
faculties = list(labs["faculty"].unique())
faculties.append("ALL")
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='faculty-select', options=[{'label': i, 'value': i} for i in faculties], value='IC', style={'width': '140px'})]),
    html.Div([dcc.Dropdown(id='sort-select', options=[{'label': i, 'value': i} for i in ["women", "total"]], value='women', style={'width': '140px'})]),
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
        faculty_labs = (labs[labs['faculty'] == faculty]).sort_values(by="number_women")

    if sort_type == 'women': 
        faculty_labs = faculty_labs.sort_values(by="number_women")
    else:
        faculty_labs["total"] = faculty_labs['number_women'] + faculty_labs['number_men']
        faculty_labs = faculty_labs.sort_values(by='total')

    fig = go.Figure(
        data=[
            go.Bar(
                name="number_women",
                x=faculty_labs["acronym"],
                y=faculty_labs["number_women"],
                offsetgroup=0,
            ),
            go.Bar(
                name="number_men",
                x=faculty_labs["acronym"],
                y=faculty_labs["number_men"],
                offsetgroup=1,
            ),
        ],
        layout=go.Layout(
            title="Labs",
            yaxis_title="Academic lab members"
        )
    )
    fig.update_layout(barmode='stack')
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)