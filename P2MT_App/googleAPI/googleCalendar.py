# Google Calendar API stuff
import datetime
from P2MT_App.main.referenceData import findEarliestPhaseIIDayNoEarlierThan
from P2MT_App.main.utilityfunctions import printLogEntry


def addCalendarEvent(
    eventName, location, classDays, startDate, endDate, startTime, endTime, recurrence
):
    printLogEntry("Running addCalendarEvent()")
    print("classDays =", classDays)
    print("startDate =", startDate)

    # Find the earliest Phase II school day to use as the starting date for the event series
    # Example: if the start date is Monday, Sep 7th and classDays='TR', earliest date will be Tuesday, Sep 8th
    earliestDate = []
    for day in classDays:
        earliestDate.append(findEarliestPhaseIIDayNoEarlierThan(startDate, day))
    earliestDate.sort()
    print("earliestDates sorted =", earliestDate)
    startDate = earliestDate[0]

    # Combine dates and times required for calendar event
    startDateTime = datetime.datetime.combine(startDate, startTime)
    endDateTime = datetime.datetime.combine(startDate, endTime)
    endRecurrence = datetime.datetime.combine(endDate, datetime.time(23, 59, 59))

    # Create BYDAY parameter to specify the days for the recurring event
    byDayList = []
    for day in classDays:
        if day == "M":
            byDayList.append("MO")
        if day == "T":
            byDayList.append("TU")
        if day == "W":
            byDayList.append("WE")
        if day == "R":
            byDayList.append("TH")
        if day == "F":
            byDayList.append("FR")
    byDay = ",".join(byDayList)

    # Create the event following the Google Calendar API
    # https://developers.google.com/calendar/v3/reference/events/insert
    # Recurrence rule per RFC 5545 https://tools.ietf.org/html/rfc5545#section-3.8.5
    event = {
        "summary": eventName,
        "location": location,
        "description": "",
        "start": {
            "dateTime": startDateTime.isoformat(),
            "timeZone": "America/New_York",
        },
        "end": {"dateTime": endDateTime.isoformat(), "timeZone": "America/New_York",},
        "recurrence": [
            "RRULE:FREQ=WEEKLY;UNTIL="
            + endRecurrence.isoformat().replace("-", "").replace(":", "")
            + "Z"
            + ";BYDAY="
            + byDay,
        ],
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

    # Add code to send event to Google Calendar API service object
    # Return the googleCalendarEventID to be added to ClassSchedule table
    googleCalendarEventID = "test"
    return googleCalendarEventID


def deleteCalendarEvent(googleCalendar, googleCalendarEventID):
    printLogEntry("Running deleteCalendarEvent()")
    print(
        "googleCalendar =",
        googleCalendar,
        "googleCalendarEventID =",
        googleCalendarEventID,
    )
    # Reference: https://developers.google.com/calendar/v3/reference/events/delete
    # Add code to create Google Calendar Service object
    # service.events().delete(calendarId=googleCalendar, eventId=googleCalendarEventID).execute()
    return
