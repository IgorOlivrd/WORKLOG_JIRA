import requests
from requests.auth import HTTPBasicAuth
import time
from datetime import datetime, timezone, timedelta
from config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

TZ = timezone(timedelta(hours=-3))

def validate_jira_login():
    r = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/myself",
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )
    return r.status_code == 200

def start_timer():
    return datetime.now(TZ), time.time()

def stop_timer(start_ts):
    return max(1, int(time.time() - start_ts))

def validate_issue(issue):
    r = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{issue}",
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )


    if r.status_code == 200:
        d = r.json()
        return {
            "valid": True,
            "key": d["key"],
            "summary": d["fields"]["summary"],
            "status": d["fields"]["status"]["name"]
        }

    return {"valid": False, "error": "Issue inválida ou sem permissão"}

def get_current_user():
    r = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/myself",
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )
    return r.json()

def log_work(issue, started_dt, seconds, comment):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue}/worklog"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    payload = {
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{
                    "type": "text",
                    "text": comment if comment else " "
                }]
            }]
        },
        "started": started_dt.strftime("%Y-%m-%dT%H:%M:%S.000%z"),
        "timeSpentSeconds": int(seconds)
    }

    response = requests.post(url, auth=auth, json=payload)
    return response.status_code, response.text