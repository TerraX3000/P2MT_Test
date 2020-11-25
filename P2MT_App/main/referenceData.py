from P2MT_App.models import (
    InterventionType,
    FacultyAndStaff,
    ClassSchedule,
    Student,
    SchoolCalendar,
    p2mtTemplates,
    Parents,
    adminSettings,
    apiKeys,
    PblEvents,
)
from P2MT_App import db
from sqlalchemy import distinct
from datetime import date, timedelta
from P2MT_App.main.utilityfunctions import printLogEntry, createListOfDates


def getInterventionTypes():
    interventionValueLabelTupleList = db.session.query(
        InterventionType.id, InterventionType.interventionType
    ).all()
    # Update intervention types to include blank choice as default
    interventionChoices = list(interventionValueLabelTupleList)
    interventionChoices.insert(0, (0, ""))
    return tuple(interventionChoices)


def getInterventionType(intervention_id):
    interventionType = (
        db.session.query(InterventionType.interventionType)
        .filter(InterventionType.id == intervention_id)
        .first()
    )
    return interventionType[0]


def getInterventionId(interventionType):
    interventionId = (
        db.session.query(InterventionType.id)
        .filter(InterventionType.interventionType == interventionType)
        .first()
    )
    return interventionId[0]


def getStaffFromFacultyAndStaff():
    # Get list of staff to display as dropdown choices but exclude system account
    teacherTupleList = (
        db.session.query(
            FacultyAndStaff.id, FacultyAndStaff.firstName, FacultyAndStaff.lastName
        )
        .filter(FacultyAndStaff.lastName != "System")
        .distinct()
        .order_by(FacultyAndStaff.lastName)
        .all()
    )
    teacherValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in teacherTupleList
    ]
    return teacherValueLabelTupleList


def getSystemAccountEmail():
    systemAccountEmail = (
        db.session.query(FacultyAndStaff.email)
        .filter(FacultyAndStaff.lastName == "System")
        .first()
    )
    return systemAccountEmail[0]


def setEmailModeStatus(emailModeStatus):
    # Set email mode statue to enableLiveEmail=True or enableLiveEmail=False
    newAdminSettings = adminSettings(enableLiveEmail=emailModeStatus)
    db.session.add(newAdminSettings)
    return


def getEmailModeStatus():
    emailModeStatus = (
        db.session.query(adminSettings.enableLiveEmail)
        .order_by(adminSettings.id.desc())
        .first()
    )
    return emailModeStatus[0]


def getTeachers():
    teacherValueLabelTupleList = (
        db.session.query(ClassSchedule.teacherLastName, ClassSchedule.teacherLastName)
        .filter(ClassSchedule.campus == "STEM School")
        .distinct()
        .order_by(ClassSchedule.teacherLastName)
        .all()
    )
    # insert a blank option into the list as the default choice
    # Note: need to convert the tuple to a list and then back to a tuple
    teacherList = list(teacherValueLabelTupleList)
    teacherList.insert(0, ("", ""))
    teacherValueLabelTupleList = tuple(teacherList)
    return teacherValueLabelTupleList


def getClassNames():
    classNameValueLabelTupleList = (
        db.session.query(ClassSchedule.className, ClassSchedule.className)
        .filter(ClassSchedule.campus == "STEM School")
        .distinct()
        .order_by(ClassSchedule.className)
        .all()
    )
    # insert a blank option into the list as the default choice
    # Note: need to convert the tuple to a list and then back to a tuple
    classList = list(classNameValueLabelTupleList)
    classList.insert(0, ("", ""))
    classNameValueLabelTupleList = tuple(classList)
    return classNameValueLabelTupleList


def getStemAndChattStateClassNames():
    classNameValueLabelTupleList = (
        db.session.query(ClassSchedule.className, ClassSchedule.className)
        .distinct()
        .order_by(ClassSchedule.className)
        .all()
    )
    # insert a blank option into the list as the default choice
    # Note: need to convert the tuple to a list and then back to a tuple
    classList = list(classNameValueLabelTupleList)
    classList.insert(0, ("", ""))
    classNameValueLabelTupleList = tuple(classList)
    return classNameValueLabelTupleList


def getCampusChoices():
    campusValueLabelTupleList = (
        db.session.query(ClassSchedule.campus, ClassSchedule.campus)
        .distinct()
        .order_by(ClassSchedule.campus.desc())
        .all()
    )
    return campusValueLabelTupleList


def getStudentName(chattStateANumber):
    studentTupleList = (
        db.session.query(Student.firstName, Student.lastName)
        .filter(Student.chattStateANumber == chattStateANumber)
        .first()
    )
    studentName = studentTupleList[0] + " " + studentTupleList[1]
    return studentName


def getStudentFirstNameAndLastName(chattStateANumber):
    studentTupleList = (
        db.session.query(Student.firstName, Student.lastName)
        .filter(Student.chattStateANumber == chattStateANumber)
        .first()
    )
    studentFirstName = studentTupleList[0]
    studentLastName = studentTupleList[1]
    return studentFirstName, studentLastName


def getStudents():
    studentTupleList = (
        db.session.query(Student.chattStateANumber, Student.firstName, Student.lastName)
        .distinct()
        .order_by(Student.lastName)
        .all()
    )
    studentTupleList.insert(0, ("", "", ""))
    studentValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in studentTupleList
    ]
    return studentValueLabelTupleList


def getStudentsById():
    studentTupleList = (
        db.session.query(Student.id, Student.firstName, Student.lastName)
        .distinct()
        .order_by(Student.lastName)
        .all()
    )
    studentTupleList.insert(0, ("", "", ""))
    studentValueLabelTupleList = [
        (item[0], item[1] + " " + item[2]) for item in studentTupleList
    ]
    return studentValueLabelTupleList


def getStudentEmail(chattStateANumber):
    studentEmail = (
        db.session.query(Student.email)
        .filter(Student.chattStateANumber == chattStateANumber)
        .first()
    )
    return studentEmail[0]


def getStudentGoogleCalendar(chattStateANumber):
    studentGoogleCalendar = (
        db.session.query(Student.googleCalendarId)
        .filter(Student.chattStateANumber == chattStateANumber)
        .first()
    )
    return studentGoogleCalendar[0]


def getStudentScheduleLink(chattStateANumber):
    studentGoogleCalendar = getStudentGoogleCalendar(chattStateANumber)
    studentScheduleLink = (
        "https://calendar.google.com/calendar/embed?src=" + studentGoogleCalendar
    )
    return studentScheduleLink


def getParentEmails(chattStateANumber):
    parentEmails = (
        db.session.query(
            Parents.motherEmail, Parents.fatherEmail, Parents.guardianEmail
        )
        .filter(Parents.chattStateANumber == chattStateANumber)
        .first()
    )
    parentEmailList = []
    for email in parentEmails:
        if len(email) == 0 or email == None:
            continue
        parentEmailList.append(email)
    return parentEmailList


def getSchoolYear():
    schoolYearValueLabelTupleList = (
        db.session.query(ClassSchedule.schoolYear, ClassSchedule.schoolYear)
        .distinct()
        .order_by(ClassSchedule.schoolYear.desc())
        .all()
    )
    return schoolYearValueLabelTupleList


def getYearOfGraduation():
    yearOfGraduationValueLabelTupleList = (
        db.session.query(Student.yearOfGraduation, Student.yearOfGraduation)
        .distinct()
        .order_by(Student.yearOfGraduation.desc())
        .all()
    )
    return yearOfGraduationValueLabelTupleList


def getSemester():
    semesterValueLabelTupleList = (
        db.session.query(ClassSchedule.semester, ClassSchedule.semester)
        .distinct()
        .order_by(ClassSchedule.semester.desc())
        .all()
    )
    return semesterValueLabelTupleList


def getSchoolYearChoices():
    schoolYearChoices = [
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
        (2023, 2023),
        (2024, 2024),
        (2025, 2025),
    ]
    return schoolYearChoices


def getSemesterChoices():
    semesterChoices = [
        ("Fall", "Fall"),
        ("Spring", "Spring"),
    ]
    return semesterChoices


def getQuarterChoices():
    quarterChoices = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]
    return quarterChoices


def getPblOptions(quarter):
    pblOptions = (
        db.session.query(PblEvents.pblName)
        .filter(PblEvents.quarter == quarter)
        .order_by(PblEvents.pblName,)
        .distinct()
    )
    pblOptions = [item[0] for item in pblOptions]
    # print(pblOptions)
    return pblOptions


def getPblEventCategoryChoices():
    pblEventCategoryChoices = [
        ("Kickoff", "Kickoff"),
        ("Final", "Final"),
        ("Design Review", "Design Review"),
        ("Sponsor Meeting", "Sponsor Meeting"),
    ]
    return pblEventCategoryChoices


def getClassDayChoices():
    classDayChoices = [
        ("M", "M"),
        ("T", "T"),
        ("W", "W"),
        ("R", "R"),
        ("F", "F"),
    ]
    return classDayChoices


def getStartTimeChoices():
    startTimeChoices = [
        ("09:30", "9:30"),
        ("10:00", "10:00"),
        ("10:30", "10:30"),
        ("11:00", "11:00"),
        ("11:30", "11:30"),
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("13:00", "1:00"),
        ("13:30", "1:30"),
        ("14:00", "2:00"),
        ("14:30", "2:30"),
        ("15:00", "3:00"),
        ("15:30", "3:30"),
        ("16:00", "4:00"),
    ]
    return startTimeChoices


def getEndTimeChoices():
    endTimeChoices = [
        ("10:00", "10:00"),
        ("10:30", "10:30"),
        ("11:00", "11:00"),
        ("11:30", "11:30"),
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("13:00", "1:00"),
        ("13:30", "1:30"),
        ("14:00", "2:00"),
        ("14:30", "2:30"),
        ("15:00", "3:00"),
        ("15:30", "3:30"),
        ("16:00", "4:00"),
        ("16:30", "4:30"),
    ]
    return endTimeChoices


def getHouseNames():
    houseValueLableTupleList = [
        ("", ""),
        ("TBD", "TBD"),
        ("Staupers", "Staupers"),
        ("Tesla", "Tesla"),
        ("Einstein", "Einstein"),
        ("Mirzakhani", "Mirzakhani"),
    ]
    return houseValueLableTupleList


def getGradeLevels():
    gradeLevelTupleList = [
        ("", ""),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    ]
    return gradeLevelTupleList


def getCurrentSchoolYear():
    printLogEntry("getCurrentSchoolYear() function called")
    schoolYear = date.today().year
    print("Current schoolYear =", schoolYear)
    return schoolYear


def getCurrentSemester():
    printLogEntry("getCurrentSemester() function called")
    if date.today().month < 6:
        semester = "Spring"
    else:
        semester = "Fall"
    print("Current month =", date.today().month, "and semester =", semester)
    return semester


def getNextTmiDay():
    today = date.today()
    nextTmiDay = (
        db.session.query(SchoolCalendar.classDate)
        .filter(SchoolCalendar.classDate >= today, SchoolCalendar.tmiDay == True)
        .first()
    )
    print("Next TMI Day =", nextTmiDay[0])
    return nextTmiDay[0]


def getListOfStart_End_Tmi_Days():
    # Create a list of dates comprised of startTmiPeriod, endTmiPeriod, and tmiDay:
    # [startTmiPeriod 1, endTmiPeriod 1, tmi Day 1]
    # [startTmiPeriod 2, endTmiPeriod 2, tmi Day 3]
    # [startTmiPeriod 2, endTmiPeriod 2, tmi Day 3]
    # etc...
    tmiDays = (
        db.session.query(SchoolCalendar.classDate)
        .filter(SchoolCalendar.tmiDay == True)
        .all()
    )
    startTmiPeriodDates = (
        db.session.query(SchoolCalendar.classDate)
        .filter(SchoolCalendar.startTmiPeriod == True)
        .all()
    )
    tmiDaysList = createListOfDates(tmiDays)
    startTmiPeriodDateList = createListOfDates(startTmiPeriodDates)
    endTmiPeriodDateList = []
    # endTmiPeriod is computed by finding the day before the next startTmiPeriod
    # Hence, loop through the startTmiPeriodList beginning with the second element
    for date in startTmiPeriodDateList[1:]:
        endTmiPeriodDate = date - timedelta(days=1)
        endTmiPeriodDateList.append(endTmiPeriodDate)
    ListOfStart_End_Tmi_Days = list(
        zip(startTmiPeriodDateList, endTmiPeriodDateList, tmiDaysList)
    )
    return ListOfStart_End_Tmi_Days


def getCurrent_Start_End_Tmi_Dates():
    ListOfStart_End_Tmi_Days = getListOfStart_End_Tmi_Days()
    nextTmiDay = getNextTmiDay()
    for startTmiPeriod, endTmiPeriod, TmiDay in ListOfStart_End_Tmi_Days:
        if nextTmiDay == TmiDay:
            print(
                "startTmiPeriod =",
                startTmiPeriod,
                "endTmiPeriod =",
                endTmiPeriod,
                "TmiDay =",
                TmiDay,
            )
            break
    return startTmiPeriod, endTmiPeriod, nextTmiDay


def findEarliestPhaseIIDayNoEarlierThan(testDate, dayOfWeek):
    earliestSchoolDayMatch = False
    while not earliestSchoolDayMatch:
        schoolCalendar = (
            db.session.query(SchoolCalendar)
            .filter(
                SchoolCalendar.classDate == testDate,
                SchoolCalendar.phaseIISchoolDay == True,
            )
            .first()
        )
        if schoolCalendar != None:
            if schoolCalendar.day == dayOfWeek:
                earliestDate = schoolCalendar.classDate
                earliestSchoolDayMatch = True
            else:
                testDate = testDate + timedelta(days=1)
        else:
            testDate = testDate + timedelta(days=1)
    return testDate


def getP2mtTemplatesToEdit():
    p2mtTemplatesValueLabelTupleList = (
        db.session.query(p2mtTemplates.id, p2mtTemplates.templateTitle)
        .outerjoin(InterventionType)
        .order_by(
            InterventionType.interventionType,
            p2mtTemplates.interventionLevel,
            p2mtTemplates.templateTitle,
        )
        .all()
    )
    p2mtTemplatesValueLabelTupleList.insert(0, ("", ""))
    return p2mtTemplatesValueLabelTupleList


def getApiKey():
    apikey_json = db.session.query(apiKeys.apiKey).order_by(apiKeys.id.desc()).first()
    return apikey_json[0]
