import MySQLdb, datetime, time, requests, json
from flask_mysqldb import MySQL
from functools import wraps
from flask import request
import os

gameversionspath = os.getenv('gameversionspath')
upload_folder = os.getenv('upload_folder')
paths = {
    'mycolony_version': os.getenv('paths_mycolony_version')
}

professions_list = ['Blue Collar', 'Botanist', 'Teacher', 'Scientist', 'Medic', 'White Collar', 'Politician',
                    'Diplomat', 'Arbiter', 'Brewmaster', 'Unskilled']

mysql = MySQL()


def query_db(query, arguments=tuple(), return_description=False, return_lastrowid=False):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query, arguments)
        mysql.connection.commit()
        if return_description:
            desc = cursor.description
            resp = cursor.fetchall()
            return resp, desc
        elif return_lastrowid:
            last = cursor.lastrowid
            resp = cursor.fetchall()
            return resp, last
        else:
            resp = cursor.fetchall()
            return resp
    finally:
        cursor.close()


def test_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # check if logged in
        sida = request.cookies.get('sida', None)
        sidb = request.cookies.get('sidb', None)
        creds = check_ape_apps_credentials(sida, sidb)
        logged_in = is_logged_in(creds)  # true or false
        if logged_in:
            logged_in = creds[1]
        # logged_in is either false or ape_account
        return f(logged_in, *args, **kwargs)

    return decorated_function


def isvaliddate(datestr, dformat):
    try:
        datetime.datetime.strptime(datestr, dformat)
    except ValueError:
        return False
    return True


def role_has_access(roledesc, user_roles):
    if 'Founder' in user_roles:
        return True
    if roledesc in user_roles:
        return True
    return False


def check_ape_apps_credentials(sida, sidb):
    req = requests.post("https://accounts.ape-apps.com/api.php",
                        data={'f': os.getenv('MCAPI_F'), 's1': sida, 's2': sidb, 'ak': os.getenv('MCAPI_AK'),
                              'am': os.getenv('MCAPI_AM')})
    if req.status_code != 200:
        return ('error', 'Invalid response from ape apps, try to log in again.')
    if req.text == '-1':
        return ('error', 'Invalid credentials, try to log in again.')
    if req.text == 'Invalid credentials, try to log in again.':
        return ('error', 'Invalid credentials, try to log in again.')
    resp = json.loads(req.text)
    resp = resp[0]
    return ('success', resp['un'])


def is_logged_in(creds):
    if creds[0] == 'success':
        return True
    else:
        return False


def intable(st):
    try:
        i = int(st)
        return True
    except ValueError:
        return False


def notNoneList(li):
    """returns False if the list contains only None values"""
    for i in li:
        if i != None:
            return True
    return False


def nearest_int(st, lt):
    pt = abs(st - lt[0])  # for comparing
    rt = lt[0]  # the result
    for k in range(len(lt)):
        if abs(st - lt[k]) <= pt:
            pt = abs(st - lt[k])
            rt = lt[k]
    return rt


def str_to_ts(st):
    """Returns timestamp IN SECONDS of date as if timezone is UTC"""
    return round(datetime.datetime.strptime(st, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp())


def tsFromReadable(fn):
    return int(time.mktime(time.strptime(fn + " UTC", "%Y-%m-%d %Z")))


def escapeString(string):
    return string.replace('"', '')


def get_user_roles(ape_account):
    resp = query_db('select roledesc,color from users_roles where ape_account=%s', (ape_account,))
    return [{'name': k[0], 'color': k[1]} for k in resp]


def compare_game_versions(old, new):
    """Returns a changelog of all new buildings, vehicles and techs."""
    r = {'buildings': [], 'vehicles': [], 'technology': [], 'resources': [], 'civilizations': [], 'races': [],
         'mapTypes': [], 'terrains': []}
    for item in r:
        try:
            for i in new[item]:
                try:
                    nameslist = [k['name'] for k in old[item]]
                except KeyError:
                    nameslist = []
                if i['name'] not in nameslist:
                    r[item].append(i)
        except KeyError:
            pass

    return r
