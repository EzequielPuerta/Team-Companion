from tests.app.database_test_case import DatabaseTestCase, auth_user_already_logged
from team_companion.app.web.modules.internal_user.models import InternalUser

class InternalUserTestCase(DatabaseTestCase):

    def internal_user(self, **kwargs):
        return InternalUser(
            username=kwargs.get("username", "bruno_diaz"),
            password=kwargs.get("password", "imbatman123"),
            last_connection=kwargs.get("last_connection", self.root_system.time_system.tz_now()),
            is_admin=kwargs.get("is_admin", True))