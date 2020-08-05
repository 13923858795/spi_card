# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FileField
from wtforms.validators import DataRequired

from app.models.users import User


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True


class FileForm(FlaskForm):
    """Login form."""

    img = FileField(
        label="图片",
        validators=[DataRequired()]
    )
    original_factory = StringField("源厂")
    remarks = StringField("备注")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(FileForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(FileForm, self).validate()
        if not initial_validation:
            return False
        return True


class CardForm(FlaskForm):
    """Login form."""

    name = StringField("姓名", validators=[DataRequired()])
    tel_cell = StringField("电话", validators=[DataRequired()])
    email = StringField("邮箱", validators=[DataRequired()])
    department = StringField("部门", validators=[DataRequired()])
    title = StringField("职位", validators=[DataRequired()])
    addr = StringField("地址", validators=[DataRequired()])
    company = StringField("公司", validators=[DataRequired()])
    original_factory = StringField("源厂")
    remarks = StringField("备注")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(CardForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(CardForm, self).validate()
        if not initial_validation:
            return False
        return True