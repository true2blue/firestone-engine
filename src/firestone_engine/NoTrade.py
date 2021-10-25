from .Mock import Mock
import logging
from datetime import datetime
from .Constants import Constants

class NoTrade(Mock):

    _logger = logging.getLogger(__name__)


    def createDelegate(self, code, price, volume, op):
        NoTrade._logger.info('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, submit order get response = {}'.format(self.tradeId, code, price, volume, op, 'mock no trade createDelegate success'))
        op_cn = '买入' if op == 'buy' else '卖出'
        message = '订单提交: 在{},以{}{}[{}] {}股'.format(datetime.now(), price, op_cn, code, volume)
        return {'state' : Constants.STATE[2], 'result' : message, 'order' : {'result' : {'data' : {'htbh' : '000000'}}}}


    def queryChenjiao(self, htbh):
        NoTrade._logger.info('mock tradeId = {} htbh = {} query chengjiao, get response = {}'.format(self.tradeId, htbh, 'mock no trade queryChenjiao success'))
        message = '以xx.xx成交xx股,合同编号{}'.format(htbh)
        state = Constants.STATE[4]
        if self.is_T0() and self.strategy.op == 'buy':
            state = Constants.STATE[6]
        if 'auto_cancel' in self.trade['params'] and self.trade['params']['auto_cancel'] == '1':
            return {'state' : Constants.STATE[5], 'result' : '超时未成交，自动取消订单'}
        return {'state' : state, 'result' : message, 'order' : {'result' : {'data' : {'htbh' : '000000'}}}}
        # return {}


    def cancelDelegate(self, htbh, wtrq):
        NoTrade._logger.info('mock tradeId = {} htbh = {} cancel delegate get response = {}'.format(self.tradeId, htbh, 'mock no trade cancelDelegate success'))
        return {'state' : Constants.STATE[0], 'result' : '合同[{}]已撤销'.format(htbh)}


