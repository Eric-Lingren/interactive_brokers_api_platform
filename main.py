import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
from constants.Bar_Durations import BarDurations
from constants.Security_Types import SecurityTypes
from constants.Primary_Exchanges import PrimaryExchanges



# vars
orderId = 1

#* Class for IB API Connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    #* Fetch and backfill historical data when bot begins
    def historicalData(self, reqId, bar):
        # print(f'Historical Data : {reqId} Date: {bar.date} Open: {bar.open} High: {bar.high} Low: {bar.low} Close: {bar.close} Volume: {bar.volume} Count: {bar.barCount} Weight Average Price (WAP): {bar.average}')
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            print(e)

    #* On Realtime Bar after historical data has been backfilled:
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
        except Exception as e:
            print(e)

    #* On Historical Data End:
    def historicalDataEnd(self, reqId, start, end):
        print('historical data end ', reqId )

    #* Fetch next valid order id we can use:
    def nextValidId(self, nextOrderId):
        global orderId
        orderId = nextOrderId

    # #* Listen for realtime bars:
    # def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
    #     super().bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
    #     try:
    #         bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
    #     except Exception as e:
    #         print(e)
        
    #* Output notifications:
    def error(self, reqId, errorCode, errorMsg):
        print(f'NOTIFY : {reqId} {errorCode} {errorMsg}')

#* Bar Object
class Bar:
    open = 0
    low = 0
    high = 0
    close = 0
    volume = 0
    date = ''
    # wap #?
    # count #?
    def __init__(self):
        self.open = 0
        self.low = 0
        self.high = 0
        self.close = 0
        self.volume = 0
        self.date = ''
        





#* Bot Logic
class Bot:
    ib = None
    bar_duration = BarDurations.HOUR1.value
    sec_type = SecurityTypes.FOREX.value
    exchange = 'SMART'
    primary_exchange = None

    def __init__(self):
        #* Connect to IB on init
        self.ib = IBApi()
        self.ib.connect('127.0.0.1', 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        
        #* Get symbol info
        symbol = input('Enter the symbol you want to trade : ')
        # self.bar_duration = BarDurations.set_bar_durations('Choose the bar duration you want to use : ' )
        # self.sec_type = SecurityTypes.set_security_type('Choose the security type : ' )
        self.primary_exchange = PrimaryExchanges.get(self.sec_type)


        #* Create our IB Contract Object
        contract = Contract()
        contract.symbol = symbol.upper()

        contract.secType = self.sec_type 
        contract.exchange = self.exchange
        contract.primaryExchange = self.primary_exchange
        
        contract.currency = 'USD'

        #* Request Market Data
        # Bonds and forex dont require a subscription
        # self.ib.reqRealTimeBars(0, contract, 5, 'MIDPOINT', 1, [])
        # self.ib.reqRealTimeBars(0, contract, 5, 'TRADE', 1, [])

        # self.ib.reqMarketDataType(4)
        # self.ib.reqMktData(1, contract, '', False, False, [])
        self.ib.reqHistoricalData(1, contract, '', '1 D', self.bar_duration, 'MIDPOINT', 0, 1, False, [])

    #* Listen to socket in separate thread
    def run_loop(self):
        self.ib.run()

    #* Pass realtime bar data back to our bot object:
    def on_bar_update(self, reqId, bar, isRealtime):
        # print(reqId)
        print(bar)
        # print(isRealtime)
    # def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
    #     print(reqId)
    #     print(close)



#* Start Bot
bot = Bot()