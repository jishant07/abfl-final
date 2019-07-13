from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashboard import Dash_App1, Dash_App2, clients_table, home_tab

@blueprint.route('/app1')
@login_required
def app1_template():
    return render_template('app1.html', dash_url = Dash_App1.url_base)

@blueprint.route('/app2')
@login_required
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)


@blueprint.route('/clients')
@login_required
def client_template():
    return render_template('client_table.html', dash_url = clients_table.url_base)

@blueprint.route('/home')
@login_required
def home_template():
    return render_template('home.html', dash_url = home_tab.url_base)

