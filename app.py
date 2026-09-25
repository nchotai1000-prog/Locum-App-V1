from datetime import date

from flask import Flask, redirect, render_template, request
from database import (
    add_profile,
    add_shift,
    delete_profile,
    delete_shift,
    get_goal,
    get_profile,
    get_profiles,
    get_shifts,
    get_shifts_for_month,
    init_db,
    set_goal,
)
from pay import calculate_earnings, shifts_needed, split_minutes

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
    today_text = today.isoformat()
    month = today.strftime("%Y-%m")

    shifts = [shift_details(shift) for shift in get_shifts()]
    month_shifts = [shift_details(shift) for shift in get_shifts_for_month(month)]

    earned = sum(
        shift["earnings"] for shift in month_shifts if shift["shift_date"] <= today_text
    )
    booked = sum(
        shift["earnings"] for shift in month_shifts if shift["shift_date"] > today_text
    )

    goal = get_goal(month)
    still_to_find = max(goal - earned - booked, 0) if goal else None

    estimate_profile_id = request.args.get("estimate_profile", type=int)
    estimate_start = request.args.get("estimate_start", "08:00")
    estimate_end = request.args.get("estimate_end", "20:00")
    estimate = None
    if goal and estimate_profile_id:
        profile = get_profile(estimate_profile_id)
        if profile:
            per_shift = calculate_earnings(
                estimate_start,
                estimate_end,
                profile["ooh_start"],
                profile["ooh_end"],
                profile["day_rate"],
                profile["ooh_rate"],
            )
            estimate = {
                "profile_name": profile["name"],
                "per_shift": per_shift,
                "needed": shifts_needed(still_to_find, per_shift),
            }

    return render_template(
        "index.html",
        shifts=shifts,
        profiles=get_profiles(),
        month=month,
        month_name=today.strftime("%B %Y"),
        earned=earned,
        booked=booked,
        goal=goal,
        still_to_find=still_to_find,
        estimate=estimate,
        estimate_profile_id=estimate_profile_id,
        estimate_start=estimate_start,
        estimate_end=estimate_end,
    )


@app.route("/goal", methods=["POST"])
def save_goal():
    month = request.form["month"]
    target = float(request.form["target"])
    set_goal(month, target)
    return redirect("/")


@app.route("/add", methods=["POST"])
def add():
    shift_date = request.form["shift_date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    specialty = request.form["specialty"].strip()
    day_rate = float(request.form["day_rate"])
    ooh_rate = float(request.form["ooh_rate"])
    ooh_start = request.form["ooh_start"]
    ooh_end = request.form["ooh_end"]
    profile_id = request.form["profile_id"]
    profile_id = int(profile_id) if profile_id else None
    add_shift(
        shift_date,
        start_time,
        end_time,
        specialty,
        day_rate,
        ooh_rate,
        ooh_start,
        ooh_end,
        profile_id,
    )
    return redirect("/")


@app.route("/delete/<int:shift_id>", methods=["POST"])
def delete(shift_id):
    delete_shift(shift_id)
    return redirect("/")


@app.route("/profiles")
def profiles():
    return render_template("profiles.html", profiles=get_profiles())


@app.route("/profiles/add", methods=["POST"])
def create_profile():
    name = request.form["name"].strip()
    specialty = request.form["specialty"].strip()
    day_rate = float(request.form["day_rate"])
    ooh_rate = float(request.form["ooh_rate"])
    ooh_start = request.form["ooh_start"]
    ooh_end = request.form["ooh_end"]
    add_profile(name, specialty, day_rate, ooh_rate, ooh_start, ooh_end)
    return redirect("/profiles")


@app.route("/profiles/delete/<int:profile_id>", methods=["POST"])
def remove_profile(profile_id):
    delete_profile(profile_id)
    return redirect("/profiles")


if __name__ == "__main__":
    app.run(debug=True)
