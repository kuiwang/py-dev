# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得top address,
因使用了br编码，引入了 brotli包
@author: user
'''
import os, sys
import logging
import requests, json
from importlib import reload


reload(sys)  
# sys.setdefaultencoding('utf8')

# PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
BASE_API = "https://blockchain.info/multiaddr?active={}"
PROCESS_NUM = 50
logger = logging.getLogger('blockchain_api')
LOG_FILE = 'blockchain_api.log'
LOG_FORMATTER = '%(message)s'
s = requests.Session()




def dev():
    api_key="pSHiIEN5mRRa02ggWQaqKVAwDMVlZ5vfGZRQWfqal8l0FE9m7IzQ76Ijm6SnOJyr"
    api_secret="VoIf886L88O81W1AgMEd7OeqZrhAQzjKvLWg0eIzNXOhIiCPX24SCCYWQrFZ0Um5"
    from binance.client import Client
    client = Client(api_key, api_secret)
    
    # get market depth
    #depth = client.get_order_book(symbol='BNBBTC')
    #print(depth)
    
    # place a test market buy order, to place an actual order use the create_order function
    '''
    order = client.create_test_order(
        symbol='BNBBTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=100)
    print(order)
    '''
    # get all symbol prices
    #prices = client.get_all_tickers()
    #print(prices)

    # withdraw 100 ETH
    # check docs for assumptions around withdrawals
    '''
    from binance.exceptions import BinanceAPIException, BinanceWithdrawException
    try:
        result = client.withdraw(
            asset='ETH',
            address='<eth_address>',
            amount=100)
    except BinanceAPIException as e:
        print(e)
    except BinanceWithdrawException as e:
        print(e)
    else:
        print("Success")
    '''

    # fetch list of withdrawals
    withdraws = client.get_withdraw_history()
    print(withdraws)
    
    # fetch list of ETH withdrawals
    eth_withdraws = client.get_withdraw_history(asset='ETH')
    print(eth_withdraws)
    
    # get a deposit address for BTC
    address = client.get_deposit_address(asset='BTC')
    print(address)

if __name__ == '__main__':
    dev()
    
