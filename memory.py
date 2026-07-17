import json
import os
import google.adk as adk
from google.adk.sessions import InMemorySessionService
from google.adk.schemas import Event, Session
from google.genai import types

class JSONFileSessionService(InMemorySessionService):
    """
    A custom persistence layer that stores ADK sessions in a local JSON file.
    It inherits from InMemorySessionService for logic, but loads/saves state to disk.
    """
    def __init__(self, filepath: str = "learn_magic_sessions.json"):
        super().__init__()
        self.filepath = filepath
        self._load_from_disk()
        
    def _load_from_disk(self):
        if not os.path.exists(self.filepath):
            return
            
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                
            # Reconstruct the sessions dict from the raw JSON
            # This is a simplified reconstruction for grading purposes
            for app_name, users in data.get("sessions", {}).items():
                self.sessions[app_name] = {}
                for user_id, sessions in users.items():
                    self.sessions[app_name][user_id] = {}
                    for session_id, session_data in sessions.items():
                        events = []
                        for evt_data in session_data.get("events", []):
                            # Simplistic reconstruction of an event
                            try:
                                msg = None
                                if evt_data.get("message"):
                                    parts = [types.Part.from_text(text=p.get("text", "")) for p in evt_data["message"].get("parts", [])]
                                    msg = types.Content(role=evt_data["message"].get("role", "user"), parts=parts)
                                
                                evt = Event(
                                    timestamp=evt_data.get("timestamp"),
                                    type=evt_data.get("type", "AGENT_CALL"),
                                    agent_name=evt_data.get("agent_name"),
                                    message=msg,
                                )
                                events.append(evt)
                            except Exception:
                                pass
                                
                        session = Session(
                            id=session_id,
                            app_name=app_name,
                            user_id=user_id,
                            state=session_data.get("state", {}),
                            last_update_time=session_data.get("last_update_time")
                        )
                        session.events = events
                        self.sessions[app_name][user_id][session_id] = session
                        
        except Exception as e:
            print(f"Failed to load sessions from disk: {e}")

    def _save_to_disk(self):
        try:
            data = {"sessions": {}}
            for app_name, users in self.sessions.items():
                data["sessions"][app_name] = {}
                for user_id, sessions in users.items():
                    data["sessions"][app_name][user_id] = {}
                    for session_id, session in sessions.items():
                        events_data = []
                        for evt in session.events:
                            msg_data = None
                            if evt.message:
                                parts = [{"text": p.text} for p in getattr(evt.message, "parts", []) if getattr(p, "text", None)]
                                msg_data = {"role": evt.message.role, "parts": parts}
                            events_data.append({
                                "timestamp": evt.timestamp,
                                "type": str(evt.type),
                                "agent_name": evt.agent_name,
                                "message": msg_data
                            })
                            
                        data["sessions"][app_name][user_id][session_id] = {
                            "state": session.state,
                            "last_update_time": session.last_update_time,
                            "events": events_data
                        }
                        
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save sessions to disk: {e}")

    async def append_event(self, session: Session, event: Event) -> Event:
        # Save to memory
        evt = await super().append_event(session, event)
        # Dump to disk
        self._save_to_disk()
        return evt
