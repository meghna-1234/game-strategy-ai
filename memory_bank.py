import json
import pickle
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

class StrategyMemory:
    def __init__(self, user_id: str, game_type: str):
        self.user_id = user_id
        self.game_type = game_type
        self.successful_strategies: List[Dict[str, Any]] = []
        self.failed_strategies: List[Dict[str, Any]] = []
        self.learning_patterns: Dict[str, Any] = {}
        self.user_preferences = {
            'preferred_strategy_style': 'balanced',
            'risk_tolerance': 'moderate',
            'detail_level': 'standard'
        }
    
    def add_strategy_result(self, strategy: Dict[str, Any], success: bool, user_feedback: int = 0):
        strategy_record = {
            'strategy_id': len(self.successful_strategies) + len(self.failed_strategies) + 1,
            'strategy_data': strategy,
            'timestamp': datetime.now(),
            'success': success,
            'user_feedback': user_feedback,
            'context': strategy.get('context', {})
        }
        
        if success or user_feedback >= 4:  # Scale of 1-5
            self.successful_strategies.append(strategy_record)
        else:
            self.failed_strategies.append(strategy_record)
        
        self._update_learning_patterns()
        print(f"Added strategy to memory. Success: {success}, Total successful: {len(self.successful_strategies)}")
    
    def _update_learning_patterns(self):
        # Analyze successful strategies for patterns
        if self.successful_strategies:
            recent_successes = self.successful_strategies[-5:]  # Last 5 successes
            
            # Extract patterns from successful strategies
            strategy_styles = []
            risk_levels = []
            successful_moves = []
            
            for success in recent_successes:
                strategy_data = success['strategy_data']
                if 'strategy_type' in strategy_data:
                    strategy_styles.append(strategy_data['strategy_type'])
                if 'risk_tolerance' in strategy_data:
                    risk_levels.append(strategy_data['risk_tolerance'])
                if 'primary_tactic' in strategy_data:
                    successful_moves.append(strategy_data['primary_tactic'])
            
            # Update learning patterns
            self.learning_patterns = {
                'preferred_strategy_styles': self._get_most_common(strategy_styles),
                'effective_risk_levels': self._get_most_common(risk_levels),
                'successful_tactics': self._get_most_common(successful_moves),
                'success_rate': len(self.successful_strategies) / max(1, (len(self.successful_strategies) + len(self.failed_strategies))),
                'total_strategies': len(self.successful_strategies) + len(self.failed_strategies),
                'last_updated': datetime.now()
            }
    
    def _get_most_common(self, items: List[str]) -> List[str]:
        if not items:
            return []
        return pd.Series(items).value_counts().head(3).index.tolist()
    
    def get_personalized_recommendation(self) -> Dict[str, Any]:
        """Generate personalized strategy recommendations based on history"""
        if not self.learning_patterns:
            return {}
        
        return {
            'recommended_strategy_style': self.learning_patterns.get('preferred_strategy_styles', ['balanced'])[0],
            'suggested_risk_level': self.learning_patterns.get('effective_risk_levels', ['moderate'])[0],
            'proven_tactics': self.learning_patterns.get('successful_tactics', []),
            'user_success_rate': f"{self.learning_patterns.get('success_rate', 0) * 100:.1f}%",
            'confidence_level': 'high' if self.learning_patterns.get('success_rate', 0) > 0.7 else 'medium'
        }

class MemoryBank:
    def __init__(self, storage_file="memory_bank.pkl"):
        self.storage_file = storage_file
        self.user_memories: Dict[str, StrategyMemory] = {}
        self.load_memories()
    
    def get_user_memory(self, user_id: str, game_type: str) -> StrategyMemory:
        key = f"{user_id}_{game_type}"
        if key not in self.user_memories:
            self.user_memories[key] = StrategyMemory(user_id, game_type)
            print(f"Created new memory for user: {user_id}, game: {game_type}")
        return self.user_memories[key]
    
    def save_memories(self):
        try:
            with open(self.storage_file, 'wb') as f:
                pickle.dump(self.user_memories, f)
            print(f"Saved memories for {len(self.user_memories)} users")
        except Exception as e:
            print(f"Error saving memories: {e}")
    
    def load_memories(self):
        try:
            with open(self.storage_file, 'rb') as f:
                self.user_memories = pickle.load(f)
            print(f"Loaded memories for {len(self.user_memories)} users")
        except FileNotFoundError:
            print("No existing memory file found. Starting fresh.")
            self.user_memories = {}
        except Exception as e:
            print(f"Error loading memories: {e}")
            self.user_memories = {}
    
    def get_system_insights(self) -> Dict[str, Any]:
        """Get aggregate insights across all users"""
        if not self.user_memories:
            return {}
        
        total_strategies = 0
        total_success_rate = 0
        game_insights = {}
        
        for memory in self.user_memories.values():
            total_strategies += memory.learning_patterns.get('total_strategies', 0)
            total_success_rate += memory.learning_patterns.get('success_rate', 0)
            
            # Track by game type
            if memory.game_type not in game_insights:
                game_insights[memory.game_type] = {
                    'users': 0,
                    'total_strategies': 0,
                    'avg_success_rate': 0
                }
            game_insights[memory.game_type]['users'] += 1
            game_insights[memory.game_type]['total_strategies'] += memory.learning_patterns.get('total_strategies', 0)
        
        avg_success = total_success_rate / len(self.user_memories) if self.user_memories else 0
        
        return {
            'total_users': len(self.user_memories),
            'total_strategies_analyzed': total_strategies,
            'average_success_rate': f"{avg_success * 100:.1f}%",
            'game_insights': game_insights,
            'most_popular_games': sorted(game_insights.keys(), key=lambda x: game_insights[x]['users'], reverse=True)[:3]
        }