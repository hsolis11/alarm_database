from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import settings


app = Flask(__name__)
app.config['SECRET_KEY'] = settings.APP_SECRET_KEY

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes
