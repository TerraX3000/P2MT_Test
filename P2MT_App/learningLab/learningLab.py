import re
from P2MT_App import db
from P2MT_App.scheduleAdmin.ScheduleAdmin import addClassSchedule
from P2MT_App.models import SchoolCalendar, ClassSchedule
from P2MT_App.main.utilityfunctions import printLogEntry, createListOfDates
from P2MT_App.scheduleAdmin.ScheduleAdmin import addClassAttendanceLog


def addLearningLabTimeAndDays(
    learningLabCommonFields, classDays, startTime, endTime,
):

    schoolYear = learningLabCommonFields[0]
    semester = learningLabCommonFields[1]
    chattStateANumber = learningLabCommonFields[2]
    campus = learningLabCommonFields[3]
    className = learningLabCommonFields[4]
    teacherLastName = learningLabCommonFields[5]
    staffID = None
    online = False
    indStudy = False
    comment = learningLabCommonFields[9]
    googleCalendarEventID = None
    interventionLog_id = learningLabCommonFields[11]
    learningLab = learningLabCommonFields[12]

    classDaysList = classDays
    classDays = ""
    for classDay in classDaysList:
        classDays = classDays + classDay

    classSchedule = addClassSchedule(
        schoolYear,
        semester,
        chattStateANumber,
        campus,
        className,
        teacherLastName,
        staffID,
        online,
        indStudy,
        classDays,
        startTime,
        endTime,
        comment,
        googleCalendarEventID,
        interventionLog_id,
        learningLab,
    )

    return classSchedule


def propagateLearningLab(classSchedule_id, startDate, endDate, schoolYear, semester):
    printLogEntry("propagateClassSchedule() function called")
    # Create lists of days to use for propagating class schedule
    schoolCalendar = db.session.query(SchoolCalendar)
    phaseIIDays = schoolCalendar.filter(SchoolCalendar.phaseIISchoolDay)
    dateRange = phaseIIDays.filter(
        SchoolCalendar.classDate >= startDate, SchoolCalendar.classDate <= endDate
    )
    list_of_mondays = createListOfDates(
        dateRange.filter(SchoolCalendar.day == "M").all()
    )
    # print(list_of_mondays)
    list_of_tuesdays = createListOfDates(
        dateRange.filter(SchoolCalendar.day == "T").all()
    )
    # print(list_of_tuesdays)
    list_of_wednesdays = createListOfDates(
        dateRange.filter(SchoolCalendar.day == "W").all()
    )
    list_of_thursdays = createListOfDates(
        dateRange.filter(SchoolCalendar.day == "R").all()
    )
    list_of_fridays = createListOfDates(
        dateRange.filter(SchoolCalendar.day == "F").all()
    )
    # Extract details from class schedule
    learningLabClassSchedule = ClassSchedule.query.get(classSchedule_id)
    print("Propagating learningLabClassSchedule:", learningLabClassSchedule)
    classSchedule_id = learningLabClassSchedule.id
    online = learningLabClassSchedule.online
    indStudy = learningLabClassSchedule.indStudy
    classDays = learningLabClassSchedule.classDays
    meetsOnMonday = re.search("[M]", classDays)
    meetsOnTuesday = re.search("[T]", classDays)
    meetsOnWednesday = re.search("[W]", classDays)
    meetsOnThursday = re.search("[R]", classDays)
    meetsOnFriday = re.search("[F]", classDays)
    if meetsOnMonday and not online and not indStudy:
        # print("Monday:", classSchedule_id, classDays)
        addClassAttendanceLog(classSchedule_id, list_of_mondays)
    if meetsOnTuesday and not online and not indStudy:
        # print("Tuesday:", classSchedule_id, classDays)
        addClassAttendanceLog(classSchedule_id, list_of_tuesdays)
    if meetsOnWednesday and not online and not indStudy:
        # print("Wednesday:", classSchedule_id, classDays)
        addClassAttendanceLog(classSchedule_id, list_of_wednesdays)
    if meetsOnThursday and not online and not indStudy:
        # print("Thursday:", classSchedule_id, classDays)
        addClassAttendanceLog(classSchedule_id, list_of_thursdays)
    if meetsOnFriday and not online and not indStudy:
        # print("Friday:", classSchedule_id, classDays)
        addClassAttendanceLog(classSchedule_id, list_of_fridays)
    return
