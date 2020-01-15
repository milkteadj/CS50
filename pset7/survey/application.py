import cs50
import csv
import os
import smtplib

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    #if any field is missing, return failure:
    name = request.form.get("name")
    gender = request.form.get("gender")
    grade = request.form.get("grade")
    email = request.form.get("email")
    house = request.form.get("house")
    if not name or not gender or not email or not grade or not house:
        return render_template("failure.html")

    file = open("survey.csv", "a")
    writer  = csv.writer(file)
    writer.writerow((name, gender, grade, email, house))
    file.close()
    return render_template("success.html")

@app.route("/sheet", methods=["GET"])
def sheet():
    with open('survey.csv', 'r') as f:
        reader = csv.reader(f)
        students = list(reader)
    return render_template("sheet.html", students=students)
