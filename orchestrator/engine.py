from agents.pipeline import build_resolution_pipeline
from state.state_manager import read_json, TICKETS_FILE, update_tickets, append_log
import json

class OmniFixOrchestrator:
    @staticmethod
    def process_ticket(ticket_id):
        tickets = read_json(TICKETS_FILE)
        ticket = next((t for t in tickets if str(t["id"]) == str(ticket_id)), None)
        
        if not ticket:
            yield f"data: {json.dumps({'log': 'Error: Ticket not found!'})}\n\n"
            return
            
        ticket["status"] = "Processing"
        update_tickets(tickets)
        
        for message in build_resolution_pipeline(ticket["type"], ticket["description"]):
            append_log(ticket_id, message)
            yield f"data: {json.dumps({'log': message})}\n\n"
            
        current_tickets = read_json(TICKETS_FILE)
        t = next((t for t in current_tickets if str(t["id"]) == str(ticket_id)), None)
        if t:
            t["status"] = "Resolved"
            update_tickets(current_tickets)
            
        final_message = "OmniFix completed execution."
        append_log(ticket_id, final_message)
        yield f"data: {json.dumps({'log': final_message, 'done': True})}\n\n"
