# engine.py
import requests
from requests.auth import HTTPBasicAuth
import time
from datetime import datetime, timezone, timedelta

JIRA_BASE_URL = "https://credisis.atlassian.net"
JIRA_EMAIL = "email@credisis.com.br" #Alterar aqui para seu e-mail
JIRA_API_TOKEN = "SEU_TOKEN_AQUI" #Alterar aqui para seu token

TZ = timezone(timedelta(hours=-3))

def start_timer():
    started_dt = datetime.now(TZ)
    start_ts = time.time()
    return started_dt, start_ts

def stop_timer(start_ts):
    return max(1, int(time.time() - start_ts))

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
