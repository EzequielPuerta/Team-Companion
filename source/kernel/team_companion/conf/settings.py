import os

# FLASK
host = "0.0.0.0"
port = 5000
accepted_hosts = {"localhost"}
current_timezone = "America/Buenos_Aires"
secret_key = os.environ["SECRET_KEY"]
settings_module = f"team_companion.conf.{os.getenv('APP_SETTINGS_MODULE')}"

# POSTGRESQL
postgresql_db_path = os.path.join("..", "postgresql_server", "data")
postgresql_user = os.environ["POSTGRES_USER"]
postgresql_pass = os.environ["POSTGRES_PASSWORD"]
postgresql_db_name = os.environ["POSTGRES_DB"]
postgresql_host = os.environ["POSTGRES_HOST"]
postgresql_port = os.environ["POSTGRES_PORT"]
postgresql_uri = f"postgresql://{postgresql_user}:{postgresql_pass}@{postgresql_host}:{postgresql_port}/{postgresql_db_name}"