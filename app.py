from datetime import date

from flask import Flask, redirect, render_template, request
from database import add_shift, delete_shift, get_shifts, get_shifts_for_month, init_db
from pay import calculate_earnings, split_minutes

app = Flask(__name__)
init_db()


@app.template_filter("uk_date")
def uk_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


def shift_details(shift):
    day_minutes, ooh_minutes = split_minutes(
        shift["start_time"], shift["end_time"], shift["ooh_start"], shift["ooh_end"]
    )
    details = dict(shift)
    details["day_hours"] = day_minutes / 60
    details["ooh_hours"] = ooh_minutes / 60
    details["earnings"] = calculate_earnings(
        shift["start_time"],
        shift["end_time"],
        shift["ooh_start"],
        shift["ooh_end"],
        shift["day_rate"],
        shift["ooh_rate"],
    )
    return details


@app.route("/")
def index():
    today = date.today()
    shifts = [shift_details(shift) for shift in get_shifts()]
    month_shifts = get_shifts_for_month(today.strftime("%Y-%m"))
    month_total = sum(shift_details(shift)["earnings"] for shift in month_shifts)
    return render_template(
        "index.html",
        shifts=shifts,
        month_name=today.strftime("%B %Y"),
        month_total=month_total,
    )


@app.route("/add", methods=["POST"])
def add():
    shift_date = request.form["shift_date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    day_rate = float(request.form["day_rate"])
    ooh_rate = float(request.form["ooh_rate"])
    ooh_start = request.form["ooh_start"]
    ooh_end = request.form["ooh_end"]
    add_shift(shift_date, start_time, end_time, day_rate, ooh_rate, ooh_start, ooh_end)
    return redirect("/")


@app.route("/delete/<int:shift_id>", methods=["POST"])
def delete(shift_id):
    delete_shift(shift_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
