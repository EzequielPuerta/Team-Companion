from team_companion.app.web.modules.main import main
from team_companion.app.common.render import render_template_with_sidebar
from team_companion.app.web import root_system

from flask import Response
from flask_login import login_required

# Routes and views
@main.route("/")
@login_required
def dashboard():
    data = {}
    data["log_times"] = root_system.log_time_system.select_all()
    return render_template_with_sidebar("main/dashboard.html", **data)

@main.route("/events/")
def stream():
    return Response(root_system.toastr_system.consume(), mimetype="text/event-stream")