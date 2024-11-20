import logging
from .Base import Base

class MultiBuy(Base):
    
    _logger = logging.getLogger(__name__)

    def matchCondition(self):
        if not hasattr(self, 'buy_count'):
            self.buy_count = 0
        if self.buy_count >= int(self.trade['params']['max_buy_count']):
            return False
        if self.buy_count == 0 and self.match_first_buy():
            self.buy_count = 1
            return True
        if self.buy_count >= 1 and self.match_next_buy():
            self.buy_count += 1
            return True
        return False


    def match_first_buy(self):
        close = float(self.dataLastRow['price'])
        pre_close = float(self.dataLastRow['pre_close'])
        percent = (close - pre_close) / pre_close * 100
        limit_open_percent = float(self.trade['params']['limit_open_percent'])
        if percent < limit_open_percent:
            self.pre_buy = close
            MultiBuy._logger.info(f'match_first_buy open_percent = {percent}, limit_open_percent = {limit_open_percent}, close = {close}')
            return True
        return False
    

    def match_next_buy(self):
        if self.pre_buy is None:
            return False
        close = float(self.dataLastRow['price'])
        pre_close = float(self.dataLastRow['pre_close'])
        percent = (self.pre_buy - close) / pre_close * 100
        drop_open_percent = float(self.trade['params']['drop_open_percent']) * self.buy_count
        if percent > drop_open_percent:
            MultiBuy._logger.info(f'match_next_buy {self.buy_count} drop percent from open = {percent}, drop_open_percent = {drop_open_percent}, pre_buy = {self.pre_buy}, close = {close}')
            return True
        return False
    

    def all_buy_done(self):
        return self.buy_count >= int(self.trade['params']['max_buy_count'])