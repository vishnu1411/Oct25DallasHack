import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_test_result(test_name, success, message=""):
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"{status}: {test_name}")
    if message:
        print(f"   {message}")

async def run_all_tests():
    print_header("Multi-Agent System Test Suite")
    
    test_results = []
    
    # Test 1: Agent Initialization
    print("\n1. Testing Agent Initialization...")
    try:
        from agents.intent_detector import IntentDetectorAgent
        from agents.inventory_agent import InventoryAgent
        from agents.recommendations_agent import RecommendationsAgent
        from agents.response_formatter import ResponseFormatterAgent
        
        agents = [
            IntentDetectorAgent(),
            InventoryAgent(), 
            RecommendationsAgent(),
            ResponseFormatterAgent()
        ]
        print_test_result("Agent Initialization", True, f"Created {len(agents)} agents")
        test_results.append(True)
    except Exception as e:
        print_test_result("Agent Initialization", False, str(e))
        test_results.append(False)
    
    # Test 2: Data Models
    print("\n2. Testing Data Models...")
    try:
        from models.data_models import UserQuery, ConversationContext, Product
        query = UserQuery(text="test query", user_id="test_user")
        context = ConversationContext(user_query=query)
        product = Product(product_id="1", name="Test Product", category="Electronics", price=99.99)
        print_test_result("Data Models", True, "All models created successfully")
        test_results.append(True)
    except Exception as e:
        print_test_result("Data Models", False, str(e))
        test_results.append(False)
    
    # Test 3: Services (Mock Mode)
    print("\n3. Testing Services...")
    try:
        from services.azure_search_service import AzureSearchService
        from services.openai_service import OpenAIService
        search_service = AzureSearchService()
        openai_service = OpenAIService()
        print_test_result("Services", True, "Mock services initialized")
        test_results.append(True)
    except Exception as e:
        print_test_result("Services", False, str(e))
        test_results.append(False)
    
    # Test 4: Mock Search Functionality
    print("\n4. Testing Mock Search...")
    try:
        from services.azure_search_service import AzureSearchService
        service = AzureSearchService()
        results = await service.search_products("test query")
        await service.close()
        print_test_result("Mock Search", True, f"Found {len(results.products)} mock products")
        test_results.append(True)
    except Exception as e:
        print_test_result("Mock Search", False, str(e))
        test_results.append(False)
    
    # Test 5: Intent Detection Rules
    print("\n5. Testing Intent Detection...")
    try:
        from agents.intent_detector import IntentDetectorAgent
        agent = IntentDetectorAgent()
        intent = agent._detect_intent_rules("I want to find laptops")
        print_test_result("Intent Detection", True, f"Detected: {intent.type.value}")
        test_results.append(True)
    except Exception as e:
        print_test_result("Intent Detection", False, str(e))
        test_results.append(False)
    
    # Final Summary
    print_header("Test Results Summary")
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Tests Completed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your multi-agent system is ready!")
        print("\nNext steps:")
        print("  1. Run: python test_app.py")
        print("  2. Run: python main.py (for interactive mode)")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")

if __name__ == "__main__":
    asyncio.run(run_all_tests())