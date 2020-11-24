from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required
from P2MT_App import db
from P2MT_App.main.setupFunctions import (
    initializeInterventionTypes,
    addSchoolCalendarDays,
)
from P2MT_App.main.testFunctions import setAttendanceForTmiTesting
from datetime import date
from flask_login import current_user, login_required

# STEM III Drag and Drop
from P2MT_App.models import Student
import json

pblPlanner_bp = Blueprint("pblPlanner_bp", __name__)


# STEM III Drag and Drop
from P2MT_App.models import Student
import json


@pblPlanner_bp.route("/stemiiiteams")
@login_required
def displayStemIIITeams():
    students = db.session.query(
        Student.firstName, Student.lastName, Student.chattStateANumber
    ).filter(Student.yearOfGraduation == 2022)

    teams = []
    for i in range(1, 31, 1):
        teams.append(f"Team {i}")

    pblOptions = [
        "",
        "EPB Holiday Windows",
        "Prosthetic Test Tool",
        "Coding Machine for Kids",
        "River Street Architecture",
        "Tiger Team Rockets",
        "Brown Academy Makeover",
    ]
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
