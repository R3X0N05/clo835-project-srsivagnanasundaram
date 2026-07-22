#CLO835 PROJECT FLAKY APP
import os
import time
import socket
import threading
from flask import Flask

app = Flask(__name__)

STUDENT_ID = "126332246"
HOSTNAME = socket.gethostname()

#ConfigMap Environment Variables
STARTUP_DELAY = int(os.environ.get("STARTUP_DELAY_SECONDS", "0"))
HEALTHZ_LAT = int(os.environ.get("HEALTHZ_LATENCY_MS", "0"))

#In-memory wedge flag
_wedged = False
_lock = threading.Lock()

#Boot-time startup delay
print(f"[boot] sleeping {STARTUP_DELAY}s before serving.....")
time.sleep(STARTUP_DELAY)
print(f"[boot] ready, hostname={HOSTNAME}, student={STUDENT_ID}")

#Route
@app.route("/")
def index():
    return f"Hello from {STUDENT_ID} pod={HOSTNAME}\n", 200

@app.route("/healthz")
def healthz():
    if HEALTHZ_LAT > 0:
        time.sleep(HEALTHZ_LAT / 1000.0)
    with _lock:
        wedged = _wedged

    if wedged:
        return f"WEDGED pod={HOSTNAME} student={STUDENT_ID}\n", 500

    return f"ok {STUDENT_ID} pod={HOSTNAME}\n", 200

@app.route("/wedge", methods=["GET", "POST"])
def wedge():
    global _wedged
    with _lock:
        _wedged = True
    return f"wedged pod={HOSTNAME} student={STUDENT_ID}\n", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)