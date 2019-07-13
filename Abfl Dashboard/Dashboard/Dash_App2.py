
from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


url_base = '/dash/app2/'

df=pd.read_csv(r'prosperLoanData_.csv', low_memory=False, nrows = 2865 )

df['LoanOriginationDate'] = pd.to_datetime(df['LoanOriginationDate'])
df['ListingCreationDate'] = pd.to_datetime(df['ListingCreationDate'])
df['ClosedDate'] = pd.to_datetime(df['ClosedDate'])
df = df.sort_values(by='LoanOriginationDate',ascending=True)
reason = df['ListingCategory (numeric)'].unique()
total_loans = df.LoanOriginalAmount.sum()
total_comp = df[df['LoanStatus']=='Completed']['ListingKey'].count()
total_curr = df[df['LoanStatus']=='Current']['ListingKey'].count()
total_defaulted = df[df['LoanStatus']=='Defaulted']['ListingKey'].count()



loan_vs_emi =[go.Scatter(
        x = df['LoanOriginalAmount'],
        y = df['MonthlyLoanPayment'],
        mode = 'markers'
        )]
loan_layout = dict(
    title='Loan Amount VS Monthly EMI',
    xaxis=dict(title='Loan Original Amount',
               rangeslider=dict(
                visible = True
        ),

        type='-',

    ),
    yaxis=dict(
        title='Monthly Loan Payment')
    )


loan_fig = dict(data=loan_vs_emi, layout = loan_layout)


layout = html.Div([

   html.Div([
       html.Div([
        html.Div(total_loans,style={'fontSize': 30, 'align' : 'center'}),
        html.Label('Total Loan Amount', style={'align' : 'center'})
       ], className='three columns'),
       html.Div([
           html.Div(total_comp, style={'fontSize': 30, 'align' : 'center'}),
           html.Label('Total Loans Completed', style={'align' : 'center'})
       ], className='three columns'),
       html.Div([
           html.Div(total_curr, style={'fontSize': 30, 'align' : 'center'}),
           html.Label('Total Current Loans', style={'align' : 'center'})
       ], className='three columns'),
       html.Div([
           html.Div(total_defaulted, style={'fontSize': 30, 'align' : 'center'}),
           html.Label('Total Loans Defaulted', style={'align' : 'center'})
       ], className='three columns'),

   ],className='row', style={'marginBottom': 50, 'marginTop': 25}),
   html.Div([
        dcc.Graph(
            figure=loan_fig, className="six columns"
        ),

        html.Div([
            html.Div([
                    dcc.Dropdown(
                    id='reason',
                        options=[
                        {'label': 'Debt Consolidation', 'value': 1},
                        {'label': 'Home Improvement', 'value': 2},
                        {'label': 'Business', 'value': 3},
                        {'label': 'Personal Loan', 'value': 4},
                        {'label': 'Student Use', 'value': 5},
                        {'label': 'Auto', 'value': 6},
                        {'label': 'Other', 'value': 7},
                        {'label': 'Baby&Adoption', 'value': 8},
                        {'label': 'Boat', 'value': 9},
                        {'label': 'Cosmetic Procedure', 'value': 10},
                        {'label': 'Engagement Ring', 'value': 11},
                        {'label': 'Green Loans', 'value': 12},
                        {'label': 'Household Expenses', 'value': 13},
                        {'label': 'Large Purchases', 'value': 14},
                        {'label': 'Medical/Dental', 'value': 15},
                        {'label': 'Motorcycle', 'value': 16},
                        {'label': 'RV', 'value': 17},
                        {'label': 'Taxes', 'value': 18},
                        {'label': 'Vacation', 'value': 19},
                        {'label': 'Wedding Loans', 'value': 20}
                    ], value=1, className="six columns"),
                    dcc.Dropdown(
                    id='term',
                    options=[
                        {'label': '1 Years', 'value': 1},
                        {'label': '3 Years', 'value': 3},
                        {'label': '5 Years', 'value': 5}
                    ], value=1, className="six columns"),
            ], className="row"),
            html.Div([
                    dcc.Graph(
                        id='term_reason', className="twelve columns",
                    )
            ], className="row", style={'width':'100%'})
        ], className="six columns")
    ], className="row")
], className="container-fluid")


def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base)
    app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
    apply_layout_with_auth(app, layout)


    @app.callback(
            Output('term_reason', 'figure'),
            [Input('reason', 'value'),Input('term','value')])
    def callback_fun(input_reason, input_term):
        new_term_reason = df[(df['Term']==input_term)&(df['ListingCategory (numeric)']==input_reason)]
        group = new_term_reason.groupby('LoanStatus')['Term'].count()
        trace = [go.Pie(labels=group.index, values=group.values,
                       hoverinfo='label+percent', textinfo='value',
                       textfont=dict(size=20))]
        return {
            'data' : trace,

        }

    return app.server