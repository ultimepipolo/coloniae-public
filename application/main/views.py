from flask import render_template, Blueprint
import json
import utilities

main_blueprint = Blueprint('main', __name__, template_folder='templates', url_prefix='/')


@main_blueprint.route('/', methods=['GET'])
@utilities.test_login
def main_index(logged_in):
    # get stable game version
    with open(utilities.paths['mycolony_version'], 'r') as readfile:
        try:
            trf = json.load(readfile)
            mycolony_version = trf['mycolony_stable_version']
            mycolony_beta_version = trf['mycolony_version']
            last_updated = trf['last_updated_epoch']
        except KeyError:
            mycolony_version = False
    # get articles
    resp = utilities.query_db(
        'select articletitle, unix_timestamp(a.created), a.ape_account, count(commentcontents), a.newsid, a.viewcount, articleresume from news_articles as a left join news_comments as b on a.newsid=b.newsid where hidden=0 group by a.newsid order by a.created desc limit 5')
    articles = [
        {'title': ar[0], 'ape_account': ar[2], 'created': ar[1], 'commentsnb': ar[3], 'nid': ar[4], 'viewcount': ar[5],
         'resume': ar[6]}
        for ar in resp]
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {
                'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]),
                'color': i[2]
            }
        )
    # number of trades made last 24 hours
    resp = utilities.query_db(
        'select count(*) from gbt_live where timesold between date_sub(now(), interval 1 day) and now();')
    gbt_trades_nb = resp[0][0]
    return render_template('main_index.html', logged_in=logged_in, articles=articles,
                           mycolony_version=mycolony_version, mycolony_beta_version=mycolony_beta_version,
                           last_updated=last_updated,
                           badges_catalog=badges_catalog, gbt_trades_nb=gbt_trades_nb)


@main_blueprint.route('/about', methods=['GET'])
@utilities.test_login
def about(logged_in):
    return render_template('about.html', logged_in=logged_in)


@main_blueprint.route('/colonies/<charter>')
@utilities.test_login
def colonies(logged_in, charter):
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    # aducol
    resp = utilities.query_db('select charter from adu_identifier where charter=%s limit 1', (charter,))
    if len(resp) == 1:
        aducol = True
    else:
        aducol = False
    # get game version
    with open(utilities.paths['mycolony_version'], 'r') as rf:
        mycolony_version = json.load(rf)['mycolony_version']
    # get name and ape account
    resp = utilities.query_db('select ape_account, name, time, colonyid from colonies as c join colonies_hist as h on '
                              'c.charter=h.charter where c.charter=%s  order by time desc limit 1;', (charter,))
    if len(resp)<1:
        lastsignal = 0
        name = ""
        owner = ""
        colonyid=0
    else:
        lastsignal = resp[0][2]
        name = resp[0][1]
        owner = resp[0][0]
        colonyid = resp[0][3]
    return render_template('colonies.html', charter=charter, logged_in=logged_in, badges_catalog=badges_catalog,
                           aducol=aducol, mycolony_version=mycolony_version, lastsignal=lastsignal,
                           name=name, owner=owner, colonyid=colonyid)


@main_blueprint.route('/player/<username>')
@utilities.test_login
def player(logged_in, username):
    # get discord user
    resp = utilities.query_db(
        'select displayname, name, tag from discord as a join discord_users as b on a.userid=b.userid where ape_account=%s',
        (username,))
    if len(resp) < 1:
        discordname = False
    else:
        if True:  # if resp[0][0] == resp[0][1]:  # if displayname equals name only show name and tag
            discordname = '{}#{}'.format(resp[0][1], resp[0][2])
        else:
            discordname = '{} ({}#{})'.format(resp[0][0], resp[0][1], resp[0][2])
    # get roles
    roles = utilities.get_user_roles(username)
    # get game version
    with open(utilities.paths['mycolony_version'], 'r') as rf:
        mycolony_version = json.load(rf)['mycolony_version']
    return render_template('player.html', username=username, logged_in=logged_in, discordname=discordname,
                           roles=roles, mycolony_version=mycolony_version)
