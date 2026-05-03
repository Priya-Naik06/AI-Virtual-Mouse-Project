from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder="../frontend")

@app.route("/")
def login():
    return send_from_directory("../frontend", "login.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory("../frontend", "dashboard.html")

@app.route("/run")
def run_virtual_mouse():
    os.system("python virtual_mouse.py")
    return "Virtual Mouse Started"

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port, debug=True)
