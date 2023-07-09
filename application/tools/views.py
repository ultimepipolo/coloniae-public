from flask import render_template, Blueprint, abort, make_response, jsonify, request, url_for
import os, MySQLdb, json, time, requests
import utilities

tools_blueprint = Blueprint('tools', __name__, template_folder='templates', url_prefix='/tools')


@tools_blueprint.route('/layouts', methods=['GET'])
@utilities.test_login
def layouts_index(logged_in):
    resp = utilities.query_db(
        'select layoutid, layoutname, ape_account, unix_timestamp(lastupdate) from layouts where hidden=0 and layoutname!="unnamed" order by lastupdate desc')
    layouts_list = [{'lid': k[0], 'name': k[1], 'author': k[2], 'date': k[3]} for k in resp]
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    return render_template('layout_index.html', logged_in=logged_in, layouts_list=layouts_list,
                           badges_catalog=badges_catalog)


@tools_blueprint.route('/layouts/c/<lid>', methods=['POST'])
@utilities.test_login
def layouts_copy(logged_in, lid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try saving here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        lid = int(lid)
    except ValueError:
        abort(400)
        return
    # only logged in after this point
    ape_account = logged_in
    resp = utilities.query_db('select ape_account from layouts where layoutid=%s', (lid,))
    if len(resp) != 1:
        abort(400)
        return
    if resp[0][0] == ape_account:
        payload = {'outcome': 'success', 'new_lid': lid}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    try:
        resp = utilities.query_db(
            "insert into layouts (ape_account, hidden, layoutname, layoutdesc, layoutimageurl, layoutspecs, layoutcontents, lastupdate) select %s,%s,layoutname, layoutdesc, layoutimageurl, layoutspecs, layoutcontents,lastupdate  from layouts where layoutid=%s",
            (ape_account, 1, lid), return_lastrowid=True)
        entryid = resp[1]
        payload = {'outcome': 'success', 'new_lid': entryid}
    except MySQLdb.Error as err:
        payload = {'outcome': 'error', 'message': str(err)}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@tools_blueprint.route('/layouts/e/<lid>', methods=['GET'])
@utilities.test_login
def layouts_tool(logged_in, lid):
    # check if lid is integer
    try:
        lid = int(lid)
    except ValueError:
        abort(400)
        return
    # get game version
    with open(utilities.paths['mycolony_version'], 'r') as readfile:
        try:
            mycolony_version = json.load(readfile)['mycolony_version']
        except KeyError:
            abort(400)
            return
    if not logged_in:
        # not logged in
        if lid == 0:
            return 'Authentication is required to create a layout. Please go back an sign in with your Ape Apps account on the top right corner of the screen, then try again.'
        else:
            resp = utilities.query_db(
                'select layoutname, layoutdesc, layoutcontents, unix_timestamp(lastupdate), hidden, ape_account from layouts where layoutid=%s',
                (lid,))
            if len(resp) != 1:
                return 'This layout does not exist.'
            resp = resp[0]
            temp_hidden = True if resp[4] == 1 else False
            layout_global_contents = {'name': resp[0], 'desc': resp[1],
                                      'contents': json.loads(resp[2].replace("'", '"')), 'lastupdate': resp[3],
                                      'hidden': temp_hidden, 'author': resp[5], 'lid': lid}
            return render_template('layout.html', newlayout=False, layout_global_contents=layout_global_contents,
                                   editallowed=False, mycolony_version=mycolony_version, logged_in=logged_in)
    else:
        # only logged in after this point
        ape_account = logged_in
        if lid == 0:
            # new blank layout
            layout_global_contents = {'name': 'unnamed', 'desc': '', 'lastupdate': 0, 'hidden': False,
                                      'author': ape_account, 'lid': lid}
            return render_template('layout.html', newlayout=True, layout_global_contents=layout_global_contents,
                                   editallowed=True, mycolony_version=mycolony_version, logged_in=logged_in)
        else:
            resp = utilities.query_db(
                'select layoutname, layoutdesc, layoutcontents, unix_timestamp(lastupdate), hidden from layouts where ape_account=%s and layoutid=%s',
                (ape_account, lid))
            if len(resp) != 1:
                # layout may exist but not belong to the guy
                resp = utilities.query_db(
                    'select layoutname, layoutdesc, layoutcontents, unix_timestamp(lastupdate), hidden, ape_account from layouts where layoutid=%s',
                    (lid,))
                if len(resp) != 1:
                    return 'This layout does not exist.<br><a href="https://coloniae.space/">Main page</a>'
                resp = resp[0]
                temp_hidden = True if resp[4] == 1 else False
                layout_global_contents = {'name': resp[0], 'desc': resp[1],
                                          'contents': json.loads(resp[2].replace("'", '"')), 'lastupdate': resp[3],
                                          'hidden': temp_hidden, 'author': resp[5], 'lid': lid}
                return render_template('layout.html', newlayout=False, layout_global_contents=layout_global_contents,
                                       editallowed=False, mycolony_version=mycolony_version, logged_in=logged_in)
            resp = resp[0]
            temp_hidden = True if resp[4] == 1 else False
            layout_global_contents = {'name': resp[0], 'desc': resp[1],
                                      'contents': json.loads(resp[2].replace("'", '"')), 'lastupdate': resp[3],
                                      'hidden': temp_hidden, 'author': ape_account, 'lid': lid}
            return render_template('layout.html', newlayout=False, layout_global_contents=layout_global_contents,
                                   editallowed=True, mycolony_version=mycolony_version, logged_in=logged_in)


@tools_blueprint.route('/layouts/s/<lid>', methods=['POST'])
@utilities.test_login
def layouts_save(logged_in, lid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try saving here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        lid = int(lid)
    except ValueError:
        abort(400)
        return
    ape_account = logged_in
    try:
        lname = request.json['layout_name']
        ldesc = request.json['layout_desc']
        lspecs = json.dumps(request.json['layout_specs'])
        lcontents = json.dumps(request.json['layout_contents'])
        lhide = request.json['layout_hide']
        limg = request.json['layout_img']
    except KeyError:
        abort(400)
        return
    lhide = True if lhide == 1 else False
    if lid == 0:
        try:
            resp = utilities.query_db(
                'insert into layouts (layoutname, layoutdesc, layoutspecs, layoutcontents, ape_account, hidden, layoutimageurl) values (%s, %s, %s, %s, %s, %s, %s)',
                (lname, ldesc, lspecs, lcontents, ape_account, lhide, limg), return_lastrowid=True)
            entryid = resp[1]
            payload = {'outcome': 'Layout successfully saved', 'lid': entryid, 'ldate': time.time()}
        except MySQLdb.Error as err:
            payload = {'outcome': str(err)}
    else:
        try:
            utilities.query_db(
                'update layouts set layoutname=%s, layoutdesc=%s, layoutspecs=%s, layoutcontents=%s, hidden=%s, layoutimageurl=%s where layoutid=%s and ape_account=%s',
                (lname, ldesc, lspecs, lcontents, lhide, limg, lid, ape_account))
            payload = {'outcome': 'layout successfully saved', 'lid': lid, 'ldate': time.time()}
        except MySQLdb.Error as err:
            payload = {'outcome': str(err)}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@tools_blueprint.route('/layouts/d/<lid>', methods=['GET'])
@utilities.test_login
def layouts_download(logged_in, lid):
    resp = utilities.query_db('select layoutname, layoutcontents from layouts where layoutid=%s and hidden=0', (lid,))
    if len(resp) != 1:
        if not logged_in:
            return 'Either this layout does not exist or it is set to private. If you are the layout owner, log in and try again.'
        # try to see if it's a private layout owned by the guy
        resp = utilities.query_db('select layoutname, layoutcontents from layouts where layoutid=%s and ape_account=%s',
                                  (lid, logged_in))
    if len(resp) != 1:
        return 'Either this layout does not exist or it is set to private.'
    layoutname = resp[0][0]
    layoutcontents = resp[0][1]
    resp = make_response(jsonify({'layout_name': layoutname, 'layout_contents': layoutcontents}))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@tools_blueprint.route('/layouts/f/<lid>', methods=['GET'])
@utilities.test_login
def layouts_delete(logged_in, lid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        lid = int(lid)
    except ValueError:
        abort(400)
        return
    # gather the parameters
    ape_account = logged_in
    utilities.query_db('delete from layouts where layoutid=%s and ape_account=%s', (lid, ape_account))
    payload = {'outcome': 'Delete successfull. Reload the page to see the changes.'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@tools_blueprint.route('/comparator')
@utilities.test_login
def advcomp(logged_in):
    return render_template('resources_adv_comparator.html', logged_in=logged_in)


@tools_blueprint.route("/market")
@utilities.test_login
def gbt(logged_in):
    # get game version
    with open(utilities.paths['mycolony_version'], 'r') as readfile:
        try:
            mycolony_version = json.load(readfile)['mycolony_version']
        except KeyError:
            abort(400)
            return
    return render_template('gbt.html', logged_in=logged_in, mycolony_version=mycolony_version)


@tools_blueprint.route("/search")
@utilities.test_login
def advanced_search(logged_in):
    resp = utilities.query_db('select distinct race from colonies')
    races = sorted([k[0] for k in resp])
    resp = utilities.query_db('select distinct maptype from colonies')
    maptypes = sorted([k[0] for k in resp])
    resp = utilities.query_db('select distinct civilization from colonies')
    civilizations = sorted([k[0] for k in resp])
    return render_template('advanced_search.html', logged_in=logged_in, races=races, civilizations=civilizations,
                           maptypes=maptypes)


@tools_blueprint.route('/translation/editor', methods=['GET'])
@utilities.test_login
def translation_editor(logged_in):
    abort(404) # they should use dev.coloniae.space instead
    return
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    if role != 1:  # this page is only for translator, not other roles
        abort(403)
        return

    return render_template('translation_editor.html', logged_in=logged_in, language=language, role=role)


@tools_blueprint.route('/translation/proofreading', methods=['GET'])
@utilities.test_login
def translation_proofreading(logged_in):
    abort(404) # they should use dev.coloniae.space instead
    return
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    if role != 2:  # this page is only for proofreaders, not other roles
        abort(403)
        return

    return render_template('translation_proofreading.html', logged_in=logged_in, language=language, role=role)


@tools_blueprint.route('/translation/overview', methods=['GET'])
@utilities.test_login
def translation_overview(logged_in):
    abort(404) # they should use dev.coloniae.space instead
    return
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    return render_template('translation_overview.html', logged_in=logged_in, language=language, role=role)
