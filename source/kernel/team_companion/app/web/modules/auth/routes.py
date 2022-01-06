from team_companion.app.web.modules.auth import auth
from team_companion.app.web.modules.auth.forms import LoginForm
from team_companion.app.web import root_system
from team_companion.app.extensions import login_manager

from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse

def login_for(persisted_user, form):
    login_user(user=persisted_user, remember=form.remember_me.data)
    root_system.internal_user_system.update_last_connection(persisted_user)
    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("main.dashboard")
    return redirect(next_page)

# Routes and views
@auth.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        if len(root_system.internal_user_system.select_all()) == 0:
            return login_for(root_system.internal_user_system.add_using(form), form)
        else:
            internal_user = root_system.internal_user_system.select_one_filter_by(username=form.username.data, using="first")
            if internal_user is not None and root_system.internal_user_system.check_password(internal_user, form.password.data):
                return login_for(internal_user, form)

    return render_template("auth/login.html",
        form = form,
        current_year = root_system.time_system.now().year,
        version = root_system.version_system.current_version(),
        body_class = "sign-in")

@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@login_manager.user_loader
def load_user(user_id):
    return root_system.internal_user_system.select_identify_by(user_id)