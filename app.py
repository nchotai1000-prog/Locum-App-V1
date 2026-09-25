from datetime import date

from flask import Flask, redirect, render_template, request
from database import add_shift, delete_shift, get_month_total, get_shifts, init_db

app = Flask(__name__)
init_db()


@app.template_filter("uk_date")
def uk_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


@app.route("/")
def index():
    today = date.today()
    shifts = get_shifts()
    month_total = get_month_total(today.strftime("%Y-%m"))
    return render_template(
        "index.html",
        shifts=shifts,
        month_name=today.strftime("%B %Y"),
        month_total=month_total,
    )


@app.route("/add", methods=["POST"])
def add():
    shift_date = request.form["shift_date"]
    hours = float(request.form["hours"])
    hourly_rate = float(request.form["hourly_rate"])
    add_shift(shift_date, hours, hourly_rate)
    return redirect("/")


@app.route("/delete/<int:shift_id>", methods=["POST"])
def delete(shift_id):
    delete_shift(shift_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
