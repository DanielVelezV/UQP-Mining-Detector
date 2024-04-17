
from datetime import datetime

day_of_the_week = {
    "1" : "Monday",
    "2" : "Tuesday",
    "3" : "Wednesday",
    "4" : "Thursday",
    "5" : "Friday",
    "6" : "Saturday",
    "7" : "Sunday"
}

time_of_the_day = {
    "A" : 11,
    "B" : 17,
    "C" : 23
}

def __check_moon_cycle(days):
    if days >= 6 and days <= 8:
        return "Weekly"
    elif days >= 13 and days <=15:
        return "Biweekly"
    else:
        return f"Threshold not able to detect it: {days}"

def __check_hours(hours, setted_hours):

    # Threshold in minutes. This refers as 6 minutes. (Using 6 cuz python sucks. should be 5)
    threshold = 0.06

    # Check the diff between the 2 hours
    time = setted_hours - hours

    # abs converts a negative number into a positive. if abs(time) is greater than the threshold, there is more than 5 min diff
    if abs(time) > threshold:
        return False
    
    return True




def is_correct(moon_name, chunk_arrival_date_iso, extraction_start_time_iso):

    arrival     = datetime.fromisoformat(chunk_arrival_date_iso)
    start_time  = datetime.fromisoformat(extraction_start_time_iso)

    calc = arrival - start_time
    
    # Example: Reisen - M1A Monday
    # split result: [Reisen , M1A Monday] and using [1] leave us with [ M1A Monday]
    # lstrip: Remove all spaces on the left. Result: [M1A Monday]
    # split result: [M1A, Monday] and using [0] leave us with [M1A]
    # string slicing ([1:]) result: 1A. Workis like this [star:stop:step]
    mid = moon_name.split("-")[1].lstrip().split(" ")[0][1:]

    # Returns Weekly or BiWeekly. If it doesnt find neither return Error string
    moon_cycle = __check_moon_cycle(calc.days)

    if len(mid) == 1:
        # Old moon
        day     = day_of_the_week[mid[0]]
        hour    = time_of_the_day["A"]

        is_hour_correct = __check_hours(hour, float(arrival.hour + (arrival.minute / 100)))
        is_day_correct = day.lower() == arrival.strftime("%A").lower()

        return is_hour_correct, is_day_correct, moon_cycle, calc
        
    elif len(mid) == 2:
        # Normal moon
        day     = day_of_the_week[mid[0]]
        hour    = time_of_the_day[mid[1]]

        is_hour_correct = __check_hours(hour, float(arrival.hour + (arrival.minute / 100)))
        is_day_correct = day.lower() == arrival.strftime("%A").lower()

        return is_hour_correct, is_day_correct, moon_cycle, calc
    elif len(mid) == 3:
        # BiWeekly Moon
        day     = day_of_the_week[mid[0]]
        hour    = time_of_the_day[mid[1]]
        
        is_hour_correct = __check_hours(hour, float(arrival.hour + (arrival.minute / 100)))
        is_day_correct = day.lower() == arrival.strftime("%A").lower()

        return is_hour_correct, is_day_correct, moon_cycle, calc
    else:
        return None




