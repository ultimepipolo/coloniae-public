from flask import render_template, Blueprint, session, request, make_response, abort, current_app
import os, MySQLdb, time, requests, json
import utilities

adu_blueprint = Blueprint('adu', __name__, template_folder='templates', url_prefix='/adu')


def adu_safe_string(s):
    return s.replace(' ', '_').replace('.', '').replace("'", '').replace("-", '_')


def normalize_dict(d, safe=True):
    """Returns dict formatted for insertion in Mysql DB"""
    if safe:
        return {adu_safe_string(k): d[k] for k in d if d[k]}
    else:
        return {k: d[k] for k in d if d[k]}


def old_normalize_dict(ddd):
    """Deletes keys with None value"""
    keystodelete = []
    for key in ddd:
        if ddd[key] == 'NaN':
            ddd[key] = None
        if ddd[key] is None:
            keystodelete.append(key)
    for delkey in keystodelete:
        ddd.pop(delkey, None)
    return ddd


def patched_inserting(ctx, query, args):
    try:
        with ctx.app_context():
            utilities.query_db(query, args)
    except MySQLdb.Error as err:
        print('----\nError inserting in adupost', err)
        print(query)
        print(args)
        print('----')


@adu_blueprint.route('/adupost', methods=['POST', 'OPTIONS'])
def adupost():
    if request.method == 'OPTIONS':
        resp = make_response('this is the response to OPTIONS call.')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers[
            "Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
        return resp
    if request.json['event'] == 'adupost':
        receiveddict = request.json['data']
        try:
            charter = receiveddict['colonyidentifier']['charter']
            name = receiveddict['colonyidentifier']['name']
        except KeyError:
            return 'Error charter or name not present'
        if type(charter) != str:
            return 'Error of charter'
        name = utilities.escapeString(name)
        timeref = receiveddict['timereference']['year'] + (receiveddict['timereference']['period'] / 60)
        treated = {}
        # there are 8 adu tables :
        # X identifier
        # N buildings
        # N resources (amounts + storage)
        # N vehicles
        # O stats
        # N salaries
        # O misc
        # N techs
        # buildings, resources, vehicles, techs and salaries are now json format in the db -> different treatement
        treated['buildings'] = normalize_dict(receiveddict['buildings'])
        treated['vehicles'] = normalize_dict(receiveddict['vehicles'])
        treated['techs'] = receiveddict['techs']
        treated['resources'] = {}
        treated['resources']['amounts'] = normalize_dict(receiveddict['resources']['amounts'])
        treated['resources']['storage'] = normalize_dict(receiveddict['resources']['storage'])
        treated['salaries'] = normalize_dict(receiveddict['misc']['salaries'])
        # old_normalize_dict creates a list of 2 elements list : [["Lander", 1], ["Auntie Bells ...", 5], ...]
        # this is for stats and misc
        receiveddict['stats'] = old_normalize_dict(receiveddict['stats'])
        receiveddict['misc'] = old_normalize_dict(receiveddict['misc'])
        stlist = [[k, receiveddict['stats'][k]] for k in receiveddict['stats']]
        stlistkeys = [k[0] for k in stlist]
        stlistvalues = [str(k[1]) for k in stlist]
        # X (IDENTIFIER) INSERTING
        if receiveddict['colonyidentifier']['subregion']:
            issubregion = '1'
        else:
            issubregion = '0'
        t_query = 'insert into adu_identifier (charter, timereference, name, ape_account, issubregion) values ("' + charter + '", ' + str(
            timeref) + ', "' + name + '", %s, ' + issubregion + ')'
        try:
            resp = utilities.query_db(t_query, (receiveddict['colonyidentifier']['account'],), return_lastrowid=True)
            entryid = str(resp[1])
        except MySQLdb.Error as err:
            print('error in adupost- identifier inserting:', err)
            print('query :', t_query)
            return 'error 1'
        # O (stats) INSERTING
        current_query = 'no current query'
        try:
            if len(stlistkeys) > 0:
                current_query = 'insert into adu_stats (entryid, ' + ', '.join(
                    stlistkeys) + ') values (' + entryid + ', ' + ', '.join(stlistvalues) + ')'
                utilities.query_db(current_query)
        except Exception as err:
            print(time.ctime(), "- adupost, error in sql inserting, query :---", current_query, "--- for", charter, "(",
                  name, ") :", err)
        # O (misc) INSERTING
        if receiveddict['misc']['privateCharter']:
            privatecharter = '1'
        else:
            privatecharter = '0'
        try:
            workerPolicy = receiveddict['misc']['workerPolicy']
        except KeyError:
            workerPolicy = -1
        ctx = current_app._get_current_object()
        patched_inserting(ctx,
                          'insert into adu_misc values (%s, %s, %s, %s, %s ,%s, %s, %s, %s, %s)',
                          (entryid, str(receiveddict['misc']['governmentLevel']), str(receiveddict['misc']['width']),
                          str(receiveddict['misc']['height']), privatecharter, str(workerPolicy),
                          str(receiveddict['misc']['powerusage']), str(receiveddict['misc']['powertotal']),
                          str(receiveddict['misc']['bandwidthusage']), str(receiveddict['misc']['bandwidthtotal'])))
        # N (buildings, vehicles, resources, techs and salaries) INSERTING
        patched_inserting(ctx, 'insert into adu_buildings values (%s, %s)', (entryid, json.dumps(treated['buildings'])))
        patched_inserting(ctx, 'insert into adu_vehicles values (%s, %s)', (entryid, json.dumps(treated['vehicles'])))
        patched_inserting(ctx, 'insert into adu_techs values (%s, %s)', (entryid, json.dumps(treated['techs'])))
        patched_inserting(ctx, 'insert into adu_resources values (%s, %s, %s)',
                           (entryid, json.dumps(treated['resources']['amounts']),
                            json.dumps(treated['resources']['storage'])))
        patched_inserting(ctx, 'insert into adu_salaries values (%s, %s)', (entryid, json.dumps(treated['salaries'])))
        resp = make_response('ok')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    if request.json['event'] == 'regiondeleted':
        receivedname = request.json['name']
        receivedchar = request.json['charter']
        if receivedname != '':
            resp = utilities.query_db('select entryid from adu_identifier where name=%s and charter=%s',
                                      (receivedname, receivedchar))
            entryid_todelete = [str(k[0]) for k in resp]
            print('adupost - from ', receivedname, receivedchar, 'deleting entries : ', entryid_todelete)
            if len(entryid_todelete) < 1:
                print('adupost - no entries : deleting nothing')
            else:
                utilities.query_db('delete from adu_identifier where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_misc where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_buildings where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_vehicles where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_resources where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_stats where entryid in (' + ','.join(entryid_todelete) + ')')
                utilities.query_db('delete from adu_salaries where entryid in (' + ','.join(entryid_todelete) + ')')
            resp = make_response('ok')
        else:
            resp = make_response('Error empty name')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    if request.json['event'] == 'namechanged':
        receivedoldname = request.json['oldname']
        receivednewname = request.json['newname']
        receivedchar = request.json['charter']
        if receivedoldname != '' and receivednewname != '' and receivedchar != '':
            print('adupost - from old name', receivedoldname, 'to new name', receivednewname, 'renaming charter : ',
                  receivedchar)
            utilities.query_db('update adu_identifier set name=%s where name=%s and charter=%s',
                               (receivednewname, receivedoldname, receivedchar))
            resp = make_response('ok')
        else:
            resp = make_response(
                'Error empty arguments :' + receivedoldname + ', ' + receivednewname + ', ' + receivedchar)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return 'Error bad event'


def notNoneList(li):
    """returns False if the list contains only None values"""
    for i in li:
        if i is not None:
            return True
    return False


def separateCities(li, etn, limiter=-1):
    fl = {}
    for i in li:
        if etn[i['entryid']]['name'] not in fl.keys():
            fl[etn[i['entryid']]['name']] = []
        if limiter > -1:
            if len(fl[etn[i['entryid']]['name']]) < limiter:
                fl[etn[i['entryid']]['name']].append(i)
        else:
            fl[etn[i['entryid']]['name']].append(i)
    return normalize_cities_dict(fl)


def normalize_cities_dict(dd):
    nd = {}
    for city in dd:
        nd[city] = []
        for entry in dd[city]:
            nd[city].append(normalize_dict(entry))
    return nd


@adu_blueprint.route('/', methods=['GET', 'POST'])
@utilities.test_login
def adu_index(logged_in):
    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    return render_template('adu_index.html', logged_in=logged_in, badges_catalog=badges_catalog)


@adu_blueprint.route('/<charter>', methods=['GET'])
@utilities.test_login
def adu_view(logged_in, charter):
    resp = utilities.query_db(
        'select b.name, a.timestamp, a.timereference, a.ape_account, b.e from adu_identifier as a inner join (select name, max(entryid) as e from adu_identifier where charter=%s group by name) as b on a.entryid=b.e order by a.timestamp desc;',
        (charter,))
    try:
        owner = resp[0][3]
    except IndexError:
        abort(404)
        return

    if not owner:
        # cant be displayed for some reason (double-attributed charter maybe)
        owner = ''

    cities_list = [{'name': k[0], 'lasttimestamp': k[1].timestamp(), 'lasttimereference': k[2]} for k in resp]
    entries_list = [str(k[4]) for k in resp]
    entries_to_citynb = {resp[i][4]: i for i in range(len(resp))}

    resp = utilities.query_db('select gdp, population, approval, unemployment, entryid from adu_stats where entryid '
                              'in ({}) order by entryid desc'.format(', '.join(entries_list)))
    for row in resp:
        t_citynb = entries_to_citynb[row[4]]
        cities_list[t_citynb]['gdp'] = row[0]
        cities_list[t_citynb]['population'] = row[1]
        cities_list[t_citynb]['approval'] = row[2]
        cities_list[t_citynb]['unemployment'] = row[3]

    if len(cities_list) < 1:
        return 'Colony not registered.'

    # get badges
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    badges_catalog = {}
    for i in resp:
        if i[1] not in badges_catalog.keys():
            badges_catalog[i[1]] = []
        badges_catalog[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    # get colony name
    resp = utilities.query_db('SELECT name FROM colonies_hist a'
                              'INNER JOIN ( SELECT MAX(time) rev FROM colonies_hist where charter=%s ) b ON '
                              'time = b.rev and charter=%s', (charter, charter))
    try:
        name = resp[0][0]
    except IndexError:
        # ask Bast's server
        resp = requests.get(url='https://mc1.my-colony.com/api.php?pf=2&g=1&c=' + charter)
        try:
            name = resp.json()['name']
        except ValueError:
            name = ''

    return render_template('adu.html', charter=charter, cities_list=cities_list, logged_in=logged_in, owner=owner,
                           badges_catalog=badges_catalog, name=name)


def treat_resp(resp, field, attribute):
    if field in ['ra', 'rs', 'bd', 'vh', 'sl']:
        # resp = ((timestamp, json data), (timestamp, {'res 1': amount 1, 'res 2':...}))
        attributes_done = []
        attribute_chart = {}  # {'attribute 1':[[timestamp*1000, amount 1]], ...}
        if attribute == 'All':
            for row in resp:
                d = json.loads(row[1])
                for attr in d:
                    if not attr in attributes_done:
                        attribute_chart[attr] = []
                        attributes_done.append(attr)
                    attribute_chart[attr].append([row[0] * 1000, d[attr]])
        else:
            attribute_chart[attribute] = []
            for row in resp:
                try:
                    d = int(row[1])
                except (TypeError, ValueError):
                    continue
                attribute_chart[attribute].append([row[0] * 1000, d])
        return [{'id': 'series', 'name': attr.replace('_', ' '), 'data': attribute_chart[attr]} for attr in
                attribute_chart]
    elif field in ['st']:
        if attribute == 'All':
            columns = resp[1]
            all_contents = [{columns[index][0]: column for index, column in enumerate(value)} for value in resp[0]]
            ch_contents = []
            # build all building names
            attributeslist = []
            for e in all_contents:  # e is a dict
                for a in e:  # a is a key (attribute)
                    if a not in attributeslist:
                        attributeslist.append(a)
            # then build all series
            for a in attributeslist:
                if a in ['unix_timestamp(timestamp)', 'entryid']: continue
                if notNoneList([k[a] for k in all_contents]):
                    thyu = []
                    for k in all_contents:
                        try:
                            thyu.append([k['unix_timestamp(timestamp)'] * 1000, k[a]])
                        except KeyError:
                            pass
                    # ch_contents.append({ 'id' :'series','name': i,'data': [[timedict[k['Name']][k['Timereference']]*1000, k[i]] for k in all_contents]})
                    ch_contents.append({'id': 'series', 'name': a.replace('_', ' '), 'data': thyu})
            for i in range(len(ch_contents)):
                ch_contents[i]['data'].sort(key=lambda x: x[0])
            return ch_contents
        else:
            attribute = adu_safe_string(attribute)
            ch_contents = [{'id': 'series', 'name': attribute.replace('_', ' '),
                            'data': [[k[0] * 1000, k[1]] for k in resp]}]
            for i in range(len(ch_contents)):
                ch_contents[i]['data'].sort(key=lambda x: x[0])
            return ch_contents
    else:
        return []


@adu_blueprint.route('/<charter>/draw', methods=['GET'])
@utilities.test_login
def adu_draw(logged_in, charter):
    try:
        field = request.args['field']
        attribute = request.args['attribute']
    except KeyError:
        abort(400)
        return
    if field not in ['bd', 'ra', 'rs', 'vh', 'sl', 'st']:
        return 'Invalid request : ' + field
    try:
        name = request.args['name']
    except KeyError:
        name = False
    if field in ['ra', 'rs', 'bd', 'vh', 'sl']:
        query_column = {'bd': 'buildings',
                        'vh': 'vehicles',
                        'ra': 'amounts',
                        'rs': 'storage',
                        'sl': 'salaries'}[field]
        query_table = {'bd': 'adu_buildings',
                       'vh': 'adu_vehicles',
                       'ra': 'adu_resources',
                       'rs': 'adu_resources',
                       'sl': 'adu_salaries'}[field]
        try:
            if name and attribute == 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), {} from {} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s and name=%s order by timestamp asc'.format(
                        query_column, query_table), (charter, name))
            elif name and attribute != 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), {}->"$.{}" from {} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s and name=%s order by timestamp asc'.format(
                        query_column, attribute, query_table), (charter, name))
            elif not name and attribute == 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), {} from {} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s order by timestamp asc'.format(
                        query_column, query_table), (charter,))
            elif not name and attribute != 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), {}->"$.{}" from {} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s order by timestamp asc'.format(
                        query_column, attribute, query_table), (charter,))
            else:
                resp = []
        except MySQLdb.Error as err:
            print(err)
            abort(400)
            return
    elif field in ['st']:
        rn = {'st': 'stats'}[field]
        try:
            if name and attribute == 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), a.* from adu_{} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s and name=%s order by timestamp asc'.format(rn),
                    (charter, name), return_description=True)
            elif name and attribute != 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), a.{} from adu_{} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s and name=%s order by timestamp asc'.format(attribute, rn),
                    (charter, name))
            elif not name and attribute == 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), a.* from adu_{} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s order by timestamp asc'.format(rn),
                    (charter,), return_description=True)
            elif not name and attribute != 'All':
                resp = utilities.query_db(
                    'select unix_timestamp(timestamp), a.{} from adu_{} as a join adu_identifier as b on '
                    'b.entryid=a.entryid where charter=%s order by timestamp asc'.format(attribute, rn),
                    (charter,))
            else:
                resp = []
        except MySQLdb.Error as err:
            print(err)
            abort(400)
            return
    else:
        resp = []
    ch_contents = treat_resp(resp, field, attribute)
    return render_template('adu_chart.html', charter=charter, attribute=attribute, chartseries=ch_contents,
                           logged_in=logged_in)
