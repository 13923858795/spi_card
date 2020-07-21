import datetime as dt

from flask_login import UserMixin

from app.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from app.extensions import bcrypt


class Cards(UserMixin, SurrogatePK, Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    image = Column(db.String())
    date = Column(db.String())
    intent = Column(db.String())
    company_url = Column(db.String())
    is_ok = Column(db.Boolean(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
