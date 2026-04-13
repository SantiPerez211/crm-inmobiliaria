
from app import db

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(20))

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer)
    mes = db.Column(db.String(10))
    monto = db.Column(db.Float)
    estado = db.Column(db.String(20))
