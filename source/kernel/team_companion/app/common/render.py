from team_companion.app.web import root_system

from flask import render_template
from flask_login import current_user

def render_template_with_sidebar(template_name, **kwargs):
    return render_template(template_name,
        current_year = root_system.time_system.tz_now().year,
        version = root_system.version_system.current_version(),
        body_class = "sb-nav-fixed",
        connection_time = root_system.time_system.as_user_friendly().formatting(
            current_user.last_connection, on_failure=lambda : "-"),
        **kwargs)