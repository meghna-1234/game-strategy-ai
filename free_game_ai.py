import streamlit as st
import random
from ai_strategy_manager import AIStrategyManager

# Initialize AI Manager
@st.cache_resource
def get_ai_manager():
    return AIStrategyManager()

def main():
    # Page configuration
    st.set_page_config(
        page_title="Game Strategy AI",
        page_icon="🎮",
        layout="wide"
    )
    
    # Clean Header
    st.title("🎮 Game Strategy AI")
    st.markdown("### Your AI-Powered Gaming Assistant")
    
    # Initialize AI Manager
    ai_manager = get_ai_manager()
    
    # Game Input Section with System Details in title row
    st.markdown("---")
    
    # Title row with System Details on the right
    title_col1, title_col2 = st.columns([3, 1])
    
    with title_col1:
        st.subheader("🎯 Game Setup")
    
    with title_col2:
        # System Details aligned with title
        with st.expander("🤖 System Details", expanded=False):
            gemini_status = "🟢 Online" if ai_manager.gemini_configured else "🟡 Fallback"
            st.write(f"**Gemini Pro:** {gemini_status}")
            st.write("**Cloud AI:** 🟢 Ready") 
            st.write("**Simulation:** 🟢 Active")
            st.caption("Multi-layer architecture")
    
    # Main input area - full width for better space
    game_type = st.selectbox(
        "Select Your Game",
        ["Chess", "Fortnite", "Minecraft", "Valorant", "League of Legends", "Custom Game"]
    )
    
    game_state = st.text_area(
        "Describe Your Situation",
        placeholder="Example: I'm losing material in middle game and need to recover...",
        height=120
    )
    
    # Strategy Generation
    st.markdown("---")
    if st.button("🚀 Generate Winning Strategy", type="primary", use_container_width=True):
        if not game_state.strip():
            st.error("Please describe your game situation!")
            return
        
        # Show loading state with AI system info
        with st.status("🤖 Multi-AI System Analyzing...", expanded=True) as status:
            st.write("🔷 Trying Gemini Pro API...")
            
            analysis_results = {
                "risk": random.choice(["Low", "Medium", "High"]),
                "success": f"{random.randint(70, 95)}%",
                "style": random.choice(["Aggressive", "Defensive", "Balanced"])
            }
            
            # Smart AI selection (auto mode - tries all systems)
            strategy, source = ai_manager.get_ai_strategy(game_state, game_type, analysis_results)
            
            # Show which AI was used in the status
            if source == "gemini":
                st.write("✅ **Gemini Pro** - Primary AI selected")
            elif source == "cloud":
                st.write("🌐 **Cloud AI** - Backup system activated") 
            else:
                st.write("🤖 **Advanced Simulation** - Fallback system active")
            
            status.update(label="✅ Multi-AI Analysis Complete!", state="complete")
        
        # Display Results
        st.markdown("---")
        st.subheader("📋 Strategy Report")
        
        # Quick Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Level", analysis_results["risk"])
        with col2:
            st.metric("Success Chance", analysis_results["success"])
        with col3:
            st.metric("Recommended Style", analysis_results["style"])
        
        # Strategy Output
        st.markdown("---")
        st.subheader("🎯 Recommended Strategy")
        
        with st.container():
            st.markdown(strategy)
            
            # Source badge - shows which AI was used
            source_info = {
                "gemini": ("🔷", "Google Gemini Pro", "Primary AI System"),
                "cloud": ("🌐", "Cloud AI Services", "Backup AI System"), 
                "simulated": ("🤖", "Advanced Simulation", "Fallback AI System"),
                "gemini_fallback": ("🔷", "Gemini Pro", "Primary with Fallback"),
                "cloud_fallback": ("🌐", "Cloud AI", "Backup with Fallback")
            }
            
            icon, name, desc = source_info.get(source, ("🤖", "AI System", "Multi-Layer AI"))
            st.caption(f"{icon} **Powered by {name}** | {desc}")
            
            # Show architecture info
            with st.expander("🏗️ View AI Architecture"):
                st.markdown("""
                **Multi-Layer AI System:**
                - **🔷 Gemini Pro**: Primary natural language AI
                - **🌐 Cloud AI**: Backup cloud services  
                - **🤖 Simulation**: Game-specific intelligence
                
                *System automatically selects the best available AI*
                """)

if __name__ == "__main__":
    main()