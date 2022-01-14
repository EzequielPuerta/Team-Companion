from team_companion.app.web.modules.version.models import Version
from tests.app.web.modules.version.test_case import VersionTestCase

class TestVersionSystem(VersionTestCase):

    def __init__(self, *args, **kwargs):
        super(TestVersionSystem, self).__init__(*args, **kwargs)

    def test_version_system_class_model(self):
        self.assertEqual(self.root_system.version_system.class_model(), Version)

    def test_version_system_name(self):
        self.assertEqual(self.root_system.version_system.system_name(), "version_system")

    def test_add_version(self):
        current_version = self.version()
        self.assertIsEmpty(self.root_system.version_system.select_all())
        current_version = self.root_system.version_system.add(current_version)
        self.assertJustOneElementIn(self.root_system.version_system.select_all(), current_version)

    def test_modify_version(self):
        current_version = self.version(tag="1.0.0")
        current_version = self.root_system.version_system.add(current_version)
        self.assertEqual(current_version.tag, "1.0.0")

        changes = {"tag":"2.0.0"}
        current_version = self.root_system.version_system.modify(current_version, changes)
        self.assertEqual(current_version.tag, "2.0.0")

    def test_delete_version(self):
        current_version = self.version()
        self.assertIsEmpty(self.root_system.version_system.select_all())
        current_version = self.root_system.version_system.add(current_version)
        self.assertJustOneElementIn(self.root_system.version_system.select_all(), current_version)
        self.root_system.version_system.delete(current_version)
        self.assertIsEmpty(self.root_system.version_system.select_all())

    def test_current_version(self):
        self.assertIsEmpty(self.root_system.version_system.select_all())
        self.assertEqual(self.root_system.version_system.current_version(), "Development")
        self.root_system.version_system.add(self.version(tag="1.0.0"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 1)
        self.assertEqual(self.root_system.version_system.current_version(), "1.0.0")

        self.root_system.version_system.add(self.version(tag="1.0.1"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 2)
        self.assertEqual(self.root_system.version_system.current_version(), "1.0.1")

        self.root_system.version_system.add(self.version(tag="1.0.2"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 3)
        self.assertEqual(self.root_system.version_system.current_version(), "1.0.2")

        self.root_system.version_system.add(self.version(tag="1.1.0"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 4)
        self.assertEqual(self.root_system.version_system.current_version(), "1.1.0")

        self.root_system.version_system.add(self.version(tag="2.0.0"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 5)
        self.assertEqual(self.root_system.version_system.current_version(), "2.0.0")

        self.root_system.version_system.add(self.version(tag="2.0.1"))
        self.assertLengthEqual(self.root_system.version_system.select_all(), 6)
        self.assertEqual(self.root_system.version_system.current_version(), "2.0.1")