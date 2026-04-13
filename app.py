from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configurar base de datos correctamente para Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "crm.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)

# ==============================
# MODELOS MÍNIMOS (evita errores)
# ==============================
class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(20))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(20))

# ==============================
# CREAR DB
# ==============================
with app.app_context():
    db.create_all()

# ==============================
# RUTA PRINCIPAL (SIN ERRORES)
# ==============================
@app.route("/")
def home():
    pagos = Pago.query.all()
    return f"CRM funcionando 🚀 | Pagos cargados: {len(pagos)}"

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run()
