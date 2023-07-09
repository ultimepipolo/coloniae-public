from flask import render_template, Blueprint, session, abort
import utilities

reference_blueprint = Blueprint('reference', __name__, template_folder='templates', url_prefix='/reference')


referencedescs = {
    'col_gen': '<b>How do colonists immigrate?</b><br><br>Each building has a colGenRate item. The engine picks a random amount of ticks, with the colGenRate as the max. So the larger the number, the longer it takes. For the cloning facilities, this amount of ticks is divided by the number of workers. When the tick amount is reached, if the building has the touristDoorway flag, it can bring in a max of 10 colonists at a time. If the building has the isStargate flag, it can bring in a max of 18 colonists at a time. If the max is > 1, then the game factors in approval rating. So if your max is 10 and the approval rating is 80%, then the max is now 8, or 80% of the max. Finally, the final number of new colonists is a random number between 1 and this max.<br><br>Numbers are calculated with :<br>Average is max/2 (mathematical expectation of an uniform law)<br>30 ticks per second<br>100% approval rating<br>100% workers on duty',
    'changelogs': 'Here you can see changelogs for versions of My Colony up to 0.5.0.'}


@reference_blueprint.route('/')
@utilities.test_login
def reference_index(logged_in):
    return render_template('reference_index.html', page='index', logged_in=logged_in)


@reference_blueprint.route('/<page>')
@utilities.test_login
def reference(logged_in, page):
    tablename = {'general': 'General Table', 'cost': 'Costs Table', 'storages': 'Storages Table',
                 'ratio_tick': 'Ratios per tick Table', 'ratio_min': 'Ratios per minute Table', 'techs_i': '--',
                 'techs_h': '--', 'col_gen': 'Colonist Generation Rates', 'gift_caps': 'Gifting and trading capacities',
                 'changelogs': 'Changelogs'}
    if page in ['general', 'cost', 'storages', 'ratio_tick', 'ratio_min', 'techs_i', 'techs_h', 'col_gen', 'gift_caps',
                'changelogs']:
        return render_template('reference_index.html', page=page, tablename=tablename[page],
                               tabledesc=referencedescs.get(page, False), logged_in=logged_in)
    abort(404)
    return
