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



