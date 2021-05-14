import logging
from .Base import Base
from datetime import datetime
from decimal import Decimal
from firestone_engine.Utils import Utils
from ..Constants import Constants

class PPT0(Base):
    
    _logger = logging.getLogger(__name__)

    _MIN_TIME_PERIOD_LENGTH = 15

    def buildPP(self):
        pre_high = Decimal(self.trade['params']['pre']['high'])
        pre_low = Decimal(self.trade['params']['pre']['low'])
        pre_close = Decimal(self.trade['params']['pre']['close'])
        pp = Utils.round_dec((pre_high + pre_low + pre_close) / 3),
        r1 = Utils.round_dec(2 * pp - pre_low)
        r2 = Utils.round_dec(pp + pre_high - pre_low)
        r3 = Utils.round_dec(pre_high + 2 * (pp - pre_low))
        s1 = Utils.round_dec(2 * pp - pre_high)
        s2 = Utils.round_dec(pp - pre_high + pre_low)
        s3 = Utils.round_dec(pre_low - 2 * (pre_high - pp))
        sm1 = (pp + s1) / 2
        sm2 = (s1 + s2) / 2
        sm3 = (s2 + s3) / 2
        rm1 = (pp + r1) / 2
        rm2 = (r1 + r2) / 2
        rm3 = (r2 + r3) / 2
        self.pp = {
            'r3' : r3,
            'rm3' : rm3,
            'r2' : r2,
            'rm2' : rm2,
            'r1' : r1,
            'rm1' : rm1,
            'pp' : pp,
            'sm1' : sm1,
            's1' : s1,
            'sm2' : sm2,
            's2' : s2,
            'sm3' : sm3,
            's3' : s3
        }

    def matchCondition(self):
        self.buildPP()
        if self.trade['state'] == Constants.STATE[6]:
            return self.match_buy_condition()
        return self.match_sell_condition()


    def match_sell_condition(self):
        if Decimal(self.dataLastRow['high']) == Decimal(self.dataLastRow['close']):
            return False
        stop_win = self.get_current_data_percent() - self.get_percent_by_price(self.buy_price, self.dataLastRow)
        if stop_win > Decimal(self.trade['params']['stop_win']):
            PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched stop_win {stop_win}')
            drop_from_high = self.get_percent_by_price(self.dataLastRow['high'], self.dataLastRow) - self.get_current_data_percent()
            if drop_from_high > Decimal(self.trade['params']['drop_from_high']):
                PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched drop_from_high {drop_from_high}')
                self.is_buy = False
                return True
        

    def match_buy_condition(self):
        return self.match_shape() and self.match_money()

    
    def match_shape(self):
        items = list(self.pp.items())[5:]
        open_p = Decimal(self.dataLastRow['open'])
        close = Decimal(self.dataLastRow['close'])
        low = Decimal(self.dataLastRow['low'])
        if close == low:
            self.low_time = datetime.strptime(f'{self.dataLastRow["date"]}{self.dataLastRow["time"]}', '%Y-%m-%d %H:%M:%S')
            return False
        body_length = self.get_percent_by_price(open_p, self.dataLastRow) - self.get_current_data_percent()
        down_shadow_length = self.get_current_data_percent() - self.get_percent_by_price(low, self.dataLastRow)
        if open_p <= close:
            return False
        if body_length > Decimal(self.trade['params']['body_length']):
            PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched body length drop {body_length}')
            ratio = Utils.round_dec(down_shadow_length / body_length)
            if ratio < Decimal(self.trade['params']['down_shadow_body_ratio']):
                PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched down_shadow_body_ratio {ratio}')
                length = len(items)
                for i in range(length):
                    if i + 2 < length:
                        if close < items[i][1] and close > items[i + 1][1]:
                            if low < items[i + 1][1] and low > items[i + 1][1]:
                                close_time = datetime.strptime(f'{self.dataLastRow["date"]}{self.dataLastRow["time"]}', '%Y-%m-%d %H:%M:%S')
                                if Decimal((close_time - self.low_time).seconds) > Decimal(self.trade['params']['close_low_interval_time']):
                                    PPT0._logger.info(f'tardeId = {self.trade["_id"]}, {datetime.now()}, the strategy {self.__class__} matched reverse up from {items[i + 1][0]}')
                                    self.buy_price = close
                                    self.is_buy = True
                                    return True
        return False



    def match_money(self):
        length = self.get_data_length()
        if(length < PPT0._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time'])
        amount = float(self.trade['params']['speed']['amount']) * 10000
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