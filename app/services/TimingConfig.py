import json
from datetime import datetime
from app.models.cards import Cards
from app.services.DistinguishServices import DistinguishServices
from app.settings import STATIC_PATH


def test_scheduler():
    models = Cards.query.filter_by(is_analysis=False).all()

    print(models)
    for model in models:
        file_name = model.image
        path = STATIC_PATH + "/photo/" + file_name
        info_str = DistinguishServices(path)
        if info_str:

            """{"addr":["第三分区:苏州工业园区双泾街59号三号厂房","第一分区:苏州工业园区钟南街北478号","第四分区:常州市钟楼区邹区工业园岳杨路8号","公司总部:中国·苏州·工业园区科教创新区新昌路68号","第二分区:宿迁市泗阳县经济开发区珠海路35号"],
                "company":["苏州苏大维格科技集团股份有限公司"],"department":["新型显示部"],"email":["wqiao@svgoptronics.com"],"name":"乔文",
                "request_id":"20200724170031_e9bdc9c4cec8a935edb4095b3dc2c299","success":true,
                "tel_cell":["18550007830"],"tel_work":[],"title":["部长"]}
            """
            info_json = json.loads(info_str)

            info = {}
            for k in info_json:

                _info = info_json[k]
                if isinstance(_info, list):

                    info[k] = ",".join(_info)
                else:
                    info[k] = _info

            print(info)
            model.name = info['name']
            model.email = info['email']
            model.tel_cell = info['tel_cell']
            # model.tel_work = info['tel_work']
            model.department = info['department']
            model.company = info['company']
            model.title = info['title']

            model.is_analysis = True
            model.save()
            print(f"处理图片{file_name}")
