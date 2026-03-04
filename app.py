import subprocess
import sys
import os
from flask import Flask, render_template

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

APPS = [
    {"path": "vulnerable/sql_injection", "port": 5001},
    {"path": "secure/sql_injection", "port": 5002},
    {"path": "vulnerable/xss_stored", "port": 5003},
    {"path": "secure/xss_stored", "port": 5004},
    {"path": "vulnerable/xss_reflected", "port": 5005},
    {"path": "secure/xss_reflected", "port": 5006},
    {"path": "vulnerable/idor", "port": 5007},
    {"path": "secure/idor", "port": 5008},
    {"path": "vulnerable/weak_password", "port": 5009},
    {"path": "secure/weak_password", "port": 5010},
    {"path": "vulnerable/broken_access_control", "port": 5011},
    {"path": "secure/broken_access_control", "port": 5012},
    {"path": "nexusbank", "port": 5013},
]

processes = []

def start_all_apps():
    for app_info in APPS:
        full_path = os.path.join(base_dir, app_info["path"])
        app_file = os.path.join(full_path, "app.py")

        if os.path.exists(app_file):
            process = subprocess.Popen(
                [sys.executable, app_file],
                cwd=full_path,  # Sets working directory to the app's own folder
                env={**os.environ, "PYTHONPATH": full_path}
            )
            processes.append(process)
            print(f"Started {app_info['path']} on port {app_info['port']}")
        else:
            print(f"Skipping {app_info['path']} — app.py not found")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting all vulnerability apps...")
    start_all_apps()
    print("Landing page starting at http://127.0.0.1:5000")
    app.run(debug=False, port=5000)