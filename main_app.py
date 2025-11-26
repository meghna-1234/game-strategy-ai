from memory_bank import MemoryBank
import streamlit as st
import uuid
from datetime import datetime
from session_manager import InMemorySessionService

# Initialize session service
if 'session_service' not in st.session_state:
    st.session_state.session_service = InMemorySessionService()
    print("Initialized session service")

# Initialize memory bank
if 'memory_bank' not in st.session_state:
    st.session_state.memory_bank = MemoryBank()

def generate_enhanced_strategy(strategy_data: dict, personalization: dict, user_input: str) -> str:
    """Generate strategy enhanced with memory insights"""
    
    # Base strategy templates
    base_strategies = {
        "chess": """
**♟️ Chess Strategy Analysis**

**Recommended {strategy_type} Approach:**
- **Primary Tactic:** {primary_tactic}
- **Risk Assessment:** {risk_tolerance} - {risk_description}
- **Success Probability:** {success_probability}%
- **Follow-up:** {follow_up_plan}

**Memory-Enhanced Insights:**
{personalization_notes}

**Key Insights:**
- Control the center with your pawns
- Develop minor pieces actively
- Watch for bishop exchanges
- {additional_insight}
        """,
        "poker": """
**🃏 Poker Strategy Analysis**

**Recommended {strategy_type} Play:**
- **Action:** {primary_action}
- **Risk Level:** {risk_tolerance}
- **Position Advantage:** {position_analysis}
- **Fold Equity:** {fold_equity}

**Memory-Enhanced Insights:**
{personalization_notes}

**Key Considerations:**
- {consideration_1}
- {consideration_2}
- {consideration_3}
        """
    }
    
    # Personalization notes
    if personalization and personalization.get('confidence_level') != 'low':
        personalization_notes = f"• Personalized based on your historical preferences\n• {personalization.get('confidence_level', 'medium').title()} confidence level\n• Your success rate: {personalization.get('user_success_rate', 'Calculating...')}"
        if personalization.get('proven_tactics'):
            personalization_notes += f"\n• Leveraging your proven tactics: {', '.join(personalization['proven_tactics'][:2])}"
    else:
        personalization_notes = "• Learning your preferences (more data needed for personalization)"
    
    # Game-specific strategy details
    strategy_details = {
        "chess": {
            "primary_tactic": "Knight to G5, putting pressure on F7" if strategy_data['strategy_type'] == "Aggressive" else "Solid center control with pawns",
            "risk_description": "This creates attacking opportunities" if strategy_data['risk_tolerance'] in ["High Risk", "All In"] else "Maintains solid position",
            "success_probability": 75 if strategy_data['risk_tolerance'] in ["High Risk", "All In"] else 85,
            "follow_up_plan": "Prepare queen-side castle and develop rook",
            "additional_insight": "Consider your opponent's typical responses based on game phase"
        },
        "poker": {
            "primary_action": "Raise 3x big blind" if strategy_data['strategy_type'] == "Aggressive" else "Call and observe",
            "position_analysis": "Use early position aggressively" if strategy_data['strategy_type'] == "Aggressive" else "Play cautiously from early position",
            "fold_equity": "High" if strategy_data['strategy_type'] == "Aggressive" else "Medium",
            "consideration_1": "Ace-King suited plays well against most hands",
            "consideration_2": "Be prepared to re-raise if facing aggression",
            "consideration_3": "Watch for flush draw opportunities"
        }
    }
    
    # Get game-specific details or use defaults
    details = strategy_details.get(strategy_data['game_type'], {})
    
    # Use base strategy or default template
    template = base_strategies.get(strategy_data['game_type'], 
        """**🤖 AI Strategy for {game_type}**

**Recommended {strategy_type} Approach:**
- **Analysis:** {user_input}
- **Risk Level:** {risk_tolerance}
- **Detail Level:** {detail_level}

**Memory-Enhanced Insights:**
{personalization_notes}
        """)
    
    # Format the strategy
    formatted_strategy = template.format(
        strategy_type=strategy_data['strategy_type'],
        risk_tolerance=strategy_data['risk_tolerance'],
        personalization_notes=personalization_notes,
        user_input=user_input[:200] + "..." if len(user_input) > 200 else user_input,
        game_type=strategy_data['game_type'],
        detail_level=strategy_data['detail_level'],
        **details
    )
    
    return formatted_strategy

# Page configuration
st.set_page_config(
    page_title="Game Strategy AI",
    page_icon="🎮",
    layout="wide"
)

# Main title
st.title("🎮 Game Strategy AI")
st.markdown("### Multi-Agent AI System for Expert Gaming Strategies")

# Sidebar for session management
st.sidebar.header("🔐 Session Management")

# User session management
if 'user_session_id' not in st.session_state:
    # New user - show session setup
    st.sidebar.subheader("Start New Session")
    
    user_id = st.sidebar.text_input("Enter your user ID:", "player_" + str(uuid.uuid4())[:8])
    game_type = st.sidebar.selectbox("Select game:", ["chess", "poker", "go", "valorant", "league-of-legends", "custom"])
    
    if st.sidebar.button("🎯 Start Gaming Session"):
        session_id = st.session_state.session_service.create_session(user_id, game_type)
        st.session_state.user_session_id = session_id
        st.session_state.user_id = user_id
        st.session_state.game_type = game_type
        st.sidebar.success(f"Session started! 🚀")
        st.rerun()
else:
    # Existing user - show session info
    session = st.session_state.session_service.get_session(st.session_state.user_session_id)
    
    if session:
        st.sidebar.subheader("Current Session")
        st.sidebar.write(f"**User:** {session.user_id}")
        st.sidebar.write(f"**Game:** {session.game_type}")
        st.sidebar.write(f"**Started:** {session.created_at.strftime('%H:%M:%S')}")
        st.sidebar.write(f"**Conversations:** {len(session.conversation_history)}")
        
        # Session actions
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Refresh Session"):
                st.rerun()
        with col2:
            if st.button("🔚 End Session"):
                # Save memories before ending session
                st.session_state.memory_bank.save_memories()
                del st.session_state.user_session_id
                st.rerun()
        
        # Show session metrics
        metrics = st.session_state.session_service.get_session_metrics()
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 System Metrics")
        st.sidebar.write(f"**Active Sessions:** {metrics['active_sessions']}")
        st.sidebar.write(f"**Total Sessions:** {metrics['total_sessions']}")
        
        # Show memory insights
        memory_insights = st.session_state.memory_bank.get_system_insights()
        if memory_insights:
            st.sidebar.markdown("---")
            st.sidebar.subheader("🧠 Memory Insights")
            st.sidebar.write(f"**Total Users:** {memory_insights['total_users']}")
            st.sidebar.write(f"**Strategies Analyzed:** {memory_insights['total_strategies_analyzed']}")
        
        # Main application interface
        st.header(f"Game Analysis: {session.game_type.upper()}")
        
        # Strategy input section
        st.subheader("🎯 Describe Your Game Situation")
        
        # Example prompts based on game type
        examples = {
            "chess": "e.g., 'I'm white, pieces on E4, D4, knight on F3. Opponent has E5, C5, bishop on C4. Best aggressive strategy?'",
            "poker": "e.g., 'Texas Holdem, I have Ace-King suited, early position. Should I raise or call?'",
            "go": "e.g., 'Mid-game, I control top right corner, opponent invading bottom side. Best response?'",
            "valorant": "e.g., 'Attack side on Ascent, I play Sova. Enemy has OP mid. Best execute strategy?'",
            "custom": "Describe your game situation in detail..."
        }
        
        st.caption(examples.get(session.game_type, examples["custom"]))
        
        user_input = st.text_area(
            "Game situation:",
            height=100,
            placeholder=f"Describe your current {session.game_type} game situation in detail..."
        )
        
        # Strategy options
        col1, col2, col3 = st.columns(3)
        with col1:
            strategy_type = st.selectbox(
                "Strategy Style:",
                ["Balanced", "Aggressive", "Defensive", "Surprise", "Economic"]
            )
        with col2:
            detail_level = st.select_slider(
                "Detail Level:",
                ["Quick", "Standard", "Detailed", "Comprehensive"]
            )
        with col3:
            risk_tolerance = st.select_slider(
                "Risk Level:",
                ["Safe", "Moderate", "High Risk", "All In"]
            )
        
        if st.button("🤖 Generate AI Strategy", type="primary"):
            if user_input.strip():
                with st.spinner("Analyzing game situation with multi-AI system..."):
                    # Get user's memory for personalization
                    user_memory = st.session_state.memory_bank.get_user_memory(session.user_id, session.game_type)
                    
                    # Get personalized recommendations from memory
                    personalization = user_memory.get_personalized_recommendation()
                    
                    # Simulate AI processing (replace with your actual AI calls)
                    import time
                    time.sleep(2)  # Simulate processing time
                    
                    # Create strategy data structure for memory storage
                    strategy_data = {
                        'strategy_type': strategy_type,
                        'risk_tolerance': risk_tolerance,
                        'user_input': user_input,
                        'game_type': session.game_type,
                        'detail_level': detail_level,
                        'personalization': personalization,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Generate enhanced strategy with memory insights
                    strategy_response = generate_enhanced_strategy(strategy_data, personalization, user_input)
                    
                    # Add to session history
                    session.add_conversation(user_input, strategy_response)
                    
                    # Store in memory (simulate success for demo - in real app, use actual success data)
                    user_memory.add_strategy_result(strategy_data, success=True, user_feedback=4)
                    
                    # Save memories to disk
                    st.session_state.memory_bank.save_memories()
                    
                    # Display strategy
                    st.markdown("---")
                    st.subheader("🎯 AI Strategy Recommendation")
                    st.markdown(strategy_response)
                    
                    # Show personalization insights from memory
                    if personalization and personalization.get('confidence_level') != 'low':
                        st.markdown("---")
                        st.subheader("🧠 Personalized Insights")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Confidence Level", personalization.get('confidence_level', 'medium').title())
                            st.metric("Your Success Rate", personalization.get('user_success_rate', 'N/A'))
                        
                        with col2:
                            if personalization.get('proven_tactics'):
                                st.write("**Your Proven Tactics:**")
                                for tactic in personalization['proven_tactics'][:3]:  # Show top 3
                                    st.write(f"• {tactic.title()}")
                        
                        st.info("💡 This strategy is enhanced with insights from your previous successful plays!")
                    
                    # User feedback
                    st.markdown("---")
                    st.subheader("📊 Strategy Feedback")
                    feedback = st.slider("How helpful was this strategy?", 1, 5, 3)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Submit Feedback"):
                            # Update memory with actual user feedback
                            user_memory.add_strategy_result(strategy_data, success=(feedback >= 3), user_feedback=feedback)
                            st.session_state.memory_bank.save_memories()
                            st.success(f"Thanks for your feedback! Rating: {feedback}/5")
                    
                    with col2:
                        if st.button("View Memory Insights"):
                            memory_insights = st.session_state.memory_bank.get_system_insights()
                            st.write("**System Memory Insights:**")
                            st.json(memory_insights)
                        
            else:
                st.warning("Please describe your game situation first!")
    
    else:
        st.error("Session expired or not found. Starting new session...")
        del st.session_state.user_session_id
        st.rerun()

# Footer
st.markdown("---")
st.markdown("Built with Multi-AI System | Session Management Enabled | Memory Enhanced")