from team_companion.app.web.modules.internal_user.system import InternalUserSystem
from team_companion.app.web.modules.lock.system import LockingSystem
from team_companion.app.web.modules.version.system import VersionSystem
from team_companion.app.system.logging_system import LoggingSystem
from team_companion.app.system.signal_system import SignalSystem
from team_companion.app.system.time_system import TimeSystem
from team_companion.app.system.toastr_system import ToastrSystem
from flask import request, url_for
from functools import wraps
from random import choice
from string import ascii_uppercase
from team_companion.app import create_app, db
from tests.utils import BaseTestCase

def auth_user_already_logged(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        myself = args[0]
        myself.login_auth_user()
        return f(*args, **kwargs)
    return wrapped

class DatabaseTestCase(BaseTestCase):
    db = None

    # SETUP
    @classmethod
    def setUpClass(cls):
        super(DatabaseTestCase, cls).setUpClass()
        cls.root_system = create_app(required_subsystems=cls.required_subsystems())
        # cls.root_system.config['SQLALCHEMY_ECHO'] = True
        cls.db = db
        cls.db.app = cls.root_system
        cls.db.create_all()
        cls.root_system.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
        super(DatabaseTestCase, cls).tearDownClass()

    @classmethod
    def required_subsystems(cls):
        return [
            LoggingSystem,
            SignalSystem,
            TimeSystem,
            ToastrSystem,
            InternalUserSystem,
            LockingSystem,
            VersionSystem]

    def setUp(self):
        super(DatabaseTestCase, self).setUp()
        self.client = self.root_system.test_client()
        self.app_context = self.root_system.app_context()
        self.app_context.push()
        for table in reversed(self.db.metadata.sorted_tables):
            self.db.session.execute(table.delete())
        self.db.session.commit()

    def tearDown(self):
        self.db.session.rollback()
        self.app_context.pop()
        super(DatabaseTestCase, self).tearDown()

    # UTILS
    def as_bytes(self, string):
        return bytes(string, encoding="utf_8")

    def login_auth_user(self):
        self.client.post("/login/", data={
            "username":"clark_kent",
            "password":"superman"})
        return self.root_system.internal_user_system.select_one()

    def random_string(self, length):
        return ''.join(choice(ascii_uppercase) for i in range(length))

    # ASSERTS
    def assertTextIn(self, text, response):
        self.assertIn(self.as_bytes(text), response.data)

    def assertStatusCode(self, response, status_code):
        self.assertEqual(status_code, response.status_code)

    def assertOk(self, response):
        self.assertStatusCode(response, 200)

    def assertRedirectToLogin(self, response):
        self.assertStatusCode(response, 302)
        self.assertIn(b"Redirecting", response.data)
        self.assertIn(b"/login/?next=", response.data)

    def assertMovesOkTo(self, response, target):
        with self.root_system.test_request_context():
            self.assertOk(response)
            # self.assertEqual(request.path, url_for(target))   NOT WORKING YET, IDKW...

    def assertRedirects(self, response, target):
        with self.root_system.test_request_context():
            self.assertStatusCode(response, 302)
            # self.assertEqual(request.path, url_for(target))   NOT WORKING YET, IDKW...