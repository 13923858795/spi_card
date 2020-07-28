import time
from app.services.TimingConfig import test_scheduler

while True:
    try:
        test_scheduler()
    except:
        continue

    time.sleep(5)
