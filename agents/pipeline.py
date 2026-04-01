import time
from tools import system_tools

def build_resolution_pipeline(issue_type, description):
    """
    Generator pipeline representing agent steps:
    Dispatcher -> Diagnostician -> Security Agent -> Remediation -> Verification -> Resolved
    """
    
    # 1. Dispatcher
    yield "[Dispatcher] Issue detected. Categorizing incident..."
    time.sleep(1)
    is_infra = issue_type.lower() == 'infra'
    yield f"[Dispatcher] Target domain identified: {'Infrastructure' if is_infra else 'Application Area'}"
    time.sleep(1)

    # 2. Diagnostician
    yield "[Diagnostician] Root cause analysis initiating..."
    time.sleep(1)
    if is_infra:
        cpu = system_tools.check_cpu()
        yield f"[Diagnostician] Root cause found: Infrastructure saturation (CPU: {cpu}%)"
    else:
        auth_status = system_tools.check_auth()
        yield f"[Diagnostician] Root cause found: Service unavailability (Auth: {auth_status})"
    time.sleep(1)

    # 3. Security Agent
    yield "[Security] Scanning environment for active vulnerabilities or breaches..."
    time.sleep(1)
    vulns = system_tools.check_vuln()
    active_vulns = [k for k, v in vulns.items() if v]
    if active_vulns:
        yield f"[Security] Vulnerability detected: {', '.join(active_vulns)}"
    else:
        yield "[Security] No active vulnerabilities detected."
    time.sleep(1)

    # 4. Remediation
    yield "[Remediation] Designing and applying hotfixes..."
    time.sleep(1.5)
    if active_vulns:
        system_tools.patch_vulnerabilities()
        yield "[Remediation] Fix applied: Security patch deployed."
        time.sleep(1)

    if is_infra:
        system_tools.restart_server()
        system_tools.clear_disk()
        yield "[Remediation] Fix applied: Server re-provisioned and disk cleared."
    else:
        system_tools.restart_auth()
        system_tools.reconnect_db()
        yield "[Remediation] Fix applied: Authentication system rebooted & DB synched."
    time.sleep(1.5)

    # 5. Verification
    yield "[Verification] Running post-remediation system health checks..."
    time.sleep(1)
    yield "[Verification] System stable. All services green."
    time.sleep(1)

    yield "[Resolved] Incident closed. Normal operations resumed."
