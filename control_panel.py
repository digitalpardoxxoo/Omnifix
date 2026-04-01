from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from state.state_manager import get_server_state, get_app_state, get_vuln_state, update_server_state, update_app_state, update_vuln_state, get_tickets, get_logs
import json

app = Flask(__name__)
CORS(app)

@app.route("/api/state", methods=["GET"])
def get_full_state():
    return jsonify({
        "server": get_server_state(),
        "app": get_app_state(),
        "vuln": get_vuln_state(),
        "tickets": get_tickets(),
        "logs": get_logs()
    })

@app.route("/api/simulate", methods=["POST"])
def simulate():
    action = request.json.get("action")
    if action == "infra_server_down":
        s = get_server_state(); s["status"] = "down"; update_server_state(s)
    elif action == "infra_high_cpu":
        s = get_server_state(); s["cpu"] = 99; update_server_state(s)
    elif action == "app_auth_down":
        s = get_app_state(); s["auth_service"] = "down"; update_app_state(s)
    elif action == "app_db_down":
        s = get_app_state(); s["db"] = "disconnected"; update_app_state(s)
    elif action == "vuln_sql_injection":
        s = get_vuln_state(); s["sql_injection"] = True; update_vuln_state(s)
    elif action == "vuln_auth_bypass":
        s = get_vuln_state(); s["auth_bypass"] = True; update_vuln_state(s)
    
    return jsonify({"success": True})

@app.route("/api/run_omnifix", methods=["GET"])
def run_omnifix():
    ticket_id = request.args.get("ticket_id")
    if not ticket_id: return jsonify({"error": "Missing ticket ID"})

    def event_stream():
        from orchestrator.engine import OmniFixOrchestrator
        yield from OmniFixOrchestrator.process_ticket(ticket_id)

    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == "__main__":
    print("Control Panel API running on port 5001")
    app.run(debug=True, port=5001, host="0.0.0.0")
