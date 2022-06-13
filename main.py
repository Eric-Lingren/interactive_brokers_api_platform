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
    def __init__(self):
        EClient.__init__(self, self)


    #* Fetch and backfill historical data when bot begins
    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            print(e)


    #* On Historical Data End:
    def historicalDataEnd(self, reqId, start, end):
        print('historical data end ', reqId )


    #* On Realtime Bar after historical data has been backfilled:
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
        except Exception as e:
            print(e)


    #* Fetch next valid order id we can use:
    def nextValidId(self, nextOrderId):
        global orderId
        orderId = nextOrderId
        

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




class Config:
    bar_size_int = None 
    bar_size_str = None

    def __init__(self, symbol:str, secType:str, exchange:str, primaryExchange:str, currency:str, bar_size_int:int):
        self.symbol = symbol
        self.secType = secType
        self.exchange = exchange
        self.primaryExchange = primaryExchange
        self.currency = currency
        self.bar_size_int = bar_size_int

        if self.bar_size_int > 1:
            self.bar_size_str = str(self.bar_size_int) + ' mins'
        else: 
            self.bar_size_str = str(self.bar_size_int) + ' min'





class Strategy:
    def run(self, bars):
        print('Running Strategy...')
        print(bars[-1])





#* Bot Logic
class Bot():
    ib = None
    bars = []
    config = None
    contract = Contract()
    strategy = Strategy()

    def __init__(self):
        #* Connect to IB on init
        self.ib = IBApi()
        self.ib.connect('127.0.0.1', 7497, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        #* Set Configs
        self.set_configs() 
        # symbol = input('Enter the symbol you want to trade : ')
        # self.config.setup('Do you want to use defaults (y/n) : ', self.ib)

        #* Create our IB Contract Object
        self.set_contract()


        #* Request Market Data
        # Bonds and forex dont require a subscription
        self.ib.reqHistoricalData(1, self.contract, '', '1 D', self.config.bar_size_str, 'MIDPOINT', 1, 1, True, [])

        # self.ib.reqRealTimeBars(0, contract, 5, 'MIDPOINT', 1, [])
        # self.ib.reqRealTimeBars(0, contract, 5, 'TRADE', 1, [])

        # self.ib.reqMarketDataType(4)
        # self.ib.reqMktData(1, contract, '', False, False, [])
        # query_time = datetime.now().astimezone(pytz.timezone('America/New_York'))-timedelta(days=1).strftime('%Y%m%d %H:%M:%S')
        # self.ib.reqHistoricalData(1, contract, '', '2 D', self.config.bar_duration, 'MIDPOINT', 1, 1, True, [])


    def set_configs(self):
        self.config = Config(
            symbol='EUR', 
            secType='CASH', 
            exchange='SMART', 
            primaryExchange='IDEALPRO', 
            currency='USD',
            bar_size_int = 1
        )


    def set_contract(self):
        self.contract.symbol = self.config.symbol
        self.contract.secType = self.config.secType
        self.contract.exchange = self.config.exchange
        self.contract.primaryExchange = self.config.primaryExchange
        self.contract.currency = self.config.currency


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
            next_requested_bar = last_saved_bar_time + timedelta(minutes=self.config.bar_size_int)

            if current_bar_time >= next_requested_bar:
                self.bars.append(bar)
                #* Run Strategy Evaluations:
                self.strategy.run(self.bars)





#* Start Bot
if __name__ == "__main__":
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
        