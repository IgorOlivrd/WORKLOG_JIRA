from flask import Flask, render_template, request, jsonify
from engine import start_timer, stop_timer, log_work

app = Flask(__name__)

STATE = {}  # memória simples (1 usuário)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    issue = request.json["issue"]
    started_dt, start_ts = start_timer()

    STATE["issue"] = issue
    STATE["started_dt"] = started_dt
    STATE["start_ts"] = start_ts

    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    seconds = stop_timer(STATE["start_ts"])
    comment = request.json.get("comment", "")

    status, response = log_work(
        STATE["issue"],
        STATE["started_dt"],
        seconds,
        comment
    )

    return jsonify({
        "seconds": seconds,
        "jira_status": status
    })

if __name__ == "__main__":
    app.run(debug=True)