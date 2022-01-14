from flask import Blueprint

log_time = Blueprint('log_time', __name__, template_folder='templates')

from . import models