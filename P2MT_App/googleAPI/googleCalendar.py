# Google Calendar API stuff
import datetime


def addCalendarEvent(
    eventName, location, classDays, startDate, endDate, startTime, endTime, recurrence
):
    startDateTime = datetime.datetime.combine(startDate, startTime)
    endDateTime = datetime.datetime.combine(startDate, endTime)
    endRecurrence = datetime.datetime.combine(endDate, endTime)
    event = {
        "summary": eventName,
        "location": location,
        "description": "",
        "start": {"dateTime": startDateTime, "timeZone": "America/New_York",},
        "end": {"dateTime": endDateTime, "timeZone": "America/New_York",},
        "recurrence": ["RRULE:FREQ=WEEKLY;UNTIL=" + endRecurrence.isoformat(),],
        # 'attendees': [
        #     {'email': 'lpage@example.com'},
        #     {'email': 'sbrin@example.com'},
        # ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    print("New calendar event details:", event)
    googleCalendarEventID = "test"
    return googleCalendarEventID
