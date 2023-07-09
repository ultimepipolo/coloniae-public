from flask import render_template, Blueprint, session, request, make_response, abort
import os, MySQLdb, time
import utilities

lbs_blueprint = Blueprint('lbs', __name__, template_folder='templates', url_prefix='/lbs')


@lbs_blueprint.route('/charts')
@utilities.test_login
def topcharts(logged_in):
    return render_template('chart_top10.html', logged_in=logged_in)


@lbs_blueprint.route('/tables')
@utilities.test_login
def tables(logged_in):
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    return render_template('tables.html', logged_in=logged_in, badges_catalog=badges_catalog)


@lbs_blueprint.route('/daily')
@utilities.test_login
def daily_lbs(logged_in):
    return render_template('daily_lbs.html', logged_in=logged_in)