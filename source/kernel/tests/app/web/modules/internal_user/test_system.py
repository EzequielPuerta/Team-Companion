from team_companion.app.web.modules.internal_user.models import InternalUser
from tests.app.web.modules.internal_user.test_case import InternalUserTestCase

class TestInternalUserSystem(InternalUserTestCase):

    def __init__(self, *args, **kwargs):
        super(TestInternalUserSystem, self).__init__(*args, **kwargs)

    def test_internal_user_system_class_model(self):
        self.assertEqual(self.root_system.internal_user_system.class_model(), InternalUser)

    def test_internal_user_system_name(self):
        self.assertEqual(self.root_system.internal_user_system.system_name(), "internal_user_system")

    def test_add_internal_user(self):
        bruno_diaz = self.internal_user()
        self.assertIsEmpty(self.root_system.internal_user_system.select_all())
        bruno_diaz = self.root_system.internal_user_system.add(bruno_diaz)
        self.assertJustOneElementIn(self.root_system.internal_user_system.select_all(), bruno_diaz)

    def test_modify_internal_user(self):
        bruno_diaz = self.internal_user(username="bruno_diaz", is_admin=True)
        bruno_diaz = self.root_system.internal_user_system.add(bruno_diaz)
        self.assertEqual(bruno_diaz.username, "bruno_diaz")
        self.assertTrue(bruno_diaz.is_admin)

        changes = {"username":"brunoDiaz", "is_admin":False}
        bruno_diaz = self.root_system.internal_user_system.modify(bruno_diaz, changes)
        self.assertEqual(bruno_diaz.username, "brunoDiaz")
        self.assertFalse(bruno_diaz.is_admin)

    def test_delete_internal_user(self):
        bruno_diaz = self.internal_user()
        self.assertIsEmpty(self.root_system.internal_user_system.select_all())
        bruno_diaz = self.root_system.internal_user_system.add(bruno_diaz)
        self.assertJustOneElementIn(self.root_system.internal_user_system.select_all(), bruno_diaz)
        self.root_system.internal_user_system.delete(bruno_diaz)
        self.assertIsEmpty(self.root_system.internal_user_system.select_all())