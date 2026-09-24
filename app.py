from datetime import date

from flask import Flask, redirect, render_template, request
from database import add_shift, get_shifts, init_db

app = Flask(__name__)


@app.template_filter("uk_date")
def uk_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


@app.route("/")
def index():
    shifts = get_shifts()
    return render_template("index.html", shifts=shifts)


@app.route("/add", methods=["POST"])
def add():
    shift_date = request.form["shift_date"]
    hours = float(request.form["hours"])
    hourly_rate = float(request.form["hourly_rate"])
    add_shift(shift_date, hours, hourly_rate)
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
