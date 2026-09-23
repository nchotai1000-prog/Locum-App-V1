from flask import Flask
from database import init_db

app = Flask(__name__)


@app.route("/")
def index():
    return "Locum Tracker is running"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
