from flask import render_template, Blueprint, make_response, abort, request, jsonify
import MySQLdb, time, os
import utilities
from lxml.html.clean import Cleaner

_cleaner = Cleaner(safe_attrs=[
    'abbr', 'accept', 'accept-charset', 'accesskey', 'action', 'align',
    'alt', 'axis', 'border', 'cellpadding', 'cellspacing', 'char', 'charoff',
    'charset', 'checked', 'cite', 'class', 'clear', 'cols', 'colspan',
    'color', 'compact', 'coords', 'datetime', 'dir', 'disabled', 'enctype',
    'for', 'frame', 'headers', 'height', 'href', 'hreflang', 'hspace', 'id',
    'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'media', 'method',
    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 'readonly',
    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'selected', 'shape',
    'size', 'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title',
    'type', 'usemap', 'valign', 'value', 'vspace', 'width', 'style'])  # just adding style as safe attribute

news_blueprint = Blueprint('news', __name__, template_folder='templates', url_prefix='/news')

_coloniae_news_admins = ['Sobeirannovaocc']


@news_blueprint.route('/e/<nid>', methods=['GET'])
@utilities.test_login
def news_tool(logged_in, nid):
    if not logged_in:
        abort(403)
        return
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    # only logged in after this point
    ape_account = logged_in
    # check if coloniae writer
    if not utilities.role_has_access('Article Writer', [k['name'] for k in utilities.get_user_roles(ape_account)]):
        abort(403)
        return
    new = False
    if nid == 0:
        # new blank article
        new = True
        article_global_contents = {'title': 'unnamed article', 'lastupdate': 0, 'hidden': True, 'author': ape_account,
                                   'nid': nid, 'resume': ''}
    else:
        resp = utilities.query_db(
            'select articletitle, articlecontents, unix_timestamp(lastupdate), hidden, articleresume, ape_account from news_articles where newsid=%s',
            (nid,))
        if len(resp) == 0:
            return 'This article does not exist.'
        resp = resp[0]
        if ape_account not in _coloniae_news_admins + [resp[5]]:
            abort(403)
            return
        temp_hidden = True if resp[3] == 1 else False
        article_global_contents = {'title': resp[0], 'contents': resp[1], 'lastupdate': resp[2], 'hidden': temp_hidden,
                                   'author': resp[5], 'nid': nid, 'resume': resp[4]}
    return render_template('news_tool.html', newarticle=new, article_global_contents=article_global_contents,
                           logged_in=ape_account)


@news_blueprint.route('/i/<nid>', methods=['POST'])
@utilities.test_login
def news_upload_image(logged_in, nid):
    if not logged_in:
        payload = {
            'outcome': False,
            'message': 'You are not logged in. To not loose data, log in in another tab and try here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    ape_account = logged_in
    # check if coloniae writer
    if not utilities.role_has_access('Article Writer', [k['name'] for k in utilities.get_user_roles(ape_account)]):
        abort(403)
        return
    try:
        img = request.files['file']
    except KeyError:
        payload = {
            'outcome': False,
            'message': 'There is no file.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if nid == 0:
        payload = {
            'outcome': False,
            'message': 'ID cant be 0.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    img.save(os.path.join(utilities.upload_folder, 'article_banner_{}.jpg'.format(nid)))
    payload = {
        'outcome': True,
        'message': 'Nice.'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@news_blueprint.route('/s/<nid>', methods=['POST'])
@utilities.test_login
def news_save(logged_in, nid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    ape_account = logged_in
    # check if coloniae writer
    if not utilities.role_has_access('Article Writer', [k['name'] for k in utilities.get_user_roles(ape_account)]):
        abort(403)
        return
    try:
        ntitle = request.json['article_title']
        nresume = request.json['article_resume']
        ncontents = request.json['article_contents']
        nhide = request.json['article_hide']
    except KeyError:
        abort(400)
        return
    ncontents = _cleaner.clean_html(ncontents)
    if ncontents[:5] == '<div>' and ncontents[-6:] == '</div>':  # remove the first divs that the cleaner adds
        ncontents = ncontents[5:-6]
    nhide = True if nhide == 1 else False
    if nid == 0:
        try:
            resp = utilities.query_db(
                'insert into news_articles (ape_account, hidden, articletitle, articlecontents, created, '
                'articleresume) values (%s, %s, %s, %s, NOW(), %s)',
                (ape_account, nhide, ntitle, ncontents, nresume), return_lastrowid=True)
            entryid = resp[1]
            payload = {'outcome': 'Article successfully saved', 'nid': entryid, 'ndate': time.time()}
        except MySQLdb.Error as err:
            payload = {'outcome': str(err)}
    else:
        try:
            resp = utilities.query_db('select ape_account from news_articles where newsid=%s', (nid,))
            owner_account = resp[0][0]
            if ape_account not in _coloniae_news_admins + [owner_account]:
                abort(403)
                return
            utilities.query_db(
                'update news_articles set articletitle=%s, articlecontents=%s, hidden=%s, articleresume=%s where newsid=%s',
                (ntitle, ncontents, nhide, nresume, nid))
            payload = {'outcome': 'Article successfully saved', 'nid': nid, 'ndate': time.time()}
        except MySQLdb.Error as err:
            payload = {'outcome': str(err)}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@news_blueprint.route('/p/<pnb>', methods=['GET'])
@utilities.test_login
def news_page(logged_in, pnb):
    # check if lid is integer
    try:
        pnb = int(pnb)
    except ValueError:
        abort(400)
        return
    if pnb < 1:
        abort(400)
        return
    resp = utilities.query_db('select articletitle, articleresume, unix_timestamp(a.created), a.ape_account, '
                              'count(commentcontents), a.newsid, a.viewcount from news_articles as a left join '
                              'news_comments as b on a.newsid=b.newsid where hidden=0 group by a.newsid order by '
                              'a.created desc limit %s', (pnb * 5,))
    articles = []
    for i in range(len(resp)):
        if i < 5 * (pnb - 1):
            continue  # we take starting from article number 6
        ar = resp[i]
        articles.append(
            {'title': ar[0], 'ape_account': ar[3], 'created': ar[2], 'resume': ar[1], 'commentsnb': ar[4],
             'nid': ar[5], 'viewcount': ar[6]})
    return render_template('news_page.html', articles=articles, pagenb=pnb, pagetitle='News - page {}'.format(pnb),
                           logged_in=logged_in)


@news_blueprint.route('/v/<nid>', methods=['GET'])
@utilities.test_login
def news_view(logged_in, nid):
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    resp = utilities.query_db(
        'select articletitle, articlecontents, unix_timestamp(a.created), unix_timestamp(a.lastupdate), a.ape_account, commentcontents,unix_timestamp(b.created),b.ape_account, a.viewcount from news_articles as a left join news_comments as b on a.newsid=b.newsid where a.newsid=%s and hidden=0 order by b.created asc',
        (nid,))
    article_comments = []
    if len(resp) == 0:
        abort(404)
        return
    for i in resp:
        if i[7] is not None:
            article_comments.append({'contents': i[5], 'ape_account': i[7], 'created': i[6]})
    article = {'id': nid, 'title': resp[0][0], 'contents': resp[0][1], 'ape_account': resp[0][4],
               'created': resp[0][2], 'lastupdate': resp[0][3], 'viewcount': resp[0][8],
               'commentsnb': len(article_comments)}
    # update view count
    utilities.query_db('update news_articles set viewcount=viewcount+1, lastupdate=lastupdate where newsid=%s', (nid,))
    return render_template('news_article.html', article_comments=article_comments, article=article, logged_in=logged_in)


@news_blueprint.route('/c/<nid>', methods=['POST'])
@utilities.test_login
def news_comment(logged_in, nid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    # gather the parameters
    try:
        commentcontents = request.json['commentcontents']
    except KeyError:
        abort(400)
        return
    ape_account = logged_in
    utilities.query_db('insert into news_comments (newsid, ape_account, commentcontents) values (%s, %s, %s)',
                       (nid, ape_account, commentcontents))
    payload = {'outcome': 'Comment successfull. Reload the page to see the changes.'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@news_blueprint.route('/u/<nid>', methods=['POST'])
@utilities.test_login
def news_update(logged_in, nid):
    if not logged_in:
        payload = {
            'outcome': 'You are not logged in. To not loose data, log in in another tab and try here again.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    # check if lid is integer
    try:
        nid = int(nid)
    except ValueError:
        abort(400)
        return
    # check if not new
    if nid < 1:
        abort(400)
        return
    ape_account = logged_in
    # check if coloniae writer
    if not utilities.role_has_access('Article Writer', [k['name'] for k in utilities.get_user_roles(ape_account)]):
        abort(403)
        return

    try:
        nevent = request.json['event']
        ndata = request.json['data']
    except KeyError:
        abort(400)
        return

    if nevent == 'publication-date':
        try:
            utilities.query_db('update news_articles set created=NOW() where newsid=%s', (nid,))
            payload = {'outcome': 'Publication date updated'}
        except MySQLdb.Error as err:
            payload = {'outcome': str(err)}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
