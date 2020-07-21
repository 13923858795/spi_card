# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired


class PlanForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("名称", validators=[DataRequired()])
    initial_quotas = FloatField("起始金额", validators=[DataRequired()])  # 最初配额
    price_top = FloatField("价格顶部", validators=[DataRequired()])  # 价格顶部
    price_bottom = FloatField("价格底部", validators=[DataRequired()])  # 价格底部
    increase_rate = FloatField("增长率", validators=[DataRequired()])  # 增长率
    reduce_rate = FloatField("减少率", validators=[DataRequired()])  # 减少率
    start_price = FloatField("起始价", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PlanForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(PlanForm, self).validate()
        if not initial_validation:
            return False
        return True
