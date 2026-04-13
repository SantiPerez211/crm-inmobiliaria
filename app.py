from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "crm.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==============================
# MODELOS
# ==============================
class Inquilino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquilino_id = db.Column(db.Integer)
    monto = db.Column(db.Float)
    fecha_inicio = db.Column(db.String(10))  # YYYY-MM

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquilino_id = db.Column(db.Integer)
    mes = db.Column(db.String(10))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(20))

# ==============================
# CREAR DB
# ==============================
with app.app_context():
    db.create_all()

# ==============================
# GENERAR DEUDAS SEGÚN CONTRATO
# ==============================
def generar_deudas():
    hoy = datetime.now()

    contratos = Contrato.query.all()

    for c in contratos:
        inicio = datetime.strptime(c.fecha_inicio, "%Y-%m")

        meses = (hoy.year - inicio.year) * 12 + (hoy.month - inicio.month)

        for m in range(meses + 1):
            mes = (inicio.month + m - 1) % 12 + 1
            año = inicio.year + (inicio.month + m - 1) // 12
            periodo = f"{año}-{mes:02d}"

            existe = Pago.query.filter_by(inquilino_id=c.inquilino_id, mes=periodo).first()

            if not existe:
                deuda = Pago(
                    inquilino_id=c.inquilino_id,
                    mes=periodo,
                    monto=c.monto,
                    estado="pendiente"
                )
                db.session.add(deuda)

    db.session.commit()

# ==============================
# DASHBOARD
# ==============================
@app.route("/")
def dashboard():
    generar_deudas()

    pagos = Pago.query.all()
    total = sum([p.monto for p in pagos if p.estado == "pagado"])
    deuda = sum([p.monto for p in pagos if p.estado == "pendiente"])

    return f"""
    <h1>Dashboard CRM</h1>
    <p>Total cobrado: ${total}</p>
    <p>Deuda total: ${deuda}</p>
    <a href='/inquilinos'>Inquilinos</a><br>
    <a href='/contratos'>Contratos</a>
    """

# ==============================
# INQUILINOS
# ==============================
@app.route("/inquilinos", methods=["GET", "POST"])
def inquilinos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        db.session.add(Inquilino(nombre=nombre))
        db.session.commit()
        return redirect("/inquilinos")

    lista = Inquilino.query.all()

    html = "<h1>Inquilinos</h1>"

    html += """
    <form method='POST'>
        <input name='nombre' placeholder='Nombre'>
        <button>Agregar</button>
    </form>
    """

    for i in lista:
        html += f"<p>{i.nombre}</p>"

    html += "<br><a href='/'>Volver</a>"
    return html

# ==============================
# CONTRATOS
# ==============================
@app.route("/contratos", methods=["GET", "POST"])
def contratos():
    if request.method == "POST":
        db.session.add(Contrato(
            inquilino_id=int(request.form["inquilino_id"]),
            monto=float(request.form["monto"]),
            fecha_inicio=request.form["fecha_inicio"]
        ))
        db.session.commit()
        return redirect("/contratos")

    inquilinos = Inquilino.query.all()

    html = "<h1>Contratos</h1>"

    html += "<form method='POST'>"
    html += "<select name='inquilino_id'>"

    for i in inquilinos:
        html += f"<option value='{i.id}'>{i.nombre}</option>"

    html += "</select>"
    html += "<input name='monto' placeholder='Alquiler'>"
    html += "<input name='fecha_inicio' placeholder='YYYY-MM'>"
    html += "<button>Crear contrato</button></form>"

    html += "<br><a href='/'>Volver</a>"

    return html

# ==============================
# PAGAR
# ==============================
@app.route("/pagar/<int:id>/<mes>")
def pagar(id, mes):
    pago = Pago.query.filter_by(inquilino_id=id, mes=mes).first()

    if pago:
        pago.estado = "pagado"

    db.session.commit()
    return redirect("/")

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run()
