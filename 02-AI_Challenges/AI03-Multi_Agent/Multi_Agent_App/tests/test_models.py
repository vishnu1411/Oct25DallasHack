import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.data_models import UserQuery, ConversationContext, IntentType, Product, SearchResult, Recommendation

try:
    print('Testing Data Models')
    print('=' * 30)
    
    # Test UserQuery
    query = UserQuery(text='I need wireless headphones', user_id='user123', session_id='session456')
    print(f'✅ UserQuery: {query.text} (User: {query.user_id})')
    
    # Test Product
    product = Product(
        product_id='P001',
        name='Sony WH-1000XM4 Headphones',
        category='Electronics',
        price=299.99,
        description='Premium noise-canceling headphones',
        in_stock=True,
        metadata={'brand': 'Sony', 'rating': 4.8}
    )
    print(f'✅ Product: {product.name} - ${product.price}')
    
    # Test SearchResult
    search_result = SearchResult(
        products=[product],
        total_count=1,
        search_query='headphones',
        search_method='exact_match'
    )
    print(f'✅ SearchResult: {search_result.total_count} products found')
    
    # Test Recommendation
    recommendation = Recommendation(
        product=product,
        reason='Highly rated by customers',
        confidence=0.95
    )
    print(f'✅ Recommendation: {recommendation.product.name} (confidence: {recommendation.confidence})')
    
    # Test ConversationContext
    context = ConversationContext(user_query=query)
    context.search_results = search_result
    context.recommendations = [recommendation]
    
    print(f'✅ ConversationContext: Query + {len(context.recommendations)} recommendations')
    print('✅ All data models working correctly')
    
except Exception as e:
    print(f'❌ Data model error: {e}')
    import traceback
    traceback.print_exc()