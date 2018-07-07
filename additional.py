import datetime


# time
def check_time(first_hour, second_hour):
    current_time = datetime.datetime.now().time().hour
    return first_hour <= current_time <= second_hour
