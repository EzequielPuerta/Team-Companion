from flask import Blueprint

version = Blueprint('version', __name__, template_folder='templates')

from . import models