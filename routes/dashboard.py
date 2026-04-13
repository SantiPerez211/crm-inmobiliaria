
from flask import Blueprint, render_template
from models import Pago
from utils import generar_deudas

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    generar_deudas()
    deudas = Pago.query.filter_by(estado='pendiente').count()
    return render_template('dashboard.html', deudas=deudas)
