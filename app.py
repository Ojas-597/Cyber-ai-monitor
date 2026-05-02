from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules.db import verify_user, load_user, add_user, init_db, bcrypt
from modules.monitor import get_network_data
from modules.detector import detect_threats
from modules.ai_helper import explain_alert

import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🔐 INIT
bcrypt.init_app(app)
init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # ✅ redirects to login if not authenticated


# 🔁 USER LOADER
@login_manager.user_loader
def load_user_callback(user_id):
    return load_user(user_id)


# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = verify_user(
            request.form["username"],
            request.form["password"]
        )
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# 🆕 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get("role", "user")

        add_user(username, password, role)
        return redirect(url_for("login"))

    return render_template("register.html")


# 📊 DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", role=current_user.role)


# 🚨 ALERTS
@app.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html", role=current_user.role)


# 👑 ADMIN PANEL
@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return "Access Denied"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT username, role FROM users")
    users = c.fetchall()
    conn.close()

    return render_template("admin.html", users=users, role=current_user.role)


# ➕ ADMIN ADD USER
@app.route("/admin/add_user", methods=["POST"])
@login_required
def admin_add_user():
    if current_user.role != "admin":
        return "Access Denied"

    add_user(
        request.form["username"],
        request.form["password"],
        request.form["role"]
    )

    return redirect(url_for("admin"))


# ❌ ADMIN DELETE USER
@app.route("/admin/delete/<username>")
@login_required
def delete_user(username):
    if current_user.role != "admin":
        return "Access Denied"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# 🔑 USER PASSWORD RESET
@app.route("/reset_password", methods=["GET", "POST"])
@login_required
def reset_password():
    if request.method == "POST":
        hashed = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode('utf-8')

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "UPDATE users SET password=? WHERE username=?",
            (hashed, current_user.id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("reset_password.html")


# 👑 ADMIN RESET USER PASSWORD
@app.route("/admin/reset/<username>", methods=["POST"])
@login_required
def admin_reset(username):
    if current_user.role != "admin":
        return "Access Denied"

    hashed = bcrypt.generate_password_hash(
        request.form["password"]
    ).decode('utf-8')

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hashed, username)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# 🔁 REAL-TIME DATA API
@app.route("/api/data")
@login_required
def api_data():
    data = get_network_data()
    alerts = detect_threats(data)

    return jsonify({
        "connections": data,
        "alerts": alerts
    })


# 🤖 AI EXPLAIN
@app.route("/explain", methods=["POST"])
@login_required
def explain():
    return explain_alert(request.form["alert"])


# 📥 PDF REPORT
@app.route("/download_report")
@login_required
def download_report():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    alerts = detect_threats(get_network_data())

    content = []
    content.append(Paragraph("Cyber Security Report", styles['Title']))
    content.append(Spacer(1, 10))

    if not alerts:
        content.append(Paragraph("No threats detected.", styles['Normal']))
    else:
        for a in alerts:
            content.append(
                Paragraph(f"[{a['severity']}] {a['message']}", styles['Normal'])
            )
            content.append(Spacer(1, 5))

    content.append(Spacer(1, 15))
    content.append(Paragraph("Generated by Cyber AI Monitor", styles['Italic']))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)


# 🔓 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ▶ RUN
if __name__ == "__main__":
    app.run(debug=True)
