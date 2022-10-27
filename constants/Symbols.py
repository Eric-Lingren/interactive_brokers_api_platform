
class Symbols:
    symbol_choice = None
    sec_type = None

    def set_symbol( prompt, sec_type):
        # SecurityTypes.print_security_types_choices()
        Symbols.sec_type = sec_type
        while True:
            Symbols.symbol_choice = input(prompt)

            if sec_type == 'STK':
                print('formatting stock ticker')
            
            if sec_type == 'CASH':
                is_valid = Symbols.has_valid_forex_length(Symbols)
                if not is_valid:
                    print("\nINPUT WARNING - Please enter a valid Forex pair.")
                    continue
                else:
                    return Symbols.format_forex_symbol(Symbols)

            if sec_type == 'CRYPTO':
                print('formatting crypto')


    def has_valid_forex_length(self):
        if len(self.symbol_choice) < 6 or len(self.symbol_choice) > 7:
            return False
        else:
            return True


    def format_forex_symbol(self):
        symbol = self.symbol_choice.upper()
        if len(symbol) == 6:
            formatted_symbol = symbol[:3] + '.' + symbol[3:]
            return formatted_symbol
        elif len(symbol) == 7:
            formatted_symbol = symbol[:3] + '.' + symbol[4:]
            return formatted_symbol
        else:
            print('ERROR - Something broke while formatting Forex pair')
        
        

