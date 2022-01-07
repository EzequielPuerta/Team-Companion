from enum import unique
from team_companion.app.extensions import db
from team_companion.app.common.equality_checker import equality_checker

class Version(db.Model):

    __tablename__ = "version"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(256), nullable=False, unique=True)

    def __eq__(self, other):
        return equality_checker(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.tag))

    def __str__(self):
        return self.tag
    
    def __repr__(self):
        return self.__str__()