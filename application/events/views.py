from flask import render_template, Blueprint, session, request, make_response, abort, url_for
import os, MySQLdb, time
import utilities

events_blueprint = Blueprint('events', __name__, template_folder='templates', url_prefix='/events')


@events_blueprint.route('/')
@utilities.test_login
def events_index(logged_in):
    return render_template('events_index.html', logged_in=logged_in)


@events_blueprint.route('/create')
@utilities.test_login
def events_form(logged_in):
    # FOR DEV
    ape_account = "Sobeirannovaocc"
    #cursor.execute('select series_title, max(edition) from events_hub where organizer=%s group by series_title',
    #              (ape_account,))
    #current_titles = [{'series_title': k[0], 'edition': k[1]} for k in cursor.fetchall()]
    logged_in = "Sobeirannovaocc"
    current_titles = [{'series_title':'test1', 'edition':1}]
    return render_template('events_form.html', logged_in=logged_in, current_titles=current_titles)
    # END DEV
    if not utilities.is_logged_in(creds):
        session.pop('message', None)
        session.pop('sida', None)
        session.pop('sidb', None)
        return render_template('loginregister.html', message='Authentication is required to create an event.',
                               seguiurl=url_for('events.events_form'))
    # only logged in after this point
    ape_account = creds[1]
    cursor.execute('select series_title, max(edition) from events_hub where organizer=%s group by series_title',
                   (ape_account,))
    current_titles = [{'series_title':k[0], 'edition':k[1]} for k in cursor.fetchall()]
    return render_template('events_form.html', logged_in=logged_in, current_titles=current_titles)