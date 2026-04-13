
from flask import Blueprint, render_template

inquilinos_bp = Blueprint('inquilinos', __name__)

@inquilinos_bp.route('/inquilinos')
def inquilinos():
    return render_template('inquilinos.html')
