from flask import render_template, Blueprint, session
import os, MySQLdb
import utilities

badges_blueprint = Blueprint('badges', __name__, template_folder='templates', url_prefix='/badges')


badges_descs = {'Article Writer': 'These people can write articles for Coloniae News.',
                'Event Planner': '',
                'Founder': 'Just God. Equivalent of having all roles.',
                'Coding Merit': 'Awarded for coding part of or a complete Coloniae feature.',
                'Testing Merit': 'Awarded for testing Coloniae features before release.'}


@badges_blueprint.route('/', methods = ['GET'])
@utilities.test_login
def badges_index(logged_in):
    resp = utilities.query_db('select distinct roledesc, color from users_roles order by roledesc asc')
    roles_list = [{'name': k[0], 'color': k[1]} for k in resp]
    resp = utilities.query_db('select distinct medalname, imageurl from users_medals order by medalname asc')
    medals_list = [{'name': k[0], 'url': k[1]} for k in resp]
    return render_template('badges.html', logged_in=logged_in, roles_list=roles_list, medals_list=medals_list,
                           badges_descs=badges_descs)
