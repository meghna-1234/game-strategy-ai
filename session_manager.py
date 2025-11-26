import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class GameSession:
    def __init__(self, session_id: str, user_id: str, game_type: str):
        self.session_id = session_id
        self.user_id = user_id
        self.game_type = game_type
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.game_state: Dict[str, Any] = {}
        self.conversation_history = []
        self.strategy_preferences = {}
        
    def update_activity(self):
        self.last_activity = datetime.now()
    
    def add_conversation(self, user_input: str, ai_response: str):
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'ai': ai_response
        })
        self.update_activity()
        
    def to_dict(self):
        """Convert session to dictionary for easy serialization"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'game_type': self.game_type,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'conversation_count': len(self.conversation_history)
        }

class InMemorySessionService:
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self.session_timeout = timedelta(hours=2)
    
    def create_session(self, user_id: str, game_type: str) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = GameSession(session_id, user_id, game_type)
        print(f"Created new session: {session_id} for user {user_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        if session_id not in self.sessions:
            print(f"Session not found: {session_id}")
            return None
            
        session = self.sessions[session_id]
        
        # Check if session expired
        if datetime.now() - session.last_activity > self.session_timeout:
            print(f"Session expired: {session_id}")
            del self.sessions[session_id]
            return None
            
        session.update_activity()
        return session
    
    def update_game_state(self, session_id: str, game_state: Dict[str, Any]):
        session = self.get_session(session_id)
        if session:
            session.game_state.update(game_state)
            print(f"Updated game state for session: {session_id}")
    
    def get_session_metrics(self) -> Dict[str, Any]:
        now = datetime.now()
        active_sessions = [
            session for session in self.sessions.values()
            if now - session.last_activity < self.session_timeout
        ]
        
        return {
            'total_sessions': len(self.sessions),
            'active_sessions': len(active_sessions),
            'session_ids': list(self.sessions.keys()),
            'sessions_by_game': self._get_sessions_by_game_type()
        }
    
    def _get_sessions_by_game_type(self) -> Dict[str, int]:
        game_counts = {}
        for session in self.sessions.values():
            game_counts[session.game_type] = game_counts.get(session.game_type, 0) + 1
        return game_counts
    
    def cleanup_expired_sessions(self):
        now = datetime.now()
        expired = []
        for session_id, session in self.sessions.items():
            if now - session.last_activity > self.session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        print(f"Cleaned up {len(expired)} expired sessions")
        return len(expired)