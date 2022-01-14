from tests.app.database_test_case import DatabaseTestCase, auth_user_already_logged
from team_companion.app.web.modules.version.models import Version

class VersionTestCase(DatabaseTestCase):

    def version(self, **kwargs):
        return Version(
            tag=kwargs.get("tag", "1.0.0"))