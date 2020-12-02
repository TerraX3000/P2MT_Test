from P2MT_App import db
from P2MT_App.main.referenceData import (
    getSchoolYearChoices,
    getSemesterChoices,
    getQuarterChoices,
    getPblEventCategoryChoices,
    getPblOptions,
    getPblOptionsTuple,
    getAcademicYearChoices,
    getSchoolYearAndSemester,
    getCurrentAcademicYear,
    getClassYearOfGraduation,
    getCurrentQuarter,
    getPblEmailRecipientChoices,
    getPblEmailTemplates,
    getQuarterOrdinal,
)
from P2MT_App.main.utilityfunctions import printFormErrors, printLogEntry
from P2MT_App.models import Student, PblEvents, PblTeams, Pbls, p2mtTemplates


# Email Sending Modules
from P2MT_App.p2mtTemplates.p2mtTemplates import renderEmailTemplate
from P2MT_App.googleAPI.googleMail import sendEmail


def sendPblEmails(
    className,
    academicYear,
    quarter,
    emailRecipients,
    selectedEmailRecipients,
    emailTemplate,
):
    # Email Recipient Codes (per referenceData.py)
    # ("-6", "Selected Students"))
    # ("-5", "Students Without a Team"))
    # ("-4", "Students With a Team"))
    # ("-3", "Students Without a PBL"))
    # ("-2", "Students With a PBL"))
    # ("-1", "All Students"))
    # ("0", "Select Recipients..."))

    emailRecipientsBaseQuery = PblTeams.query.outerjoin(Pbls).filter(
        PblTeams.className == className,
        PblTeams.academicYear == academicYear,
        PblTeams.quarter == quarter,
    )
    if emailRecipients < 0:
        if emailRecipients == -1:
            # All Students
            pblEmailRecipients = emailRecipientsBaseQuery
            print("Email Recipients: All Students")
        if emailRecipients == -2:
            # Students with a PBL
            pblEmailRecipients = emailRecipientsBaseQuery.filter(
                PblTeams.pbl_id != None
            )
            print("Email Recipients: Students with a PBL")
        if emailRecipients == -3:
            # Students without a PBL
            pblEmailRecipients = emailRecipientsBaseQuery.filter(
                PblTeams.pbl_id == None
            )
            print("Email Recipients: Students without a PBL")
            print(pblEmailRecipients)
        if emailRecipients == -4:
            # Students with a team
            pblEmailRecipients = emailRecipientsBaseQuery.filter(
                PblTeams.pblTeamNumber != 0
            )
            print("Email Recipients: Students with a team")
        if emailRecipients == -5:
            # Students without a team
            pblEmailRecipients = emailRecipientsBaseQuery.filter(
                PblTeams.pblTeamNumber == 0
            )
            print("Email Recipients: Students without a team")
        if emailRecipients == -6:
            # Selected students
            # Pending future development
            pblEmailRecipients = emailRecipientsBaseQuery.filter(
                PblTeams.chattStateANumber.in_(selectedEmailRecipients)
            )
            print("Email Recipients: Selected students")
    elif emailRecipients > 0:
        pblEmailRecipients = emailRecipientsBaseQuery.filter(
            PblTeams.pbl_id == emailRecipients,
        )
        # pbl = Pbls.query.get_or_404(emailRecipients)
        selectedPbl = Pbls.query.get_or_404(emailRecipients)
        print("Email Recipients: PBL Teams for ", selectedPbl.pblName)
    template = p2mtTemplates.query.get_or_404(emailTemplate)
    print("Email Template:", template.templateTitle)

    for pblTeamMember in pblEmailRecipients:
        print(pblTeamMember.Student.firstName, pblTeamMember.Student.lastName)
        if pblTeamMember.Pbls:

            pblName = pblTeamMember.Pbls.pblName
            pblParams = {
                "pblName": pblTeamMember.Pbls.pblName,
                "pblSponsor": pblTeamMember.Pbls.pblSponsor,
                "pblSponsorPersonName": pblTeamMember.Pbls.pblSponsorPersonName,
                "pblComments": pblTeamMember.Pbls.pblComments,
            }
            # Get kickoff details
            kickoffEvent = PblEvents.query.filter(
                PblEvents.pbl_id == pblTeamMember.pbl_id,
                PblEvents.eventCategory == "Kickoff",
            ).first()
            finalEvent = PblEvents.query.filter(
                PblEvents.pbl_id == pblTeamMember.pbl_id,
                PblEvents.eventCategory == "Final",
            ).first()
            eventParams = {
                "kickoffEventDate": kickoffEvent.eventDate,
                "kickoffStartTime": kickoffEvent.startTime,
                "kickoffEndTime": kickoffEvent.endTime,
                "kickoffEventLocation": kickoffEvent.eventLocation,
                "kickoffEventStreetAddress": kickoffEvent.eventStreetAddress1,
                "kickoffEventCity": kickoffEvent.eventCity,
                "kickoffEventState": kickoffEvent.eventState,
                "kickoffEventZip": kickoffEvent.eventZip,
                "kickoffEventComments": kickoffEvent.eventComments,
                "finalEventDate": finalEvent.eventDate,
                "finalStartTime": finalEvent.startTime,
                "finalEndTime": finalEvent.endTime,
                "finalEventLocation": finalEvent.eventLocation,
                "finalEventStreetAddress": finalEvent.eventStreetAddress1,
                "finalEventCity": finalEvent.eventCity,
                "finalEventState": finalEvent.eventState,
                "finalEventZip": finalEvent.eventZip,
                "finalEventComments": finalEvent.eventComments,
            }
        else:
            pblParams = {}
            eventParams = {}
        basicParams = {
            "chattStateANumber": pblTeamMember.chattStateANumber,
            "studentFirstName": pblTeamMember.Student.firstName,
            "studentLastName": pblTeamMember.Student.lastName,
            "pblTeamNumber": pblTeamMember.pblTeamNumber,
            "academicYear": pblTeamMember.academicYear,
            "semester": pblTeamMember.semester,
            "quarter": pblTeamMember.quarter,
            "quarterOrdinal": getQuarterOrdinal(pblTeamMember.quarter),
        }
        templateParams = {**basicParams, **pblParams, **eventParams}
        email_to = pblTeamMember.Student.email
        emailSubject, emailContent = renderEmailTemplate(
            template.emailSubject, template.templateContent, templateParams
        )
        try:
            email_cc = current_user.email
        except:
            email_cc = ""
        # try:
        sendEmail(email_to, email_cc, emailSubject, emailContent)
        # except:
        #     print("Error sending email")
    return
