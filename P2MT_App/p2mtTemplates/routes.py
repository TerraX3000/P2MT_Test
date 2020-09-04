from flask import render_template, redirect, url_for, flash, Blueprint, request
from jinja2 import Template
from P2MT_App import db
from P2MT_App.models import p2mtTemplates
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.p2mtTemplates.forms import (
    submitNewTemplateForm,
    chooseTemplateToEditForm,
    editTemplateForm,
)
from P2MT_App.p2mtTemplates.p2mtTemplates import add_Template, update_Template
from P2MT_App.main.referenceData import getInterventionTypes, getP2mtTemplatesToEdit
from datetime import date

p2mtTemplates_bp = Blueprint("p2mtTemplates_bp", __name__)


@p2mtTemplates_bp.route("/p2mttemplates", methods=["GET", "POST"])
def displayTemplates():
    printLogEntry("displayEmailTemplates() function called")
    newTemplateFormDetails = submitNewTemplateForm()
    # print("newTemplateFormDetails", newTemplateFormDetails.templateTitle)
    newTemplateFormDetails.interventionType.choices = getInterventionTypes()

    # Populate the selection form with the existing templates to choose edit
    chooseTemplateToEdit = chooseTemplateToEditForm()
    chooseTemplateToEdit.templateTitle.choices = getP2mtTemplatesToEdit()

    editTemplateFormDetails = editTemplateForm()
    editTemplateFormDetails.interventionType.choices = getInterventionTypes()

    if "submitNewTemplate" in request.form:
        if newTemplateFormDetails.validate_on_submit():
            printLogEntry("New Template Submitted")
            print("templateFormDetails=", request.form)
            add_Template(
                newTemplateFormDetails.templateTitle.data,
                newTemplateFormDetails.emailSubject.data,
                newTemplateFormDetails.templateContent.data,
                newTemplateFormDetails.interventionType.data,
                newTemplateFormDetails.interventionLevel.data,
                newTemplateFormDetails.sendToStudent.data,
                newTemplateFormDetails.sendToParent.data,
                newTemplateFormDetails.sendToTeacher.data,
            )
            db.session.commit()
            flash("New template has been added!", "success")
            return redirect(url_for("p2mtTemplates_bp.displayTemplates"))

    if "submitUpdatedTemplate" in request.form:
        if editTemplateFormDetails.validate_on_submit():
            printLogEntry("Updated Template Submitted")
            print("editTemplateFormDetails=", request.form)
            update_Template(
                editTemplateFormDetails.template_id.data,
                editTemplateFormDetails.templateTitle.data,
                editTemplateFormDetails.emailSubject.data,
                editTemplateFormDetails.templateContent.data,
                editTemplateFormDetails.interventionType.data,
                editTemplateFormDetails.interventionLevel.data,
                editTemplateFormDetails.sendToStudent.data,
                editTemplateFormDetails.sendToParent.data,
                editTemplateFormDetails.sendToTeacher.data,
            )
            db.session.commit()
            flash("New template has been added!", "success")
            return redirect(url_for("p2mtTemplates_bp.displayTemplates"))

    # Return the current template details of the form selected for editing
    if "chooseTemplateToEdit" in request.form:
        print("chooseTemplateToEdit form", request.form)
        emailTemplate = p2mtTemplates.query.filter(
            p2mtTemplates.id == chooseTemplateToEdit.templateTitle.data
        ).first()
        if emailTemplate:
            editTemplateFormDetails.template_id.data = emailTemplate.id
            editTemplateFormDetails.templateTitle.data = emailTemplate.templateTitle
            editTemplateFormDetails.emailSubject.data = emailTemplate.emailSubject
            editTemplateFormDetails.templateContent.data = emailTemplate.templateContent
            editTemplateFormDetails.interventionType.data = (
                emailTemplate.intervention_id
            )
            editTemplateFormDetails.interventionLevel.data = (
                emailTemplate.interventionLevel
            )
            editTemplateFormDetails.sendToStudent.data = emailTemplate.sendToStudent
            editTemplateFormDetails.sendToParent.data = emailTemplate.sendToParent
            editTemplateFormDetails.sendToTeacher.data = emailTemplate.sendToTeacher
    else:
        editTemplateFormDetails = None

    return render_template(
        "p2mttemplates.html",
        title="Email Templates",
        templateForm=newTemplateFormDetails,
        chooseTemplateToEdit=chooseTemplateToEdit,
        editTemplateForm=editTemplateFormDetails,
    )


@p2mtTemplates_bp.route("/p2mttemplates/<int:log_id>/delete", methods=["POST"])
def delete_p2mtTemplate(log_id):
    log = p2mtTemplates.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.templateTitle}"
    printLogEntry("Running delete_p2mtTemplate(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("Template has been deleted!", "success")
    return redirect(url_for("p2mtTemplates_bp.displayTemplates"))


@p2mtTemplates_bp.route("/printtemplate")
def sendDressCodeInterventionEmail():
    chattStateANumber = "A12345678"
    subject = "STEM Dress Intervention"
    interventionID = 4
    interventionLevel = 1
    templateParams = {"startDate": date(2020, 9, 1), "endDate": date(2020, 9, 8)}
    sendInterventionEmail(
        chattStateANumber, subject, interventionID, interventionLevel, templateParams
    )
    return redirect(url_for("p2mtTemplates_bp.displayTemplates"))


def getInterventionTemplate(interventionID, interventionLevel):
    interventionEmailTemplate = (
        p2mtTemplates.query()
        .filter(
            p2mtTemplates.intervention_id == interventionID,
            p2mtTemplates.interventionLevel == interventionLevel,
        )
        .first()
    )
    return interventionEmailTemplate


def sendInterventionEmail(
    chattStateANumber, subject, interventionID, interventionLevel, templateParams
):
    studentOnlyFlag = False
    #   formatStudentAndParentEmailAddress(Chatt_State_A_Number, connection, studentOnlyFlag)
    interventionEmailTemplate = p2mtTemplates.query.filter(
        p2mtTemplates.intervention_id == interventionID,
        p2mtTemplates.interventionLevel == interventionLevel,
    ).first()

    if interventionEmailTemplate != None:
        jinja2_email_subject = Template(interventionEmailTemplate.emailSubject)
        print(
            jinja2_email_subject.render(
                studentFirstName=chattStateANumber, studentLastName=chattStateANumber
            )
        )
        jinja2_template_content = Template(interventionEmailTemplate.templateContent)
        print(
            jinja2_template_content.render(
                studentFirstName=chattStateANumber,
                startDate=templateParams["startDate"],
                endDate=templateParams["endDate"],
            )
        )

    # Applying template parameters
    # bodyTemplate = HtmlService.createTemplate(templateBlob)
    # bodyTemplate.data = templateParams
    # body = bodyTemplate.evaluate().getContent()

    # Sending email
    # sendEmail(to, subject, body)

    # console.log('sendInterventionEmail: Intervention=' + interventionID + ' level=' + level + ' interventionTemplate=' + interventionTemplate)
    return


# Generic_Intervention_Template = '1xBroas-qCXOAP2wrlLMKQERjyYMX-Ycv'

# Conduct_Behavior_Level_I = Generic_Intervention_Template
# Conduct_Behavior_Level_II = Generic_Intervention_Template
# Conduct_Behavior_Level_III = Generic_Intervention_Template
# Conduct_Behavior_Level_IV = Generic_Intervention_Template
# Conduct_Behavior_Level_V = Generic_Intervention_Template
# Conduct_Behavior_Level_VI = Generic_Intervention_Template

# Academic_Behavior_Level_I = '1xIUXl6E19CdEg-10ZypZuIQDMpa2p5h-'
# Academic_Behavior_Level_II = null
# Academic_Behavior_Level_III = null
# Academic_Behavior_Level_IV = null


# Dress_Code_Level_I = '1x7GPQ1l0SIllywFvecSM2l-pNfTuxzKw'
# Dress_Code_Level_II = '1x7H_A1eSnt8jjNjv6DU2m62FwFEO7Y8I'
# Dress_Code_Level_III = '1xIrkcJVOrA-XIk2DQBzBfmcQrQZ298I5'
# Dress_Code_Level_IV = null
# Dress_Code_Level_V = null
# Dress_Code_Level_VI = null

# newDailyAttendanceTemplate = '1AbJSjLS6TLd5vosETidx1aZZ7Fo1MaMj'

# Attendance_Level_I_Student_Notification = '1FQwrHEpJczDZ-CdJiNrzq3TW3-Kbxn4q'
# Attendance_Level_I_Parent_Notification = '1FiiPttDWc5LxiqNQbluViV_D6WH_iS9L'

# tmiSignInSignOutEmailNotification = '1GXHTsF-uqTOmg5rLGIGtFsO0QRCk3mJ6'
# parentApprovalOfStudentSchedule = '1QVccoW1dxoz5gehCpWSZccHPIe0Hp3LJ'

# ER_PARENT_NOTIFICATION = '1vW6GK_nLnf_7pCCwVHSwPmZdGhI-PA76'
# PBL_TEAM_EMAIL_NOTIFICATION = '1xZevW6nZdD4vxwBLKYReWjYhQhxOufkH'
# SLC_PARENT_NOTIFICATION = '1gZoHyygqINsZWUEsTdW-Kd7cJMxqxfIw'

