from tests.app.web.modules.lock.test_case import LockTestCase

class TestLockModel(LockTestCase):

    def __init__(self, *args, **kwargs):
        super(TestLockModel, self).__init__(*args, **kwargs)

    def test_lock_creation(self):
        properties = {"locker_class":"Bloqueador",
            "locker_identifier":"1",
            "locked_class":"Bloqueado",
            "locked_identifier":"9"}
        a_lock = self.lock(**properties)
        
        self.assertEqual(a_lock.locker_class, properties["locker_class"])
        self.assertEqual(a_lock.locker_identifier, properties["locker_identifier"])
        self.assertEqual(a_lock.locked_class, properties["locked_class"])
        self.assertEqual(a_lock.locked_identifier, properties["locked_identifier"])

    def test_lock_as_string(self):
        a_lock = self.lock()
        self.assertEqual(str(a_lock), f"{a_lock.locker_class}({a_lock.locker_identifier}) -> {a_lock.locked_class}({a_lock.locked_identifier})")

    def test_lock_representation(self):
        a_lock = self.lock()
        self.assertEqual(repr(a_lock), f"{a_lock.locker_class}({a_lock.locker_identifier}) -> {a_lock.locked_class}({a_lock.locked_identifier})")

    def test_lock_equality(self):
        a_lock = self.lock()
        another_lock = self.lock()
        self.assertEqual(a_lock, a_lock)
        self.assertEqual(hash(a_lock), hash(a_lock))
        self.assertEqual(a_lock, another_lock)
        self.assertEqual(hash(a_lock), hash(another_lock))

        another_lock.locker_identifier = str(int(a_lock.locker_identifier)+10)
        self.assertEqual(another_lock, another_lock)
        self.assertEqual(hash(another_lock), hash(another_lock))
        self.assertNotEqual(a_lock, another_lock)
        self.assertNotEqual(hash(a_lock), hash(another_lock))

        a_lock.id = 1
        another_lock.id = 1
        another_lock.locker_identifier = a_lock.locker_identifier
        self.assertEqual(a_lock, a_lock)
        self.assertEqual(hash(a_lock), hash(a_lock))
        self.assertEqual(a_lock, another_lock)
        self.assertEqual(hash(a_lock), hash(another_lock))
        
        another_lock.id = 2
        self.assertEqual(a_lock, a_lock)
        self.assertEqual(hash(a_lock), hash(a_lock))
        self.assertNotEqual(a_lock, another_lock)
        self.assertNotEqual(hash(a_lock), hash(another_lock))