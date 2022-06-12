from enum import Enum

class BarDurations(Enum):
    SEC1 = '1 secs'
    SEC5 = '5 secs'
    SEC10 = '10 secs'
    SEC15 = '15 secs'
    SEC30 = '30 secs'
    MIN1 = '1 min'
    MIN2 = '2 mins'
    MIN3 = '3 mins'
    MIN5 = '5 mins'
    MIN10 = '10 mins'
    MIN15 = '15 mins'
    MIN20 = '20 mins'
    MIN30 = '30 mins'
    HOUR1 = '1 hour'
    HOUR2 = '2 hours'
    HOUR3 = '3 hours'
    HOUR4 = '4 hours'
    HOUR8 = '8 hours'
    DAY1 = '1 day'
    WEEK1 = '1W'
    MONTH1 = '1M'

    def print_bar_duration_choices():
        for i, barDuration in enumerate(BarDurations):
            print(f'[{i}] - {barDuration.value}')

    def set_bar_durations(prompt):
        BarDurations.print_bar_duration_choices()
        while True:
            try:
                users_bar_choice = int(input(prompt))
            except ValueError:
                print("\nINPUT WARNING - I didn't understand that, please try again.")
                BarDurations.print_bar_duration_choices()
                continue
            if users_bar_choice < 0 or users_bar_choice >= len(BarDurations):
                print("\nINPUT WARNING - Please make a valid selection.")
                BarDurations.print_bar_duration_choices()
                continue
            else:
                break
        enum_list = list(BarDurations)
        selected_enum_value = enum_list[users_bar_choice].value
        return selected_enum_value
