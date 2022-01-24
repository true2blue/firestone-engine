import logging
from .Base import Base
from datetime import datetime
from decimal import Decimal
from firestone_engine.Utils import Utils
from ..Constants import Constants

class PPT0(Base):
    
    _logger = logging.getLogger(__name__)
    
    _MIN_TIME_PERIOD_LENGTH = 15


    def matchCondition(self):
        if self.trade['state'] == Constants.STATE[0]:
            self.op = 'buy'
            return self.match_buy_condition()
        elif self.trade['state'] == Constants.STATE[6]:
            self.op = 'sell'
            return self.match_sell_condition()
        return False


    def match_sell_condition(self):
        close = float(self.dataLastRow['price'])
        if(not hasattr(self, 'high')):
            self.high = close
        elif close > self.high:
            self.high = close
        stop_win = self.get_current_data_percent() - self.get_percent_by_price(self.buy_price, self.dataLastRow)
        if hasattr(self, 'start_stop_win') or stop_win > Decimal(self.trade['params']['stop_win']):
            self.start_stop_win = True
            PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched stop_win {stop_win}')
            drop_from_high = self.get_percent_by_price(self.high, self.dataLastRow) - self.get_current_data_percent()
            if drop_from_high > Decimal(self.trade['params']['drop_from_high']):
                PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched drop_from_high {drop_from_high}')
                return True
        if self.dataLastRow["time"] > self.trade['params']['force_sell_time']:
            PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched force_sell_time {self.dataLastRow["time"]}')
            return True    
        return False
        

    def match_buy_condition(self):
        flag = self.match_shape() and self.match_speed() and self.match_money()
        if flag:
            self.buy_price = float(self.dataLastRow['price'])
        return flag

    
    def match_shape(self):
        close = float(self.dataLastRow['price'])
        open_p = float(self.dataLastRow['open'])
        pre_close = float(self.dataLastRow['pre_close'])
        drop_percent_from_open = (close - open_p) / pre_close * 100
        start_buy_line = float(self.trade['params']['start_buy_line'])
        target_p = Utils.round_dec(start_buy_line * -1 / 100 * pre_close + open_p)
        low_limit = Utils.round_dec(pre_close * 0.9)
        if hasattr(self, 'start_monitor') or (drop_percent_from_open < 0 and abs(drop_percent_from_open) >= start_buy_line) or (low_limit >= target_p and self.trade['params']['buy_on_low_limit'] == '1'):
            PPT0._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, PPT0 matched buy_shape, open_p = {open_p}, target_p = {target_p}, low_limit = {low_limit}, start_buy_line= {start_buy_line}, close={close}, pre_close={pre_close}')
            self.start_monitor = True
            low = float(self.dataLastRow['low'])
            percent = Utils.round_dec((close - low) / pre_close * 100)
            min_rebound = Decimal(self.trade['params']['min_rebound'])
            max_rebound = Decimal(self.trade['params']['max_rebound'])
            if percent >= min_rebound and percent <= max_rebound:
                PPT0._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, PPT0 matched rebound low={low}, percent={percent}, min_rebound={min_rebound}, max_rebound={max_rebound}')
                return True
        return False
    
    
    def match_speed(self):
        length = self.get_data_length()
        if(length < PPT0._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time_2'])
        index = int(20 * time) + 1
        index = index * -1 if length >= index else length * -1
        pre_price = Decimal(self.data[index]['price'])
        price = Decimal(self.dataLastRow['price'])
        pre_close = Decimal(self.dataLastRow['pre_close'])
        percent = Utils.round_dec((price - pre_price) / (pre_close) * 100)
        flag = percent >= Decimal(self.trade['params']['speed']['percent'])
        if(flag):
            PPT0._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, PPT0 matched speed percnet = {percent}')
        return flag


    def match_money(self):
        length = self.get_data_length()
        if(length < PPT0._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['money']['time'])
        amount = float(self.trade['params']['money']['amount']) * 10000
        index = int(20 * time) + 1
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
            PPT0._logger.info(f'TradeId = {self.trade["_id"]}, Code={self.dataLastRow["code"]}, PPT0 matched money buy_amount = {buy_amount}')
        return flag