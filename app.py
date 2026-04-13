from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "crm.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==============================
# MODELOS
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
# RUTAS
# ==============================
@app.route("/")
def dashboard():
    pagos = Pago.query.all()
    total = sum([p.monto for p in pagos if p.estado == "pagado"])
    deuda = len([p for p in pagos if p.estado == "pendiente"])

    return f"""
    <h1>Dashboard CRM</h1>
    <p>Total cobrado: ${total}</p>
    <p>Deudas: {deuda}</p>
    """

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run()
