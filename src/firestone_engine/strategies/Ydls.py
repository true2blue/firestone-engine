import logging
from .Basic import Basic
from decimal import Decimal
from firestone_engine.Utils import Utils

class Ydls(Basic):

    _logger = logging.getLogger(__name__)

    _MIN_TIME_PERIOD_LENGTH = 2


    def match_data(self):
        if self.is_forece_stop():
            return False
        if(Basic.match_data(self)):
            result = self.match_shape() and self.match_speed() and self.match_money()
            if result:
                self.add_to_force_stop()
            return result
        return False


    def is_forece_stop(self):
        return hasattr(self, 'force_stop') and self.dataLastRow["code"] in self.force_stop


    def add_to_force_stop(self):
        if(not hasattr(self, 'force_stop')):
            self.force_stop = []
        code = self.dataLastRow["code"]
        if code not in self.force_stop:
            self.force_stop.append(code)


    def match_shape(self):
        stock_percent = self.get_current_data_percent()
        index_percent = self.get_current_index_percent()
        high = Decimal(self.dataLastRow['high'])
        low = Decimal(self.dataLastRow['low'])
        open_price = float(self.dataLastRow['open'])
        price = Decimal(self.dataLastRow['price'])
        pre_close = Decimal(self.dataLastRow['pre_close'])
        open_percent = self.get_percent_by_price(open_price, self.dataLastRow)
        if(open_percent < Decimal(self.trade['params']['open_percent']['low']) or open_percent > Decimal(self.trade['params']['open_percent']['high'])):
            return False
        break_top = Utils.round_dec((high - price) / (pre_close) * 100)
        if(break_top > Decimal(self.trade['params']['speed']['break_top'])):
            self.add_to_force_stop()
            Ydls._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, Ydls break_top = {break_top}, force stop')
            return False
        upper_shadow = Utils.round_dec((high - price) / (high - low))
        if(upper_shadow > Decimal(self.trade['params']['speed']['upper_shadow'])):
            return False    
        flag = False
        if(index_percent < 0):
            flag = stock_percent > index_percent * Decimal(self.trade['params']['speed']['ratio_l'])
        else:
            flag = stock_percent > Decimal(self.trade['params']['speed']['ratio_r']) * index_percent
        if(flag):
            Ydls._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, Ydls matched shape upper_shadow = {upper_shadow}, stock_percent = {stock_percent}')
        return flag


    def match_speed(self):
        length = self.get_data_length()
        if(length < Ydls._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time_2'])
        index = int(10 * time) + 1
        index = index * -1 if length >= index else length * -1
        pre_price = Decimal(self.data[index]['price'])
        price = Decimal(self.dataLastRow['price'])
        pre_close = Decimal(self.dataLastRow['pre_close'])
        percent = Utils.round_dec((price - pre_price) / (pre_close) * 100)
        flag = percent >= Decimal(self.trade['params']['speed']['percent'])
        if(flag):
            Ydls._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, Ydls matched speed percnet = {percent}')
        return flag


    
    def match_money(self):
        length = self.get_data_length()
        if(length < Ydls._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time'])
        amount = float(self.trade['params']['speed']['amount']) * 10000
        index = int(10 * time) + 1
        index = index * -1 if length >= index else length * -1
        buy_amount = 0
        while(index < -1):
            pre_amount = float(self.data[index]['amount'])
            next_amount = float(self.data[index + 1]['amount'])
            if(self.is_positive_buy(self.data[index + 1], self.data[index])):
                buy_amount += (next_amount - pre_amount)
            index += 1
        flag = buy_amount >= amount
        if(flag):
            Ydls._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, Ydls matched money buy_amount = {buy_amount}')
        return flag