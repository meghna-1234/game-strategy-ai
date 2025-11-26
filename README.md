# 🎮 Game Strategy AI Agent

A smart AI assistant that provides winning strategies for ANY video game! Built with Python and Streamlit.

## 🚀 Features

- **Free to use** - No API costs required
- **Expert strategies** for popular games  
- **Smart generic advice** for any game
- **Beautiful web interface**
- **100% Python** - Easy to modify and extend

## 🆕 Latest Updates

- **Enhanced AI logic** - Improved decision-making algorithms
- **Improved strategy algorithms** - More accurate game predictions
- **Web deployment** - Live website at [github.io](https://meghna-1234.github.io/game-strategy-ai/)
- **Automated CI/CD** - GitHub Actions for automatic deployments
- **Professional documentation** - Enhanced project structure

## 🎯 Supported Games

- **Action/RPG**: Dark Souls, Elden Ring, Sekiro
- **Strategy**: Chess, StarCraft, Civilization  
- **Shooters**: Fortnite, Valorant, Call of Duty
- **Survival**: Minecraft, Terraria
- **MOBA**: League of Legends, DOTA 2
- **And many more!**

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/meghna-1234/game-strategy-ai.git
cd game-strategy-ai

## 🎯 Session Management Feature

The system now includes robust session management:

- **User Session Tracking**: Each user gets a unique session ID
- **Conversation History**: All strategy conversations are stored per session
- **Session Timeouts**: Automatic cleanup of expired sessions (2-hour timeout)
- **Session Metrics**: Real-time monitoring of active sessions and usage patterns
- **Game State Persistence**: Maintains game context across interactions

**Technical Implementation**:
- `InMemorySessionService` class for session management
- `GameSession` class for individual session data
- Integrated with Streamlit state management
- Demonstrates course concept: **Sessions & Memory**