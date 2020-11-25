from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    HiddenField,
    SubmitField,
    StringField,
    SelectField,
    TimeField,
    BooleanField,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
from P2MT_App.main.referenceData import getStartTimeChoices, getEndTimeChoices


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class selectSingleClassScheduleToEditForm(FlaskForm):
    logId = HiddenField("log_id")
    submitSingleClassScheduleToEdit = SubmitField("Edit")


class pblEventEditorForm(FlaskForm):
    log_id = HiddenField()
    className = SelectField("Class", validators=[DataRequired()])
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    quarter = SelectField("Quarter", coerce=int, validators=[DataRequired()])
    pblName = StringField("PBL Name", validators=[DataRequired()])
    eventCategory = SelectField("Event Category", validators=[DataRequired()])
    confirmed = BooleanField("Confirmed", validators=[Optional()])
    eventDate = DateField("Event Date", validators=[Optional()])
    startTime = SelectField(
        "Start Time", validators=[Optional()], choices=getStartTimeChoices()
    )
    endTime = SelectField(
        "End Time", validators=[Optional()], choices=getEndTimeChoices()
    )
    eventLocation = StringField("Location", validators=[Optional()])
    eventStreetAddress1 = StringField("Street Address", validators=[Optional()])
    eventStreetAddress2 = StringField("Street Address 2", validators=[Optional()])
    eventCity = StringField("City", validators=[Optional()])
    eventState = StringField("State", validators=[Optional()])
    eventZip = StringField("Zip", validators=[Optional()])
    eventComments = StringField("Comments", validators=[Optional()])
    googleCalendarEventID = StringField("Google Calendar Event ID (Optional)")
    submitEditPblEvent = SubmitField("Submit PBL Event")
