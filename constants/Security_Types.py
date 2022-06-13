from enum import Enum

#! See types here https://interactivebrokers.github.io/tws-api/basic_contracts.html
class SecurityTypes(Enum):
    FOREX = 'CASH'
    CRYPTO = 'CRYPTO'
    STOCK = 'STK'
    # INDEX = 'IND'
    # CFD = 'CFD'
    # FUTURE = 'FUT'
    # OPTION = 'OPT'
    # FUTURE_OPTION = 'FOP'
    # BOND = 'BOND'
    # MUTUAL_FUND = 'FUND'
    # COMMODITY = 'CMDTY'

    def print_security_types_choices():
        for i, security_type in enumerate(SecurityTypes):
            print(f'[{i}] - {security_type.name}')

    def set_security_type(prompt):
        SecurityTypes.print_security_types_choices()
        while True:
            try:
                users_security_choice = int(input(prompt))
            except ValueError:
                print("\nINPUT WARNING - I didn't understand that, please try again.")
                SecurityTypes.print_security_types_choices()
                continue
            if users_security_choice < 0 or users_security_choice >= len(SecurityTypes):
                print("\nINPUT WARNING - Please make a valid selection.")
                SecurityTypes.print_security_types_choices()
                continue
            else:
                break
        enum_list = list(SecurityTypes)
        selected_enum_value = enum_list[users_security_choice].value
        return selected_enum_value