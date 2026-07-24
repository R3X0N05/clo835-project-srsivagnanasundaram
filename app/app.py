#CLO835 PROJECT FLAKY APP
import os
import time
import socket
import threading
from flask import Flask

app = Flask(__name__)

STUDENT_ID = "126332246" #declaring studentID as a variable
HOSTNAME = socket.gethostname()

#ConfigMap Environment Variables
STARTUP_DELAY = int(os.environ.get("STARTUP_DELAY_SECONDS", "0"))
HEALTHZ_LAT = int(os.environ.get("HEALTHZ_LATENCY_MS", "0"))

#In-memory wedge flag
wedged = False
lock = threading.Lock()

#Boot-time startup delay
time.sleep(STARTUP_DELAY)

#Route
@app.route("/")
def index():
    return f"Hello from {STUDENT_ID} pod={HOSTNAME}\n", 200

@app.route("/healthz")
def healthz():
    if HEALTHZ_LAT > 0:
        time.sleep(HEALTHZ_LAT / 1000.0)
    with lock:
        is_wedged = wedged
    if is_wedged:
        return f"wedged pod={HOSTNAME} student={STUDENT_ID}\n", 500
    return f"ok {STUDENT_ID} pod={HOSTNAME}\n", 200

@app.route("/wedge", methods=["GET", "POST"])
def do_wedge():
    global wedged
    with lock:
        wedged = True
    return f"wedged pod={HOSTNAME} student={STUDENT_ID}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)