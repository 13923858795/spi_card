import time
from app.services.TimingConfig import test_scheduler, STATIC_PATH

while True:
    test_scheduler()
    time.sleep(5)

# test_scheduler()

# import os
# file = '1595310102.jpg'
# path = os.path.abspath(os.path.dirname(__file__)) + "\\app\\static\\photo\\1595310102.jpg"
#
# from app.services.DistinguishServices import DistinguishServices
#
# a = DistinguishServices(path)
#
# print(a)