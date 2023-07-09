from flask import Flask
from flask_jsglue import JSGlue
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.', static_folder='../static')

jsglue = JSGlue(app)

app.config['MAX_CONTENT_PATH'] = os.getenv('MAX_CONTENT_PATH')  # 1MB

from utilities import mysql
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql.init_app(app)


from application.integrations.views import integrations_blueprint
from application.main.views import main_blueprint
from application.tools.views import tools_blueprint
from application.perso.views import perso_blueprint
from application.adu.views import adu_blueprint
from application.stats.views import stats_blueprint
from application.lbs.views import lbs_blueprint
from application.news.views import news_blueprint
# from application.badges.views import badges_blueprint
# from application.events.views import events_blueprint
from application.reference.views import reference_blueprint
from application.api.views import api_blueprint

# register the blueprints
app.register_blueprint(integrations_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(tools_blueprint)
app.register_blueprint(perso_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(lbs_blueprint)
app.register_blueprint(news_blueprint)
# app.register_blueprint(badges_blueprint)
# app.register_blueprint(events_blueprint)
app.register_blueprint(reference_blueprint)
app.register_blueprint(adu_blueprint)
