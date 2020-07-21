#
# initial_quotas = 1
#
# increase = 1.05
#
# _c = 0
#
# for i in range(15):
#     buy = int(initial_quotas * increase**i)
#     _c += buy
#     print(buy)
#
# print(initial_quotas * (0.97 **15), _c)


# import math
#
# r = math.log(4, 2)
# print(r)
#
# # print(0.975 ** 17)
# import tushare as ts
#
#
# TOKEN = '8fd4826df4da30db172ac6fe205c0d44aac29805de23ddc626edd835'
# # pro = ts.pro_api(TOKEN)
# ts.set_token(TOKEN)
#
# # # df = pro.daily(ts_code='600104.SH', start_date='20200101', end_date='20200528')
# #
# # df = ts.get_hist_data('600848')
# # # df = ts.get_realtime_quotes('600104')  # 实时分笔
#
#
#
# date = ts.pro_bar('600104.SH', start_date='20180201', adj='qfq')
# # date = ts.get_k_data('600104.SH', start='20180201')
# # df = pro.daily(ts_code='600104.SH', start_date='20180201', end_date='20200527')#
# # df = pro.ts.pro_bar(ts_code='600104.SH', adj='qfq', start_date='20180201', end_date='20200527')
# print(date)

from app.services.TimingConfig import test_scheduler
test_scheduler()
