from team_companion.app.extensions import db
from team_companion.app.common.equality_checker import equality_checker

class Lock(db.Model):

    __tablename__ = "lock"
    __table_args__ = (db.UniqueConstraint("locker_identifier", "locked_identifier", name="unique_lock_constraint"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locker_class = db.Column(db.String(256), nullable=False)
    locker_identifier = db.Column(db.String(256), nullable=False)
    locked_class = db.Column(db.String(256), nullable=False)
    locked_identifier = db.Column(db.String(256), nullable=False)

    def __eq__(self, other):
        return equality_checker(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.locker_class, self.locker_identifier, self.locked_class, self.locked_identifier))

    def __str__(self):
        return f"{self.locker_class}({self.locker_identifier}) -> {self.locked_class}({self.locked_identifier})"
    
    def __repr__(self):
        return self.__str__()