import easytrader
from datetime import datetime
# import ptvsd


# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()

user = easytrader.use('universal_client')
user.connect(r'C:/同花顺软件/同花顺/xiadan.exe')
user.enable_type_keys_for_editor()

# print(user.balance)
# print(user.position)
print(f'start buy {datetime.now()}')
result = user.buy('000683', price=3.21, amount=100)
if 'message' in result and result['message'] == 'success':
    print(result['message'])
print(f'end buy {datetime.now()}')
# user.sell('002177', price=9.90, amount=100)
# print(user.today_trades)
entrusts = user.today_entrusts
if entrusts is not None and len(entrusts) > 0:
    for entrust in entrusts:
        if entrust['证券代码'] == '000683' and entrust['操作'] == '买入':
            print('found')
# user.refresh()