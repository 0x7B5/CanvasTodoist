import todoist
from canvasapi import Canvas
from datetime import datetime
from dateutil import parser
from dateutil import tz
import time


def getCanvasToken():
    canvas_token = open("Tokens/canvas.txt", "r")
    return canvas_token.read().strip("\n")


def getTodoistToken():
    canvas_token = open("Tokens/todoist.txt", "r")
    return canvas_token.read().strip("\n")


def getCanvasEvents():
    API_URL = "https://canvas.vt.edu"
    canvas = Canvas(API_URL, getCanvasToken())
    events = canvas.get_upcoming_events()

    events_dict = {}

    for item in events:
        if 'assignment' in item:
            date = parser.parse(item['assignment']['due_at'])

            # formated_date = "{}-{}-{} {}:{}".format(date.year,
            # date.month, date.day, date.hour, date.minute)
            formated_date = "{}-{}-{} {}:{}:{}".format(
                date.year, date.month, date.day, date.hour, date.minute, date.second)
            formated_date = convertToUTC(date)
            # formated_date = time.strftime("%Y-%m-%dT%H:%M:%SZ", date)

            title = item['title']

            if formated_date in events_dict:
                events_dict[formated_date].append(title)
            else:
                events_dict[formated_date] = [title]
    return events_dict


def convertToUTC(date):
    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    temp_date = date.replace(tzinfo=from_zone)

    # Convert time zone
    central = temp_date.astimezone(to_zone)

    return central


def addToTodoist(assignments):
    api = todoist.TodoistAPI(getTodoistToken())
    api.sync()

    items = api.state["items"]

    for key, value in assignments.items():
        for i in value:
            if i in items:
                print("woah")
                continue
            else:
                due = {"date": key}
                api.items.add(i, due=due)
                result = api.commit()
                print(result)


def main():
    addToTodoist(getCanvasEvents())


if __name__ == '__main__':
    main()
