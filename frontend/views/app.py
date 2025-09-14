from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

app = Flask(__name__)
CORS(app)

API_TOKEN = '13~47Y8UAZaYt32LhLHxNh9uDTZMHWRahEM3Ue7U3uL4v999QH97YFHyN44CDDA9cMa'
CANVAS_DOMAIN = 'https://usflearn.instructure.com'
TODO_ENDPOINT = f"{CANVAS_DOMAIN}/api/v1/users/self/todo"
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}


@app.route('/api/weekly-tasks')
def get_weekly_tasks():
    response = requests.get(TODO_ENDPOINT, headers=HEADERS)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch tasks'}), 500

    todos = response.json()
    now = datetime.now(ZoneInfo("America/New_York"))
    one_week_from_now = now + timedelta(days=7)

    weekly_tasks = []

    for item in todos:
        due_at = item.get('due_at') or item.get('assignment', {}).get('due_at')
        if due_at:
            try:
                due_date = datetime.fromisoformat(due_at.replace(
                    "Z", "+00:00"))
                if now <= due_date <= one_week_from_now:
                    title = item.get('title') or item.get(
                        'assignment', {}).get('name', 'No Title')
                    course = item.get('context_name', 'Unknown Course')
                    weekly_tasks.append({
                        'title':
                        title,
                        'due_date':
                        due_date.strftime('%Y-%m-%d %H:%M'),
                        'course':
                        course
                    })
            except Exception:
                continue

    return jsonify(weekly_tasks)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # or any other port like 5002 if 5000 is busy
