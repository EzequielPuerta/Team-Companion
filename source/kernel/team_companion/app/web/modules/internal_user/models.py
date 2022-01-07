from flask_login import UserMixin
from team_companion.app.extensions import db
from team_companion.app.common.equality_checker import equality_checker

class InternalUser(db.Model, UserMixin):

    __tablename__ = "internal_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_connection = db.Column(db.DateTime(), nullable=True)
    is_admin = db.Column(db.Boolean, default=True)

    def __eq__(self, other):
        return equality_checker(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.username, self.password, self.last_connection, self.is_admin))

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return self.__str__()