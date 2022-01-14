from sqlalchemy import or_
from team_companion.app.web.modules.lock.models import Lock
from tests.app.web.modules.lock.test_case import LockTestCase, Product, Package, Branch, Sender, Shipment

class TestLockSystem(LockTestCase):

    def __init__(self, *args, **kwargs):
        super(TestLockSystem, self).__init__(*args, **kwargs)

    def test_lock_system_class_model(self):
        self.assertEqual(self.root_system.locking_system.class_model(), Lock)

    def test_lock_system_name(self):
        self.assertEqual(self.root_system.locking_system.system_name(), "locking_system")

    def test_add_lock(self):
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        xbox = Product(100, "987654")
        extra_joystick = Product(101, "123456")
        package = Package(50, [xbox, extra_joystick])
        a_lock = self.root_system.locking_system.add(locker=package, locked=xbox)
        self.assertJustOneElementIn(self.root_system.locking_system.select_all(), a_lock)

    def test_modify_lock_not_supported(self):
        with self.assertRaises(UserWarning):
            xbox = Product(100, "987654")
            package = Package(50, [xbox])
            a_lock = self.root_system.locking_system.add(locker=package, locked=xbox)
            self.root_system.locking_system.modify(a_lock, {"locked_identifier":"200"})

    def test_lock(self):
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        first_branch = Branch(10, "Av. Belgrano 1234")
        second_branch = Branch(15, "Av. de Mayo 5678")
        andreani = Sender(2, "Andreani", [first_branch, second_branch])
        bike = Product(100, "987654")
        laptop = Product(230, "765432")
        cellphone = Product(432, "123987")
        first_package = Package(50, [bike])
        second_package = Package(60, [laptop, cellphone])
        shipment = Shipment(1, "AR123456", andreani, [first_package, second_package])

        self.root_system.locking_system.lock(locker=shipment, locked_attributes=["sender", "sender.branches", "packages", "packages->products"])
        self.assertLengthEqual(self.root_system.locking_system.select_all(), 8)
        self.assertIsEmpty(self.root_system.locking_system.select_all_filter(condition=\
            lambda lock: or_(lock.locker_class != shipment.__class__.__name__, lock.locker_identifier != str(shipment.id))))
        for blocked in [andreani, first_branch, second_branch, first_package, second_package, bike, laptop, cellphone]:
            self.assertIsNotNone(self.root_system.locking_system.select_one_filter_by(locked_class=blocked.__class__.__name__, locked_identifier=str(blocked.id)))

    def test_unlock(self):
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        first_branch = Branch(10, "Av. Belgrano 1234")
        second_branch = Branch(15, "Av. de Mayo 5678")
        andreani = Sender(2, "Andreani", [first_branch, second_branch])
        bike = Product(100, "987654")
        laptop = Product(230, "765432")
        cellphone = Product(432, "123987")
        first_package = Package(50, [bike])
        second_package = Package(60, [laptop, cellphone])
        shipment = Shipment(1, "AR123456", andreani, [first_package, second_package])

        self.root_system.locking_system.lock(locker=shipment, locked_attributes=["sender", "sender.branches", "packages", "packages->products"])
        self.assertLengthEqual(self.root_system.locking_system.select_all(), 8)
        self.root_system.locking_system.unlock(locker=shipment)
        self.assertIsEmpty(self.root_system.locking_system.select_all())

    def test_is_locked(self):
        xbox = Product(100, "987654")
        package = Package(50, [xbox])
        
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        self.assertFalse(self.root_system.locking_system.is_locked(xbox))
        self.assertFalse(self.root_system.locking_system.is_locked(package))

        a_lock = self.root_system.locking_system.add(locker=package, locked=xbox)
        self.assertJustOneElementIn(self.root_system.locking_system.select_all(), a_lock)
        self.assertTrue(self.root_system.locking_system.is_locked(xbox))
        self.assertFalse(self.root_system.locking_system.is_locked(package))

    def test_is_unlocked(self):
        xbox = Product(100, "987654")
        package = Package(50, [xbox])
        
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        self.assertTrue(self.root_system.locking_system.is_unlocked(xbox))
        self.assertTrue(self.root_system.locking_system.is_unlocked(package))
        
        a_lock = self.root_system.locking_system.add(locker=package, locked=xbox)
        self.assertJustOneElementIn(self.root_system.locking_system.select_all(), a_lock)
        self.assertFalse(self.root_system.locking_system.is_unlocked(xbox))
        self.assertTrue(self.root_system.locking_system.is_unlocked(package))

    def test_assert_is_unlocked(self):
        xbox = Product(100, "987654")
        package = Package(50, [xbox])
        
        self.assertIsEmpty(self.root_system.locking_system.select_all())
        self.assertTrue(self.root_system.locking_system.is_unlocked(xbox))
        self.assertTrue(self.root_system.locking_system.is_unlocked(package))
        self.root_system.locking_system.assert_is_unlocked(xbox)
        self.root_system.locking_system.assert_is_unlocked(package)
        
        a_lock = self.root_system.locking_system.add(locker=package, locked=xbox)
        self.assertJustOneElementIn(self.root_system.locking_system.select_all(), a_lock)
        self.assertFalse(self.root_system.locking_system.is_unlocked(xbox))
        self.assertTrue(self.root_system.locking_system.is_unlocked(package))
        self.root_system.locking_system.assert_is_unlocked(package)
        with self.assertRaises(AssertionError):
            self.root_system.locking_system.assert_is_unlocked(xbox)