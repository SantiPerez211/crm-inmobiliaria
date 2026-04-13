
from flask import Blueprint, Response
import pandas as pd
from models import Pago

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/exportar')
def exportar():
    pagos = Pago.query.all()
    data = [{"mes":p.mes,"monto":p.monto} for p in pagos]
    df = pd.DataFrame(data)
    return Response(df.to_csv(index=False), mimetype="text/csv")
