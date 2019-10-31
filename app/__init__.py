from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

# CSS
bootstrap = Bootstrap(app)

# Login manager
login = LoginManager(app)
login.login_view = 'login'





# Database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import routes, models,errors