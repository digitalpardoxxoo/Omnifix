import json
import os

SERVER_STATE_FILE = "server_state.json"
APP_STATE_FILE = "app_state.json"
USERS_FILE = "users.json"
TICKETS_FILE = "tickets.json"
VULN_STATE_FILE = "vuln_state.json"
LOGS_FILE = "logs.json"

def read_json(file_path):
    if not os.path.exists(file_path): 
        if file_path == TICKETS_FILE: return []
        if file_path == LOGS_FILE: return []
        if file_path == VULN_STATE_FILE: return {"sql_injection": False, "auth_bypass": False, "input_issues": False}
        return {}
    try:
        with open(file_path, "r") as f: 
            return json.load(f)
    except:
        return {}

def write_json(file_path, data):
    with open(file_path, "w") as f: 
        json.dump(data, f, indent=2)

def get_server_state(): return read_json(SERVER_STATE_FILE)
def get_app_state(): return read_json(APP_STATE_FILE)
def get_vuln_state(): return read_json(VULN_STATE_FILE)
def get_tickets(): return read_json(TICKETS_FILE)
def get_logs(): return read_json(LOGS_FILE)

def update_server_state(data): write_json(SERVER_STATE_FILE, data)
def update_app_state(data): write_json(APP_STATE_FILE, data)
def update_vuln_state(data): write_json(VULN_STATE_FILE, data)
def update_tickets(data): write_json(TICKETS_FILE, data)
def append_log(ticket_id, message):
    logs = get_logs()
    logs.append({"ticket_id": ticket_id, "message": message})
    write_json(LOGS_FILE, logs)

if not os.path.exists(VULN_STATE_FILE):
    update_vuln_state({"sql_injection": False, "auth_bypass": False, "input_issues": False})
