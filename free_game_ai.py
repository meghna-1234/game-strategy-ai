import streamlit as st
import random

# Set up the page
st.set_page_config(page_title="FREE Game Strategy AI", page_icon="🎮")

# Title and description
st.title("🎮 FREE Game Strategy AI")
st.write("**No API costs!** I'll help you win ANY game with expert strategies!")

# Game input form
st.header("🎯 Your Game Challenge")
game_name = st.text_input("What game are you playing?", placeholder="e.g., Dark Souls, Chess, Minecraft, Fortnite")

situation = st.text_area(
    "Describe your situation:", 
    placeholder="e.g., I'm stuck on the first boss...\nI keep losing in multiplayer...\nI can't solve this puzzle...",
    height=100
)

difficulty = st.selectbox("How difficult is this challenge?", ["Easy", "Medium", "Hard", "Very Hard"])

# Expert game knowledge database
GAME_STRATEGIES = {
    "dark souls": {
        "boss fights": [
            "Learn attack patterns - most bosses have 3-5 move combos",
            "Stay medium distance to bait specific attacks", 
            "Roll through attacks, not away from them",
            "Use elemental weaknesses - check boss color for hints",
            "Upgrade your weapon to +6 minimum for mid-game bosses"
        ],
        "general": [
            "Patience is key - don't get greedy with attacks",
            "Manage stamina - always leave enough for a dodge",
            "Explore thoroughly for better gear and estus shards",
            "Don't be afraid to summon help for tough areas",
            "Level vigor first - survivability is more important than damage early"
        ]
    },
    "chess": {
        "opening": [
            "Control the center with pawns and pieces",
            "Develop knights and bishops early",
            "Castle your king to safety",
            "Don't move the same piece multiple times in opening",
            "Connect your rooks"
        ],
        "midgame": [
            "Look for tactical opportunities - pins, forks, skewers",
            "Improve your worst-placed piece",
            "Create pawn weaknesses in opponent's position",
            "Trade pieces when you're ahead",
            "Keep your king safe"
        ]
    },
    "minecraft": {
        "survival": [
            "Punch trees first to get wood",
            "Build shelter before nightfall",
            "Craft wooden tools then stone tools",
            "Find coal for torches or make charcoal from wood",
            "Don't dig straight down - always staircase mine"
        ],
        "combat": [
            "Use bow and arrow for dangerous mobs",
            "Carry a water bucket for fall damage prevention",
            "Create mob farms for XP and resources",
            "Use shield to block attacks",
            "Enchant your gear as soon as possible"
        ]
    },
    "fortnite": {
        "building": [
            "Practice 90s turns for quick high ground",
            "Master the ramp-wall-floor push combo",
            "Use pyramids for quick cover",
            "Edit doors and windows for surprise attacks",
            "Build defensively when being shot at"
        ],
        "combat": [
            "Aim for headshots - they do double damage",
            "Use shotguns for close range, AR for medium",
            "Crouch while shooting for better accuracy",
            "Listen for enemy footsteps and building",
            "Use natural cover before building"
        ]
    },
    "valorant": {
        "aiming": [
            "Practice crosshair placement at head level",
            "Learn spray patterns for each weapon",
            "Tap fire at long range, spray at close range",
            "Use the Range to warm up before matches",
            "Focus on positioning over raw aim"
        ],
        "game sense": [
            "Learn common angles and pre-aim them",
            "Use abilities to gain information",
            "Coordinate with teammates for site executes",
            "Save your ultimate for important rounds",
            "Play time when defending - don't peek unnecessarily"
        ]
    }
}

def get_smart_strategy(game, situation, difficulty):
    """Generate smart strategy using rule-based AI"""
    
    game_lower = game.lower()
    situation_lower = situation.lower()
    
    strategy = f"# 🎯 Strategy for {game}\n\n"
    strategy += f"**Situation:** {situation}\n"
    strategy += f"**Difficulty:** {difficulty}\n\n"
    
    # Check if we have specific strategies for this game
    found_strategy = False
    
    for known_game, strategies in GAME_STRATEGIES.items():
        if known_game in game_lower:
            strategy += "## 🚀 Immediate Actions:\n"
            # Add relevant strategies based on situation
            if "boss" in situation_lower or "fight" in situation_lower:
                for tip in strategies.get("boss fights", strategies["general"]):
                    strategy += f"• {tip}\n"
            elif "open" in situation_lower or "begin" in situation_lower:
                for tip in strategies.get("opening", strategies["general"]):
                    strategy += f"• {tip}\n"
            elif "aim" in situation_lower or "shoot" in situation_lower:
                for tip in strategies.get("aiming", strategies["general"]):
                    strategy += f"• {tip}\n"
            elif "build" in situation_lower:
                for tip in strategies.get("building", strategies["general"]):
                    strategy += f"• {tip}\n"
            else:
                for tip in strategies["general"][:5]:
                    strategy += f"• {tip}\n"
            found_strategy = True
            break
    
    # Generic strategy for unknown games
    if not found_strategy:
        strategy += "## 🚀 Immediate Actions:\n"
        generic_tips = [
            "Analyze what's causing you to fail and focus on that",
            "Watch tutorial videos or gameplay of experts",
            "Take breaks - coming back fresh often helps",
            "Practice the specific challenging section repeatedly",
            "Adjust game settings or difficulty if available",
            "Look for better equipment or upgrades you might have missed",
            "Learn enemy patterns and attack tells"
        ]
        for tip in generic_tips[:5]:
            strategy += f"• {tip}\n"
    
    strategy += "\n## 📈 Short-term Strategy:\n"
    strategy += "• Master the core mechanics of the game\n"
    strategy += "• Focus on one improvement at a time\n"
    strategy += "• Learn from each failure - identify what went wrong\n"
    strategy += "• Build consistency in your gameplay\n"
    
    strategy += "\n## 🏆 Long-term Approach:\n"
    strategy += "• Develop muscle memory for key actions\n"
    strategy += "• Study advanced techniques for your game\n"
    strategy += "• Join community forums for specific advice\n"
    strategy += "• Record your gameplay to analyze mistakes\n"
    
    strategy += "\n## 💡 Pro Tips:\n"
    strategy += "• Stay calm and patient - frustration leads to more mistakes\n"
    strategy += "• Watch the enemy, not your character\n"
    strategy += "• Learn when to be aggressive vs defensive\n"
    strategy += "• Practice regularly but take breaks to avoid burnout\n"
    
    return strategy

# When user clicks the button
if st.button("🚀 Get FREE Winning Strategy", type="primary"):
    if not game_name or not situation:
        st.error("❌ Please fill in both the game name and your situation!")
    else:
        # Show loading spinner
        with st.spinner("🤔 Analyzing your game and generating expert strategy..."):
            try:
                # Generate strategy using our smart rules
                strategy = get_smart_strategy(game_name, situation, difficulty)
                
                # Display the strategy
                st.success("✅ FREE Strategy Generated!")
                st.markdown(strategy)
                
                # Success message
                st.balloons()
                st.info("💡 **This strategy was generated using expert game knowledge - no API costs!**")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try being more specific about your game and situation.")

# Game examples
st.markdown("---")
st.header("🎮 Popular Games I Can Help With:")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Action/RPG Games**")
    st.write("• Dark Souls/Bloodborne")
    st.write("• Elden Ring")
    st.write("• Sekiro")
    st.write("• Hollow Knight")

with col2:
    st.markdown("**Strategy Games**")
    st.write("• Chess")
    st.write("• StarCraft")
    st.write("• Civilization")
    st.write("• XCOM")

with col3:
    st.markdown("**Shooter Games**")
    st.write("• Fortnite")
    st.write("• Valorant")
    st.write("• Call of Duty")
    st.write("• Apex Legends")

with col1:
    st.markdown("**Survival Games**")
    st.write("• Minecraft")
    st.write("• Terraria")
    st.write("• Rust")
    st.write("• Ark")

with col2:
    st.markdown("**MOBA Games**")
    st.write("• League of Legends")
    st.write("• DOTA 2")
    st.write("• Smite")
    st.write("• Heroes of the Storm")

with col3:
    st.markdown("**Sports/Racing**")
    st.write("• FIFA/Madden")
    st.write("• Rocket League")
    st.write("• Forza")
    st.write("• Gran Turismo")

# Footer
st.markdown("---")
st.markdown("### 🆓 100% Free - No API Keys Needed!")
st.markdown("This AI uses expert game knowledge and smart rules to provide winning strategies.")
st.markdown("**Built with ❤️ using Python and Streamlit**")