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

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquilino_id = db.Column(db.Integer)
    mes = db.Column(db.String(20))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(20))  # pagado / pendiente

# ==============================
# CREAR DB
# ==============================
with app.app_context():
    db.create_all()

# ==============================
# GENERAR DEUDAS AUTOMÁTICAS
# ==============================
def generar_deudas():
    hoy = datetime.now()
    mes_actual = hoy.strftime("%Y-%m")

    inquilinos = Inquilino.query.all()

    for i in inquilinos:
        existe = Pago.query.filter_by(inquilino_id=i.id, mes=mes_actual).first()
        if not existe:
            deuda = Pago(
                inquilino_id=i.id,
                mes=mes_actual,
                monto=100000,  # después lo hacemos variable
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
    deuda = len([p for p in pagos if p.estado == "pendiente"])

    return f"""
    <h1>Dashboard CRM</h1>
    <p>Total cobrado: ${total}</p>
    <p>Deudas: {deuda}</p>
    <a href='/inquilinos'>Ir a Inquilinos</a>
    """

# ==============================
# INQUILINOS
# ==============================
@app.route("/inquilinos", methods=["GET", "POST"])
def inquilinos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        nuevo = Inquilino(nombre=nombre)
        db.session.add(nuevo)
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
        pagos = Pago.query.filter_by(inquilino_id=i.id).all()

        html += f"<h3>{i.nombre}</h3>"

        for p in pagos:
            color = "green" if p.estado == "pagado" else "red"
            html += f"<p style='color:{color}'>{p.mes} - ${p.monto} - {p.estado}</p>"

        html += f"""
        <form action='/pagar/{i.id}' method='POST'>
            <input name='mes' placeholder='Mes (YYYY-MM)'>
            <input name='monto' placeholder='Monto'>
            <button>Pagar</button>
        </form>
        """

    html += "<br><a href='/'>Volver</a>"

    return html

# ==============================
# PAGAR
# ==============================
@app.route("/pagar/<int:id>", methods=["POST"])
def pagar(id):
    mes = request.form["mes"]

    pago = Pago.query.filter_by(inquilino_id=id, mes=mes).first()

    if pago:
        pago.estado = "pagado"
    else:
        pago = Pago(
            inquilino_id=id,
            mes=mes,
            monto=float(request.form["monto"]),
            estado="pagado"
        )
        db.session.add(pago)

    db.session.commit()
    return redirect("/inquilinos")

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    app.run()
