from tests.app.web.modules.version.test_case import VersionTestCase

class TestVersionModel(VersionTestCase):

    def __init__(self, *args, **kwargs):
        super(TestVersionModel, self).__init__(*args, **kwargs)

    def test_version_creation(self):
        properties = {"tag":"1.0.0"}
        current_version = self.version(**properties)
        
        self.assertEqual(current_version.tag, properties["tag"])

    def test_version_as_string(self):
        current_version = self.version()
        self.assertEqual(str(current_version), current_version.tag)

    def test_version_representation(self):
        current_version = self.version()
        self.assertEqual(repr(current_version), current_version.tag)

    def test_version_equality(self):
        current_version = self.version()
        another_current_version = self.version()
        self.assertEqual(current_version, current_version)
        self.assertEqual(hash(current_version), hash(current_version))
        self.assertEqual(current_version, another_current_version)
        self.assertEqual(hash(current_version), hash(another_current_version))

        another_current_version.tag = current_version.tag[::-1]
        self.assertEqual(another_current_version, another_current_version)
        self.assertEqual(hash(another_current_version), hash(another_current_version))
        self.assertNotEqual(current_version, another_current_version)
        self.assertNotEqual(hash(current_version), hash(another_current_version))

        current_version.id = 1
        another_current_version.id = 1
        another_current_version.tag = current_version.tag
        self.assertEqual(current_version, current_version)
        self.assertEqual(hash(current_version), hash(current_version))
        self.assertEqual(current_version, another_current_version)
        self.assertEqual(hash(current_version), hash(another_current_version))
        
        another_current_version.id = 2
        self.assertEqual(current_version, current_version)
        self.assertEqual(hash(current_version), hash(current_version))
        self.assertNotEqual(current_version, another_current_version)
        self.assertNotEqual(hash(current_version), hash(another_current_version))