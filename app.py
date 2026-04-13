from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Crear app
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar DB
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# IMPORTANTE: importar modelos DESPUÉS de db
import models

# Crear tablas automáticamente (SOLUCIÓN AL ERROR)
with app.app_context():
    db.create_all()

# Importar rutas
from routes.dashboard import dashboard_bp
from routes.inquilinos import inquilinos_bp
from routes.reportes import reportes_bp

# Registrar rutas
app.register_blueprint(dashboard_bp)
app.register_blueprint(inquilinos_bp)
app.register_blueprint(reportes_bp)

# Ejecutar app
if __name__ == '__main__':
    app.run()
