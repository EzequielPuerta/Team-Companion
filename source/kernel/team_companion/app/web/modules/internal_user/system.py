from team_companion.app.system.persistence_system import PersistenceSystem
from team_companion.app.web.modules.internal_user.models import InternalUser
from werkzeug.security import generate_password_hash, check_password_hash

class InternalUserSystem(PersistenceSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def class_model(self):
        return InternalUser

    @classmethod
    def system_name(cls):
        return "internal_user_system"

    def _attributes_to_synchronize(self):
        return ["username", "password", "confirm", "is_admin"]

    def _create(self, form, **kwargs):
        try:
            is_admin = form.is_admin.data
        except AttributeError:
            is_admin = True
        finally:
            user = InternalUser(username=form.username.data, is_admin=is_admin)
            user.password = generate_password_hash(form.password.data)
            return user

    def check_password(self, user, password):
        return check_password_hash(user.password, password)

    def update_last_connection(self, internal_user):
        return super().modify(internal_user, {"last_connection":self.root_system.time_system.tz_now()})