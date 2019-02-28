from binance.client import Client
from api_keys import API_KEY, SECRET


def balances_available(client):
    """ found balances available for the client """
    account_info = client.get_account()
    all_balances = account_info['balances']
    balances = {}
    for balance in all_balances:
        if balance['free'] != '0.00000000':
            balances[balance['asset']] = balance['free']
    return balances


def select_prices(client, currency_1, currency_2, risk):
    """ return current and sell prices """
    # sell price
    klines = client.get_klines(
        symbol=''.join([currency_1, currency_2]),
        interval=client.KLINE_INTERVAL_1MINUTE)
    klines_list_of_dict = [{
        "openTime": data[0],
        "open": data[1],
        "high": data[2],
        "low": data[3],
        "close": data[4],
        "volume": data[5],
        "closeTime": data[6],
        "quoteVolume": data[7],
        "numTrades": data[8],
    } for data in klines]
    close_prices = [
        float(data['close']) for data in klines_list_of_dict[-15:-1]]
    sell_price = max(close_prices)
    # current price
    all_prices = client.get_all_tickers()
    current_prices = {
        data["symbol"]: data["price"] for data in all_prices}
    current_price = float(current_prices[''.join([currency_1, currency_2])])
    # current price with risk
    if risk == "high":
        risk = 0.001
    elif risk == "medium":
        risk = 0.0005
    elif risk == "small":
        risk = 0.0003
    else:
        risk = 0
    risk_price = current_price + (current_price * risk)
    return sell_price, current_price, risk_price


# CLIENT
TRADER = Client(API_KEY, SECRET)
print(balances_available(TRADER))

# TRADE
CURRENCY_1 = 'BTC'
CURRENCY_2 = 'USDT'
RISK = 'small'  # high, medium, small or nothing

OPEN_ORDER = False
while not OPEN_ORDER:
    sell_price, current_price, risk_price = select_prices(
        TRADER, CURRENCY_1, CURRENCY_2, RISK)
    if risk_price < sell_price:
        print(''.join([
            'Current price: ', '1 ', CURRENCY_1,
            ' at ', '{0:.8f}'.format(current_price), ' ', CURRENCY_2,
            '  with risk: ', '{0:.8f}'.format(risk_price),
            ' ||| Wait for selling -> 1 ', CURRENCY_1, ' at ',
            '{0:.8f}'.format(sell_price), ' ', CURRENCY_2]))
    else:
        print("open order ok")
        OPEN_ORDER = True
print("Selling: Waiting for completed")
