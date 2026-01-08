import requests
from requests.auth import HTTPBasicAuth
import json
import time
from datetime import datetime, timezone, timedelta

# =========================
# CONFIGURAÇÃO
# =========================
JIRA_BASE_URL = "https://credisis.atlassian.net"
JIRA_EMAIL = "email@credisis.com.br" #Alterar aqui para seu e-mail
JIRA_API_TOKEN = "SEU_TOKEN_AQUI" #Alterar aqui para seu token

TZ = timezone(timedelta(hours=-3))  # Brasil

# =========================
# INPUT DA ISSUE
# =========================
ISSUE_ID_OR_KEY = input("Issue (ex: PROJ-123): ").strip()

url = f"{JIRA_BASE_URL}/rest/api/3/issue/{ISSUE_ID_OR_KEY}/worklog"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# =========================
# CRONÔMETRO
# =========================
print("\n⏱️ Pressione ENTER para iniciar o cronômetro")
input()

started_dt = datetime.now(timezone(timedelta(hours=-3)))
start_ts = time.time()

print("▶️ Cronômetro iniciado")
print("⏸️ Pressione ENTER para pausar")
input()

elapsed_seconds = max(1, int(time.time() - start_ts))

timeSpentSeconds = int(max(1, elapsed_seconds))

if elapsed_seconds <= 0:
    print("❌ Tempo inválido. Abortando.")
    exit()

print(f"\n⏱️ Tempo registrado: {elapsed_seconds} segundos")

# =========================
# COMENTÁRIO OPCIONAL
# =========================
comment_text = input("Comentário (opcional): ").strip()

# =========================
# PAYLOAD (DOC-FIRST)
# =========================
payload = {
    "comment": {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": comment_text
                    }
                ]
            }
        ]
    },
    "started": started_dt.strftime("%Y-%m-%dT%H:%M:%S.000%z"),
    "timeSpentSeconds": int(timeSpentSeconds)
}

# =========================
# POST WORKLOG
# =========================
response = requests.post(
    url,
    headers=headers,
    auth=auth,
    json=payload
)

print("\n📥 Status:", response.status_code)

try:
    print(json.dumps(response.json(), indent=4))
except Exception:
    print(response.text)
    
def format_seconds(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    return f"{h}h {m}m" if h else f"{m}m"


print(f"⏱ Tempo registrado: {format_seconds(elapsed_seconds)}")
