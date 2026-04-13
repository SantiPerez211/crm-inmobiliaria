
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from routes.dashboard import dashboard_bp
from routes.inquilinos import inquilinos_bp
from routes.reportes import reportes_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(inquilinos_bp)
app.register_blueprint(reportes_bp)

if __name__ == '__main__':
    app.run()
