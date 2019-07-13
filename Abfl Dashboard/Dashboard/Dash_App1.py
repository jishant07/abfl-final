from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_html_components as html

url_base = '/dash/app1/'

#--------------------------------- Data ---------------------------
df=pd.read_csv(r'prosperLoanData_.csv', low_memory=False)

df['LoanOriginationDate'] = pd.to_datetime(df['LoanOriginationDate'])
df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'])
df['ClosedDate'] = pd.to_datetime(df['ClosedDate'])
df = df.sort_values(by='LoanOriginationDate',ascending=True)

total_customers = df.ListingKey.count()
total_loans = df.LoanOriginalAmount.sum()

year_groups = df.groupby(df.LoanOriginationDate.dt.year)
avg_year_groups = year_groups['LenderYield','EstimatedLoss','BorrowerRate','BorrowerAPR','EstimatedEffectiveYield'].mean()
prosper_groups = df.groupby(df.ProsperScore)
avg_prosper = prosper_groups['BorrowerRate','BorrowerAPR'].mean()

# -------------------------------- End Data -------------------------
layout = html.Div([

    # html.Div([
    #
    #     html.Div([
    #         html.H2(total_customers),
    #         html.Div(["Total Customers"],
    #                 className="subtitle padded",
    #         ),
    #
    #     ], className='two columns'),
    #     html.Div([
    #         html.H2(total_loans),
    #         html.Div(["Total Loan Disbursed"],
    #                 className="subtitle padded",
    #         ),
    #
    #     ], className='two columns'),
    #
    # ], className='row'),
    html.Div([
        html.Div([
                dcc.Dropdown(
                    id='prosper-button',
                    options=[
                            {'label': 'Borrower APR', 'value': 'BorrowerAPR'},
                            {'label': 'Borrower Rate', 'value': 'BorrowerRate'},
                    ],
                    value='BorrowerAPR',
                    multi = True
                ),
        ], className='four columns'),
        html.Div([
                dcc.Dropdown(
                    id='performance-dropdown',
                    options=[
                            {'label': 'Borrower APR', 'value': 'BorrowerAPR'},
                            {'label': 'Borrower Rate', 'value': 'BorrowerRate'},
                            {'label': 'Lender Yield', 'value': 'LenderYield'},
                            {'label': 'Estimated Yield', 'value': 'EstimatedEffectiveYield'}
                    ],
                    value='LenderYield',
                    multi = True
                ),
        ], className='four columns offset-by-three columns'),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Graph(
            id='prosper-graph',

            )
        ], className='six columns'),
        html.Div([
            dcc.Graph(
            id='performance-graph'
            )
        ], className='six columns'),

    ], className='row')
])

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('performance-graph', 'figure'),
            [Input('performance-dropdown', 'value')])
    def update_graph(value):
        plot_df = avg_year_groups[value]
        perform = []
        for field in value:
            data = go.Scatter(
                x=plot_df.index,
                y=plot_df[field],
                showlegend=True,
                name=field
            )
            perform.append(data)
        return {
            'data' : perform,
            'layout': go.Layout(title="Rate Distribution through Years  ",
                                xaxis = {"title":"Years"},
                                yaxis = {"title":"Rate"})

            }


    @app.callback(
        Output('prosper-graph', 'figure'),
        [Input('prosper-button','value')]
    )
    def update_box(value):
        plot_df = avg_prosper[value]
        perform = []
        for field in value:
            data = go.Bar(
                x=plot_df.index,
                y=plot_df[field],
                showlegend=True,
                name=field
            )
            perform.append(data)
        return {
            'data' : perform,
            'layout': go.Layout(title="Distribution of Credit Scores  ",
                                xaxis = {"title":"Credit Scores"},
                                yaxis = {"title":"Rate"})

            }

    return app.server