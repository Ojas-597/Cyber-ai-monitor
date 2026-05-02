from flask import Flask, render_template, request, redirect, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import threading

from modules.auth import User
from modules.db import init_db, add_user, verify_user
from modules.monitor import get_network_data
from modules.detector import detect_threats
from modules.ai_helper import explain_alert

# Optional sniffer
try:
    from modules.sniffer import start_sniffing
    threading.Thread(target=start_sniffing, daemon=True).start()
except:
    print("Sniffer not started")

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)

init_db()
add_user("admin", "admin123", "admin")
add_user("user", "user123", "user")

traffic_log = []

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, "user")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = verify_user(request.form["username"], request.form["password"])
        if user:
            login_user(User(user["username"], user["role"]))
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", role=current_user.role)

@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return "Access Denied"
    return render_template("admin.html")

@app.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html")

@app.route("/api/data")
@login_required
def api_data():
    data = get_network_data()
    alerts = detect_threats(data)
    return jsonify({"connections": data, "alerts": alerts})

@app.route("/api/traffic")
@login_required
def traffic():
    data = get_network_data()
    count = len(data)
    traffic_log.append(count)

    if len(traffic_log) > 20:
        traffic_log.pop(0)

    return jsonify(traffic_log)

@app.route("/explain", methods=["POST"])
@login_required
def explain():
    return explain_alert(request.form["alert"])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
