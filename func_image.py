import time
from app.services.TimingConfig import test_scheduler
from app.app import create_app

APP = create_app()


def get_app():

    global APP

    return APP if APP else create_app()


with get_app().app_context():
    # test_scheduler()
    while True:
        try:
            test_scheduler()
        except:
            continue

        time.sleep(5)
