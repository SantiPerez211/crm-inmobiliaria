
from models import Pago
from app import db

def generar_deudas():
    # demo simple
    if not Pago.query.first():
        deuda = Pago(contrato_id=1, mes="2026-01", monto=1000, estado="pendiente")
        db.session.add(deuda)
        db.session.commit()
