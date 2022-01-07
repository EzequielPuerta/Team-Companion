from abc import abstractmethod
from sqlalchemy import exc as sql_exceptions
from sqlalchemy.orm import exc as sql_orm_exceptions
from team_companion.app.system.generic_system import GenericSystem
from team_companion.app.extensions import db

class PersistenceSystem(GenericSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @abstractmethod
    def class_model(self):
        pass

    @abstractmethod
    def _attributes_to_synchronize(self):
        pass

    @abstractmethod
    def _create(self, form, **kwargs):
        pass

    def _update(self, object_to_update, updated_values, form=None):
        db.session.query(self.class_model()).filter_by(id=object_to_update.id).update(updated_values)

    # Errors
    def integrity_assertion_failed_during_add(self):
        raise AssertionError(f"El objeto está en conflicto con uno preexistente. No se pudo registrar.")

    def integrity_assertion_failed_during_modify(self):
        raise AssertionError(f"El objeto está en conflicto con uno preexistente. No se pudo modificar.")

    def integrity_assertion_failed_during_delete(self):
        raise AssertionError(f"El objeto no pudo ser eliminado.")

    def raise_integrity_error(self):
        raise sql_exceptions.IntegrityError("", {}, None)

    def raise_value_error(self):
        raise ValueError("Valores inválidos.")

    # Validations
    def _include_any_invalid_value(self, form, **kwargs):
        # For a more specific conflict check, redefine this method in the desired system
        return False

    # Management
    def add(self, object_to_manage, on_success=lambda persisted_object : None):
        try:
            if not object_to_manage.id:
                db.session.add(object_to_manage)
            db.session.commit()
            on_success(object_to_manage)
            return self.select_identify_by(object_to_manage.id)
        except sql_exceptions.IntegrityError:
            db.session.rollback()
            self.integrity_assertion_failed_during_add()

    def modify(self, object_to_update, updated_values, on_success=lambda persisted_object : None, **kwargs):
        self.root_system.locking_system.assert_is_unlocked(object_to_update)
        try:
            self._update(object_to_update, updated_values, **kwargs)
            db.session.commit()
            on_success(object_to_update)
            return self.select_identify_by(object_to_update.id)
        except sql_exceptions.IntegrityError:
            db.session.rollback()
            self.integrity_assertion_failed_during_modify()

    def delete(self, managed_object, on_success=lambda deleted_object : None):
        self.root_system.locking_system.assert_is_unlocked(managed_object)
        try:
            db.session.delete(managed_object)
            db.session.commit()
            on_success(managed_object)
        except sql_exceptions.IntegrityError:
            db.session.rollback()
            self.integrity_assertion_failed_during_delete()

    def add_using(self, form, **kwargs):
        if form.validate_on_submit():
            if self._include_any_invalid_value(form):
                self.integrity_assertion_failed_during_add()
            keyword_args = {}
            if kwargs.get("on_success"):
                keyword_args["on_success"] = kwargs.pop("on_success")
            new_object = self._create(form, **kwargs)
            return self.add(new_object, **keyword_args)
        else:
            self.raise_value_error()

    def modify_using(self, object_to_update, updated_form, **kwargs):
        keyword_args = {}
        if kwargs.get("on_success"):
            keyword_args["on_success"] = kwargs.pop("on_success")
        return self.modify(object_to_update, self._values_to_synchronize(updated_form), form=updated_form, **keyword_args)

    def delete_identified_by(self, id_to_remove):
        self.delete(self.select_identify_by(id_to_remove))

    def _values_to_synchronize(self, form):
        if form.validate_on_submit():
            dict_values = {}
            for attribute in self._attributes_to_synchronize():
                attribute_path = attribute.split(".")
                base_attribute, delegated_attributes = attribute_path[0], attribute_path[1:]
                try:
                    current_object = getattr(getattr(form, base_attribute), "data")
                except AttributeError:
                    pass
                else:
                    for delegated_attribute in delegated_attributes:
                        current_object = getattr(current_object, delegated_attribute)
                    dict_values[base_attribute] = current_object
            return dict_values
        else:
            self.raise_value_error()

    # Querying
    def select_all(self):
        with self.root_system.app_context():
            return self.class_model().query.all()

    def select_all_filter_by(self, **criteria):
        with self.root_system.app_context():
            return self.class_model().query.filter_by(**criteria).all()

    def select_all_filter(self, condition=lambda model: False):
        with self.root_system.app_context():
            return self.class_model().query.filter(condition(self.class_model())).all()

    def select_identify_by(self, identifier):
        with self.root_system.app_context():
            return self.class_model().query.get(identifier)

    def select_one_filter_by(self, using="one", **criteria):
        with self.root_system.app_context():
            try:
                result = getattr(self.class_model().query.filter_by(**criteria), using)()
            except sql_orm_exceptions.MultipleResultsFound:
                raise AssertionError(f"Se encontraron múltiples resultados y se esperaba uno solo.")
            except sql_orm_exceptions.NoResultFound:
                raise AssertionError(f"No se encontró ningún resultado.")
            else:
                return result

    def select_one_filter(self, using="one", condition=lambda model: False):
        with self.root_system.app_context():
            try:
                result = getattr(self.class_model().query.filter(condition(self.class_model())), using)()
            except sql_orm_exceptions.MultipleResultsFound:
                raise AssertionError(f"Se encontraron múltiples resultados y se esperaba uno solo.")
            except sql_orm_exceptions.NoResultFound:
                raise AssertionError(f"No se encontró ningún resultado.")
            else:
                return result

    def select_one(self, using="one"):
        return getattr(self.class_model().query, using)()