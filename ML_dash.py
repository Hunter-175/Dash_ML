import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(selected_category):
    # Your update logic here
    # For example, update the figure based on the selected category
    updated_figure = {
        'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': selected_category}],
        'layout': {'title': f'Sample Graph - {selected_category}'}
    }
    return updated_figure

app.layout = html.Div([
    html.H1("My Dash App"),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Category 1'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Category 2'},
            ],
            'layout': {
                'title': 'Sample Graph'
            }
        }
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)