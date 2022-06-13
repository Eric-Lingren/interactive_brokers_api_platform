from asyncio import current_task
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
# from constants.Bar_Durations import BarDurations
# from constants.Security_Types import SecurityTypes
# from constants.Primary_Exchanges import PrimaryExchanges
# from constants.Symbols import Symbols
from config.Config import Config



# vars
orderId = 1

#* Class for IB API Connection
class IBApi(EWrapper, EClient):
    # config = Config()
    
    def __init__(self):
        EClient.__init__(self, self)

    #* Fetch and backfill historical data when bot begins
    def historicalData(self, reqId, bar):
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


    def render_matched_contract_descriptions(self, contractDescriptions):
        for i, contractDescription in enumerate(contractDescriptions):
            print(
                f'[{i}] - ',
                contractDescription.contract.symbol,
                contractDescription.contract.secType,
                contractDescription.contract.primaryExchange,
                contractDescription.contract.currency)


    def select_contract_description(self):
        users_symbol_choice = int(input('Make a selection : '))
        return users_symbol_choice


    def symbolSamples(self, reqId, contractDescriptions):
        if len(contractDescriptions) == 0:
            self.config.set_chosen_contract(None)
        else:
            self.render_matched_contract_descriptions(contractDescriptions)
            choice_int = self.select_contract_description()
            chosen_contract = contractDescriptions[choice_int]            
            self.config.set_chosen_contract(chosen_contract.contract)




# class CustomContract:
#     symbol = None
#     secType = None
#     symbol = None
#     symbol = None
#     symbol = None

#     def __init__(self, symbol, secType, exchange, primaryExchange, currency):
#         self.symbol = symbol
#         self.secType = secType
#         self.exchange = exchange
#         self.primaryExchange = primaryExchange
#         self.currency = currency

# contract = CustomContract(
#     symbol = 'EUR', 
#     secType = 'CASH', 
#     exchange = 'SMART', 
#     primaryExchange = 'IDEALPRO', 
#     currency = 'USD')


#* Bot Logic
class Bot():
    ib = None
    # config = Config(ib)
    bar_size = 1
    bars = []
    config = None

    def __init__(self):
        #* Connect to IB on init
        self.ib = IBApi()
        self.ib.connect('127.0.0.1', 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        
        # self.config = Config(self.ib)

        #* Get symbol info
        # symbol = input('Enter the symbol you want to trade : ')
        # self.config.setup('Do you want to use defaults (y/n) : ', self.ib)
        # self.config.setup('Do you want to use defaults (y/n) : ', self.ib)


        #* Create our IB Contract Object
        # contract = Contract()
        # contract.symbol = self.config.symbol
        # contract.secType = self.config.sec_type 
        # contract.exchange = self.config.exchange
        # contract.primaryExchange = self.config.primary_exchange
        # contract.currency = 'USD'

        contract = Contract()
        contract.symbol = 'EUR'
        contract.secType = 'CASH'
        contract.exchange = 'SMART'
        contract.primaryExchange = 'IDEALPRO'
        contract.currency = 'USD'



        #* Request Market Data
        # Bonds and forex dont require a subscription
        # self.ib.reqRealTimeBars(0, contract, 5, 'MIDPOINT', 1, [])
        # self.ib.reqRealTimeBars(0, contract, 5, 'TRADE', 1, [])

        barsizing = str(self.bar_size)+' min'
        print(barsizing)

        self.ib.reqHistoricalData(1, contract, '', '1 D', barsizing, 'MIDPOINT', 1, 1, True, [])

        # self.ib.reqMarketDataType(4)
        # self.ib.reqMktData(1, contract, '', False, False, [])
        # query_time = datetime.now().astimezone(pytz.timezone('America/New_York'))-timedelta(days=1).strftime('%Y%m%d %H:%M:%S')
        # self.ib.reqHistoricalData(1, contract, '', '2 D', self.config.bar_duration, 'MIDPOINT', 1, 1, True, [])


    # #* Listen to socket in separate thread
    def run_loop(self):
        self.ib.run()


    #* Pass realtime bar data back to our bot object:
    def on_bar_update(self, reqId, bar, is_realtime):
        if is_realtime == False:
            self.bars.append(bar)
            print(self.bars[-1])
        else:
            current_bar_time = datetime.strptime(bar.date, '%Y%m%d %H:%M:%S')
            last_saved_bar_time = datetime.strptime(self.bars[-1].date, '%Y%m%d %H:%M:%S')
            next_requested_bar = last_saved_bar_time + timedelta(minutes=self.bar_size)

            if current_bar_time >= next_requested_bar:
                self.bars.append(bar)
                print(self.bars[-1])





#* Start Bot
# bot = Bot()


# class App:
#     ib = IBApi()
#     bot = None

#     def __init__(self):
#         print('init app')
#         self.ib.connect('127.0.0.1', 7497, 1)
#         ib_thread = threading.Thread(target=self.run_loop, daemon=True)
#         ib_thread.start()
#         time.sleep(1)
#         self.set_configs()

#     def set_configs(self):
#         print('setting configs')

#     def set_configs(self):
#         print('setting bot')
#         self.bot = Bot()

#     #* Listen to socket in separate thread
#     def run_loop(self):
#         print('running loop')
#         self.ib.run()



if __name__ == "__main__":
    # app = App()
    bot = Bot()

# #* Bar Object
# class Bar:
#     open = 0
#     low = 0
#     high = 0
#     close = 0
#     volume = 0
#     date = ''
#     # wap #?
#     # count #?
#     def __init__(self):
#         self.open = 0
#         self.low = 0
#         self.high = 0
#         self.close = 0
#         self.volume = 0
#         self.date = ''
        