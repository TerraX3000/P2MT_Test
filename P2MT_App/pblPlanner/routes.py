from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required
from P2MT_App import db
from P2MT_App.main.referenceData import (
    getSchoolYearChoices,
    getSemesterChoices,
    getQuarterChoices,
    getPblEventCategoryChoices,
    getPblOptions,
)
from P2MT_App.main.utilityfunctions import printFormErrors, printLogEntry
from P2MT_App.pblPlanner.forms import pblEventEditorForm
from P2MT_App.pblPlanner.pblPlanner import downloadPblEvents
from datetime import date
from flask_login import current_user, login_required

# STEM III Drag and Drop
from P2MT_App.models import Student, PblEvents, PblTeams
import json
from datetime import datetime

pblPlanner_bp = Blueprint("pblPlanner_bp", __name__)


# STEM III Drag and Drop
from P2MT_App.models import Student
import json


@pblPlanner_bp.route("/stemiiipblplanner")
@login_required
def displayStemIIIPblPlanner():
    pblEvents = (
        db.session.query(PblEvents)
        .filter(PblEvents.quarter > 0)
        .order_by(
            PblEvents.quarter.desc(),
            PblEvents.eventDate,
            PblEvents.startTime,
            PblEvents.pblName,
        )
    )

    return render_template(
        "pblplanner.html", title="STEM III PBL Planner", pblEvents=pblEvents,
    )


@pblPlanner_bp.route("/stemiiipblplanner/download")
@login_required
def download_PblEvents():
    printLogEntry("Running download_PblEvents()")
    return downloadPblEvents()


@pblPlanner_bp.route("/stemiiiteams")
@login_required
def displayStemIIITeams():
    students = db.session.query(
        Student.firstName, Student.lastName, Student.chattStateANumber
    ).filter(Student.yearOfGraduation == 2022)

    teams = []
    for i in range(1, 31, 1):
        teams.append(f"Team {i}")

    pblOptions = getPblOptions(2)
    pblOptions.insert(0, (""))
    print(pblOptions)
    return render_template(
        "pblteams.html",
        title="STEM III Team Builder",
        students=students,
        teams=teams,
        pblOptions=pblOptions,
    )


@pblPlanner_bp.route("/saveteams", methods=["GET", "POST"])
@login_required
def saveTeams():
    print("Running saveTeams()")
    teamListjson = request.form["teamList"]
    teamList = json.loads(teamListjson)
    for team, teamInfo in teamList.items():
        print(team, teamInfo["teamMemberList"], teamInfo["pblChoice"])
    return redirect(url_for("pblPlanner_bp.displayStemIIITeams"))


@pblPlanner_bp.route("/stemiiipblplanner/<int:log_id>/edit", methods=["POST"])
@login_required
def edit_PblEvent(log_id):
    pblEventEditorFormDetails = pblEventEditorForm()
    pblEventEditorFormDetails.className.choices = [("STEM III", "STEM III")]
    pblEventEditorFormDetails.schoolYear.choices = getSchoolYearChoices()
    pblEventEditorFormDetails.semester.choices = getSemesterChoices()
    pblEventEditorFormDetails.quarter.choices = getQuarterChoices()
    pblEventEditorFormDetails.eventCategory.choices = getPblEventCategoryChoices()

    log = PblEvents.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.pblName} {log.eventCategory}"
    printLogEntry("Running edit_PblEvent(" + LogDetails + ")")

    if "submitEditPblEvent" in request.form:
        print("request.form", request.form)
        if not pblEventEditorFormDetails.validate_on_submit():
            print("Edit PBL Event Form errors")
            printFormErrors(pblEventEditorFormDetails)
        if pblEventEditorFormDetails.validate_on_submit():
            print("submitEditPblEvent submitted")

            # Update the database with the values submitted in the form
            log.className = pblEventEditorFormDetails.className.data
            log.schoolYear = pblEventEditorFormDetails.schoolYear.data
            log.semester = pblEventEditorFormDetails.semester.data
            log.quarter = pblEventEditorFormDetails.quarter.data
            log.pblName = pblEventEditorFormDetails.pblName.data
            log.eventCategory = pblEventEditorFormDetails.eventCategory.data
            log.confirmed = pblEventEditorFormDetails.confirmed.data
            log.eventDate = pblEventEditorFormDetails.eventDate.data

            # Format time values from string objects to time objects
            startTime = datetime.strptime(
                pblEventEditorFormDetails.startTime.data, "%H:%M"
            ).time()
            endTime = datetime.strptime(
                pblEventEditorFormDetails.endTime.data, "%H:%M"
            ).time()

            log.startTime = startTime
            log.endTime = endTime
            log.eventLocation = pblEventEditorFormDetails.eventLocation.data
            log.eventStreetAddress1 = pblEventEditorFormDetails.eventStreetAddress1.data
            log.eventCity = pblEventEditorFormDetails.eventCity.data
            log.eventState = pblEventEditorFormDetails.eventState.data
            log.eventZip = pblEventEditorFormDetails.eventZip.data
            log.eventComments = pblEventEditorFormDetails.eventComments.data
            log.googleCalendarEventID = (
                pblEventEditorFormDetails.googleCalendarEventID.data
            )
            db.session.commit()
            return redirect(url_for("pblPlanner_bp.displayStemIIIPblPlanner"))

    pblName = log.pblName
    print("pblName =", pblName)
    if log:
        pblEventEditorFormDetails.log_id.data = log.id
        pblEventEditorFormDetails.className.data = log.className
        pblEventEditorFormDetails.schoolYear.data = log.schoolYear
        pblEventEditorFormDetails.semester.data = log.semester
        pblEventEditorFormDetails.quarter.data = log.quarter
        pblEventEditorFormDetails.pblName.data = log.pblName
        pblEventEditorFormDetails.eventCategory.data = log.eventCategory
        pblEventEditorFormDetails.confirmed.data = log.confirmed
        pblEventEditorFormDetails.eventDate.data = log.eventDate
        pblEventEditorFormDetails.startTime.data = log.startTime.strftime("%H:%M")
        pblEventEditorFormDetails.endTime.data = log.endTime.strftime("%H:%M")
        pblEventEditorFormDetails.eventLocation.data = log.eventLocation
        pblEventEditorFormDetails.eventStreetAddress1.data = log.eventStreetAddress1
        pblEventEditorFormDetails.eventCity.data = log.eventCity
        pblEventEditorFormDetails.eventState.data = log.eventState
        pblEventEditorFormDetails.eventZip.data = log.eventZip
        pblEventEditorFormDetails.eventComments.data = log.eventComments
        pblEventEditorFormDetails.googleCalendarEventID.data = log.googleCalendarEventID
        print(
            "editPblEventDetails=",
            pblEventEditorFormDetails.log_id.data,
            pblEventEditorFormDetails.pblName.data,
            pblEventEditorFormDetails.eventCategory.data,
        )
    return render_template(
        "pblEventEditor.html",
        title="PBL Event Editor",
        pblEventEditorForm=pblEventEditorFormDetails,
        pblName=pblName,
    )


@pblPlanner_bp.route("/stemiiipblplanner/new", methods=["POST"])
@login_required
def new_PblEvent():
    pblEventEditorFormDetails = pblEventEditorForm()
    pblEventEditorFormDetails.className.choices = [("STEM III", "STEM III")]
    pblEventEditorFormDetails.schoolYear.choices = getSchoolYearChoices()
    pblEventEditorFormDetails.semester.choices = getSemesterChoices()
    pblEventEditorFormDetails.quarter.choices = getQuarterChoices()
    pblEventEditorFormDetails.eventCategory.choices = getPblEventCategoryChoices()
    pblEventEditorFormDetails.log_id.data = 0

    printLogEntry("Running new_PblEvent()")

    if "submitEditPblEvent" in request.form:
        print("request.form", request.form)
        if not pblEventEditorFormDetails.validate_on_submit():
            print("Edit PBL Event Form errors")
            printFormErrors(pblEventEditorFormDetails)
        if pblEventEditorFormDetails.validate_on_submit():
            print("submitEditPblEvent submitted")

            # Update the database with the values submitted in the form
            className = pblEventEditorFormDetails.className.data
            schoolYear = pblEventEditorFormDetails.schoolYear.data
            semester = pblEventEditorFormDetails.semester.data
            quarter = pblEventEditorFormDetails.quarter.data
            pblName = pblEventEditorFormDetails.pblName.data
            eventCategory = pblEventEditorFormDetails.eventCategory.data
            confirmed = pblEventEditorFormDetails.confirmed.data
            eventDate = pblEventEditorFormDetails.eventDate.data

            # Format time values from string objects to time objects
            startTime = datetime.strptime(
                pblEventEditorFormDetails.startTime.data, "%H:%M"
            ).time()
            endTime = datetime.strptime(
                pblEventEditorFormDetails.endTime.data, "%H:%M"
            ).time()

            eventLocation = pblEventEditorFormDetails.eventLocation.data
            eventStreetAddress1 = pblEventEditorFormDetails.eventStreetAddress1.data
            eventCity = pblEventEditorFormDetails.eventCity.data
            eventState = pblEventEditorFormDetails.eventState.data
            eventZip = pblEventEditorFormDetails.eventZip.data
            eventComments = pblEventEditorFormDetails.eventComments.data
            googleCalendarEventID = pblEventEditorFormDetails.googleCalendarEventID.data
            pblEventLog = PblEvents(
                className=className,
                schoolYear=schoolYear,
                semester=semester,
                quarter=quarter,
                pblName=pblName,
                eventCategory=eventCategory,
                confirmed=confirmed,
                eventDate=eventDate,
                startTime=startTime,
                endTime=endTime,
                eventLocation=eventLocation,
                eventStreetAddress1=eventStreetAddress1,
                eventCity=eventCity,
                eventState=eventState,
                eventZip=eventZip,
                eventComments=eventComments,
                googleCalendarEventID=googleCalendarEventID,
            )
            db.session.add(pblEventLog)
            db.session.commit()
            return redirect(url_for("pblPlanner_bp.displayStemIIIPblPlanner"))

    return render_template(
        "pblEventEditor.html",
        title="New PBL Event Editor",
        pblEventEditorForm=pblEventEditorFormDetails,
        pblName=None,
    )


@pblPlanner_bp.route("/stemiiipblplanner/<int:log_id>/delete", methods=["POST"])
@login_required
def delete_PblEvent(log_id):
    log = PblEvents.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.pblName} {log.eventCategory}"
    printLogEntry("Running delete_PblEvent(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("PBL Event has been deleted!", "success")
    return redirect(url_for("pblPlanner_bp.displayStemIIIPblPlanner"))
