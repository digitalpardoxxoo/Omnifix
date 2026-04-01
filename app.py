from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

# --- IN-MEMORY STATE FOR DEMO SIMPLICITY ---
state = {
    "server_status": "Running",
    "db_status": "Connected",
    "auth_status": "Working",
    "task_service_status": "Working",
    "vuln_bypass": False,
    "vuln_input": False
}

tickets = []
logs = []
tasks = [
    {"id": 1, "title": "Submit Quarterly Report", "status": "Pending", "assigned_to": "employee1"},
    {"id": 2, "title": "Approve Node Licenses", "status": "Pending", "assigned_to": "employee2"},
    {"id": 3, "title": "Audit Security Logs", "status": "Completed", "assigned_to": "employee1"},
    {"id": 4, "title": "Update Firewall Rules", "status": "Pending", "assigned_to": "employee3"},
    {"id": 5, "title": "Draft Onboarding Docs", "status": "Completed", "assigned_to": "employee4"},
    {"id": 6, "title": "Review Access Permissions", "status": "Pending", "assigned_to": "manager1"},
    {"id": 7, "title": "Renew SSL Certificates", "status": "Pending", "assigned_to": "employee5"},
    {"id": 8, "title": "Server Maintenance Check", "status": "Completed", "assigned_to": "employee6"}
]

users = {
    "admin1": {"password": "password123", "role": "Admin"},
    
    "manager1": {"password": "password123", "role": "Manager"},
    "manager2": {"password": "password123", "role": "Manager"},
    "manager3": {"password": "password123", "role": "Manager"},

    "employee1": {"password": "password123", "role": "Employee"},
    "employee2": {"password": "password123", "role": "Employee"},
    "employee3": {"password": "password123", "role": "Employee"},
    "employee4": {"password": "password123", "role": "Employee"},
    "employee5": {"password": "password123", "role": "Employee"},
    "employee6": {"password": "password123", "role": "Employee"},
    "employee7": {"password": "password123", "role": "Employee"},
    "employee8": {"password": "password123", "role": "Employee"},
    "employee9": {"password": "password123", "role": "Employee"},
    "employee10": {"password": "password123", "role": "Employee"}
}

# --- EMPLOYEE API ---
@app.route("/api/login", methods=["POST"])
def login():
    if state["server_status"] != "Running" or state["auth_status"] != "Working":
        return jsonify({"success": False, "error": "System is temporarily unavailable. Please wait..."})

    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if state["vuln_bypass"] and username == "admin":
        return jsonify({"success": True, "username": "admin", "role": "Manager"})

    if username and username in users and users[username]["password"] == password:
        return jsonify({"success": True, "username": username, "role": users[username]["role"]})

    return jsonify({"success": False, "error": "Invalid credentials"})

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    if state["server_status"] != "Running" or state["db_status"] != "Connected" or state["task_service_status"] != "Working":
        return jsonify({"success": False, "error": "System is temporarily unavailable. Please wait..."})
    return jsonify({"success": True, "tasks": tasks})

# --- TICKETS & OMNIFIX ---
@app.route("/api/ticket", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    ticket_id = len(tickets) + 1
    tickets.append({"id": ticket_id, "type": data.get("type", "Error"), "desc": data.get("description", ""), "status": "Created"})
    return jsonify({"success": True, "ticket_id": ticket_id})

@app.route("/api/run_omnifix", methods=["GET"])
def run_omnifix():
    ticket_id = request.args.get("ticket_id")
    if not ticket_id: return jsonify({"error": "No ID"})

    def event_stream():
        def _log(sender, msg):
            log_entry = f"[{sender}] {msg}"
            logs.append(log_entry)
            return f"data: {json.dumps({'sender': sender, 'message': msg, 'log': log_entry, 'type': 'chat'})}\n\n"

        # 1. Dispatcher
        yield _log("Dispatcher", "New anomaly detected on the network. Initializing OmniFix protocol.")
        time.sleep(1)
        
        # 2. Diagnostician
        yield _log("Diagnostician", f"Acknowledged. Analyzing ticket #{ticket_id}. Scanning system nodes...")
        time.sleep(1.5)

        if state["server_status"] != "Running":
            yield _log("Diagnostician", "Critical Alert: Core Backend Server is unresponsive.")
            cause = "Server Down"
        elif state["db_status"] != "Connected":
            yield _log("Diagnostician", "Critical Alert: Database Cluster connection severed.")
            cause = "Database Disconnected"
        elif state["auth_status"] != "Working":
            yield _log("Diagnostician", "Critical Alert: OAuth2.0 Gateway authentication failure.")
            cause = "Auth Service Failed"
        elif state["task_service_status"] != "Working":
            yield _log("Diagnostician", "Warning: Task scheduling service subsystem stalled.")
            cause = "Task Service Failed"
        elif state["vuln_bypass"]:
            yield _log("Diagnostician", "Security Alert: Authentication bypass vulnerability exploited.")
            cause = "Auth Bypass vulnerability"
        elif state["vuln_input"]:
            yield _log("Diagnostician", "Security Alert: Malicious input payload detected in user parameters.")
            cause = "Input vulnerability"
        else:
            yield _log("Diagnostician", "Scanning complete. No primary services are currently down, but re-verifying system integrity.")
            cause = "Unknown Anomaly"

        time.sleep(1.2)
        
        # 3. Remediation
        yield _log("Remediation", f"Target locked on {cause}. Engaging automated repair sequences.")
        time.sleep(1.5)
        
        yield _log("Remediation", "Recompiling configurations and deploying hotfixes across nodes...")
        state["server_status"] = "Running"
        state["db_status"] = "Connected"
        state["auth_status"] = "Working"
        state["task_service_status"] = "Working"
        state["vuln_bypass"] = False
        state["vuln_input"] = False
        time.sleep(1.5)
        
        yield _log("Remediation", 'Hotfixes successfully deployed. Systems restored to optimal parameters.')
        time.sleep(1)
        
        # 4. Verifier
        yield _log("Verifier", "Performing post-remediation system checks... All green. Ticket can be closed.")
        time.sleep(1)

        # 5. Done
        for t in tickets:
            if str(t["id"]) == str(ticket_id):
                t["status"] = "Resolved"
                
        yield f"data: {json.dumps({'log': 'System successfully restored by OmniFix.', 'done': True, 'type': 'system'})}\n\n"
        
    return Response(event_stream(), mimetype='text/event-stream')

# --- CONTROL PANEL API ---
@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify({
        "state": state,
        "tickets": list(reversed(tickets)),
        "logs": logs
    })

@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    if action == "server_down": state["server_status"] = "Down"
    elif action == "db_down": state["db_status"] = "Disconnected"
    elif action == "auth_fail": state["auth_status"] = "Failed"
    elif action == "task_fail": state["task_service_status"] = "Failed"
    elif action == "vuln_bypass": state["vuln_bypass"] = True
    elif action == "vuln_input": state["vuln_input"] = True
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
