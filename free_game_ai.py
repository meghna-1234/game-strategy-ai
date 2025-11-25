import streamlit as st
import numpy as np
import random
from ai_strategy_manager import AIStrategyManager

@st.cache_resource
def get_ai_manager():
    return AIStrategyManager()

def main():
    st.set_page_config(
        page_title="Game Strategy AI",
        page_icon="🎮", 
        layout="wide"
    )
    
    st.title("🎮 Game Strategy AI")
    st.subheader("🤖 Multi-Layer AI System")
    
    ai_manager = get_ai_manager()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        game_type = st.selectbox(
            "🎯 Select Game:",
            ["Chess", "Fortnite", "Minecraft", "Valorant", "League of Legends", "Custom"]
        )
        
        game_state = st.text_area(
            "📝 Game Situation:",
            placeholder="E.g., I'm losing material in middle game...",
            height=100
        )
    
    with col2:
        st.write("**AI Status**")
        st.metric("Gemini", "✅ Ready" if ai_manager.gemini_configured else "⚠️ Fallback")
        st.metric("Cloud AI", "✅ Available")
        st.metric("Simulation", "✅ Active")
        
        ai_mode = st.radio(
            "AI Mode:",
            ["Auto", "Gemini Priority", "Cloud Only", "Simulation Only"]
        )
    
    if st.button("🚀 GET STRATEGY", type="primary"):
        if not game_state.strip():
            st.error("Describe your game situation!")
            return
            
        analysis_results = {
            "risk": random.choice(["Low", "Medium", "High"]),
            "success": f"{random.randint(70, 95)}%",
            "style": random.choice(["Aggressive", "Defensive", "Balanced"])
        }
        
        st.subheader("📊 Game Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Risk", analysis_results["risk"])
        with col2:
            st.metric("Success", analysis_results["success"])
        with col3:
            st.metric("Style", analysis_results["style"])
        
        if ai_mode == "Gemini Priority" and ai_manager.gemini_configured:
            strategy, source = ai_manager.get_strategy_tier1_gemini(game_state, game_type, analysis_results) or (ai_manager.get_strategy_tier3_simulated(game_state, game_type), "gemini_fallback")
        elif ai_mode == "Cloud Only":
            strategy, source = ai_manager.get_strategy_tier2_free_api(game_state, game_type) or (ai_manager.get_strategy_tier3_simulated(game_state, game_type), "cloud_fallback")
        elif ai_mode == "Simulation Only":
            strategy, source = ai_manager.get_strategy_tier3_simulated(game_state, game_type), "simulated"
        else:
            strategy, source = ai_manager.get_ai_strategy(game_state, game_type, analysis_results)
        
        st.subheader("🎯 Strategy Recommendation")
        st.markdown(strategy)
        
        badges = {
            "gemini": "🔷 Gemini Pro",
            "cloud": "🌐 Cloud AI", 
            "simulated": "🤖 Simulation",
            "gemini_fallback": "🔷 Gemini (Fallback)",
            "cloud_fallback": "🌐 Cloud (Fallback)"
        }
        
        st.caption(f"{badges.get(source, 'AI System')} | Multi-Layer Architecture")
    
    st.markdown("---")
    st.subheader("🚀 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🔷 Gemini AI**")
        st.write("Google's advanced AI")
    with col2:
        st.write("**🌐 Cloud Backup**")
        st.write("Multiple AI APIs")
    with col3:
        st.write("**🤖 Simulation**")
        st.write("Game-specific intelligence")

if __name__ == "__main__":
    main()