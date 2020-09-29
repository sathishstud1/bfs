import pandas as pd
import numpy as np
import re
import datetime

week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
weekMap = {week[i]: i for i in range(len(week))}

data = pd.read_csv("../data.csv", names=["Restaurant", "Timing"])


def getDays(day1, day2):
    """Creates a list of the days between the 2 specified days
    Args:
    day1 (str) : Takes the first day of the list to be created

    day2 (str) : Takes the last day of the list to be created

    Returns:
    List: All the days from day1 to day2"""
    return week[weekMap[day1]:weekMap[day2] + 1]


def cleanTime(x):
    """
    Converts the string of timings for each restaurant into a dictionary of Open and close timings for the days that the restaurant is operational

    Args:

    x(str) : Takes the string under the timing column in the dataset as input

    Returns:

    Dictionary : Open and close timings for the days that the restaurant is operational
    """

    res = {}
    for d in week:
        res[d + "Open"] = 0
        res[d + "Close"] = 0

    tsplit = x.split("/")
    for div in tsplit:
        div = div.strip()
        days = re.split(r"[\d:]{1,5}\s*[a|p]m - [\d:]{1,5}\s*[a|p]m", div)[0].strip()
        times = re.findall(r"[\d:]{1,5}\s*[a|p]m - [\d:]{1,5}\s*[a|p]m", div)[0].strip()
        finalTime = []
        assert len(times.split('-')) == 2
        for time in times.split('-'):
            for frmt in ["%I:%M %p", "%I %p"]:
                try:
                    finalTime.append(datetime.datetime.strptime(time.strip(), frmt).time())
                except:
                    pass
        for group in days.split(','):
            if len(group.split('-')) > 1:
                day = group.split('-')
                for i in getDays(day[0].strip(), day[1].strip()):
                    res[i + "Open"] = finalTime[0]
                    res[i + "Close"] = finalTime[1]
            else:
                res[group.strip() + "Open"] = finalTime[0]
                res[group.strip() + "Close"] = finalTime[1]

    return res


dataCopy = pd.read_csv("../data.csv", names=["Restaurant"], usecols=[0])  # Extracting the list of restaurant names
dataCopy = dataCopy.join(
    pd.DataFrame(data["Timing"].apply(cleanTime).tolist()))  # Joining the list of restaurant names with their timings


def query(day, time):
    """Converts the string input of Day and time into a python datetime object and queries the open and close timings data

    Args:

    day(str) : Takes the day of the week as input, inputs can be 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'

    time(str) : Takes the time as input in the format of a 12 hour clock eg: 9:30 pm

    returns: Pandas series object containing all the restaurants open at the given time
    """
    time = datetime.datetime.strptime(time.strip(), "%I:%M %p").time()
    nonZero = dataCopy.loc[(dataCopy[day + "Open"] != 0)]
    return nonZero.loc[(nonZero[day + "Open"] < time) & (nonZero[day + "Close"] > time)].Restaurant


def get_open_places1(day, time, data_path='data.csv'):
    """
    Prints a list of open places
    Args:

    day(str) : Takes the day of the week as input, inputs can be 'Mon','Tue','Wed','Thu','Fri','Sat','Sun'

    time(str) : Takes the time as input in the format of a 12 hour clock eg: 9:30 pm

    data_path(str) : Takes the path of the datafile as input

    returns : None"""
    data = pd.read_csv(data_path, names=["Restaurant", "Timing"])
    dataCopy = pd.read_csv("../data.csv", names=["Restaurant"], usecols=[0])
    dataCopy = dataCopy.join(pd.DataFrame(data["Timing"].apply(cleanTime).tolist()))
    print(query(day, time))


def convertDatetime(datetime):
    Day = datetime.strftime("%A")[:3]
    Time = datetime.strftime("%I:%M") + " " + datetime.strftime("%p").lower()
    return Day, Time


def get_open_places(DateTime_object, data_path='data.csv'):
    """
    Prints a list of open places
    Args:

    DateTime_object(datetime object) : Takes the input as the datetime object of python

    data_path(str) : Takes the path of the datafile as input
SuMon
    returns : None"""

    day, time = convertDatetime(DateTime_object)
    data = pd.read_csv(data_path, names=["Restaurant", "Timing"])
    dataCopy = pd.read_csv("../data.csv", names=["Restaurant"], usecols=[0])
    dataCopy = dataCopy.join(pd.DataFrame(data["Timing"].apply(cleanTime).tolist()))
    print(query(day, time))

#get_open_places(datetime.datetime.now())

day = input("Enter the required day:")
time = input("Enter the time:")
get_open_places1(day=day,time=time)
