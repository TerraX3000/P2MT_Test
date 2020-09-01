from flask import flash, current_app, send_file
from P2MT_App import db
from P2MT_App.models import InterventionLog, Student, FacultyAndStaff, InterventionType
from P2MT_App.main.utilityfunctions import printLogEntry
import os
import csv
from datetime import datetime


def add_InterventionLog(
    chattStateANumber,
    interventionType,
    interventionLevel,
    startDate,
    endDate,
    comment,
    tmiMinutes=None,
):
    printLogEntry("add_InterventionLog() function called")
    print(chattStateANumber, interventionType, interventionLevel, startDate, endDate)
    interventionLog = InterventionLog(
        intervention_id=interventionType,
        interventionLevel=interventionLevel,
        startDate=startDate,
        endDate=endDate,
        comment=comment,
        staffID=1,
        chattStateANumber=chattStateANumber,
        tmiMinutes=tmiMinutes,
    )
    db.session.add(interventionLog)
    return interventionLog


def downloadInterventionLog():
    printLogEntry("downloadDailyAttendanceLog() function called")
    # Create a CSV output file and append with a timestamp
    output_file_path = os.path.join(current_app.root_path, "static/download")
    output_file_path = "/tmp"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    csvFilename = output_file_path + "/" + "intervention_log_" + timestamp + ".csv"
    csvOutputFile = open(csvFilename, "w")
    csvOutputWriter = csv.writer(
        csvOutputFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    # Write header row for CSV file
    csvOutputWriter.writerow(
        [
            "chattStateANumber",
            "firstName",
            "lastName",
            "interventionType",
            "interventionLevel",
            "logEntryDate",
            "startDate",
            "endDate",
            "staffLastName",
            "comment",
        ]
    )
    csvOutputFileRowCount = 0
    # Query for information
    interventionLogs = (
        InterventionLog.query.join(InterventionType)
        .join(Student)
        .join(FacultyAndStaff)
        .order_by(Student.lastName)
        .all()
    )
    # Process each record in the query and write to the output file
    for log in interventionLogs:
        csvOutputWriter.writerow(
            [
                log.Student.chattStateANumber,
                log.Student.firstName,
                log.Student.lastName,
                log.InterventionType.interventionType,
                log.interventionLevel,
                log.createDate,
                log.startDate,
                log.endDate,
                log.FacultyAndStaff.lastName,
                log.comment,
            ]
        )
        csvOutputFileRowCount = csvOutputFileRowCount + 1
    csvOutputFile.close()
    return send_file(csvFilename, as_attachment=True, cache_timeout=0)
