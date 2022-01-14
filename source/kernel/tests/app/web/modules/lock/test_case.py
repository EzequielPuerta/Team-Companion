from abc import ABC
from tests.app.database_test_case import DatabaseTestCase, auth_user_already_logged
from team_companion.app.web.modules.lock.models import Lock

class LockTestCase(DatabaseTestCase):
    def lock(self, **kwargs):
        return Lock(
            locker_class=kwargs.get("locker_class", "Bloqueador"),
            locker_identifier=kwargs.get("locker_identifier", "1"),
            locked_class=kwargs.get("locked_class", "Bloqueado"),
            locked_identifier=kwargs.get("locked_identifier", "9"))

# Mock Classes
class MockPersistentObject(ABC):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return str(self.id)

class Shipment(MockPersistentObject):
    def __init__(self, id, tracking_code, sender, packages):
        super().__init__(id)
        self.tracking_code = tracking_code
        self.sender = sender
        self.packages = packages

class Sender(MockPersistentObject):
    def __init__(self, id, name, branches, main_office=None):
        super().__init__(id)
        self.name = name
        self.branches = branches
        self.main_office = main_office

class Branch(MockPersistentObject):
    def __init__(self, id, address):
        super().__init__(id)
        self.address = address

class Package(MockPersistentObject):
    def __init__(self, id, products):
        super().__init__(id)
        self.products = products

class Product(MockPersistentObject):
    def __init__(self, id, barcode):
        super().__init__(id)
        self.barcode = barcode