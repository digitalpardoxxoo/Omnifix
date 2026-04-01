import time
import requests
import random
import json

BASE_URL = "http://127.0.0.1:5000"

ISSUES = [
    {
        "action": "infra_server_down",
        "type": "Infra",
        "description": "The server is completely unresponsive. I'm getting a 500 Internal Server Error when trying to load any page."
    },
    {
        "action": "infra_high_cpu",
        "type": "Infra",
        "description": "The employee portal is extremely slow. Looks like CPU is spiked."
    },
    {
        "action": "infra_disk_full",
        "type": "Infra",
        "description": "Getting strange errors about disk space when trying to save my work."
    },
    {
        "action": "app_auth_down",
        "type": "App",
        "description": "Authentication service is unavailable. I can't log in at all."
    },
    {
        "action": "app_db_down",
        "type": "App",
        "description": "Dashboard is broken, saying database connection is lost."
    },
    {
        "action": "app_login_fail",
        "type": "App",
        "description": "Login keeps failing even though I know my password is correct."
    }
]

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def start_bot():
    print_colored("🤖 Chaos Bot Started! Monitoring and attacking system...", "95")
    print_colored("Press Ctrl+C to stop the bot.\n", "90")
    
    while True:
        # Wait a bit between attacks (e.g., 10-15 seconds for demo purposes)
        sleep_time = random.randint(10, 15)
        print_colored(f"[*] Waiting {sleep_time} seconds before next random failure...", "90")
        time.sleep(sleep_time)

        # Pick a random issue
        issue = random.choice(ISSUES)
        
        print_colored(f"\n[💥 CHAOS MONKEY] Injecting failure: {issue['action']}", "91")
        try:
            # 1. Simulate the failure
            requests.post(f"{BASE_URL}/api/simulate", json={"action": issue["action"]})
            print_colored(f"[⚠️ SYSTEM ALERT] System has been degraded!", "93")
            
            time.sleep(2) # Simulate user taking time to notice
            
            # 2. Simulate User reporting the ticket
            print_colored(f"[📩 USER REPORT] User experiencing issue! Submitting ticket: '{issue['description']}'", "33")
            response = requests.post(f"{BASE_URL}/api/ticket", json={
                "type": issue["type"],
                "description": issue["description"]
            })
            
            if response.status_code == 200:
                ticket_data = response.json()
                ticket_id = ticket_data.get("ticket_id")
                print_colored(f"[✅ TICKET CREATED] Ticket #{ticket_id} submitted to OmniFix queue.", "92")
                
                time.sleep(1)
                
                # 3. Trigger OmniFix to auto-resolve (simulating OmniFix background worker)
                print_colored(f"[⚙️ OMNIFIX] OmniFix Auto-remediation initializing for Ticket #{ticket_id}...", "96")
                
                # We consume the event stream to let OmniFix do its job live and print the agent logs
                fix_response = requests.get(f"{BASE_URL}/api/run_omnifix?ticket_id={ticket_id}", stream=True)
                for line in fix_response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            try:
                                data = json.loads(decoded_line[6:])
                                print_colored(f"   > {data.get('log')}", "94")
                            except ValueError:
                                pass
                
                print_colored(f"[🎉 RESOLVED] Ticket #{ticket_id} has been resolved! System is healthy again.\n", "92")
            else:
                print_colored(f"[❌ ERROR] Failed to submit ticket. Server might be fully offline!", "91")

        except requests.exceptions.ConnectionError:
            print_colored(f"[❌ ERROR] Bot couldn't reach the server. Make sure Flask app is running on port 5000.", "91")
            time.sleep(5)
        except Exception as e:
            print_colored(f"[❌ ERROR] Bot encountered an error: {e}", "91")


if __name__ == "__main__":
    try:
        # Optional requirements warning
        try:
            import requests
        except ImportError:
            print("Please run: pip install requests")
            exit(1)
            
        start_bot()
    except KeyboardInterrupt:
        print_colored("\nBot stopped.", "95")
