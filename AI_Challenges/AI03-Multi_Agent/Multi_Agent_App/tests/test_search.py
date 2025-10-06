import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from services.azure_search_service import AzureSearchService

async def test_search():
    print('Testing Mock Search Service')
    print('=' * 40)
    
    service = AzureSearchService()
    
    test_queries = ['laptops', 'headphones', 'running shoes', 'wireless mouse']
    
    for query in test_queries:
        try:
            results = await service.search_products(query)
            print(f'Search Query: "{query}"')
            print(f'Products Found: {len(results.products)}')
            print(f'Search Method: {results.search_method}')
            
            for i, product in enumerate(results.products, 1):
                print(f'  {i}. {product.name} - ${product.price}')
                print(f'     Category: {product.category}')
            print('-' * 30)
        except Exception as e:
            print(f'❌ Search error for "{query}": {e}')
    
    await service.close()
    print('✅ Mock search testing completed')

if __name__ == "__main__":
    asyncio.run(test_search())