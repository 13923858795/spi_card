from app.models.plan import Plan
import math


class PlanServices:

    @classmethod
    def crate(cls, form):

        _id = form.id.data

        if _id != 0:
            model = Plan.query.filter_by(id=_id).first()
            model.name = form.name.data
            model.initial_quotas = form.initial_quotas.data
            model.price_top = form.price_top.data
            model.price_bottom = form.price_bottom.data
            model.increase_rate = form.increase_rate.data
            model.reduce_rate = form.reduce_rate.data
            model.start_price = form.start_price.data
            model.save()
            return model

        model = Plan.create(initial_quotas=form.initial_quotas.data, price_top=form.price_top.data,
                            price_bottom=form.price_bottom.data, increase_rate=form.increase_rate.data,
                            reduce_rate=form.reduce_rate.data, name=form.name.data, start_price=form.start_price.data
                            )
        return model

    @classmethod
    def filter_by(cls, _id):
        if not _id:
            model = Plan.query.filter_by().first()
        else:
            model = Plan.query.filter_by(id=_id).first()
        return model

    @classmethod
    def filter_all(cls):
        return Plan.query.filter_by().all()

    @classmethod
    def compute(cls, model):
        name = model.name
        initial_quotas = model.initial_quotas
        price_top = model.price_top
        price_bottom = model.price_bottom
        increase_rate = model.increase_rate  # 金额增加比例
        reduce_rate = model.reduce_rate  # reduce_rate 每次跌幅比率
        start_price = model.start_price

        discount_rate = round(price_bottom/price_top, 3)  # 最大跌幅
        layers = int(math.log(discount_rate, reduce_rate)) + 1  # 获取 分层数

        data = [{} for i in range(layers)]
        amount_money = 0
        amount_shares = 0
        FLAG = True
        for i in range(layers):
            """ 
            第 0 层 不操作 
            """
            cell = data[i]

            now_price = round(price_top * (reduce_rate ** i), 3)  # 当前价位
            now_quotas = round(initial_quotas * (increase_rate ** (i-1)), 3)  # 当前额度
            if i != 0:
                buy_shares = int(now_quotas // (now_price * 100) * 100)  # 当前数量
            else:
                buy_shares = 0
            now_quotas = round(buy_shares * now_price, 3)  # 本次金额

            cell["now_price"] = now_price  # 价格

            amount_money = round(amount_money + now_quotas)
            amount_shares += buy_shares

            # cell["amount_money"] = amount_money  # 累计额度
            # cell["amount_shares"] = amount_shares  # 累计股数

            data[layers - 1 - i]["sell_number"] = buy_shares

            if now_price > start_price:  # 如果大于 起始价位 不操作 但累计
                cell["amount_money"] = 0  # 累计额度
                cell["amount_shares"] = 0  # 累计股数
                cell["buy_shares"] = 0  # 本次数量
                cell["now_quotas"] = 0  # 本次额度
            else:
                if FLAG:  # 第一次 直接计算累计值
                    # amount_shares = int(amount_money // (now_price * 100) * 100)

                    amount_money = round(amount_shares * now_price, 2)

                    cell["amount_shares"] = amount_shares  # 累计数
                    cell["amount_money"] = amount_money  # 累计额度
                    cell["buy_shares"] = amount_shares  # 本次数量
                    cell["now_quotas"] = amount_money  # 本次额度
                    FLAG = False
                else:

                    cell["amount_shares"] = amount_shares  # 累计数
                    cell["amount_money"] = amount_money  # 累计额度
                    cell["buy_shares"] = buy_shares  # 本次数量
                    cell["now_quotas"] = now_quotas  # 本次额度

            cell["average_price"] = round(cell["amount_money"]/cell["amount_shares"] if cell["amount_shares"] else 0, 2)

        sell_money = 0
        for i in data:

            i["position"] = round(i["amount_money"]/amount_money * 100, 1)

            sell_money += i["sell_number"] * i["now_price"]

        profit = int(sell_money - amount_money)
        profit_margin = round(profit / amount_money, 3)
        resp = {"profit_margin": profit_margin, "profit": profit, "amount_money": amount_money, "data": data}
        return resp







