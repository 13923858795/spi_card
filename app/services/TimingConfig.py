import time
from datetime import datetime
from app.models.cards import Cards
from app.services.DistinguishServices import DistinguishServices
from app.settings import STATIC_PATH


def test_scheduler():
    from app.app import create_app
    app = create_app()
    with app.app_context():
        models = Cards.query.filter_by(is_ok=False).all()
        for model in models:
            file_name = model.image
            path = STATIC_PATH + "/photo/" + file_name
            info = DistinguishServices(path)
            if info:
                model.date = info
                model.is_ok = True
                model.save()
                print(f"处理图片{file_name}")
