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

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html", title="Home")


@main_bp.route("/about")
def displayAbout():
    return render_template("about.html", title="About")


@main_bp.route("/setupP2mt")
@login_required
def setupP2mt():
    # Create all the database tables if not already created
    db.create_all()
    initializeInterventionTypes()
    addSchoolCalendarDays(date(2020, 8, 3), date(2021, 6, 4))
    db.session.commit()
    return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))


@main_bp.route("/testP2mt")
@login_required
def testP2mt():
    initializeInterventionTypes()
    setAttendanceForTmiTesting(date(2020, 8, 3), date(2020, 8, 18))
    db.session.commit()
    return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))


# Temporary routes for testing new features


@main_bp.route("/analytics")
def displayAnalyticsTest():
    return render_template("analytics.html")


@main_bp.route("/sandbox")
def displaySandbox():
    return render_template("sandbox.html")


@main_bp.route("/stemiiiteams")
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
        "stemiiiteams.html",
        title="STEM III Team Builder",
        students=students,
        teams=teams,
        pblOptions=pblOptions,
    )


@main_bp.route("/saveteams", methods=["GET", "POST"])
def saveTeams():
    print("Running saveTeams()")
    teamListjson = request.form["teamList"]
    teamList = json.loads(teamListjson)
    for team, teamInfo in teamList.items():
        print(team, teamInfo["teamMemberList"], teamInfo["pblChoice"])
    return redirect(url_for("main_bp.displayStemIIITeams"))
