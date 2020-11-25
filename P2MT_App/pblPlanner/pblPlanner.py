from flask import send_file, current_app
from P2MT_App import db
from P2MT_App.models import PblEvents
from P2MT_App.main.utilityfunctions import download_File, printLogEntry
from datetime import datetime, date, time
import re
import os
import csv


def downloadPblEvents():
    printLogEntry("downloadPblEvents() function called")
    # Create a CSV output file and append with a timestamp
    output_file_path = os.path.join(current_app.root_path, "static/download")
    output_file_path = "/tmp"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csvFilename = output_file_path + "/" + "pbl_events_" + timestamp + ".csv"
    csvOutputFile = open(csvFilename, "w")
    csvOutputWriter = csv.writer(
        csvOutputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # Write header row for CSV file
    csvOutputWriter.writerow(
        [
            "Class",
            "School Year",
            "Semester",
            "Quarter",
            "PBL Name",
            "Event Category",
            "Confirmed",
            "Event Date",
            "Start Time",
            "End Time",
            "Event Location",
            "Event Street Address",
            "Event City",
            "Event State",
            "Event Zip",
            "Event Comments",
            "googleCalendarEventID",
        ]
    )
    csvOutputFileRowCount = 0
    # Query the PblEvents with a join to include student information
    pblEvents = PblEvents.query.order_by(
        PblEvents.quarter, PblEvents.eventDate, PblEvents.startTime, PblEvents.pblName
    )
    # Process each record in the query and write to the output file
    for pblEvent in pblEvents:
        className = pblEvent.className
        schoolYear = pblEvent.schoolYear
        semester = pblEvent.semester
        quarter = pblEvent.quarter
        pblName = pblEvent.pblName
        eventCategory = pblEvent.eventCategory
        confirmed = pblEvent.confirmed
        eventDate = pblEvent.eventDate
        startTime = pblEvent.startTime
        endTime = pblEvent.endTime
        eventLocation = pblEvent.eventLocation
        eventStreetAddress1 = pblEvent.eventStreetAddress1
        eventCity = pblEvent.eventCity
        eventState = pblEvent.eventState
        eventZip = pblEvent.eventZip
        eventComments = pblEvent.eventComments
        googleCalendarEventID = pblEvent.googleCalendarEventID

        csvOutputWriter.writerow(
            [
                className,
                str(schoolYear),
                semester,
                str(quarter),
                pblName,
                eventCategory,
                confirmed,
                eventDate.strftime("%Y-%m-%d"),
                startTime.strftime("%-I:%M %p"),
                endTime.strftime("%-I:%M %p"),
                eventLocation,
                eventStreetAddress1,
                eventCity,
                eventState,
                eventZip,
                eventComments,
                googleCalendarEventID,
            ]
        )
        csvOutputFileRowCount = csvOutputFileRowCount + 1
    csvOutputFile.close()
    return send_file(csvFilename, as_attachment=True, cache_timeout=0)
