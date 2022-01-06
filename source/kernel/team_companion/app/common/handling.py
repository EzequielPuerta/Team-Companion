from team_companion.app.common.render import render_template_with_sidebar
from flask import redirect, url_for, flash
from team_companion.app.common.exceptions import AppInfo, AppWarning, AppError
from functools import wraps

def handling_crud_exceptions(f):
    @wraps(f)
    def wrapped(self, **kwargs):
        url = kwargs.get("url")
        form = kwargs.get("form")
        try:
            return f(self, **kwargs)
        except ValueError as error_message:
            return render_template_with_sidebar(url, form=form, error=None)
        except AssertionError as error_message:
            return render_template_with_sidebar(url, form=form, error=error_message)
        except AppInfo as error_message:
            flash(f"{error_message}", "info")
            return redirect(url_for(self.dashboard))
        except AppWarning as error_message:
            flash(f"{error_message}", "warning")
            return redirect(url_for(self.dashboard))
        except AppError as error_message:
            flash(f"{error_message}", "danger")
            return redirect(url_for(self.dashboard))
    return wrapped

def handling_exceptions(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        url = kwargs.get("url")
        try:
            return f(*args, **kwargs)
        except ValueError as error_message:
            flash(f"{error_message}", "danger")
        except AssertionError as error_message:
            flash(f"{error_message}", "danger")
        except AppInfo as error_message:
            flash(f"{error_message}", "info")
        except AppWarning as error_message:
            flash(f"{error_message}", "warning")
        except AppError as error_message:
            flash(f"{error_message}", "danger")
        return redirect(url_for(url))
    return wrapped