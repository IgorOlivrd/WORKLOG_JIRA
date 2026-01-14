from flask import Flask, render_template, jsonify, request
from engine import (
    start_timer,
    stop_timer,
    validate_issue,
    log_work,
    validate_jira_login, get_current_user
)
from config import has_credentials, JIRA_EMAIL

app = Flask(__name__)
STATE = {}

@app.route("/")
def index():
    if not has_credentials():
        return "❌ Arquivo .env não configurado", 500

    if not validate_jira_login():
        return "❌ Token Jira inválido", 401

    return render_template("index.html", user_email=JIRA_EMAIL)

@app.route("/validate-issue", methods=["POST"])
def validate():
    return jsonify(validate_issue(request.json["issue"]))

@app.route("/start", methods=["POST"])
def start():
    started_dt, start_ts = start_timer()
    STATE.update({
        "issue": request.json["issue"],
        "started_dt": started_dt,
        "start_ts": start_ts
    })
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    seconds = stop_timer(STATE["start_ts"])
    status = log_work(
        STATE["issue"],
        STATE["started_dt"],
        seconds,
        request.json.get("comment")
    )
    return jsonify({"seconds": seconds, "jira_status": status})

if __name__ == "__main__":
    app.run(debug=True)
