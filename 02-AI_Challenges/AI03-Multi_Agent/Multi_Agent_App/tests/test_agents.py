import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.intent_detector import IntentDetectorAgent
from agents.inventory_agent import InventoryAgent
from agents.recommendations_agent import RecommendationsAgent
from agents.response_formatter import ResponseFormatterAgent

try:
    print('Testing Agent Initialization')
    print('=' * 35)
    
    # Test each agent
    intent_agent = IntentDetectorAgent()
    print(f'✅ {intent_agent.name} initialized')
    
    inventory_agent = InventoryAgent()
    print(f'✅ {inventory_agent.name} initialized')
    
    rec_agent = RecommendationsAgent()
    print(f'✅ {rec_agent.name} initialized')
    
    formatter_agent = ResponseFormatterAgent()
    print(f'✅ {formatter_agent.name} initialized')
    
    print('\n✅ All agents successfully initialized!')
    
except Exception as e:
    print(f'❌ Agent initialization error: {e}')
    import traceback
    traceback.print_exc()