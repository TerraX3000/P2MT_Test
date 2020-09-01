from flask import render_template, redirect, url_for, flash, Blueprint, request
from datetime import date
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
)
from P2MT_App.scheduleAdmin.forms import addSingleClassSchedule
from P2MT_App.scheduleAdmin.routes import addClassSchedule
from P2MT_App.learningLab.learningLab import (
    addLearningLabTimeAndDays,
    propagateLearningLab,
)
from P2MT_App.interventionInfo.interventionInfo import add_InterventionLog


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
    addLearningLabDetails.submitAddSingleClassSchedule.label.text = (
        "Submit New Learning Lab"
    )
    print(request.form)
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
            ]
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
            if addLearningLabDetails.addTimeAndDays2.data:
                print("Adding learning lab time 2")
                learningLabClassSchedule = addLearningLabTimeAndDays(
                    learningLabCommonFields,
                    addLearningLabDetails.classDays2.data,
                    addLearningLabDetails.startTime2.data,
                    addLearningLabDetails.endTime2.data,
                )
                propagateLearningLab(
                    learningLabClassSchedule.id,
                    startDate,
                    endDate,
                    schoolYear,
                    semester,
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
            return redirect(url_for("learningLab_bp.displayLearningLab"))
    print("addLearningLabDetails.errors: ", addLearningLabDetails.errors)

    # LearningLabSchedules = (
    #     ClassSchedule.query.join(InterventionLog, ClassSchedule.Student)
    #     .filter(ClassSchedule.learningLab == True)
    #     .order_by(
    #         ClassSchedule.Student.id.asc(),
    #         ClassSchedule.InterventionLog.endDate.desc(),
    #     )
    # )
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
