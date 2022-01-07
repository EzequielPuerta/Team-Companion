from flask import Blueprint

lock = Blueprint('lock', __name__, template_folder='templates')

from . import models