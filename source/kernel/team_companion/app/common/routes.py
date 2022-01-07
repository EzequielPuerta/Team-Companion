from team_companion.app.common.render import render_template_with_sidebar
from flask import request, redirect, url_for, abort, jsonify, flash
from team_companion.app.common.handling import handling_crud_exceptions
from team_companion.app.web import root_system

class RoutingSpecification:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.system_name = kwargs.get("system_name")
        self.dashboard = kwargs.get("dashboard")
        self.dashboard_url = kwargs.get("dashboard_url", None)
        self.add_url = kwargs.get("add_url", None)
        self.modify_url = kwargs.get("modify_url", None)
        self.process_form = kwargs.get("process_form", (lambda form, rootsystem: form))

    # ACCESSING
    def _system(self):
        return getattr(root_system, self.system_name)

    def build_form(self, using, doing=lambda used_form_class: used_form_class(request.form)):
        form = doing(using)
        self.process_form(form, root_system)
        return form

    # ROUTES ############################################################################################
    
    # DASHBOARD
    def route_dashboard_request(self, listing=None):
        kwargs = {}
        kwargs[listing] = self._system().select_all()
        return render_template_with_sidebar(self.dashboard_url, **kwargs)

    # ADD
    def route_add_request(self, using=None):
        form = self.build_form(using)
        return self._secure_add_request(url=self.add_url, form=form)

    @handling_crud_exceptions
    def _secure_add_request(self, url=None, form=None):
        persisted_object = self._system().add_using(form)
        root_system.logging_system.debug(f"Add: {self.name}({persisted_object.id})")
        return redirect(url_for(self.dashboard))

    # MODIFY
    def route_modify_request(self, identifier=None, using=None):
        persisted_object = self._system().select_identify_by(identifier)
        if persisted_object is None:
            abort(404)
        if root_system.locking_system.is_locked(persisted_object):
            flash(f"El objeto que se intenta modificar ya se encuentra en uso.", "warning")
            return redirect(url_for(self.dashboard))
        else:
            if request.method == "POST":
                form = self.build_form(using, doing=lambda used_form_class: used_form_class(formdata=request.form))
                return self._secure_modify_request(url=self.modify_url, form=form, persisted_object=persisted_object)
            else:
                form = self.build_form(using, doing=lambda used_form_class: used_form_class(obj=persisted_object))
                return render_template_with_sidebar(self.modify_url, form=form, error=None)

    @handling_crud_exceptions
    def _secure_modify_request(self, url=None, form=None, persisted_object=None):
        updated_object = self._system().modify_using(persisted_object, form)
        root_system.logging_system.debug(f"Update: {self.name}({updated_object.id})")
        return redirect(url_for(self.dashboard))

    # DELETE
    def route_delete_request(self):
        try:
            id_to_remove = request.form["element_id"]
            self._system().delete_identified_by(id_to_remove)
            root_system.logging_system.debug(f"Delete: {self.name}({id_to_remove})")
            return jsonify({"processed": True})
        except Exception:
            abort(500)