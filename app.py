from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# 🔴 IMPORTANTE: ruta absoluta para SQLite (Render fix)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "crm.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# importar modelos después de db
import models

# crear base y tablas
with app.app_context():
    db.create_all()

# importar rutas
from routes.dashboard import dashboard_bp
from routes.inquilinos import inquilinos_bp
from routes.reportes import reportes_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(inquilinos_bp)
app.register_blueprint(reportes_bp)

@app.route("/")
def home():
    return "CRM funcionando correctamente 🚀"

if __name__ == "__main__":
    app.run()
