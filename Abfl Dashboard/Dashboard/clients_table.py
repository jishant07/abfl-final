import pandas as pd
import numpy as np
from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

# app = Dash(__name__ )
url_base = '/dash/clients/'

df = pd.read_csv(r'prosperLoanData_.csv', low_memory=False, nrows = 20)
table_df = df[['LoanNumber','LoanOriginationDate','ListingKey','LoanOriginalAmount','LoanStatus']]

layout = html.Div([
    dash_table.DataTable(
        id='datatable-filtering-fe',
        data= table_df.to_dict('records'),

        columns=[{"name": i, "id": i} for i in table_df.columns],
        filtering='be',

        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(224, 211, 211)',
                'font': 'Montserrat-Black'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(201, 32, 32)',
            'font': 'Montserrat-Black',
            'fontWeight': 'bold'
        }
    ),
    html.Div(id='datatable-filter-container')
])
def Add_Dash(server):
    # app = Dash(__name__ )
    app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)
    app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

    @app.callback(
        Output('datatable-filter-container', "children"),
        [Input('datatable-filtering-fe', "data")])
    def update_graph(rows):
        if rows is None:
            dff = table_df
        else:
            dff = pd.DataFrame(rows)

        return html.Div(dff)
    return app.server


# print(table_df)

# for row in table_df.itertuples():
#     print(row.Index, row.LoanNumber, row.LoanOriginationDate)


# @app.route('/')
# def html_table():
#     return render_template("client_table.html", table = table_df)
#     # passes dataframe as table to jinja template where itertuples() is used to get values
#     # for each attribute in each entry
#
# if __name__ =='__main__':
#     app.run_server(debug=True)
