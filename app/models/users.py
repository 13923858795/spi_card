# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from app.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col
)
from app.extensions import bcrypt


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    crm_employee_id = Column(db.String(80), unique=True, nullable=True)  # 职工crm系统 职工emp_id编号
    nickname = Column(db.String(80), nullable=True)  # 职工名
    english_name = Column(db.String(200), nullable=True)  # 职工英文名
    abbreviation_name = Column(db.String(200), nullable=True)  # 英文名缩写  唯一
    office = Column(db.String(80), nullable=True)  # 办公室名  台北，北京， 深圳，上海
    superior_account = Column(db.String(200), nullable=True)  # 有职工没有crm管理系统账户，需要通过上级账户来查询
    position_type = Column(db.String(200), nullable=True)  # 职工岗位类型   sales  service  等等
    portrait_image = Column(db.String(200), nullable=True)  # 用户头像
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    roles = Column(db.Integer(), nullable=True)
    is_leave = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
