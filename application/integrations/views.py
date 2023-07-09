from flask import render_template, Blueprint, make_response
import os
import utilities
import urllib.request, json,base64, time, datetime

integrations_blueprint = Blueprint('integrations', __name__, template_folder='templates', url_prefix='/integrations')


@integrations_blueprint.route('/discord', methods = ['GET'])
@utilities.test_login
def discord_index(logged_in):
    # start real page processing
    resp = utilities.query_db('select count(distinct serverid) from discord_users where serverid!="583576890565066753"')
    nb_servers = resp[0][0]
    resp = utilities.query_db('select count(distinct userid) from discord')
    nb_registered = resp[0][0]
    lastmodif = os.path.getmtime(os.path.join('application', integrations_blueprint.name, integrations_blueprint.template_folder, 'discord_index.html'))
    return render_template('discord_index.html', logged_in = logged_in, nb_servers=nb_servers, nb_registered=nb_registered, lastmodif=lastmodif)


@integrations_blueprint.route('/translation', methods = ['GET'])
@utilities.test_login
def translation_index(logged_in):
    return render_template('translation_index.html', logged_in = logged_in)


@integrations_blueprint.route('/rss', methods = ['GET'])
def rss_feed():
    resp = utilities.query_db('select newsid, ape_account, articletitle, unix_timestamp(created), articleresume '
                              'from news_articles '
                              'where hidden=0 order by created desc')
    #print(resp[0][3])
    #print(datetime.datetime.fromtimestamp(resp[0][3]).astimezone(datetime.timezone.utc).tzinfo)
    entries = [{'title':k[2],
                'nid':k[0],
                'author':k[1],
                'published':datetime.datetime.fromtimestamp(k[3]),#.astimezone(datetime.timezone.utc),
                'description':k[4]} for k in resp]

    resp = make_response(render_template('rss.xml', entries = entries))
    resp.headers["Content-Type"] = "text/xml; charset=utf-8"
    return resp
