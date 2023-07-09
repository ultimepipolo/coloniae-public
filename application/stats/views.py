from flask import render_template, Blueprint, session, abort
import json
import utilities

stats_blueprint = Blueprint('stats', __name__, template_folder='templates', url_prefix='/stats')


@stats_blueprint.route('/game')
@utilities.test_login
def gamestats(logged_in):
    return render_template('game_stats.html', logged_in=logged_in)
    

@stats_blueprint.route('/gbt')
@utilities.test_login
def gbtstats(logged_in):
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    return render_template('gbt_stats.html', logged_in=logged_in, badges_catalog=badges_catalog)


@stats_blueprint.route('/adu')
@utilities.test_login
def adustats(logged_in):
    # get game version
    with open(utilities.paths['mycolony_version'], 'r') as readfile:
        try:
            mycolony_version = json.load(readfile)['mycolony_version']
        except KeyError:
            abort(400)
            return
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    return render_template('adu_stats.html', logged_in=logged_in, mycolony_version=mycolony_version, badges_catalog=badges_catalog)


@stats_blueprint.route('/prices')
@utilities.test_login
def prices(logged_in):
    return render_template('prices_history.html', logged_in=logged_in)