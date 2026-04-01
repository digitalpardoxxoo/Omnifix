from state.state_manager import get_server_state, update_server_state, get_app_state, update_app_state, get_vuln_state, update_vuln_state

# INFRA TOOLS
# Future: AWS SDK / Kubernetes integration goes here
def check_cpu(): 
    return get_server_state().get("cpu", 0)

def restart_server():
    s = get_server_state()
    s.update({"status": "running", "cpu": 30, "service": "active"})
    update_server_state(s)

def clear_disk():
    s = get_server_state()
    s["disk"] = 20
    update_server_state(s)

# APP TOOLS
def check_auth(): 
    return get_app_state().get("auth_service", "unknown")

def check_vuln(): 
    return get_vuln_state()

def restart_auth():
    s = get_app_state()
    s["auth_service"] = "working"
    s["login_system"] = "working"
    update_app_state(s)

def reconnect_db():
    s = get_app_state()
    s["db"] = "connected"
    update_app_state(s)

def patch_vulnerabilities():
    s = get_vuln_state()
    s.update({"sql_injection": False, "auth_bypass": False, "input_issues": False})
    update_vuln_state(s)
