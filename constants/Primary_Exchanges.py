from enum import Enum

class PrimaryExchanges(Enum):
    CASH = ['IDEALPRO']
    CRYPTO = ['PAXOS']
    #TODO - scale in exchange options
    STK = ['NASDAQ', 'ARCA']
    IND = ['DTB']
    FUT = ['GLOBEX']

    def get(security_type):
        primary_exchange = PrimaryExchanges[security_type].value
        if len(primary_exchange) == 1:
            return primary_exchange[0]
        else:
            return primary_exchange
            #TODO - add logic to choose correct exchange