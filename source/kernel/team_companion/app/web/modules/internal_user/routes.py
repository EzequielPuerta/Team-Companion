from team_companion.app.web.modules.internal_user import internal_user
from team_companion.app.web.modules.internal_user.forms import CRUDAddInternalUserForm, CRUDModifyInternalUserForm
from team_companion.app.common.routes import RoutingSpecification
from team_companion.app.common.filters import formatted_boolean
from team_companion.app.web import root_system
from flask_login import login_required

specification = \
    RoutingSpecification(
        name = "InternalUser",
        system_name = "internal_user_system",
        dashboard = "internal_user.dashboard",
        dashboard_url = "internal_user/dashboard.html",
        add_url = "internal_user/add.html",
        modify_url = "internal_user/modify.html")

# Filters for templates
@internal_user.app_template_filter("formatted_timestamp")
def timestamp_filter(timestamp):
    return root_system.time_system.as_user_friendly().formatting(timestamp, on_failure=lambda : "-")

@internal_user.app_template_filter("formatted_boolean")
def boolean_filter(boolean_value):
    return formatted_boolean(boolean_value)

# Routes and views
@internal_user.route("/internal_user/")
@login_required
def dashboard():
    return specification.route_dashboard_request(listing="internal_users")

@internal_user.route("/internal_user/add/", methods=["GET", "POST"])
@login_required
def add():
    return specification.route_add_request(using=CRUDAddInternalUserForm)

@internal_user.route("/internal_user/modify_<int:id>/", methods=["GET", "POST"])
@login_required
def modify(id):
    return specification.route_modify_request(identifier=id, using=CRUDModifyInternalUserForm)

@internal_user.route("/internal_user/delete/", methods=["POST"])
@login_required
def delete():
    return specification.route_delete_request()