from constants.Bar_Durations import BarDurations
from constants.Security_Types import SecurityTypes
from constants.Primary_Exchanges import PrimaryExchanges
from constants.Symbols import Symbols

class Config:
    ib = None
    symbol = 'EUR'
    base_currency = 'USD'
    bar_duration = None
    sec_type = None
    exchange = 'SMART'
    primary_exchange = None
    chosen_contract = None

    def __init__(self, ib):
        print('in config init')
        self.ib = ib
        self.bar_duration = BarDurations.MIN1.value
        self.sec_type = SecurityTypes.FOREX.value
        self.primary_exchange = PrimaryExchanges.get(self.sec_type)
        self.setup('Do you want to use defaults (y/n) : ')


    # def setup(self, prompt, ib):
    def setup(self, prompt):
        while True:
            using_defaults = input(prompt).upper()
            if using_defaults != 'Y' and using_defaults != 'N':
                print("\nINPUT WARNING - Please make a valid selection.")
                continue
            else:
                if using_defaults == 'Y':
                    self.print_config()
                else:
                    # self.run_setup()
                    self.set_symbol()
                    self.lookup_symbol()
                break


    # def run_setup(self):
    #     # self.set_sec_types()
    #     # self.set_primary_exchange()
    #     self.set_and_lookup_symbol()
    #     # self.set_bar_durations()

    
    # def set_and_lookup_symbol(self):
    #     self.set_symbol()
    #     self.lookup_symbol()

    def set_symbol(self):
        self.symbol = Symbols.set_symbol('\nEnter the symbol you want to trade : ', self.sec_type)

    def lookup_symbol(self):
        print(self.symbol)
        self.ib.reqMatchingSymbols(211, self.symbol)


    def set_chosen_contract(self, contract):
        if contract == None:
            print('No match found, try searching again')
            self.set_and_lookup_symbol()
        else:
            print('Contract SET')
            self.chosen_contract = contract
            self.symbol = contract.symbol
            self.sec_type = contract.secType
            self.base_currency = contract.currency
            self.primary_exchange = contract.primaryExchange

    def print_config(self):
        print('\n***********************************************')
        print('\n     CONFIGURATION:\n')
        print(f'     Symbol : {self.symbol}')
        print(f'     Base Currency : {self.base_currency}')
        print(f'     Security : {self.sec_type}')
        print(f'     Exchange : {self.exchange}')
        print(f'     Primary Exchange : {self.primary_exchange}')
        print(f'     Bar Duration : {self.bar_duration}')
        print('\n***********************************************\n')



    # def set_sec_types(self):
    #     self.sec_type = SecurityTypes.set_security_type('\nChoose the security type : ' )

    # def set_primary_exchange(self):
    #     self.primary_exchange = PrimaryExchanges.get(self.sec_type)


    # def set_bar_durations(self):
    #     self.bar_duration = BarDurations.set_bar_durations('\nChoose the bar duration you want to use : ' )
