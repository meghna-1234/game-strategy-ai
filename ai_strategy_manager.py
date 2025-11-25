import google.generativeai as genai
import requests
import random
import os
import streamlit as st
from dotenv import load_dotenv
import time

load_dotenv()

class AIStrategyManager:
    def __init__(self):
        self.gemini_configured = False
        self.setup_gemini()
    
    def setup_gemini(self):
        try:
            api_key = (os.getenv('GEMINI_API_KEY') or 
                      st.secrets.get('GEMINI_API_KEY') or 
                      "your_gemini_api_key_here")
            
            if api_key and api_key != "your_gemini_api_key_here":
                genai.configure(api_key=api_key)
                self.gemini_configured = True
                st.success("✅ Gemini AI Agent: ONLINE")
            else:
                st.warning("⚠️ Gemini API key not found - using fallback AI services")
        except Exception as e:
            st.error(f"❌ Gemini setup failed: {e}")
    
    def get_strategy_tier1_gemini(self, game_state, game_type, analysis_results):
        if not self.gemini_configured:
            return None
            
        try:
            prompt = f"""
            ACT as professional gaming strategist. Provide SPECIFIC advice.

            GAME: {game_type}
            SITUATION: {game_state}
            ANALYSIS: {analysis_results}

            Provide in EXACT format:
            🎯 IMMEDIATE ACTIONS:
            1. [Action 1]
            2. [Action 2] 
            3. [Action 3]

            ⚠️ AVOID:
            • [What to avoid]

            📊 RESOURCES:
            • [Resource tips]

            🎲 SUCCESS: [X%] - [Reason]
            """
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return f"**🤖 Gemini Pro Analysis:**\n\n{response.text}"
            
        except Exception as e:
            return None
    
    def get_strategy_tier2_free_api(self, game_state, game_type):
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={'Content-Type': 'application/json'},
                json={
                    'model': 'google/gemma-7b-it:free',
                    'messages': [{
                        'role': 'user',
                        'content': f"As {game_type} expert, give 3 tips for: {game_state}"
                    }]
                },
                timeout=5
            )
            
            if response.status_code == 200:
                advice = response.json()['choices'][0]['message']['content']
                return f"**🌐 Cloud AI Analysis:**\n\n{advice}"
        except:
            pass
        return None
    
    def get_strategy_tier3_simulated(self, game_state, game_type):
        strategies = {
            "chess": [
                "Control center with pawns and knights",
                "Castle early for king safety",
                "Develop pieces before attacking",
                "Avoid moving same piece repeatedly"
            ],
            "fortnite": [
                "Build for high ground advantage",
                "Carry healing items always",
                "Use natural cover while rotating",
                "Prioritize headshot accuracy"
            ],
            "minecraft": [
                "Base near water and food sources",
                "Light areas to prevent mob spawns",
                "Use fortune enchantment for resources",
                "Carry water bucket for falls"
            ],
            "valorant": [
                "Use abilities for site execution",
                "Communicate enemy positions",
                "Manage economy for full buys",
                "Trade kills effectively"
            ],
            "default": [
                "Analyze opponent patterns",
                "Manage resources efficiently",
                "Use positioning advantages",
                "Coordinate with team"
            ]
        }
        
        game_strats = strategies.get(game_type.lower(), strategies["default"])
        selected = random.sample(game_strats, min(3, len(game_strats)))
        
        response = f"""**🎮 AI Strategy Report**

Game: {game_type}
Situation: {game_state}

🎯 RECOMMENDATIONS:
"""
        for i, strat in enumerate(selected, 1):
            response += f"{i}. {strat}\n"
        
        response += f"""
📊 ASSESSMENT:
• Success: {random.randint(65, 92)}%
• Risk: {random.choice(['Low', 'Medium', 'High'])}
• Difficulty: {random.choice(['Easy', 'Medium', 'Hard'])}

🤖 Multi-AI System Analysis Complete
"""
        return response
    
    def get_ai_strategy(self, game_state, game_type, analysis_results=None):
        st.info("🔍 Multi-AI System Analyzing...")
        
        with st.spinner("Processing..."):
            time.sleep(1)
            
            strategy = self.get_strategy_tier1_gemini(game_state, game_type, analysis_results)
            if strategy:
                st.success("✅ Primary AI: Gemini Pro")
                return strategy, "gemini"
            
            strategy = self.get_strategy_tier2_free_api(game_state, game_type)
            if strategy:
                st.warning("✅ Backup AI: Cloud Services")
                return strategy, "cloud"
            
            st.info("✅ Fallback AI: Simulation")
            strategy = self.get_strategy_tier3_simulated(game_state, game_type)
            return strategy, "simulated"