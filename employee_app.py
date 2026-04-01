from flask import Flask, request, jsonify
from flask_cors import CORS
from state.state_manager import get_app_state, get_server_state, get_vuln_state, read_json, USERS_FILE, TICKETS_FILE, update_tickets

app = Flask(__name__)
CORS(app)

@app.route("/api/login", methods=["POST"])
def login():
    state = get_app_state()
    server = get_server_state()
    
    if server.get("status") != "running" or state.get("auth_service") != "working" or state.get("login_system") != "working":
         return jsonify({"success": False, "error": "System is temporarily unavailable."}), 503

    users = read_json(USERS_FILE)
    username = request.json.get("username")
    password = request.json.get("password")
    
    for u in users:
        vulns = get_vuln_state()
        if vulns.get("sql_injection") and "' OR 1=1" in password:
            return jsonify({"success": True, "username": "admin", "token": "fake-jwt-token"})
        if vulns.get("auth_bypass") and username == "admin":
            return jsonify({"success": True, "username": "admin", "token": "fake-jwt-token"})
            
        if u["username"] == username and u["password"] == password:
            return jsonify({"success": True, "username": username, "token": "fake-jwt-token"})
            
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    server = get_server_state()
    state = get_app_state()
    
    if server.get("status") != "running" or state.get("db") != "connected":
         return jsonify({"success": False, "error": "System is temporarily unavailable."}), 503
         
    return jsonify({"success": True, "tasks": [{"title": "Review Q3 Financials", "status": "Pending"}, {"title": "Compliance Training", "status": "Overdue"}]})

@app.route("/api/ticket", methods=["POST"])
def submit_ticket():
    issue_type = request.json.get("type", "App")
    desc = request.json.get("description", "")
    
    tickets = read_json(TICKETS_FILE)
    ticket_id = len(tickets) + 1
    new_ticket = {"id": ticket_id, "type": issue_type, "description": desc, "status": "Created"}
    tickets.append(new_ticket)
    update_tickets(tickets)
    return jsonify({"success": True, "ticket_id": ticket_id})

if __name__ == "__main__":
    print("Employee API running on port 5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
