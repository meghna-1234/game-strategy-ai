from session_manager import InMemorySessionService

# Test the session manager
def test_session_management():
    print("Testing Session Management...")
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a session
    session_id = session_service.create_session("test_user", "chess")
    print(f"Created session: {session_id}")
    
    # Retrieve the session
    session = session_service.get_session(session_id)
    if session:
        print(f"Retrieved session for user: {session.user_id}")
        
        # Add some conversation
        session.add_conversation("What's the best opening?", "Try the Queen's Gambit!")
        print("Added conversation to session")
    
    # Check metrics
    metrics = session_service.get_session_metrics()
    print(f"Session Metrics: {metrics}")
    
    # Test cleanup
    cleaned = session_service.cleanup_expired_sessions()
    print(f"Cleaned up {cleaned} sessions")

if __name__ == "__main__":
    test_session_management()