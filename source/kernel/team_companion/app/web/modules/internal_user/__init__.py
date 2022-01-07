from flask import Blueprint

internal_user = Blueprint('internal_user', __name__, template_folder='templates')

from . import routes, models