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



"""
{"addr":["第三分区:苏州工业园区双泾街59号三号厂房","第一分区:苏州工业园区钟南街北478号","第四分区:常州市钟楼区邹区工业园岳杨路8号","公司总部:中国·苏州·工业园区科教创新区新昌路68号","第二分区:宿迁市泗阳县经济开发区珠海路35号"],
"company":["苏州苏大维格科技集团股份有限公司"],"department":["新型显示部"],"email":["wqiao@svgoptronics.com"],"name":"乔文",
"request_id":"20200724170031_e9bdc9c4cec8a935edb4095b3dc2c299","success":true,
"tel_cell":["18550007830"],"tel_work":[],"title":["部长"]}

"""

class Cards(UserMixin, SurrogatePK, Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(1000))
    email = Column(db.String(500))   # 邮箱
    tel_cell = Column(db.String(500))  # 电话
    tel_work = Column(db.String(500))  # 工作电话
    department = Column(db.String(500))  # 部门
    title = Column(db.String(500))  # 头衔

    company = Column(db.String(500))  # 公司
    original_factory = Column(db.String(500))
    remarks = Column(db.String(5000))  # 备注

    image = Column(db.String(500))
    is_analysis = Column(db.Boolean(), default=False)
    own = db.Column(db.Integer)  # 上传人员所属id
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
