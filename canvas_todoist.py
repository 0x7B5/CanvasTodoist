import todoist
from canvasapi import Canvas
from dateutil import parser


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
            formated_date = "{}-{}-{}".format(date.year, date.month, date.day)
            title = item['title']

            if formated_date in events_dict:
                events_dict[formated_date].append(title)
            else:
                events_dict[formated_date] = [title]
    return events_dict


def main():
    print(getCanvasEvents())


if __name__ == '__main__':
    main()
