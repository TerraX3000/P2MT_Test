from flask import flash, current_app, send_file
from jinja2 import Template
from P2MT_App import db
from P2MT_App.models import p2mtTemplates
from P2MT_App.main.utilityfunctions import printLogEntry


def add_Template(
    templateTitle,
    emailSubject,
    templateContent,
    interventionType,
    interventionLevel,
    sendToStudent,
    sendToParent,
    sendToTeacher,
):
    printLogEntry("add_Template() function called")
    print(templateTitle)
    # Set intervention type or intervention level to None if no choice selected (i.e. = 0)
    if interventionType == 0:
        interventionType = None
    if interventionLevel == 0:
        interventionLevel = None
    newTemplate = p2mtTemplates(
        templateTitle=templateTitle,
        emailSubject=emailSubject,
        templateContent=templateContent,
        intervention_id=interventionType,
        interventionLevel=interventionLevel,
        sendToStudent=sendToStudent,
        sendToParent=sendToParent,
        sendToTeacher=sendToTeacher,
    )
    db.session.add(newTemplate)
    return


def update_Template(
    template_id,
    templateTitle,
    emailSubject,
    templateContent,
    interventionType,
    interventionLevel,
    sendToStudent,
    sendToParent,
    sendToTeacher,
):
    printLogEntry("update_Template() function called")
    templateFromDB = p2mtTemplates.query.get(template_id)
    print(templateTitle)
    # Set intervention type or intervention level to None if no choice selected (i.e. = 0)
    if interventionType == 0:
        interventionType = None
    if interventionLevel == 0:
        interventionLevel = None
    templateFromDB.templateTitle = templateTitle
    templateFromDB.emailSubject = emailSubject
    templateFromDB.templateContent = templateContent
    templateFromDB.intervention_id = interventionType
    templateFromDB.interventionLevel = interventionLevel
    templateFromDB.sendToStudent = sendToStudent
    templateFromDB.sendToParent = sendToParent
    templateFromDB.sendToTeacher = sendToTeacher
    return


def renderEmailTemplate(emailSubject, templateContent, templateParams):
    # Try to render the template but provide a nice message if it fails to render
    # print(emailSubject, templateContent, templateParams)
    try:
        jinja2Template_emailSubject = Template(emailSubject)
        jinja2Rendered_emailSubject = jinja2Template_emailSubject.render(templateParams)
    except:
        jinja2Rendered_emailSubject = (
            "Rendering error.  Fix your template and try again."
        )
    try:
        jinja2Template_templateContent = Template(templateContent)
        jinja2Rendered_templateContent = jinja2Template_templateContent.render(
            templateParams
        )
    except:
        jinja2Rendered_templateContent = (
            "Rendering error.  Fix your template and try again."
        )
    print(jinja2Rendered_emailSubject)
    print(jinja2Rendered_templateContent)
    return jinja2Rendered_emailSubject, jinja2Rendered_templateContent
