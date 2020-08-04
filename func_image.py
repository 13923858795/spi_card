import time
from app.services.TimingConfig import test_scheduler
from app.app import create_app

app = create_app()
with app.app_context():
    # test_scheduler()
    while True:
        try:
            test_scheduler()
        except:
            continue

        time.sleep(5)
