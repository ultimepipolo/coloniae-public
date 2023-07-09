from flask import render_template, Blueprint, abort, make_response, jsonify, request, redirect
import os, MySQLdb, json, time, requests
import utilities

perso_blueprint = Blueprint('perso', __name__, template_folder='templates', url_prefix='/perso')


@perso_blueprint.route('/', methods=['GET'])
@utilities.test_login
def perso_index(logged_in):
    if not logged_in:
        abort(403)
        return
    # start real page processing
    ape_account = logged_in
    roles = utilities.get_user_roles(ape_account)
    user_roles = [k['name'] for k in roles]
    articles = []
    # check if is coloniae writer
    if utilities.role_has_access('Article Writer', user_roles):
        resp = utilities.query_db(
            'select articletitle, unix_timestamp(created), unix_timestamp(lastupdate), newsid, hidden from news_articles where ape_account=%s order by created desc',
            (ape_account,))
        articles = [{'title': k[0], 'nid': k[3], 'created': k[1], 'lastupdate': k[2],
                     'hidden': 'Not published' if k[4] == 1 else 'Published'} for k in resp]
    # discord
    resp = utilities.query_db('select userid from discord where ape_account=%s', (ape_account,))
    if len(resp) == 0:
        discordid = 0
    else:
        discordid = resp[0][0]
    # layouts
    resp = utilities.query_db(
        'select layoutid, layoutname, hidden, unix_timestamp(lastupdate) from layouts where ape_account=%s order by lastupdate desc',
        (ape_account,))
    layouts = [{'lid': k[0], 'name': k[1], 'lastupdate': k[3], 'hidden': 'Private' if k[2] == 1 else 'Public'} for k in
               resp]
    # active and inactive colonies
    resp = utilities.query_db('select s1.name, s1.charter, unix_timestamp(s1.time) from colonies_hist as s1 inner '
                              'join (select charter, max(time) rev from colonies_hist where charter in (select charter '
                              'from colonies where ape_account=%s) group by charter) as s2 on '
                              's1.charter=s2.charter and s1.time=s2.rev order by unix_timestamp(s1.time) '
                              'desc', (ape_account,))
    inactive_colonies, active_colonies = [], []
    char_to_name = {}
    curr_epoch = int(time.time())
    for e in resp:
        # determine if active or not
        if curr_epoch - e[2] > 26 * 3600:  # consider inactive
            inactive_colonies.append({'charter': e[1], 'name': e[0], 'datedeleted': e[2]})
            char_to_name[e[1]] = e[0]
        else:
            active_colonies.append({'charter': e[1], 'name': e[0], 'linkedto': None})
            char_to_name[e[1]] = e[0]
    resp2 = utilities.query_db('select newcharter, oldcharter from colonies_links where oldcharter '
                               'in ({})'.format(','.join(['"'+k['charter']+'"' for k in inactive_colonies])))
    old_to_new = {k[1]: k[0] for k in resp2}
    for c in inactive_colonies:
        try:
            c['linkedto'] = {'charter': old_to_new[c['charter']], 'name': char_to_name[old_to_new[c['charter']]]}
        except KeyError:
            c['linkedto'] = None
    return render_template('perso_index.html', layouts=layouts, discordid=discordid,
                           inactive_colonies=inactive_colonies, active_colonies=active_colonies,
                           roles=roles, user_roles=user_roles, articles=articles, logged_in=ape_account)


@perso_blueprint.route('/logout', methods=['GET'])
def logout():
    resp = redirect('https://coloniae.space', code=302)
    resp.set_cookie('sida', '', max_age=0)
    resp.set_cookie('sidb', '', max_age=0)
    return resp


@perso_blueprint.route('/intlogin', methods=['GET'])
def intlogin():
    # RETURNS TO THE URL WITH THE CREDETIALS
    try:
        sida = request.args['sida']
        sidb = request.args['sidb']
        seguiurl = request.args['seguiurl']
    except KeyError:
        abort(400)
        return
    resp = redirect(seguiurl, code=302)
    resp.set_cookie('sida', sida, max_age=3600 * 24 * 15)  # 15 days
    resp.set_cookie('sidb', sidb, max_age=3600 * 24 * 15)
    return resp
