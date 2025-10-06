"""
Simple test script to verify the multi-agent application works
Run this with: python test_app.py
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.data_models import UserQuery, ConversationContext
from agents.intent_detector import IntentDetectorAgent
from agents.inventory_agent import InventoryAgent
from agents.recommendations_agent import RecommendationsAgent
from agents.response_formatter import ResponseFormatterAgent

class MultiAgentOrchestrator:
    """Main orchestrator for the multi-agent system"""
    
    def __init__(self):
        self.intent_detector = IntentDetectorAgent()
        self.inventory_agent = InventoryAgent()
        self.recommendations_agent = RecommendationsAgent()
        self.response_formatter = ResponseFormatterAgent()
    
    async def process_query(self, user_query: str, user_id: str = None) -> str:
        """Process user query through the multi-agent pipeline"""
        try:
            # Create conversation context
            context = ConversationContext(
                user_query=UserQuery(text=user_query, user_id=user_id)
            )
            
            print(f"🤖 Processing: '{user_query}'")
            
            # Agent 1: Intent Detection
            print("  Step 1: Detecting intent...")
            intent_response = await self.intent_detector.process(context)
            print(f"    ✅ Intent: {context.intent.type.value} (confidence: {context.intent.confidence})")
            
            # Agent 2: Inventory Search (if needed)
            print("  Step 2: Searching inventory...")
            inventory_response = await self.inventory_agent.process(context)
            if context.search_results:
                print(f"    ✅ Found {len(context.search_results.products)} products")
            
            # Agent 3: Generate Recommendations
            print("  Step 3: Generating recommendations...")
            rec_response = await self.recommendations_agent.process(context)
            print(f"    ✅ Generated {len(context.recommendations)} recommendations")
            
            # Agent 4: Format Response
            print("  Step 4: Formatting response...")
            final_response = await self.response_formatter.process(context)
            print(f"    ✅ Response formatted")
            
            return final_response.response_text
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return "I apologize, but I encountered an error processing your request."
    
    async def close(self):
        """Close all agent connections"""
        await self.inventory_agent.close()

async def test_basic_functionality():
    """Test basic functionality of the multi-agent system"""
    print("=" * 60)
    print("  🧪 TESTING MULTI-AGENT APPLICATION")
    print("=" * 60)
    
    orchestrator = MultiAgentOrchestrator()
    
    test_queries = [
        "I'm looking for Router",
        "I'm looking for Drone?",
        "Show me headphones under $100",
        "What products do you have in electronics?"
    ]
    
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\n📋 Test {i}/4:")
            print("-" * 40)
            
            response = await orchestrator.process_query(query, user_id="test_user")
            
            print(f"\n💬 Final Response:")
            print(f"   {response}")
            print("-" * 40)
    
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await orchestrator.close()
        print("\n🎉 Tests completed!")

if __name__ == "__main__":
    try:
        asyncio.run(test_basic_functionality())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")