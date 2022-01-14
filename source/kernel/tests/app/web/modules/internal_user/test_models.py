from tests.app.web.modules.internal_user.test_case import InternalUserTestCase

class TestInternalUserModel(InternalUserTestCase):

    def __init__(self, *args, **kwargs):
        super(TestInternalUserModel, self).__init__(*args, **kwargs)

    def test_internal_user_creation(self):
        properties = {
            "username":"bruno_diaz",
            "password":"imbatman123",
            "last_connection":self.root_system.time_system.tz_now(),
            "is_admin":True}
        bruno_diaz = self.internal_user(**properties)
        
        self.assertEqual(bruno_diaz.username, properties["username"])
        self.assertEqual(bruno_diaz.password, properties["password"])
        self.assertEqual(bruno_diaz.last_connection, properties["last_connection"])
        self.assertTrue(bruno_diaz.is_admin)

    def test_internal_user_as_string(self):
        bruno_diaz = self.internal_user()
        self.assertEqual(str(bruno_diaz), bruno_diaz.username)

    def test_representation(self):
        bruno_diaz = self.internal_user()
        self.assertEqual(repr(bruno_diaz), bruno_diaz.username)

    def test_internal_user_equality(self):
        current_time = self.root_system.time_system.tz_now()
        bruno_diaz = self.internal_user(last_connection=current_time)
        another_bruno_diaz = self.internal_user(last_connection=current_time)
        self.assertEqual(bruno_diaz, bruno_diaz)
        self.assertEqual(hash(bruno_diaz), hash(bruno_diaz))
        self.assertEqual(bruno_diaz, another_bruno_diaz)
        self.assertEqual(hash(bruno_diaz), hash(another_bruno_diaz))

        another_time = self.root_system.time_system.tz_now()
        another_bruno_diaz.last_connection = another_time
        self.assertEqual(another_bruno_diaz, another_bruno_diaz)
        self.assertEqual(hash(another_bruno_diaz), hash(another_bruno_diaz))
        self.assertNotEqual(bruno_diaz, another_bruno_diaz)
        self.assertNotEqual(hash(bruno_diaz), hash(another_bruno_diaz))

        bruno_diaz.id = 1
        another_bruno_diaz.id = 1
        another_bruno_diaz.last_connection = current_time
        self.assertEqual(bruno_diaz, bruno_diaz)
        self.assertEqual(hash(bruno_diaz), hash(bruno_diaz))
        self.assertEqual(bruno_diaz, another_bruno_diaz)
        self.assertEqual(hash(bruno_diaz), hash(another_bruno_diaz))
        
        another_bruno_diaz.id = 2
        self.assertEqual(bruno_diaz, bruno_diaz)
        self.assertEqual(hash(bruno_diaz), hash(bruno_diaz))
        self.assertNotEqual(bruno_diaz, another_bruno_diaz)
        self.assertNotEqual(hash(bruno_diaz), hash(another_bruno_diaz))