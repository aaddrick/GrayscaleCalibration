import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

dash_app = dash.Dash()
app = dash_app.server

params = [
    'IntensityIndex', 'PixelMap', 'Luminosity'
]

dash_app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Double (0-1)', 'value': 'double'},
            {'label': '8-bit (0-255)', 'value': '8bit'},
            {'label': '16-bit (0-65535)', 'value': '16bit'}
        ],
        value='8bit',
        style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.Div(id='dd-output-container'),
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'IntensityIndex', 'name': 'Intensity Index'}] + #, 'editable': False
            [{'id': 'PixelMap', 'name': 'Pixel Map'}] +
            [{'id': 'Luminosity', 'name': 'Luminosity (L*)'}]

        ),
        data=[
            dict(Model=i, **{param: 0 for param in params})
            for i in range(1, 16)
        ],
        editable=True
    ),
    dcc.Graph(id='table-editing-simple-output')
])

# dash_app.layout = html.Div([
#
# ])

@dash_app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@dash_app.callback(
    Output('table-editing-simple-output', 'figure'),
    [Input('table-editing-simple', 'data'),
     Input('table-editing-simple', 'columns')])

def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    return {
        'data': [{
            'type': 'parcoords',
            'dimensions': [{
                'label': col['name'],
                'values': df[col['id']]
            } for col in columns]
        }]
    }

if __name__ == '__main__':
    dash_app.run_server(debug=True)
