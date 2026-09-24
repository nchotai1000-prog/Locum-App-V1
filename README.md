# Locum Tracker

A simple web app to log locum shifts and track monthly earnings.

## Features

- Log a shift with its date, hours worked and hourly rate
- See all shifts, newest first, with earnings calculated for each
- See a running total of earnings for the current month
- Delete a shift, with a confirmation step

## Built with

- Python and Flask
- SQLite database, stored locally in `locum.db`
- HTML templates

## Running it

1. Create and activate a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Start the app:

   ```
   python app.py
   ```

4. Open http://127.0.0.1:5000 in your browser.
