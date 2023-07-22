import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go

# Set the matplotlib backend to a non-multi-threaded one (agg)
matplotlib.use('agg')

data = pd.read_csv("TEMG4940C - Assignment Dataset.csv", sep="\t")
data['Y'] = data['AcceptedCmp1'] + data['AcceptedCmp2'] + data['AcceptedCmp3'] + data['AcceptedCmp4'] + data['AcceptedCmp5'] + data['Response']
data['Income'] = data.groupby('Education')['Income'].transform(lambda x: x.fillna(x.mean()))
#handle outliers, remove rows with year of birth, income outliers using quantile method, remove rows with income that is outside the range of Q1-1.5*IQR and Q3+1.5*IQR
#first calculate the IQR, Q1 and Q3
iqr_income = data['Income'].quantile(0.75) - data['Income'].quantile(0.25)
q1_income = data['Income'].quantile(0.25)
q3_income = data['Income'].quantile(0.75)

iqr_year_of_birth = data['Year_Birth'].quantile(0.75) - data['Year_Birth'].quantile(0.25)
q1_year_of_birth = data['Year_Birth'].quantile(0.25)
q3_year_of_birth = data['Year_Birth'].quantile(0.75)

#remove rows with income outliers
data = data[(data['Income'] >= q1_income - 1.5*iqr_income) & (data['Income'] <= q3_income + 1.5*iqr_income)]

#remove rows with year of birth outliers
data = data[(data['Year_Birth'] >= q1_year_of_birth - 1.5*iqr_year_of_birth) & (data['Year_Birth'] <= q3_year_of_birth + 1.5*iqr_year_of_birth)]

#replace Alone mariatal status with single
data['Marital_Status'] = data['Marital_Status'].replace('Alone', 'Single') # they are the same thing

#remove rows with marital status = Absurd, YOLO
data = data[(data['Marital_Status'] != 'Absurd') & (data['Marital_Status'] != 'YOLO')] # cannot determine what the actual marital status is

columns = ['Year_Birth', 'Income', 'Kidhome',
       'Teenhome', 'Recency', 'MntWines', 'MntFruits',
       'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts',
       'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases',
       'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth','Y', 'Education', 'Marital_Status']

data = data[columns]

print(data.head(10))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Exploratory Data Analysis'),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in data.columns],
        value=data.columns[0],
        multi=False
    ),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='box-chart'),
    dcc.Graph(id='pie-chart'),
])

# Define callback for the column dropdown
@app.callback(
    [dash.dependencies.Output('histogram', 'figure'),
     dash.dependencies.Output('box-chart', 'figure'),
     dash.dependencies.Output('pie-chart', 'figure')],
    [dash.dependencies.Input('column-dropdown', 'value')]
)
def update_charts(selected_column):
    # Create histogram
    histogram = {
        'data': [{
            'x': data[selected_column],
            'type': 'histogram',
            'name': 'Histogram',
            'marker': {'color': 'rgba(255, 0, 0, 0.5)', 'line': {'color': 'black', 'width': 1}}
        }],
        'layout': {
            'title': f'Histogram of {selected_column}',
            'xaxis': {'title': selected_column},
            'yaxis': {'title': 'Count'}
        }
    }

    # Create box chart
    box_chart = {
        'data': [{
            'x': data[selected_column],
            'type': 'box',
            'name': 'Box Chart'
        }],
        'layout': {
            'title': f'Box Chart of {selected_column}',
            'xaxis': {'title': selected_column},
            'yaxis': {'title': 'Value'}
        }
    }

    # Create pie chart
    pie_chart = {
        'data': [{
            'labels': data[selected_column].value_counts().index.tolist(),
            'values': data[selected_column].value_counts().values.tolist(),
            'type': 'pie',
            'name': 'Pie Chart'
        }],
        'layout': {
            'title': f'Pie Chart of {selected_column}'
        }
    }

    return histogram, box_chart, pie_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
