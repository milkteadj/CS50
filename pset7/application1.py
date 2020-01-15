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
    name = request.form.get("name") #get arguments are in args, post arguments are in form
    email = request.form.get("email")
    house = request.form.get("house")
    if not name or not email or not house:
        mess = "you failed. Try again"
        return render_template("error.html", message=mess)
    message = "You are registered! Check your email"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("milkteadj@gmail.com", os.getenv("PASSWORD"))
    server.sendmail("milkteadj@gmail.com", email, message)
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r"):
    #if there is no file, return error message:
    if not file:
        mess= "file not found"
        return render_template("error.html", message=mess)
    #open file
    reader = csv.reader(file)
    students = list(reader)
    return render_template("success.html")
