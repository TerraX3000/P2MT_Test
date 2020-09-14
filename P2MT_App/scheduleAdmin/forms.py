from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
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


class uploadClassScheduleForm(FlaskForm):
    csvClassScheduleFile = FileField(
        "Class Schedule File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitUploadClassSchedule = SubmitField("Upload Class Schedule")


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class addSingleClassSchedule(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    studentName = SelectField("Student Name", validators=[DataRequired()])
    campus = SelectField("Campus", validators=[DataRequired()])
    className = SelectField("Class Name", validators=[DataRequired()])
    teacherName = SelectField("Teacher", coerce=str, validators=[DataRequired()])

    addTimeAndDays = BooleanField("Add", default=True)
    classDays = MultiCheckboxField("Class Days", validators=[DataRequired()])
    startTime = TimeField(
        "Start Time",
        validators=[DataRequired()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )
    endTime = TimeField(
        "End Time",
        validators=[DataRequired()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )

    addTimeAndDays2 = BooleanField("Add", default=True)
    classDays2 = MultiCheckboxField("Class Days")
    startTime2 = SelectField("Start Time", validators=[Optional()])
    endTime2 = SelectField("End Time", validators=[Optional()])
    # startTime2 = TimeField(
    #     "Start Time",
    #     validators=[Optional()],
    #     render_kw={"placeholder": "HH:MM 24-Hour Format"},
    # )
    # endTime2 = TimeField(
    #     "End Time",
    #     validators=[Optional()],
    #     render_kw={"placeholder": "HH:MM 24-Hour Format"},
    # )

    addTimeAndDays3 = BooleanField("Add", default=True)
    classDays3 = MultiCheckboxField("Class Days")
    startTime3 = TimeField(
        "Start Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )
    endTime3 = TimeField(
        "End Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )

    addTimeAndDays4 = BooleanField("Add", default=True)
    classDays4 = MultiCheckboxField("Class Days")
    startTime4 = TimeField(
        "Start Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )
    endTime4 = TimeField(
        "End Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )

    addTimeAndDays5 = BooleanField("Add", default=True)
    classDays5 = MultiCheckboxField("Class Days")
    startTime5 = TimeField(
        "Start Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )
    endTime5 = TimeField(
        "End Time",
        validators=[Optional()],
        render_kw={"placeholder": "HH:MM 24-Hour Format"},
    )

    online = BooleanField("Online")
    indStudy = BooleanField("Independent Study")
    comment = StringField("Comment (Optional)")
    googleCalendarEventID = StringField("Google Calendar Event ID (Optional)")
    # Start and end dates used for learning lab and recorded in intervention log
    startDate = DateField("Start Date")
    endDate = DateField("End Date")
    submitAddSingleClassSchedule = SubmitField("Add Class Schedule for Single Student")


class propagateClassAttendanceLogsForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    startDate = DateField("Start Date", validators=[DataRequired()])
    endDate = DateField("End Date", validators=[DataRequired()])
    submitPropagatelassAttendanceLogs = SubmitField("Propagate Class Attendance Logs")


class deleteClassScheduleForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    yearOfGraduation = SelectField("Year of Graduation", coerce=int)
    confirmDeleteClassSchedule = StringField(
        "Type DELETE to confirm", validators=[DataRequired()]
    )
    submitDeleteClassScheduleForm = SubmitField("Delete Class Schedule")


class downloadClassScheduleForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    submitDownloadClassScheduleForm = SubmitField("Download Class Schedule")


class downloadClassAttendanceForm(FlaskForm):
    schoolYear = SelectField("Year", coerce=int, validators=[DataRequired()])
    semester = SelectField("Semester", validators=[DataRequired()])
    teacherName = SelectField("Teacher", coerce=str, validators=[DataRequired()])
    startDate = DateField("Start Date", validators=[DataRequired()])
    endDate = DateField("End Date", validators=[DataRequired()])
    submitDownloadClassAttendanceForm = SubmitField("Download Class Attendance Log")
