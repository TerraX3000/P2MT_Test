from flask import render_template, redirect, url_for, flash, Blueprint, request
from datetime import date, datetime
from P2MT_App import db
from P2MT_App.models import InterventionLog, ClassSchedule, Student
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.interventionInfo.interventionInfo import downloadInterventionLog
from P2MT_App.main.referenceData import (
    getTeachers,
    getClassNames,
    getSchoolYear,
    getSemester,
    getStudents,
    getCampusChoices,
    getYearOfGraduation,
    getClassDayChoices,
    getCurrentSchoolYear,
    getCurrentSemester,
    getInterventionId,
    getStartTimeChoices,
    getEndTimeChoices,
)
from P2MT_App.scheduleAdmin.forms import addSingleClassSchedule
from P2MT_App.scheduleAdmin.routes import addClassSchedule
from P2MT_App.learningLab.learningLab import (
    addLearningLabTimeAndDays,
    propagateLearningLab,
    updatelearningLabList,
)
from P2MT_App.interventionInfo.interventionInfo import (
    add_InterventionLog,
    sendInterventionEmail,
)


learningLab_bp = Blueprint("learningLab_bp", __name__)


@learningLab_bp.route("/learninglab", methods=["GET", "POST"])
def displayLearningLab():
    printLogEntry("Running displayLearningLab()")
    # Learning lab uses the same form as adding a single class schedule
    # This form includes several fields which can be pre-set rather
    # than including the fields on the form
    # Pre-setting the fields will avoid form validation errors later
    addLearningLabDetails = addSingleClassSchedule()
    # Pre-set campus equal to STEM School
    addLearningLabDetails.campus.choices = getCampusChoices()
    addLearningLabDetails.campus.data = "STEM School"
    # Pre-set school year to current school year
    addLearningLabDetails.schoolYear.choices = getSchoolYear()
    addLearningLabDetails.schoolYear.data = getCurrentSchoolYear()
    # Pre-set semester to current semester
    addLearningLabDetails.semester.choices = getSemester()
    addLearningLabDetails.semester.data = getCurrentSemester()
    addLearningLabDetails.teacherName.choices = getTeachers()
    addLearningLabDetails.studentName.choices = getStudents()
    addLearningLabDetails.className.choices = getClassNames()
    addLearningLabDetails.classDays.choices = getClassDayChoices()
    addLearningLabDetails.classDays2.choices = getClassDayChoices()
    addLearningLabDetails.classDays3.choices = getClassDayChoices()
    addLearningLabDetails.classDays4.choices = getClassDayChoices()
    addLearningLabDetails.classDays5.choices = getClassDayChoices()
    addLearningLabDetails.startTime2.choices = getStartTimeChoices()
    addLearningLabDetails.endTime2.choices = getEndTimeChoices()
    addLearningLabDetails.submitAddSingleClassSchedule.label.text = (
        "Submit New Learning Lab"
    )
    print(request.form)
    # Handle form submission for adding new learning lab
    if "submitAddSingleClassSchedule" in request.form:
        if addLearningLabDetails.validate_on_submit():
            printLogEntry("Add Learning Lab submitted")

            schoolYear = addLearningLabDetails.schoolYear.data
            semester = addLearningLabDetails.semester.data
            chattStateANumber = addLearningLabDetails.studentName.data
            teacherLastName = addLearningLabDetails.teacherName.data
            className = addLearningLabDetails.className.data
            startDate = addLearningLabDetails.startDate.data
            endDate = addLearningLabDetails.endDate.data
            online = addLearningLabDetails.online.data
            indStudy = addLearningLabDetails.indStudy.data
            comment = addLearningLabDetails.comment.data
            googleCalendarEventID = addLearningLabDetails.googleCalendarEventID.data
            campus = "STEM School"
            staffID = None
            learningLab = True

            print(
                schoolYear,
                semester,
                chattStateANumber,
                teacherLastName,
                className,
                online,
                indStudy,
                comment,
                googleCalendarEventID,
                learningLab,
            )

            printLogEntry("Adding intervention")
            interventionType = 2
            interventionLevel = 1
            interventionLog = add_InterventionLog(
                chattStateANumber,
                interventionType,
                interventionLevel,
                startDate,
                endDate,
                comment,
            )
            db.session.commit()
            print("new intervention log ID:", interventionLog.id)
            # Store all of the common fields in a single variable for later use
            learningLabCommonFields = [
                schoolYear,
                semester,
                chattStateANumber,
                campus,
                className,
                teacherLastName,
                staffID,
                online,
                indStudy,
                comment,
                googleCalendarEventID,
                interventionLog.id,
                learningLab,
                startDate,
                endDate,
            ]
            # Initialize a list to store details of learning labs for email notifications
            learningLabList = []
            # Process each of the five possible entries of learning lab days/time
            if addLearningLabDetails.addTimeAndDays.data:
                print("Adding learning lab time 1")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays.data,
                    addLearningLabDetails.startTime.data,
                    addLearningLabDetails.endTime.data,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
                )
                learningLabList = updatelearningLabList(
                    learningLabList,
                    addLearningLabDetails.classDays.data,
                    addLearningLabDetails.startTime.data,
                    addLearningLabDetails.endTime.data,
                )
            if addLearningLabDetails.addTimeAndDays2.data:
                startTime2 = datetime.strptime(
                    addLearningLabDetails.startTime2.data, "%I:%M"
                ).time()
                endTime2 = datetime.strptime(
                    addLearningLabDetails.endTime2.data, "%I:%M"
                ).time()
                print("Adding learning lab time 2")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays2.data,
                    startTime2,
                    endTime2,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
                )
                learningLabList = updatelearningLabList(
                    learningLabList,
                    addLearningLabDetails.classDays2.data,
                    startTime2,
                    endTime2,
                )
            if addLearningLabDetails.addTimeAndDays3.data:
                print("Adding learning lab time 3")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays3.data,
                    addLearningLabDetails.startTime3.data,
                    addLearningLabDetails.endTime3.data,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
                )
                learningLabList = updatelearningLabList(
                    learningLabList,
                    addLearningLabDetails.classDays3.data,
                    addLearningLabDetails.startTime3.data,
                    addLearningLabDetails.endTime3.data,
                )
            if addLearningLabDetails.addTimeAndDays4.data:
                print("Adding learning lab time 4")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays4.data,
                    addLearningLabDetails.startTime4.data,
                    addLearningLabDetails.endTime4.data,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
                )
                learningLabList = updatelearningLabList(
                    learningLabList,
                    addLearningLabDetails.classDays4.data,
                    addLearningLabDetails.startTime4.data,
                    addLearningLabDetails.endTime4.data,
                )
            if addLearningLabDetails.addTimeAndDays5.data:
                print("Adding learning lab time 5")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays5.data,
                    addLearningLabDetails.startTime5.data,
                    addLearningLabDetails.endTime5.data,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
                )
                learningLabList = updatelearningLabList(
                    learningLabList,
                    addLearningLabDetails.classDays5.data,
                    addLearningLabDetails.startTime5.data,
                    addLearningLabDetails.endTime5.data,
                )
            print("learningLabList =", learningLabList)
            # Define learning lab parameters for intervention email
            intervention_id = getInterventionId("Academic Behavior")
            interventionLevel = 1
            templateParams = {
                "learningLabList": learningLabList,
                "className": className,
                "teacherLastName": teacherLastName,
            }
            sendInterventionEmail(
                chattStateANumber,
                intervention_id,
                interventionLevel,
                startDate,
                endDate,
                comment,
                templateParams=templateParams,
            )
            return redirect(url_for("learningLab_bp.displayLearningLab"))
    print("addLearningLabDetails.errors: ", addLearningLabDetails.errors)

    # Get list of learning labs to display on learning lab manager
    LearningLabSchedules = (
        db.session.query(ClassSchedule)
        .join(InterventionLog)
        .join(Student)
        .filter(ClassSchedule.learningLab == True)
        .order_by(InterventionLog.endDate.desc(), Student.lastName.asc())
    ).all()

    return render_template(
        "learninglabmanager.html",
        title="Learning Lab",
        addSingleClassSchedule=addLearningLabDetails,
        ClassSchedules=LearningLabSchedules,
    )
