from flask import Blueprint, session, abort, make_response, jsonify, request
import os, MySQLdb, json, time
import utilities

api_blueprint = Blueprint('api', __name__, template_folder='templates', url_prefix='/api')


# ----------------------------- STATS -----------------------------
@api_blueprint.route('/changelogs/<ver>', methods=['GET'])
def changelogs(ver):
    if ver == '1.0.0':
        oldversion = '0.99.0'
    elif ver[0] == '1':
        oldversion = '1.{}.0'.format(int(ver.split('.')[1]) - 1)
    else:
        oldversion = '0.{}.0'.format(int(ver.split('.')[1]) - 1)
    try:
        with open(os.path.join(utilities.gameversionspath, '{}.json'.format(oldversion)), 'r') as oldfile:
            old = json.load(oldfile)
    except FileNotFoundError:
        payload = {'outcome': 'error', 'data': 'game version unavailable'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    try:
        with open(os.path.join(utilities.gameversionspath, '{}.json'.format(ver)), 'r') as newfile:
            new = json.load(newfile)
    except FileNotFoundError:
        payload = {'outcome': 'error', 'data': 'game version unavailable'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    payload = {'outcome': 'success', 'data': utilities.compare_game_versions(old, new)}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/adustats', methods=['GET'])
def adustats():
    try:
        command = request.args['command']
    except KeyError:
        abort(400)
        return

    if command == 'adu-power':
        abort(410)  # gone
        return
        try:
            resp = utilities.query_db('select t2.charter, t1.Powertotal, t1.Powerusage from adu_misc as t1 right  '
                                      'outer join (select charter, max(entryid) as m from adu_identifier group by '
                                      'charter) as t2 on t1.entryid=t2.m where t1.Powertotal>3 group by t2.charter')
        except MySQLdb.Error as err:
            print('error in adu-salaries api', err)
            abort(500)
            return
        payload = []
        for k in resp:
            if k[1] is not None and k[2] is not None:
                payload.append({'Charter': k[0], 'y': {'Power total': float(k[1]), 'Power usage': float(k[2])}})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'adu-bandwidth':
        abort(410)  # gone
        return
        try:
            resp = utilities.query_db('select t2.charter, t1.Bandwidthtotal, t1.Bandwidthusage from adu_misc as t1 '
                                      'right  outer join (select charter, max(entryid) as m from adu_identifier group '
                                      'by charter) as t2 on t1.entryid=t2.m where t1.Bandwidthtotal>3 group by '
                                      't2.charter')
        except MySQLdb.Error as err:
            print('error in adu-salaries api', err)
            abort(500)
            return
        payload = []
        for k in resp:
            if k[1] is not None and k[2] is not None:
                payload.append({'Charter': k[0], 'y': {'Bandwidth total': float(k[1]), 'Bandwidth usage': float(k[2])}})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'adu-salaries':
        abort(410)  # gone
        return
        # try:
        #     resp = utilities.query_db('select t2.charter, avg(t1.Blue_Collar), avg(t1.Botanist), avg(t1.Teacher), avg(t1.Scientist), avg(t1.Medic), avg(t1.White_Collar), avg(t1.Politician), avg(t1.Diplomat), avg(t1.Arbiter), avg(t1.Brewmaster), avg(t1.Unskilled) from adu_salaries as t1 right  outer join (select charter, max(entryid) as m from adu_identifier group by name) as t2 on t1.entryid=t2.m group by t2.charter')
        # except MySQLdb.Error as err:
        #     print('error in adu-salaries api', err)
        # payload = []
        # for k in resp:
        #     t_c = {}
        #     if utilities.notNoneList(k[1:]):
        #         for i in range(1, 12):
        #             try:
        #                 t_c[utilities.professions_list[i - 1]] = float(k[i])
        #             except TypeError:
        #                 t_c[utilities.professions_list[i - 1]] = k[i]
        #     payload.append({'Charter': k[0], 'y': t_c})
        # resp = make_response(jsonify(payload))
        # resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        # return resp
    if command == 'adu-govlevels':
        abort(410)  # gone
        return
        # resp = utilities.query_db(
        #     'select t3.n, count(t3.n) from (select t2.charter as c, max(t1.Govlevel) as n from adu_misc as t1 right  outer join (select charter, max(entryid) as m from adu_identifier group by name) as t2 on t1.entryid=t2.m group by t2.charter) as t3 group by t3.n')
        # payload = [{'name': 'Level ' + str(k[0]), 'y': k[1]} for k in resp]
        # resp = make_response(jsonify(payload))
        # resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        # return resp
    if command == 'adunbcolonies':
        resp = utilities.query_db('select count(distinct charter) from adu_identifier')
        payload = {'adunbcolonies': resp[0][0]}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    try:
        charter = request.args['charter']
    except KeyError:
        abort(400)
        return
    if command == 'adu-reslead':
        abort(410)  # gone
        return
        if charter not in ['Water', 'Food', 'Sugar', 'Money', 'Painting', 'Wood', 'Ant Paste', 'Wool', 'Regolith',
                           'Pottery', 'Water', 'Bricks', 'Charcoal', 'Cloth', 'Wheel', 'Ore', 'Rum', 'Steel', 'Toy',
                           'Antanium', 'Helium 3', 'Aluminum', 'Gold', 'Oil', 'Diamond', 'Uranium', 'Crystalline',
                           'Microchip', 'Plastic', 'Robot', 'Alien Relic', 'Alien Artifact', 'Obsidian',
                           'Ancient Instructions', 'Triantanium', 'Starship', 'Ether', 'Civics', 'Research', 'Antaura',
                           'Atmosphere', 'Trash', 'Fish', 'Software', 'Salt Water', 'Cobalt', 'Nanite']:
            payload = {'error': 'Invalid argument.'}
        else:
            charter = charter.replace(' ', '_').replace('.', '').replace("'", '').replace("-", '_')
            try:
                resp = utilities.query_db('select t2.charter, t1.{} from adu_resamounts as t1 right '
                                          'outer join ( select charter, max(entryid) as m from '
                                          'adu_identifier group by charter) as '
                                          't2 on t1.entryid=t2.m where t1.{}>0 order by t1.{} desc'
                                          .format(charter, charter, charter))
            except MySQLdb.Error as err:
                print('error in adu-reslead api', err)
                abort(500)
                return
            f_char_list = ['"' + k[0] + '"' for k in resp]
            # get their names and owners
            resp2 = utilities.query_db('select a.*, b.ape_account from (select s1.name, s1.charter from colonies_hist '
                                       'as s1 left join colonies_hist as s2 on s1.charter=s2.charter and '
                                       's1.time<s2.time where s1.charter in ({}) and s2.charter is NULL) as a left '
                                       'join colonies as b on a.charter=b.charter;'.format(','.join(f_char_list)))
            char_to_attribs = {k[1]: (k[0], k[2]) for k in resp2}
            payload = []
            for k in resp:
                payload.append({
                    'Charter': k[0],
                    'y': k[1],
                    'name': char_to_attribs.get(k[0], [None, None])[0],
                    'ape_account': char_to_attribs.get(k[0], [None, None])[1]})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    abort(400)
    return


@api_blueprint.route('/gbtstats', methods=['GET'])
def gbtstats():
    try:
        command = request.args['command']
    except KeyError:
        abort(400)
        return
    try:
        bs = request.args['bs']
    except KeyError:
        bs = None

    if command == 'leg-soldday':
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, count(*) '
                                  'from gbt_sold group by ddd order by ddd asc;')
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, count(*) from gbt_sold group by ddd order by ddd asc')
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-volumeday':
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, sum(quantity) '
                                  'from gbt_sold group by ddd order by ddd asc;')
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, sum(quantity) from gbt_sold group by ddd order by ddd'
        #                           ' asc')
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-avgquantity':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, avg(quantity) '
                                  'from gbt_sold where offerflag=%s '
                                  'group by ddd order by ddd asc', (offerflag,))
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, avg(quantity) from gbt_sold where offerflag=%s'
        #                           ' group by ddd order by ddd asc', (offerflag,))
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-avgprice':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return

        resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
                                  ')-utc_time)) hour))) as ddd, avg(price) from gbt_sold where offerflag=%s'
                                  ' group by ddd order by ddd asc', (offerflag,))
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, avg(price) from gbt_sold where offerflag = %s group by ddd order by ddd '
        #                           'asc', (offerflag,))
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-quantities2019':
        resp = utilities.query_db('select sum(quantity), resource from gbt_sold where timesold between "2019-01-01" '
                                  'and "2020-01-01" group by resource order by sum(quantity) desc')
        payload = [{'name': k[1], 'y': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-quantities2020':
        resp = utilities.query_db('select sum(quantity), resource from gbt_sold where timesold between "2020-01-01" '
                                  'and "2021-01-01" group by resource order by sum(quantity) desc')
        payload = [{'name': k[1], 'y': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-quantitiesyesterday':
        resp = utilities.query_db('select sum(quantity), resource from gbt_sold where timesold between date_sub(date('
                                  'now()), interval 1 day) and date(now()) group by resource order by sum(quantity) '
                                  'desc')
        payload = [{'name': k[1], 'y': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-sellers2019':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select sum(price), sum(quantity), sellercharter from gbt_sold where timesold '
                                  'between "2019-01-01" and "2020-01-01" and offerflag=%s group by sellercharter order by sum('
                                  'quantity) desc', (offerflag,))
        payload = [{'charter': k[2], 'quantity': int(k[1]), 'price': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-sellers2020':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select sum(price), sum(quantity), sellercharter from gbt_sold where timesold between '
                                  '"2020-01-01" and "2021-01-01" and offerflag=%s group by sellercharter order by sum(quantity) desc',
                                  (offerflag,))
        payload = [{'charter': k[2], 'quantity': int(k[1]), 'price': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'leg-sellersyesterday':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select sum(price), sum(quantity), sellercharter from gbt_sold where timesold '
                                  'between date_sub(date(now()),interval 1 day) and date(now()) and offerflag=%s group by '
                                  'sellercharter order by sum(quantity) desc', (offerflag,))
        payload = [{'charter': k[2], 'quantity': int(k[1]), 'price': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    if command == 'soldday':
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, count(*) '
                                  'from gbt_live group by ddd order by ddd asc;')
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval '
        #                           '(select hour(time(now())-utc_time())) hour))) as ddd, count(*) '
        #                           'from gbt_live group by ddd order by ddd asc;')
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'volumeday':
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, sum(quantity) '
                                  'from gbt_live group by ddd order by ddd asc;')
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, sum(quantity) from gbt_live group by ddd order by ddd'
        #                           ' asc') (not working)
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'avgquantity':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, avg(quantity) '
                                  'from gbt_live where offerflag=%s group by ddd order by ddd asc;', (offerflag,))
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, avg(quantity) from gbt_live where offerflag=%s'
        #                           ' group by ddd order by ddd asc', (offerflag,)) (not working)
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'avgprice':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return

        resp = utilities.query_db('select unix_timestamp(date(timesold)) as ddd, avg(price) '
                                  'from gbt_live where offerflag=%s group by ddd order by ddd asc;', (offerflag,))
        # resp = utilities.query_db('select unix_timestamp(date(date_sub(timesold, interval (select hour(now('
        #                           ')-utc_time)) hour))) as ddd, avg(price) from gbt_live where offerflag = %s group '
        #                           'by ddd order by ddd '
        #                           'asc', (offerflag,))
        payload = []
        for k in resp:
            try:
                payload.append([k[0] * 1000, int(k[1])])
            except TypeError:
                pass
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'quantitiesyesterday':
        resp = utilities.query_db('select sum(quantity), resourceid from gbt_live where timesold between date_sub(date('
                                  'now()), interval 1 day) and date(now()) group by resourceid order by sum(quantity) '
                                  'desc')
        payload = [{'resourceid': k[1], 'y': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'quantitiesalltime':
        resp = utilities.query_db('select sum(quantity), resourceid from gbt_live group by resourceid order by sum('
                                  'quantity) desc')
        payload = [{'resourceid': k[1], 'y': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'sellersyesterday':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select sum(price), sum(quantity), sellercharter from gbt_live where timesold '
                                  'between date_sub(date(now()),interval 1 day) and date(now()) and offerflag=%s group by '
                                  'sellercharter order by sum(quantity) desc', (offerflag,))
        payload = [{'charter': k[2], 'quantity': int(k[1]), 'price': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'sellers2020':
        if bs == 'rb':
            offerflag = 0
        elif bs == 'rs':
            offerflag = 1
        else:
            abort(400)
            return
        resp = utilities.query_db('select sum(price), sum(quantity), sellercharter from gbt_live where timesold between '
                                  '"2020-01-01" and "2021-01-01" and offerflag=%s group by sellercharter order by sum(quantity) desc',
                                  (offerflag,))
        payload = [{'charter': k[2], 'quantity': int(k[1]), 'price': int(k[0])} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    abort(400)
    return


@api_blueprint.route('/gamestats', methods=['GET'])
def gamestats():
    try:
        command = request.args['command']
    except KeyError:
        abort(400)
        return

    if command == 'gdpsum':
        resp = utilities.query_db('select unix_timestamp(time) as d,sum(gdp) from colonies_hist group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'gdpavg':
        resp = utilities.query_db('select unix_timestamp(time) as d,avg(gdp) from colonies_hist group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'populationsum':
        resp = utilities.query_db('select unix_timestamp(time) as d,sum(population) from colonies_hist group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'populationavg':
        resp = utilities.query_db('select unix_timestamp(date(time)) as d,avg(population) from colonies_hist group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'ownersnb':
        resp = utilities.query_db('select unix_timestamp(date(time)) as d,count(distinct ape_account) from colonies_hist as h '
                                  'join colonies as c on c.charter=h.charter group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'coloniesnb':
        resp = utilities.query_db('select unix_timestamp(date(time)) as d,count(*) from colonies_hist  group by d order by d')
        payload = [[k[0] * 1000, int(k[1])] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'capitol':
        try:
            resp = utilities.query_db('select unix_timestamp(a.t),a.nb,b.nb from (select date(time) as t,count(capitol) '
                                      'as nb from colonies_hist where capitol=1 group by t) as a join (select '
                                      'date(time) as t, count(capitol) as nb from colonies_hist where capitol=0 group by '
                                      't) as b where b.t=a.t')
        except MySQLdb.Error as err:
            print('error in capitol api', err)
            payload = {'error': 'error in api'}
        else:
            payload = {'yes': [], 'no': []}
            for k in resp:
                payload['yes'].append([k[0] * 1000, k[1]])
                payload['no'].append([k[0] * 1000, k[2]])
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    try:
        charter = request.args['charter']
    except KeyError:
        abort(400)
        return

    if command == 'regions':
        if len(charter) != 10:
            payload = {'error': 'Invalid argument.'}
        if not 1531180799 < utilities.tsFromReadable(charter) < time.time():
            payload = {'error': 'Data doesnt exist for this date. Data exists from 10 July 2018.'}
        else:
            try:
                resp = utilities.query_db('select c.region, count(c.region) from colonies as c right join '
                                          'colonies_hist as h on h.charter=c.charter where date(time)=%s group by '
                                          'c.region order by count(c.region) asc',
                                          (charter,))
            except MySQLdb.Error as err:
                print('error in maptypes api', err)
                payload = {'error': 'error in api'}
            else:
                payload = []
                for k in resp:
                    if k[0] == 0:
                        payload.append({'name': 'No', 'y': k[1]})
                    if k[0] == 1:
                        payload.append({'name': 'Yes', 'y': k[1]})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'civilizations':
        if len(charter) != 10:
            payload = {'error': 'Invalid argument.'}
        if not 1531180799 < utilities.tsFromReadable(charter) < time.time():
            payload = {'error': 'Data doesnt exist for this date. Data exists from 10 July 2018.'}
        else:
            try:
                resp = utilities.query_db('select c.civilization, count(c.civilization) from colonies as c right join '
                                          'colonies_hist as h on h.charter=c.charter where date(time)=%s group by '
                                          'c.civilization order by count(c.civilization) asc',
                                          (charter,))
            except MySQLdb.Error as err:
                print('error in maptypes api', err)
                payload = {'error': 'error in api'}
            else:
                payload = [{'name': k[0], 'y': k[1]} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'maptypes':
        if len(charter) != 10:
            payload = {'error': 'Invalid argument.'}
        if not 1531180799 < utilities.tsFromReadable(charter) < time.time():
            payload = {'error': 'Data doesnt exist for this date. Data exists from 10 July 2018.'}
        else:
            try:
                resp = utilities.query_db('select c.maptype, count(c.maptype) from colonies as c right join '
                                          'colonies_hist as h on h.charter=c.charter where date(time)=%s group by '
                                          'c.maptype order by count(c.maptype) asc',
                                          (charter,))
            except MySQLdb.Error as err:
                print('error in maptypes api', err)
                payload = {'error': 'error in api'}
            else:
                payload = [{'name': k[0], 'y': k[1]} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'platform':
        if len(charter) != 10:
            payload = {'error': 'Invalid argument.'}
        if not 1531180799 < utilities.tsFromReadable(charter) < time.time():
            payload = {'error': 'Data doesnt exist for this date. Data exists from 10 July 2018.'}
        else:
            try:
                resp = utilities.query_db('select c.playson, count(c.playson) from colonies as c right join '
                                          'colonies_hist as h on h.charter=c.charter where date(time)=%s group by '
                                          'c.playson order by count(c.maptype) asc',
                                          (charter,))
            except MySQLdb.Error as err:
                print('error in platform api', err)
                payload = {'error': 'error in api'}
            else:
                payload = [{'name': k[0], 'y': k[1]} for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if command == 'platformg':
        if len(charter) != 10:
            payload = {'error': 'Invalid argument.'}
        if not 1531180799 < utilities.tsFromReadable(charter) < time.time():
            payload = {'error': 'Data doesnt exist for this date. Data exists from 10 July 2018.'}
        else:
            try:
                resp = utilities.query_db('select c.playson, count(c.playson) from colonies as c right join '
                                          'colonies_hist as h on h.charter=c.charter where date(time)=%s group by '
                                          'c.playson order by count(c.maptype) asc',
                                          (charter,))
            except MySQLdb.Error as err:
                print('error in platformg api', err)
                payload = {'error': 'error in api'}
            else:
                payload = []
                for k in resp:
                    splited = k[0].split('.')
                    found = False
                    for i in range(len(payload)):
                        if payload[i]['name'] == splited[0]:
                            found = True
                            payload[i]['y'] += k[1]
                    if not found:
                        payload.append({'name': splited[0], 'y': k[1]})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp

    abort(400)
    return


# ----------------------------- MAIN -----------------------------
@api_blueprint.route('/badges', methods=['GET'])
def badges():
    resp = utilities.query_db('select roledesc, ape_account, color from users_roles')
    payload = {}
    for i in resp:
        if i[1] not in payload.keys():
            payload[i[1]] = []
        payload[i[1]].append(
            {'badgename': ''.join([k[0] for k in i[0].split(' ') if k[0].isupper()]), 'color': i[2]})
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/activecwmembers/<charter>', methods=['GET'])
def activecwmembers(charter):
    resp = utilities.query_db('select activechars.charter, h.name, h.population, h.gdp, c.ape_account, c.mother_charter,o.ape_account, gdpcount from colonies as c inner join (select charter, max(time) as t, count(distinct gdp) as gdpcount from colonies_hist where time between DATE_SUB(date(now()), INTERVAL 7 DAY) and DATE_ADD(date(now()), INTERVAL 1 DAY) and capitol=0 group by charter having count(distinct gdp)>3) as activechars on activechars.charter =c.charter inner join colonies as o on c.mother_charter=o.charter inner join colonies_hist as h on activechars.charter=h.charter and activechars.t=h.time where c.ape_account<>o.ape_account and c.mother_charter=%s order by h.population desc;', (charter,))
    payload = [{'child_charter': k[0], 'child_name': k[1], 'child_population': k[2], 'child_gdp': k[3],
                'child_owner': k[4], 'child_timesactive': k[7] - 1, 'mother_charter': k[5], 'mother_owner': k[6]}
               for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/colonyinfo/<charter>', methods=['GET'])
def colonyinfo(charter):
    # see recursively if there is a linked colony
    linked_colony = True
    linked_colonies = [charter]
    n = 0  # safe breaker
    while linked_colony:
        n += 1
        if n == 10:
            abort(500)
            return
        resp = utilities.query_db('select oldcharter from colonies_links where newcharter=%s', (linked_colonies[-1],))
        if len(resp) == 1:
            linked_colonies.append(resp[0][0])
        else:
            linked_colony = False
    resp = utilities.query_db(
        "select unix_timestamp(time),population,cw_size,gdp,charter,name from colonies_hist where charter "
        "in ({}) order by time".format(','.join(['"' + char + '"' for char in linked_colonies])))
    res = resp
    payload = {'pop': [], 'cw_size': [], 'gdp': []}
    for d in res:
        cd = d[0] * 1000
        payload['pop'].append({'name': d[5] + ' (' + d[4] + ')', 'x': cd, 'y': d[1]})
        payload['gdp'].append({'name': d[5] + ' (' + d[4] + ')', 'x': cd, 'y': d[3]})
        payload['cw_size'].append({'name': d[5] + ' (' + d[4] + ')', 'x': cd, 'y': d[2]})
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/playerinfo/<username>', methods=['GET'])
def playerinfo(username):
    # get colonies
    resp = utilities.query_db(
        "select c.charter, unix_timestamp(max(a.timestamp)) as ttt, c.colonyid from colonies as c left join "
        "adu_identifier as a on a.charter=c.charter where c.ape_account=%s group by c.charter",
        (username,))
    char_to_adudata = {k[0]: {'Last active ADU': k[1], 'cid': k[2]} for k in resp}
    if len(char_to_adudata.keys()) < 1:
        resp = make_response(jsonify({'infocols': []}))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    resp2 = utilities.query_db('select s1.name, s1.charter, unix_timestamp(s1.time) from colonies_hist as s1 left '
                               'join colonies_hist as s2 on s1.charter=s2.charter and s1.time<s2.time where '
                               's1.charter in ({}) and s2.charter is NULL order by unix_timestamp(s1.time) '
                               'desc;'.format(','.join(['%s'] * len(char_to_adudata.keys()))),
                               tuple(char_to_adudata.keys()))
    inactive, adu_active, all_active = [], [], []
    curr_epoch = int(time.time())
    # order contents that way :
    # 1.active adu colonies by date of last played
    # 2.active non-adu colonies by name
    # 3.inactive colonies by date of last played regardless of adu
    for e in resp2:
        # determine if active or not
        if curr_epoch - e[2] > 26 * 3600:  # consider inactive
            inactive.append({'Charter': e[1], 'Name': e[0], 'Last active server': e[2],
                             'Last active adu': char_to_adudata[e[1]]['Last active ADU'],
                             'cid': char_to_adudata[e[1]]['cid']})
        else:
            if char_to_adudata[e[1]]['Last active ADU'] is None:
                all_active.append({'Charter': e[1], 'Name': e[0], 'Last active server': e[2],
                                   'Last active adu': None, 'cid': None})
            else:
                adu_active.append({'Charter': e[1], 'Name': e[0], 'Last active server': e[2],
                                   'Last active adu': char_to_adudata[e[1]]['Last active ADU'],
                                   'cid': char_to_adudata[e[1]]['cid']})
    adu_active.sort(key=lambda x: x['Last active adu'], reverse=True)
    all_active.sort(key=lambda x: x['Name'])
    infocols = adu_active + all_active + inactive
    resp = make_response(jsonify({'infocols': infocols}))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/playertrades/<username>/<typee>', methods=['GET'])
def playertrades(username, typee):
    try:
        draw = int(request.args['draw'])
        length = int(request.args['length'])
        offset = int(request.args['start'])
        ordercol = int(request.args['order[0][column]'])
        orderdir = request.args['order[0][dir]']
    except:
        abort(400)
        return
    if ordercol == 1:
        ordercol = 'GOT'
    elif ordercol == 4:
        ordercol = 'IEO'
    else:
        ordercol = 'a.timesold'
    if orderdir not in ['asc', 'desc']:
        orderdir = 'desc'
    if typee == 'bought':
        # get bought trades
        resp = utilities.query_db("select a.resourceid, IF(a.offerflag=1, a.price, a.quantity) as GOT, "
                                  "IF(a.offerflag=1,a.quantity, a.price) as IEO, unix_timestamp(a.timesold), "
                                  "a.sellercharter, a.buyercharter,a.offerflag from gbt_live as a join colonies as b "
                                  "on a.buyercharter=b.charter  where b.ape_account=%s order by {} {} limit "
                                  "%s offset %s".format(ordercol, orderdir), (username, length, offset))
        bought_trades = [{
            'resourceid': k[0],
            'got': k[1],
            'ieo': k[2],
            'timesold': k[3],
            'seller': k[4],
            'buyer': k[5],
            'offerflag': k[6]
        } for k in resp]
        resp = utilities.query_db("select count(distinct idtrade) from gbt_live as a join colonies as b "
                                  "on a.buyercharter=b.charter  where b.ape_account=%s", (username,))
        payload = {'data': bought_trades, 'recordsFiltered': resp[0][0], 'draw': draw, 'recordsTotal': resp[0][0]}
    elif typee == 'sold':
        # get sold trades
        resp = utilities.query_db("select a.resourceid, IF(a.offerflag=1, a.price, a.quantity) as GOT, "
                                  "IF(a.offerflag=1, a.quantity, a.price) as IEO, unix_timestamp(a.timesold), "
                                  "a.sellercharter,a.buyercharter,a.offerflag from gbt_live as a join colonies as b on "
                                  "a.sellercharter=b.charter where b.ape_account=%s order by {} {} limit %s "
                                  "offset %s;".format(ordercol, orderdir), (username, length, offset))
        sold_trades = [{
            'resourceid': k[0],
            'got': k[1],
            'ieo': k[2],
            'timesold': k[3],
            'seller': k[4],
            'buyer': k[5],
            'offerflag': k[6]
        } for k in resp]
        resp = utilities.query_db("select count(distinct idtrade) from gbt_live as a join colonies as b "
                                  "on a.sellercharter=b.charter where b.ape_account=%s", (username,))
        payload = {'data': sold_trades, 'recordsFiltered': resp[0][0], 'draw': draw, 'recordsTotal': resp[0][0]}
    else:
        payload = {'error': 'Bought or sold? not specified'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/chartertrades/<charter>/<typee>', methods=['GET'])
def chartertrades(charter, typee):
    try:
        draw = int(request.args['draw'])
        length = int(request.args['length'])
        offset = int(request.args['start'])
        ordercol = int(request.args['order[0][column]'])
        orderdir = request.args['order[0][dir]']
    except:
        abort(400)
        return
    if orderdir not in ['asc', 'desc']:
        orderdir = 'desc'
    if typee == 'bought':
        if ordercol == 0:
            ordercol = 'GOT'
        elif ordercol == 3:
            ordercol = 'IEO'
        else:
            ordercol = 'timesold'
        # get bought trades
        resp = utilities.query_db("select resourceid, IF(offerflag=1, price, quantity) as GOT, "
                                  "IF(offerflag=1,quantity, price) as IEO, unix_timestamp(timesold), "
                                  "sellercharter, offerflag from gbt_live where buyercharter=%s order by "
                                  "{} {} limit %s offset %s".format(ordercol, orderdir), (charter, length, offset))
        bought_trades = [{
            'resourceid': k[0],
            'got': k[1],
            'ieo': k[2],
            'timesold': k[3],
            'seller': k[4],
            'offerflag': k[5]
        } for k in resp]
        resp = utilities.query_db("select count(distinct idtrade) from gbt_live where buyercharter=%s", (charter,))
        payload = {'data': bought_trades, 'recordsFiltered': resp[0][0], 'draw': draw, 'recordsTotal': resp[0][0]}
    elif typee == 'sold':
        if ordercol == 1:
            ordercol = 'GOT'
        elif ordercol == 3:
            ordercol = 'IEO'
        else:
            ordercol = 'timesold'
        # get sold trades
        resp = utilities.query_db("select resourceid, IF(offerflag=1, price, quantity) as GOT, "
                                  "IF(offerflag=1, quantity, price) as IEO, unix_timestamp(timesold), "
                                  "buyercharter, offerflag from gbt_live where sellercharter=%s order "
                                  "by {} {} limit %s offset %s;".format(ordercol, orderdir), (charter, length, offset))
        sold_trades = [{
            'resourceid': k[0],
            'got': k[1],
            'ieo': k[2],
            'timesold': k[3],
            'buyer': k[4],
            'offerflag': k[5]
        } for k in resp]
        resp = utilities.query_db("select count(distinct idtrade) from gbt_live where sellercharter=%s", (charter,))
        payload = {'data': sold_trades, 'recordsFiltered': resp[0][0], 'draw': draw, 'recordsTotal': resp[0][0]}
    else:
        payload = {'error': 'Bought or sold? not specified'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/naminghistory/<charter>', methods=['GET'])
def naminghistory(charter):
    # see recursively if there is a linked colony
    linked_colony = True
    linked_colonies = [charter]
    n = 0  # safe breaker
    while linked_colony:
        n += 1
        if n == 10:
            abort(500)
            return
        resp = utilities.query_db('select oldcharter from colonies_links where newcharter=%s', (linked_colonies[-1],))
        if len(resp) == 1:
            linked_colonies.append(resp[0][0])
        else:
            linked_colony = False
    resp = utilities.query_db('select name,unix_timestamp(time),charter from colonies_hist where charter in ({}) '
                              'order by time asc'.format(','.join(['%s' for char in linked_colonies])),
                              tuple(linked_colonies))
    try:
        payload = [{'name': resp[0][0], 'from': resp[0][1], 'to': None, 'charter': resp[0][2]}]
    except IndexError:
        payload = [{'name': '', 'from': 0, 'to': None, 'charter': ''}]
    p = 0  # this is the index of the payload we need to determine the end date ('to')
    for i in range(1, len(resp)):
        if (resp[i][0] != payload[p]['name']) or (resp[i][2] != payload[p]['charter']):
            # this row has a different name OR CHARTER, we take the day before to end the current set
            payload[p]['to'] = resp[i - 1][1]
            payload.append({'name': resp[i][0], 'from': resp[i][1], 'to': None, 'charter': resp[i][2]})
            p += 1
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/cfcid', methods=['GET'])
def charter_from_colonyid():
    try:
        cid = request.args['cid']
    except KeyError:
        abort(400)
        return
    try:
        cid = int(cid)
    except:
        abort(400)
        return
    resp = utilities.query_db("select h.charter, name, ape_account from colonies_hist as h join colonies as c on "
                              "h.charter=c.charter where c.colonyid=%s order by time desc limit 1;",
                              (cid,))
    if len(resp) != 1:
        payload = {'result': False}
    else:
        payload = {'charter': resp[0][0], 'name': resp[0][1], 'ape_account': resp[0][2], 'result': True}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/linkcolonies', methods=['POST'])
@utilities.test_login
def linkcolonies(logged_in):
    if not logged_in:
        abort(401)
        return
    try:
        linkfrom = request.json['linkfrom']
        linkto = request.json['linkto']
    except KeyError:
        abort(400)
        return
    # see if authorized to modify
    resp = utilities.query_db('select charter from colonies where ape_account=%s', (logged_in,))
    authorized_charters = [k[0] for k in resp]
    if (linkfrom not in authorized_charters) or (linkto not in authorized_charters):
        abort(403)
        return
    # actually process
    try:
        utilities.query_db('replace into colonies_links (newcharter, oldcharter) values (%s,%s)', (linkto, linkfrom))
    except:
        payload = {'outcome': 'there was an error with inserting'}
    else:
        payload = {'outcome': 'Successfully linked. Reload the page to see the changes.'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/unlinkcolony', methods=['POST'])
def unlinkcolony():
    try:
        linkfrom = request.json['linkfrom']
    except KeyError:
        abort(400)
        return
    # lets not care about security
    try:
        utilities.query_db('delete from colonies_links where oldcharter=%s', (linkfrom,))
    except:
        payload = {'outcome': 'there was an error with deleting'}
    else:
        payload = {'outcome': 'Successfully unlinked. Reload the page to see the changes.'}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


# ----------------------------- LAYOUTS -----------------------------
@api_blueprint.route('/layoutpreview/<lid>', methods=['GET'])
def layoutpreview(lid):
    # check if lid is integer
    try:
        lid = int(lid)
    except ValueError:
        abort(400)
        return
    if lid < 1:
        abort(400)
    resp = utilities.query_db("select layoutname, ape_account, layoutdesc, layoutspecs, unix_timestamp(lastupdate), "
                              "layoutimageurl from layouts where layoutid=%s", (lid,))
    if len(resp) != 1:
        abort(400)
    res = resp[0]
    payload = {'outcome': 'success', 'name': res[0], 'author': res[1], 'description': res[2],
               'specs': json.loads(res[3]), 'lastupdate': res[4], 'imageurl': res[5]}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


# ----------------------------- ADU -----------------------------
@api_blueprint.route('/adutable', methods=['GET'])
def adutable():
    resp = utilities.query_db('SELECT charter,unix_timestamp(timestamp),ape_account, name FROM adu_identifier a'
                              'INNER JOIN ( SELECT MAX(entryid) rev FROM adu_identifier GROUP BY charter ) b ON '
                              'entryid = b.rev order by timestamp desc')
    charter_list = [k[0] for k in resp]
    resp2 = utilities.query_db('SELECT a.charter, a.name FROM colonies_hist a INNER JOIN ( '
                               'SELECT charter, MAX(time) rev FROM colonies_hist where charter in '
                               '({})'
                               'GROUP BY charter '
                               ') b ON a.charter = b.charter AND a.time = b.rev;'.format(
        ','.join(['%s'] * len(charter_list))),
        tuple(charter_list))
    char_to_name = {k[0]: k[1] for k in resp2}
    data = [{'charter': k[0],
             'lastts': k[1],
             'owner': k[2],
             'lastcity': k[3],
             'name': char_to_name.get(k[0], k[0])} for k in resp]
    resp = make_response(jsonify({'data': data}))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/aducharters', methods=['GET'])
def aducharters():
    resp = utilities.query_db('select distinct charter from adu_identifier')
    payload = [k[0] for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/aducharterdata/<charter>', methods=['GET'])
def aducharterdata(charter):
    try:
        tabname = request.args['tabname']
        cityname = request.args['cityname']
    except KeyError:
        abort(400)
        return
    if tabname == 'bddiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, buildings from adu_buildings as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname))
    elif tabname == 'stdiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, a.* from adu_stats as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname), True)
    elif tabname == 'rsdiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, storage from adu_resources as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname))
    elif tabname == 'radiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, amounts from adu_resources as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname))
    elif tabname == 'sldiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, salaries from adu_salaries as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname))
    elif tabname == 'vhdiv':
        resp = utilities.query_db(
            'select unix_timestamp(timestamp) as timestamp, vehicles from adu_vehicles as a join adu_identifier as i on a.entryid=i.entryid '
            'where charter=%s and name = %s order by a.entryid desc limit 7;', (charter, cityname))
    else:
        abort(400)
        return

    if tabname in ['stdiv']:
        columns = resp[1]
        payload = [{columns[index][0]: column for index, column in enumerate(value) if
                    column is not None and columns[index][0] != 'entryid'} for value in resp[0]]
    elif tabname in ['bddiv', 'radiv', 'rsdiv', 'sldiv', 'vhdiv']:
        payload = []
        for row in resp:
            t_d = json.loads(row[1])
            t_d['timestamp'] = row[0]
            payload.append(t_d)
    else:
        payload = []
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/aducharterstats/<charter>', methods=['GET'])
def aducharterstats(charter):
    return 'bla bla bla'
    # # get the column names
    # resp = utilities.query_db('describe adu_buildings')
    # columns = [k[0] for k in resp if k[0] != "entryid"]
    # selection_query = ['sum({})'.format(k) for k in columns]
    # query = 'select ' + ', '.join(selection_query) + ' from adu_buildings as a join adu_identifier as i ' \
    #                                                  'on a.entryid=i.entryid where charter="' + charter + '" and a.entryid=max(i.entryid) group by name'
    # print(query)
    # return 'ok'
    # resp = utilities.query_db(
    #     'select ' + ', '.join(selection_query) + ' from adu_buildings as a join adu_identifier as i '
    #                                              'on a.entryid=i.entryid where charter=%s and entryid=max(i.entryid) group by name',
    #     (charter,))
    #
    # return 'ok'
    #
    # resp = utilities.query_db('select sum(a.*) from adu_buildings as a join adu_identifier as i on a.entryid=i.entryid '
    #                           'where charter=%s order by a.entryid desc limit 1;', (charter,))
    # columns = cursor.description
    # payload = [{columns[index][0]: column for index, column in enumerate(value) if
    #             column is not None and columns[index][0] != 'entryid'} for value in resp]
    # resp = make_response(jsonify(payload))
    # resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    # return resp


@api_blueprint.route('/mc2report', methods=['POST', 'OPTIONS'])
def mc2report():
    if request.method == 'OPTIONS':
        resp = make_response('this is the response to OPTIONS call.')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
        return resp
    try:
        event = request.json['event']
        sid = request.json['sid']
        ses = request.json['ses']
        cli = request.json['cli']
        gid = request.json['gid']
        aun = request.json['aun']
    except KeyError:
        abort(400)
        return
    try:
        data = request.json['data']
    except KeyError:
        data = {}
    print(time.time(), 'hello, this is event', event, 'of sid', sid)
    resp = utilities.query_db('insert into srs_events (eventtype, serverid, sessionid, clientid, gameid,'
                              'ape_account) values (%s, %s, %s, %s, %s, %s)', (event, sid, ses, cli, gid, aun), return_lastrowid=True)
    eventid = resp[1]
    print(eventid)
    if event == 'serverConnected':
        utilities.query_db('insert into srs_event_connected values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (eventid, data['gameData'], data['worldTypeId'], data['worldTypeName'], data['worldName'],
                            data['gameVersion'], data['created'], data.get('hostOS'), data['gameSession'], data['universe']))
    if event == 'serverDisconnected':
        utilities.query_db('insert into srs_event_disconnected values (%s, %s)', (eventid, data['gameSession']))
    if event == 'statReport':
        utilities.query_db('insert into srs_event_report values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (eventid, data['bannedPlayers'], data['exploredChunks'], data['settledChunks'],
                            data['totalGDP'], data['totalMoney'], data['totalPlayers'], data['totalPlaytime'],
                            data['totalPopulation']))
        for pid in data['players']:
            p = data['players'][pid]
            utilities.query_db('insert into srs_players values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (eventid, p['id'], p['username'], p['color'], p['mod'], p['admin'], p['joined'],
                                p['level'], p['civ'], p['money'], p['research'], p['playTime']))
        for sid in data['settlements']:
            s = data['settlements'][sid]
            utilities.query_db('insert into srs_settlements values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               (eventid, s['id'], s['name'], s['owner'], s['population'], s['gdp'], s['approval'],
                                s['color'], s['level']))
        for uid in data['utilities']:
            u = data['utilities'][uid]
            utilities.query_db('insert into srs_utilities values (%s, %s, %s, %s)',(eventid, uid, u['usage'], u['capacity']))
    resp = make_response(jsonify({'success': True}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# ----------------------------- BADGES -------------------------
@api_blueprint.route('/roleholders/<rolename>', methods=['GET'])
def roleholders(rolename):
    resp = utilities.query_db('select distinct ape_account from users_roles where roledesc=%s order by ape_account asc',
                              (rolename,))
    payload = [k[0] for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/medalholders/<medalname>', methods=['GET'])
def medalholders(medalname):
    resp = utilities.query_db(
        'select distinct ape_account from users_medals where medalname=%s order by ape_account asc',
        (medalname,))
    payload = [k[0] for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/usermedals/<username>', methods=['GET'])
def usermedals(username):
    # deprecated
    resp = make_response(jsonify([]))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp
    resp = utilities.query_db(
        'select medalname, imageurl, unix_timestamp(delivrance), message from users_medals where ape_account=%s',
        (username,))
    payload = [{'name': k[0], 'url': k[1], 'delivrance': k[2], 'message': k[3]} for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


# ----------------------------- PERSO -------------------------
@api_blueprint.route('/removediscordlink/', methods=['GET'])
@utilities.test_login
def removediscordlink(logged_in):
    if not logged_in:
        abort(403)
        return
    # start real page processing
    ape_account = logged_in
    utilities.query_db('delete from discord where ape_account=%s', (ape_account,))
    payload = {'outcome': 'Discord account link with {} removed, if existed.'.format(ape_account)}
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


# -------------------------- REFERENCE ----------------------------
@api_blueprint.route('/cibt/<stage>', methods=['GET'])
@utilities.test_login
def cibt(logged_in, stage):
    if not logged_in:
        abort(403)
        return
    # start real page processing
    ape_account = logged_in
    if stage == "colonies":
        resp = utilities.query_db(
            'select charter, name from colonies_hist where charter in (select charter from adu_identifier '
            'where ape_account=%s) and date(time)=CURDATE();', (ape_account,))
        payload = [[k[0], k[1]] for k in resp]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    if stage == "coldata":
        try:
            charter = request.args['charter']
        except KeyError:
            abort(400)
            return
        resp = utilities.query_db('select * from adu_resamounts where entryid=(select max(entryid) from adu_identifier '
                                  'where charter=%s);', (charter,), True)
        columns = resp[1]
        try:
            resources = [{columns[index][0].replace('_', ' '): column for index, column in enumerate(value) if
                          column not in [0, None] and columns[index][0] != 'entryid'} for value in resp[0]][0]
        except IndexError:
            resources = {}
        resp = utilities.query_db('select * from adu_techs where entryid=(select max(entryid) from adu_identifier '
                                  'where charter=%s);', (charter,), True)
        columns = resp[1]
        try:
            techs = [[columns[index][0].replace('_', ' ') for index, column in enumerate(value) if
                      column == 1 and columns[index][0] != 'entryid'] for value in resp[0]][0]
        except IndexError:
            techs = []
        resp = utilities.query_db('select * from adu_vehicles where entryid in (select max(entryid) from adu_identifier'
                                  ' where charter=%s group by name);', (charter,), True)
        columns = resp[1]
        try:
            vehicles = [[columns[index][0].replace('_', ' ') for index, column in enumerate(value) if
                         column not in [0, None] and columns[index][0] != 'entryid'] for value in resp[0]]
            vehicles = list({item for sublist in vehicles for item in sublist})
        except IndexError:
            vehicles = []
        resp = utilities.query_db('select s1.capitol, s1.mapstage from colonies_hist as s1 left join '
                                  'colonies_hist as s2 on s1.charter=s2.charter and s1.time<s2.time where '
                                  's1.charter=%s and s2.charter is NULL;', (charter,))
        independent, atmostage = resp[0]
        independent = True if independent == 1 else False
        print(resources)
        print(techs)
        print(vehicles)
        print(independent)
        print(atmostage)
        payload = {
            'resources': resources,
            'techs': techs,
            'vehicles': vehicles,
            'independent': independent,
            'atmostage': atmostage
        }
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    abort(400)
    return


# -------------------------- ADV SEARCH ----------------------------
@api_blueprint.route('/search', methods=['GET'])
def adv_search():
    try:
        colony_name = request.args['colony_name']
        colony_owner = request.args['colony_owner']
        region = request.args['region']
        population_min = request.args['population_min']
        population_max = request.args['population_max']
        gdp_min = request.args['gdp_min']
        gdp_max = request.args['gdp_max']
        foundation_min = request.args['foundation_min']
        foundation_max = request.args['foundation_max']
        independence_min = request.args['independence_min']
        independence_max = request.args['independence_max']
        maptypes = request.args['maptypes']
        civilizations = request.args['civilizations']
        races = request.args['races']
    except KeyError:
        abort(400)
        return
    maptypes = maptypes.split(',')
    civilizations = civilizations.split(',')
    races = races.split(',')
    if region == "":
        f_region = ''
    elif region in ["0", "1"]:
        f_region = 'and c.region={}'.format(region)
    else:
        abort(400)
        return
    if independence_max == "":
        f_independence_max = ''
    else:
        if utilities.isvaliddate(independence_max, '%Y-%m-%d'):
            f_independence_max = 'and c.independenceday<"' + independence_max + '"'
        else:
            abort(400)
            return
    if independence_min == "":
        f_independence_min = ''
    else:
        if utilities.isvaliddate(independence_min, '%Y-%m-%d'):
            f_independence_min = 'and c.independenceday>"' + independence_min + '"'
        else:
            abort(400)
            return
    if foundation_min == "":
        f_foundation_min = ''
    else:
        if utilities.isvaliddate(foundation_min, '%Y-%m-%d'):
            f_foundation_min = 'and c.foundationday>"' + foundation_min + '"'
        else:
            abort(400)
            return
    if foundation_max == "":
        f_foundation_max = ''
    else:
        if utilities.isvaliddate(foundation_max, '%Y-%m-%d'):
            f_foundation_max = 'and c.foundationday<"' + foundation_max + '"'
        else:
            abort(400)
            return
    f_maptypes = 'and c.maptype in ({})'.format(','.join(['%s' for k in maptypes])) if maptypes[0] != '' else ''
    f_civilizations = 'and c.civilization in ({})'.format(','.join(['%s' for k in civilizations])) \
        if civilizations[0] != '' else ''
    f_races = 'and c.race in ({})'.format(','.join(['%s' for k in races])) if races[0] != '' else ''
    mcr = [m for m in maptypes if m != ''] + [c for c in civilizations if c != ''] + [r for r in races if r != '']
    population_min = population_min or 0
    population_max = population_max or int(1e9)
    gdp_min = gdp_min or 0
    gdp_max = gdp_max or int(1e18)
    nested_query = '''
        (select s1.charter, s1.name, c.ape_account, s1.population, s1.gdp, s1.cw_size, c.region, c.race,
        c.civilization, c.maptype, c.independenceday, c.foundationday, s1.time
        from colonies_hist as s1 
        left join colonies as c on c.charter=s1.charter  
        where s1.name regexp %s 
        and c.ape_account regexp %s  
        {} 
        and s1.population>%s 
        and s1.population<%s 
        and s1.gdp>%s 
        and s1.gdp<%s 
        {} 
        {} 
        {} 
        {} 
        {} 
        {}
        {} ) '''.format(f_region, f_independence_min, f_foundation_max, f_independence_min, f_independence_max,
                        f_maptypes, f_civilizations, f_races)
    nested_query_arguments = (colony_name, colony_owner, population_min, population_max,
                              gdp_min, gdp_max, *mcr)
    # print(nested_query)
    # print(nested_query_arguments)
    try:
        resp = utilities.query_db('''
            select /*+ MAX_EXECUTION_TIME(1000)*/ 
            a.charter, a.name, a.ape_account, a.population, a.gdp, a.cw_size, a.region, a.race,
            a.civilization, a.maptype, unix_timestamp(a.independenceday), unix_timestamp(a.foundationday) from 
            ''' + nested_query + '''
            as a left join 
            ''' + nested_query + '''
            as s2 on a.charter=s2.charter and a.time<s2.time
            where s2.charter is NULL;''', (*nested_query_arguments, *nested_query_arguments))
    except MySQLdb.OperationalError:
        resp = {'error': 'Error : timeout (8 seconds). Please narrow the filters.'}
    resp = make_response(jsonify(resp))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


# ------------- TRANSLATION TOOL ----------------

@api_blueprint.route('/translationstrings', methods=['GET'])
@utilities.test_login
def translationstrings(logged_in):
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    if role in [1, 2]:  # translator or proofreaders only
        try:
            draw = int(request.args['draw'])
            length = int(request.args['length'])
            offset = int(request.args['start'])
            ordercol = int(request.args['order[0][column]'])
            orderdir = request.args['order[0][dir]']
        except:
            abort(400)
            return
        # order will always be by string_id
        # get strings
        resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                                  "proofreader_ape_account, translator_ape_account, translation_id, "
                                  "translation_id_chosen, string_context from trs_original as a left join (select * "
                                  "from trs_translated as b left join trs_users as c on "
                                  "ape_account=translator_ape_account where language=%s and role=1) as d on "
                                  "a.string_id=d.string_id left join trs_proofreading as e on a.string_id=e.string_id "
                                  "and e.translation_id_chosen=d.translation_id where a.string_id between %s and %s "
                                  "order by a.string_id;",
                                  (language, offset + 1, offset + length))
        strings = [{
            'string_id': resp[0][0],
            'string_original': resp[0][1],
            'string_translated': [resp[0][2]],
            'string_comments': [resp[0][3]],
            'proofreader_ape_account': resp[0][4],
            'translator_ape_account': [resp[0][5]],
            'translation_id': [resp[0][6]],
            'translation_id_chosen': resp[0][7],
            'string_context': resp[0][8]
        }]
        for rownb in range(1, len(resp)):
            if resp[rownb][0] == resp[rownb - 1][0]:  # it must have already been added into strings
                if resp[rownb][2]:
                    strings[-1]['string_translated'].append(resp[rownb][2])
                if resp[rownb][3]:
                    strings[-1]['string_comments'].append(resp[rownb][3])
                if resp[rownb][5]:
                    strings[-1]['translator_ape_account'].append(resp[rownb][5])
                if resp[rownb][6]:
                    strings[-1]['translation_id'].append(resp[rownb][6])
            else:  # not added. create new entry
                strings.append({
                    'string_id': resp[rownb][0],
                    'string_original': resp[rownb][1],
                    'string_translated': [resp[rownb][2]],
                    'string_comments': [resp[rownb][3]],
                    'proofreader_ape_account': resp[rownb][4],
                    'translator_ape_account': [resp[rownb][5]],
                    'translation_id': [resp[rownb][6]],
                    'translation_id_chosen': resp[rownb][7],
                    'string_context': resp[rownb][8]
                })
        resp = utilities.query_db('select count(string_id) from trs_original')
        payload = {'data': strings, 'recordsFiltered': resp[0][0], 'draw': draw, 'recordsTotal': resp[0][0]}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    else:
        abort(400)
        return



@api_blueprint.route('/trssubmitchanges', methods=['POST'])
@utilities.test_login
def trssubmitchanges(logged_in):
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    if role == 1:  # translator
        try:
            comment = request.json['comment']
            translation = request.json['translation']
            string_id = request.json['string_id']
        except:
            abort(400)
            return
        # if the string is already proofread (some string of the same language ardy approved), impossible to modify it.
        resp = utilities.query_db('select * from trs_proofreading as a join trs_users as b on '
                                  'proofreader_ape_account=ape_account where string_id=%s and language=%s',
                                  (string_id, language))
        if len(resp) == 1:
            payload = {'message852': 'This string is already proofread. Impossible to modify.'}
            resp = make_response(jsonify(payload))
            resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
            return resp
        if comment == '':
            # then retrieve previous comment
            resp = utilities.query_db('select string_comments from trs_translated'
                                      ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
            if len(resp) == 1:
                comment = resp[0][0]
        if translation == '':
            # then retrieve previous translation
            resp = utilities.query_db('select string_translated from trs_translated'
                                      ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
            if len(resp) == 1:
                translation = resp[0][0]
        if (translation, comment) == ('', ''):
            payload = {'message852': 'No contents provided.'}
            resp = make_response(jsonify(payload))
            resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
            return resp
        resp = utilities.query_db('replace into trs_translated '
                                  ' (string_id, string_translated, string_comments, translator_ape_account)'
                                  ' values'
                                  ' (%s, %s, %s, %s)', (string_id, translation, comment, logged_in))
        # now, re-query this row to get all data
        resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                                  "proofreader_ape_account, translator_ape_account, translation_id, "
                                  "translation_id_chosen, string_context from trs_original as a left join (select * from "
                                  "trs_translated as b left join trs_users as c on ape_account=translator_ape_account "
                                  "where language=%s and role=1) as d on a.string_id=d.string_id left join "
                                  "trs_proofreading as e on a.string_id=e.string_id and "
                                  "e.translation_id_chosen=d.translation_id where a.string_id=%s",
                                  (language, string_id))
        distinct_ids = {k[0] for k in resp}  # this is a set (no multiple elements)
        if len(distinct_ids) != 1:
            abort(500)
            return
        strings = [] * len(distinct_ids)
        for rownb in range(len(resp)):
            if resp[rownb][0] in distinct_ids:  # it hasn't been added into strings list yet
                distinct_ids.remove(resp[rownb][0])  # remove it and add it into strings
                strings.append({
                    'string_id': resp[rownb][0],
                    'string_original': resp[rownb][1],
                    'string_translated': [resp[rownb][2]],
                    'string_comments': [resp[rownb][3]],
                    'proofreader_ape_account': resp[rownb][4],
                    'translator_ape_account': [resp[rownb][5]],
                    'translation_id': [resp[rownb][6]],
                    'translation_id_chosen': resp[rownb][7],
                    'string_context': resp[rownb][8]
                })
            else:  # it has already been added into strings
                if resp[rownb][2] is not None:
                    strings[-1]['string_translated'].append(resp[rownb][2])
                if resp[rownb][3] is not None:
                    strings[-1]['string_comments'].append(resp[rownb][3])
                if resp[rownb][5] is not None:
                    strings[-1]['translator_ape_account'].append(resp[rownb][5])
                if resp[rownb][6] is not None:
                    strings[-1]['translation_id'].append(resp[rownb][6])
        payload = strings[0]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    else:
        abort(403)
        return


@api_blueprint.route('/pfrsubmitchanges', methods=['POST'])
@utilities.test_login
def pfrsubmitchanges(logged_in):
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    if role == 2:  # proofreader
        try:
            action = request.json['action']
            string_id = request.json['string_id']
            if action == 'accept':
                translation_id = request.json['translation_id']
        except:
            abort(400)
            return

        if action == 'accept':
            # first, check if the translation_id exists
            resp = utilities.query_db('select * from trs_translated where translation_id=%s', (translation_id,))
            if len(resp) != 1:
                abort(400)
                return
            resp = utilities.query_db('replace into trs_proofreading (string_id, translation_id_chosen, '
                                      'proofreader_ape_account) values (%s, %s, %s)',
                                      (string_id, translation_id, logged_in))

        elif action == 'remove':
            resp = utilities.query_db('delete from trs_proofreading where string_id=%s and proofreader_ape_account=%s',
                                      (string_id, logged_in))

        else:
            abort(400)
            return

        # now, re-query this row to get all data
        resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                                  "proofreader_ape_account, translator_ape_account, translation_id, "
                                  "translation_id_chosen, string_context from trs_original as a left join (select * from "
                                  "trs_translated as b left join trs_users as c on ape_account=translator_ape_account "
                                  "where language=%s and role=1) as d on a.string_id=d.string_id left join "
                                  "trs_proofreading as e on a.string_id=e.string_id and "
                                  "e.translation_id_chosen=d.translation_id where a.string_id=%s",
                                  (language, string_id))
        distinct_ids = {k[0] for k in resp}  # this is a set (no multiple elements)
        if len(distinct_ids) != 1:
            abort(500)
            return
        strings = [] * len(distinct_ids)
        for rownb in range(len(resp)):
            if resp[rownb][0] in distinct_ids:  # it hasn't been added into strings list yet
                distinct_ids.remove(resp[rownb][0])  # remove it and add it into strings
                strings.append({
                    'string_id': resp[rownb][0],
                    'string_original': resp[rownb][1],
                    'string_translated': [resp[rownb][2]],
                    'string_comments': [resp[rownb][3]],
                    'proofreader_ape_account': resp[rownb][4],
                    'translator_ape_account': [resp[rownb][5]],
                    'translation_id': [resp[rownb][6]],
                    'translation_id_chosen': resp[rownb][7],
                    'string_context': resp[rownb][8]
                })
            else:  # it has already been added into strings
                if resp[rownb][2] is not None:
                    strings[-1]['string_translated'].append(resp[rownb][2])
                if resp[rownb][3] is not None:
                    strings[-1]['string_comments'].append(resp[rownb][3])
                if resp[rownb][5] is not None:
                    strings[-1]['translator_ape_account'].append(resp[rownb][5])
                if resp[rownb][6] is not None:
                    strings[-1]['translation_id'].append(resp[rownb][6])
        payload = strings[0]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    else:
        abort(403)
        return


@api_blueprint.route('/trsoverview', methods=['GET'])
def trsoverview():
    resp = utilities.query_db('select count(string_id) from trs_original')
    total_strings = resp[0][0]

    resp = utilities.query_db('select language, count(distinct b.string_id) as proofread from trs_proofreading as b '
                              'left join trs_users as c on b.proofreader_ape_account = c.ape_account where role=2 '
                              'group by language order by proofread desc;')

    proofread = {k[0]: k[1] for k in resp}

    resp = utilities.query_db('select language, role, ape_account from trs_users order by language')

    users = {resp[0][0]: [{'role': resp[0][1], 'ape_account': resp[0][2]}]}

    for rownb in range(1, len(resp)):
        if resp[rownb - 1][0] == resp[rownb][0]:  # it is already in the dict (same language entry)
            users[resp[rownb][0]].append({'role': resp[rownb][1], 'ape_account': resp[rownb][2]})
        else:
            users[resp[rownb][0]] = [{'role': resp[rownb][1], 'ape_account': resp[rownb][2]}]

    resp = utilities.query_db('select language, count(distinct b.string_id) as count from trs_translated as b left '
                              'join trs_users as c on b.translator_ape_account = c.ape_account where (role is NULL or '
                              'role=1) group by language order by count desc;')

    payload = [{
        'language': k[0],
        'translated': k[1],
        'proofread': proofread.get(k[0], 0),
        'total': total_strings,
        'users': [k for k in users.get(k[0], [])]
    } for k in resp]

    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/trsprogress', methods=['GET'])
@utilities.test_login
def trsprogress(logged_in):
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    resp = utilities.query_db('select count(string_id) from trs_original')
    payload = {'total': resp[0][0]}

    if role == 1:  # translator
        resp = utilities.query_db('select count(distinct b.string_id) from trs_translated as b left join trs_users '
                                  'as c on b.translator_ape_account = c.ape_account where role=1 '
                                  'and language=%s', (language,))
        if range(len(resp)) == 0:
            payload['done'] = 0
        else:
            payload['done'] = resp[0][0]
    elif role == 2:  # proofreader
        resp = utilities.query_db('select count(distinct b.string_id) from trs_proofreading as b '
                                  'left join trs_users as c on b.proofreader_ape_account = c.ape_account where role=2 '
                                  'and language = %s', (language,))
        if range(len(resp)) == 0:
            payload['done'] = 0
        else:
            payload['done'] = resp[0][0]
    else:
        abort(400)
        return

    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/translationuser', methods=['GET'])
@utilities.test_login
def translationuser(logged_in):
    """THIS IS FOR THE APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    payload = {'role': role, 'language': language, 'username': logged_in}

    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/trsstringdata', methods=['GET'])
@utilities.test_login
def trsstringdata(logged_in):
    """THIS IS FOR THE ANDROID APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    try:
        string_id = request.args['string_id']
    except:
        abort(400)
        return

    if not string_id.isdigit():
        abort(400)
        return

    # now, re-query this row to get all data
    resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                              "proofreader_ape_account, translator_ape_account, translation_id, "
                              "translation_id_chosen, a.string_key, unix_timestamp(date_modified), string_context "
                              "from trs_original as a left join (select * from "
                              "trs_translated as b left join trs_users as c on ape_account=translator_ape_account "
                              "where language=%s and role=1) as d on a.string_id=d.string_id left join "
                              "trs_proofreading as e on a.string_id=e.string_id and "
                              "e.translation_id_chosen=d.translation_id where a.string_id=%s",
                              (language, string_id))
    distinct_ids = {k[0] for k in resp}  # this is a set (no multiple elements)
    if len(distinct_ids) != 1:
        payload = {'message852': 'ID ' + str(string_id) + ' does not exist'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    strings = [] * len(distinct_ids)
    for rownb in range(len(resp)):
        if resp[rownb][0] in distinct_ids:  # it hasn't been added into strings list yet
            distinct_ids.remove(resp[rownb][0])  # remove it and add it into strings
            strings.append({
                'string_id': resp[rownb][0],
                'string_original': resp[rownb][1],
                'string_translated': [resp[rownb][2]],
                'string_comments': [resp[rownb][3]],
                'proofreader_ape_account': resp[rownb][4],
                'translator_ape_account': [resp[rownb][5]],
                'translation_id': [resp[rownb][6]],
                'translation_id_chosen': resp[rownb][7],
                'string_key': resp[rownb][8],
                'date_modified': [resp[rownb][9]],
                'string_context': resp[rownb][10]
            })
        else:  # it has already been added into strings
            if resp[rownb][2] is not None:
                strings[-1]['string_translated'].append(resp[rownb][2])
            if resp[rownb][3] is not None:
                strings[-1]['string_comments'].append(resp[rownb][3])
            if resp[rownb][5] is not None:
                strings[-1]['translator_ape_account'].append(resp[rownb][5])
            if resp[rownb][6] is not None:
                strings[-1]['translation_id'].append(resp[rownb][6])
            if resp[rownb][9] is not None:
                strings[-1]['date_modified'].append(resp[rownb][9])
    payload = strings[0]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/trsstringdatabatch', methods=['GET'])
@utilities.test_login
def trsstringdatabatch(logged_in):
    """THIS IS FOR THE ANDROID APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    try:
        string_id_start = request.args['string_id_start']
        string_id_stop = request.args['string_id_stop']
    except:
        abort(400)
        return

    if not (string_id_start.isdigit() and string_id_stop.isdigit()):
        abort(400)
        return

    # now, re-query this row to get all data
    resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                              "proofreader_ape_account, translator_ape_account, translation_id, "
                              "translation_id_chosen, a.string_key, unix_timestamp(date_modified), string_context "
                              "from trs_original as a left join (select * from "
                              "trs_translated as b left join trs_users as c on ape_account=translator_ape_account "
                              "where language=%s and role=1) as d on a.string_id=d.string_id left join "
                              "trs_proofreading as e on a.string_id=e.string_id and "
                              "e.translation_id_chosen=d.translation_id where a.string_id between %s and %s",
                              (language, string_id_start, string_id_stop))
    distinct_ids = {k[0] for k in resp}  # this is a set (no multiple elements)
    if len(distinct_ids) < 1:
        payload = {'message852': 'There are no strings with IDs from ' + str(string_id_start) + ' to ' + str(string_id_stop) + '.'}
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    strings = [] * len(distinct_ids)
    for rownb in range(len(resp)):
        if resp[rownb][0] in distinct_ids:  # it hasn't been added into strings list yet
            distinct_ids.remove(resp[rownb][0])  # remove it and add it into strings
            strings.append({
                'string_id': resp[rownb][0],
                'string_original': resp[rownb][1],
                'string_translated': [resp[rownb][2]],
                'string_comments': [resp[rownb][3]],
                'proofreader_ape_account': resp[rownb][4],
                'translator_ape_account': [resp[rownb][5]],
                'translation_id': [resp[rownb][6]],
                'translation_id_chosen': resp[rownb][7],
                'string_key': resp[rownb][8],
                'date_modified': [resp[rownb][9]],
                'string_context': resp[rownb][10]
            })
        else:  # it has already been added into strings
            if resp[rownb][2] is not None:
                strings[-1]['string_translated'].append(resp[rownb][2])
            if resp[rownb][3] is not None:
                strings[-1]['string_comments'].append(resp[rownb][3])
            if resp[rownb][5] is not None:
                strings[-1]['translator_ape_account'].append(resp[rownb][5])
            if resp[rownb][6] is not None:
                strings[-1]['translation_id'].append(resp[rownb][6])
            if resp[rownb][9] is not None:
                strings[-1]['date_modified'].append(resp[rownb][9])
    payload = strings
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp


@api_blueprint.route('/trsappsubmitchanges', methods=['POST'])
@utilities.test_login
def trsappsubmitchanges(logged_in):
    """THIS IS FOR THE APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    if role == 1:  # translator
        try:
            comment = request.json['comment']
            translation = request.json['translation']
            string_id = request.json['string_id']
        except:
            abort(400)
            return
        # if the string is already proofread (some string of the same language ardy approved), impossible to modify it.
        resp = utilities.query_db('select * from trs_proofreading as a join trs_users as b on '
                                  'proofreader_ape_account=ape_account where string_id=%s and language=%s',
                                  (string_id, language))
        if len(resp) == 1:
            payload = {'message852': 'This string is already proofread. Impossible to modify.'}
            resp = make_response(jsonify(payload))
            resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
            return resp
        if comment == '':
            # then retrieve previous comment
            resp = utilities.query_db('select string_comments from trs_translated'
                                      ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
            if len(resp) == 1:
                comment = resp[0][0]
        if translation == '':
            # then retrieve previous translation
            resp = utilities.query_db('select string_translated from trs_translated'
                                      ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
            if len(resp) == 1:
                translation = resp[0][0]
        if (translation, comment) == ('', ''):
            payload = {'message852': 'No contents provided.'}
            resp = make_response(jsonify(payload))
            resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
            return resp
        resp = utilities.query_db('replace into trs_translated '
                                  ' (string_id, string_translated, string_comments, translator_ape_account)'
                                  ' values'
                                  ' (%s, %s, %s, %s)', (string_id, translation, comment, logged_in))
        # now, re-query this row to get all data (this is the only thing that changes compared to web app
        resp = utilities.query_db("select a.string_id, string_original, string_translated, string_comments, "
                                  "proofreader_ape_account, translator_ape_account, translation_id, "
                                  "translation_id_chosen, a.string_key, unix_timestamp(date_modified), string_context "
                                  "from trs_original as a left join (select * from "
                                  "trs_translated as b left join trs_users as c on ape_account=translator_ape_account "
                                  "where language=%s and role=1) as d on a.string_id=d.string_id left join "
                                  "trs_proofreading as e on a.string_id=e.string_id and "
                                  "e.translation_id_chosen=d.translation_id where a.string_id=%s",
                                  (language, string_id))
        distinct_ids = {k[0] for k in resp}  # this is a set (no multiple elements)
        if len(distinct_ids) != 1:
            payload = {'message852': 'ID ' + str(string_id) + ' does not exist'}
            resp = make_response(jsonify(payload))
            resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
            return resp
        strings = [] * len(distinct_ids)
        for rownb in range(len(resp)):
            if resp[rownb][0] in distinct_ids:  # it hasn't been added into strings list yet
                distinct_ids.remove(resp[rownb][0])  # remove it and add it into strings
                strings.append({
                    'string_id': resp[rownb][0],
                    'string_original': resp[rownb][1],
                    'string_translated': [resp[rownb][2]],
                    'string_comments': [resp[rownb][3]],
                    'proofreader_ape_account': resp[rownb][4],
                    'translator_ape_account': [resp[rownb][5]],
                    'translation_id': [resp[rownb][6]],
                    'translation_id_chosen': resp[rownb][7],
                    'string_key': resp[rownb][8],
                    'date_modified': [resp[rownb][9]],
                    'string_context': resp[rownb][10]
                })
            else:  # it has already been added into strings
                if resp[rownb][2] is not None:
                    strings[-1]['string_translated'].append(resp[rownb][2])
                if resp[rownb][3] is not None:
                    strings[-1]['string_comments'].append(resp[rownb][3])
                if resp[rownb][5] is not None:
                    strings[-1]['translator_ape_account'].append(resp[rownb][5])
                if resp[rownb][6] is not None:
                    strings[-1]['translation_id'].append(resp[rownb][6])
                if resp[rownb][9] is not None:
                    strings[-1]['date_modified'].append(resp[rownb][9])
        payload = strings[0]
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    else:
        abort(403)
        return


@api_blueprint.route('/trsappsubmitbatch', methods=['POST'])
@utilities.test_login
def trsappsubmitbatch(logged_in):
    """THIS IS FOR THE APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    if role == 1:  # translator
        try:
            strlist = request.json['strlist']  # this list contains dicts with comment,translation and string_id in them
        except:
            abort(400)
            return
        payload = []
        for string_data in strlist:
            try:
                comment = string_data['string_comment']
                translation = string_data['string_translation']
                string_id = string_data['string_id']
                date_modified = string_data['date_modified']
            except:
                payload.append({'success': False, 'message852': 'Bad contents provided.'})
                continue
            else:
                # if the string is already proofread, impossible to modify it.
                resp = utilities.query_db('select * from trs_proofreading as a join trs_users as b on '
                                          'proofreader_ape_account=ape_account where string_id=%s and language=%s',
                                          (string_id, language))
                if len(resp) == 1:
                    payload.append({'success': False, 'message852': 'This string is already proofread. Impossible to modify.', 'string_id':string_id})
                    continue
                if comment == '':
                    # then retrieve previous comment
                    resp = utilities.query_db('select string_comments from trs_translated'
                                              ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
                    if len(resp) == 1:
                        comment = resp[0][0]
                if translation == '':
                    # then retrieve previous translation
                    resp = utilities.query_db('select string_translated from trs_translated'
                                              ' where translator_ape_account=%s and string_id=%s', (logged_in, string_id))
                    if len(resp) == 1:
                        translation = resp[0][0]
                if (translation, comment) == ('', ''):
                    payload.append({'success': False, 'message852': 'No contents provided.', 'string_id':string_id})
                    continue
                # try to fetch it to see if there already exists a newer version by the same guy
                resp = utilities.query_db('select unix_timestamp(date_modified) from trs_translated '
                                          'where string_id=%s and translator_ape_account=%s', (string_id, logged_in))
                if len(resp) > 1:
                    abort(500)
                    return
                elif len(resp) == 1:
                    if resp[0][0] > date_modified:
                        payload.append({'success':False, 'message852':'A newer version exists on the server.', 'string_id':string_id})
                        continue
                resp = utilities.query_db('replace into trs_translated '
                                          ' (string_id, string_translated, string_comments, translator_ape_account)'
                                          ' values'
                                          ' (%s, %s, %s, %s)', (string_id, translation, comment, logged_in))
                # now we assume it's a success
                payload.append({'success': True, 'string_id':string_id})
        resp = make_response(jsonify(payload))
        resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
        return resp
    else:
        abort(403)
        return


@api_blueprint.route('/recentedits', methods=['GET'])
@utilities.test_login
def recentedits(logged_in):
    """THIS IS FOR THE APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]

    resp = utilities.query_db('select a.string_id, unix_timestamp(date_modified), translator_ape_account '
                              'from trs_translated as a join trs_users as b on a.translator_ape_account=b.ape_account '
                              'and b.language=%s and b.role=1 join trs_original as c on a.string_id=c.string_id '
                              'order by date_modified desc limit 10;', (language,))

    payload = [{'id': k[0], 'date': k[1], 'ape_account': k[2]} for k in resp]
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp
    
    
@api_blueprint.route('/nextstringtotranslate', methods=['GET'])
@utilities.test_login
def nextstringtotranslate(logged_in):
    """THIS IS FOR THE APP"""
    if not logged_in:
        abort(403)
        return
    resp = utilities.query_db('select language, role from trs_users where ape_account=%s', (logged_in,))
    if len(resp) != 1:
        abort(403)
        return
    language = resp[0][0]
    role = resp[0][1]
    
    resp = utilities.query_db('select min(string_id) from trs_original where string_id not in (select string_id from '
                              'trs_translated as a join trs_users as b on a.translator_ape_account=b.ape_account and '
                              'b.language=%s and b.role=1);', (language,))

    try:
        payload = {'string_id': resp[0][0]}
    except KeyError:
        payload = {'string_id': 1}
    if not payload['string_id']:
        payload['string_id'] = 1
    resp = make_response(jsonify(payload))
    resp.headers['Access-Control-Allow-Origin'] = 'https://coloniae.space'
    return resp
