from team_companion.app.system.persistence_system import PersistenceSystem
from team_companion.app.web.modules.version.models import Version
from team_companion.app.extensions import db

class VersionSystem(PersistenceSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def class_model(self):
        return Version

    @classmethod
    def system_name(cls):
        return "version_system"

    def _attributes_to_synchronize(self):
        return ["tag"]

    def _create(self, form, **kwargs):
        self.should_not_implement()

    def add_using(self, form, **kwargs):
        self.should_not_implement()

    def modify_using(self, object_to_update, updated_form, **kwargs):
        self.should_not_implement()
    
    def current_version(self):
        with self.root_system.app_context():
            _current_version = self.class_model().query.order_by(self.class_model().id.desc()).first()
            if _current_version:
                return _current_version.tag
            else:
                return "Development"