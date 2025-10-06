import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from models.data_models import UserQuery, ConversationContext
from agents.intent_detector import IntentDetectorAgent
from agents.inventory_agent import InventoryAgent
from agents.recommendations_agent import RecommendationsAgent
from agents.response_formatter import ResponseFormatterAgent

async def test_pipeline():
    print('Testing Complete Multi-Agent Pipeline')
    print('=' * 50)
    
    # Initialize all agents
    intent_agent = IntentDetectorAgent()
    inventory_agent = InventoryAgent()
    rec_agent = RecommendationsAgent()
    formatter_agent = ResponseFormatterAgent()
    
    # Test different types of queries
    test_queries = [
        'I want to find good wireless headphones',
        'Can you recommend some laptops for gaming?',
        'Show me running shoes under $100'
    ]
    
    for query_text in test_queries:
        print(f'🔍 Testing Query: "{query_text}"')
        print('-' * 60)
        
        try:
            # Create context
            context = ConversationContext(
                user_query=UserQuery(text=query_text, user_id='test_user')
            )
            
            # Step 1: Intent Detection
            print('Step 1: Intent Detection')
            intent_response = await intent_agent.process(context)
            print(f'✅ Intent: {context.intent.type.value} (confidence: {context.intent.confidence})')
            
            # Step 2: Inventory Search
            print('\nStep 2: Inventory Search')
            inventory_response = await inventory_agent.process(context)
            if context.search_results:
                print(f'✅ Found {len(context.search_results.products)} products')
                for product in context.search_results.products[:2]:
                    print(f'   - {product.name}: ${product.price}')
            
            # Step 3: Generate Recommendations
            print('\nStep 3: Generate Recommendations')
            rec_response = await rec_agent.process(context)
            print(f'✅ Generated {len(context.recommendations)} recommendations')
            for rec in context.recommendations[:2]:
                print(f'   - {rec.product.name}: {rec.reason} (confidence: {rec.confidence})')
            
            # Step 4: Format Response
            print('\nStep 4: Format Response')
            final_response = await formatter_agent.process(context)
            print(f'✅ Final Response: {final_response.response_text[:100]}...')
            
            print('\n' + '=' * 60)
            
        except Exception as e:
            print(f'❌ Pipeline test failed for "{query_text}": {e}')
            import traceback
            traceback.print_exc()
    
    # Cleanup
    await inventory_agent.close()
    print('\n✅ Complete pipeline testing finished!')

if __name__ == "__main__":
    asyncio.run(test_pipeline())