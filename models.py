from util_db import ResourceMixin
from sqlalchemy.orm import relationship
from collections import OrderedDict
from app import db


class Bug(db.Model, ResourceMixin):
    """
    here is where all the bugs will be stored
    """
    __tablename__ = "bugs"
    STATUS = OrderedDict([("resolved", "Resolved"), ("unresolved", "Unresolved")])

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    body = db.Column(db.String(250), nullable=False)

    status = db.Column(
        db.Enum(*STATUS, name="status_types", native_enum=False),
        index=True,
        nullable=False,
        server_default="unresolved",
    )

    assigned_user = db.Column(db.String(250), nullable=True)
    bug_comments = relationship("BugComment", back_populates="bug", cascade="all, delete-orphan")

    def change_status(self):
        if self.status == "unresolved":
            self.status = "resolved"
        else:
            self.status = "unresolved"
        self.save()
        return None

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "status": self.status,
            "assigned_user": self.assigned_user,
        }


class BugComment(db.Model, ResourceMixin):
    """
    here is where all the comments will be stored,
    """
    __tablename__ = "bug_comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(250), nullable=False)

    bug_id = db.Column(db.String, db.ForeignKey("bugs.id"))
    bug = relationship("Bug", back_populates="bug_comments")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "bug_id": self.bug_id,
        }


db.create_all()
