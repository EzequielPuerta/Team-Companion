from team_companion.app.extensions import login_manager, db, migrate
from team_companion.app.web import root_system, modules
from team_companion.app.system.generic_system import GenericSystem
from team_companion.app.common.classes import all_concrete_subclasses
from team_companion.conf.settings import settings_module

def create_app(**kwargs):
    root_system.config.from_object(settings_module)
    root_system.installing(kwargs.get("required_subsystems", all_concrete_subclasses(GenericSystem)))
    register_extensions(root_system)
    register_blueprints(root_system)
    return root_system

def register_extensions(root_system):
    login_manager.init_app(root_system)
    db.init_app(root_system)
    migrate.init_app(root_system, db)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "No hay una sesión abierta. Ingrese con un usuario válido."
    login_manager.login_message_category = "info"

def register_blueprints(root_system):
    root_system.register_blueprint(modules.auth.auth)
    root_system.register_blueprint(modules.internal_user.internal_user)
    root_system.register_blueprint(modules.lock.lock)
    root_system.register_blueprint(modules.main.main)
    root_system.register_blueprint(modules.version.version)