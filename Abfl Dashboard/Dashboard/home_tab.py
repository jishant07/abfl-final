from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import dash_html_components as html

url_base = '/dash/home/'

#--------------------------------- Data ---------------------------
df=pd.read_csv(r'prosperLoanData_.csv', low_memory=False, nrows=2865)
df['LoanOriginationDate'] = pd.to_datetime(df['LoanOriginationDate'])
df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'])
df['ClosedDate'] = pd.to_datetime(df['ClosedDate'])
df = df.sort_values(by='LoanOriginationDate', ascending=True)
new = df.groupby('ProsperScore')['ListingKey'].count()

customers = df.groupby(df.LoanOriginationDate.dt.year)['ListingKey'].count()

total_customers = df.ListingKey.count()
total_loans = df.LoanOriginalAmount.sum()

# -------------------------------- End Data -------------------------
trace = [go.Bar(
x=new.index,
y=new.values)]

pros_layout = dict(
    title='Credit Score Vs No. of Borrowers',
    yaxis = dict(
        title = 'Number of Customers'),
    xaxis=dict(
        title = 'Credit Score',
    ))
pros_fig=dict(data=trace, layout=pros_layout)

data = []
for i in range(0, len(pd.unique(df['ProsperScore']))):
    trace = {
        "type": 'violin',
        "x": df['ProsperScore'][df['ProsperScore'] == pd.unique(df['ProsperScore'])[i]],
        "y": df['LenderYield'][df['ProsperScore'] == pd.unique(df['ProsperScore'])[i]],
        "name": pd.unique(df['ProsperScore'])[i],
        "box": {
            "visible": True
        },
        "meanline": {
            "visible": True
        }
    }
    data.append(trace)

voilin_fig = {
    "data": data,
    "layout": {
        "title": " Credit Score VS Lender Yield",
        "xaxis": {
            "title": "Credit Score"
        },
        "yaxis": {
            "title": "Lender Yield",
            "zeroline": False,
        }
    }
}

layout = html.Div([
    html.Div([
        html.Div([
            html.Div(total_loans, style={'fontSize': 30, 'align': 'center'}),
            html.Label('Total Loan Disbursed', style={'align': 'center'})
        ], className='six columns'),
        html.Div([
            html.Div(total_customers, style={'fontSize': 30, 'align': 'center'}),
            html.Label('Total Customers', style={'align': 'center'})
        ], className='six columns'),


    ], className='row', style={'marginBottom': 30, 'marginTop': 20}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='pros_graph',
                figure=pros_fig
            )
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='voilin_graph',
                figure=voilin_fig
            )
        ], className='six columns')
    ], className='row')
])



def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
    apply_layout_with_auth(app, layout)

    # @app.callback(
    #     Output('score-borrower-graph', 'figure'),
    #     [Input('', 'value')])

    return app.server
