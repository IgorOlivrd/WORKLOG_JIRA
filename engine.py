# engine.py
import requests
from requests.auth import HTTPBasicAuth
import time
from datetime import datetime, timezone, timedelta

JIRA_BASE_URL = "https://credisis.atlassian.net"
JIRA_EMAIL = "igor.oliveira@credisis.com.br"
JIRA_API_TOKEN = "ATATT3xFfGF06H7x6YDPRS-Mw9Ss7T46m1k1SWckUhVCorxrtR4PKDWk9Z2WJeeqF7t4rNR6hyuT69CFy0IFE87NbTmi5gKo5onINy-IL2usr72ImNysL1jgmY_rcx4xJPypWKB_OwfU6rE2NxUfRtUs_yYadS2NT9kyCFIjGyQBZ0Kicr6413k=9FC1F0BC"

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