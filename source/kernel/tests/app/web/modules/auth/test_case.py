from tests.app.database_test_case import DatabaseTestCase, auth_user_already_logged

class AuthTestCase(DatabaseTestCase):

    @classmethod
    def required_subsystems(cls):
        return super(AuthTestCase, cls).required_subsystems()