import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.intent_detector import IntentDetectorAgent
from models.data_models import UserQuery, ConversationContext

agent = IntentDetectorAgent()
test_queries = [
    'I want to find running shoes',
    'Can you recommend headphones?',
    'What are your store hours?',
    'Show me laptops under $1000',
    'Do you have wireless mice?'
]

print('Testing intent detection (offline):')
print('=' * 50)
for query_text in test_queries:
    try:
        intent = agent._detect_intent_rules(query_text)
        print(f'Query: "{query_text}"')
        print(f'Intent: {intent.type.value}')
        print(f'Confidence: {intent.confidence}')
        print(f'Entities: {intent.entities}')
        print('-' * 30)
    except Exception as e:
        print(f'❌ Error with query "{query_text}": {e}')