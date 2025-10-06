import asyncio
from typing import List, Dict, Any, Optional
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from models.data_models import Product, SearchResult
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class AzureSearchService:
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure Search client"""
        try:
            credential = AzureKeyCredential(settings.AZURE_SEARCH_KEY)
            self.client = SearchClient(
                endpoint=settings.AZURE_SEARCH_ENDPOINT,
                index_name=settings.AZURE_SEARCH_INDEX,
                credential=credential
            )
            logger.info("Azure Search client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure Search client: {e}")
            raise
    
    async def search_products(self, query: str, max_results: int = 10) -> SearchResult:
        """Search for products using multiple strategies"""
        try:
            logger.info(f"Searching Azure Search index for: {query}")
            
            # Strategy 1: Search in ProductName field
            products = await self._product_name_search(query, max_results)
            if products:
                return SearchResult(
                    products=products,
                    total_count=len(products),
                    search_query=query,
                    search_method="product_name_search"
                )
            
            # Strategy 2: Search in ProductCategory field  
            products = await self._category_search(query, max_results)
            if products:
                return SearchResult(
                    products=products,
                    total_count=len(products),
                    search_query=query,
                    search_method="category_search"
                )
            
            # Strategy 3: General search across all fields
            products = await self._general_search(query, max_results)
            return SearchResult(
                products=products,
                total_count=len(products),
                search_query=query,
                search_method="general_search"
            )
            
        except Exception as e:
            logger.error(f"Azure Search failed: {e}")
            return SearchResult(
                products=[],
                total_count=0,
                search_query=query,
                search_method="error"
            )
    
    async def _product_name_search(self, query: str, max_results: int) -> List[Product]:
        """Search specifically in ProductName field"""
        try:
            results = await self.client.search(
                search_text=query,
                search_fields=["ProductName"],
                top=max_results,
                include_total_count=True
            )
            
            products = []
            async for result in results:
                product = self._convert_to_product(result)
                if product:
                    products.append(product)
            
            logger.info(f"Product name search found {len(products)} results")
            return products
            
        except Exception as e:
            logger.error(f"Product name search failed: {e}")
            return []
    
    async def _category_search(self, query: str, max_results: int) -> List[Product]:
        """Search in ProductCategory field"""
        try:
            results = await self.client.search(
                search_text=query,
                search_fields=["ProductCategory"],
                top=max_results,
                include_total_count=True
            )
            
            products = []
            async for result in results:
                product = self._convert_to_product(result)
                if product:
                    products.append(product)
            
            logger.info(f"Category search found {len(products)} results")
            return products
            
        except Exception as e:
            logger.error(f"Category search failed: {e}")
            return []
    
    async def _general_search(self, query: str, max_results: int) -> List[Product]:
        """General search across all searchable fields"""
        try:
            results = await self.client.search(
                search_text=query,
                top=max_results,
                include_total_count=True
            )
            
            products = []
            async for result in results:
                product = self._convert_to_product(result)
                if product:
                    products.append(product)
            
            logger.info(f"General search found {len(products)} results")
            return products
            
        except Exception as e:
            logger.error(f"General search failed: {e}")
            return []
    
    def _convert_to_product(self, search_result: Dict[str, Any]) -> Optional[Product]:
        """Convert Azure Search result to Product model based on your CSV structure"""
        try:
            # Map your CSV fields to the Product model
            return Product(
                product_id=search_result.get('CustomerID', ''),
                name=search_result.get('ProductName', ''),
                category=search_result.get('ProductCategory', ''),
                price=float(search_result.get('UnitPrice', 0)),
                description=f"{search_result.get('ProductName', '')} available at {search_result.get('StoreLocation', 'our store')}",
                in_stock=True,  # Assuming all products in CSV are available
                metadata={
                    'search_score': search_result.get('@search.score', 0),
                    'customer_name': search_result.get('CustomerName', ''),
                    'email_address': search_result.get('EmailAddress', ''),
                    'store_location': search_result.get('StoreLocation', ''),
                    'quantity': search_result.get('Quantity', 0),
                    'total_amount': search_result.get('TotalAmount', 0),
                    'purchase_date': search_result.get('PurchaseDate', ''),
                    'payment_method': search_result.get('PaymentMethod', ''),
                    'loyalty_tier': search_result.get('LoyaltyTier', ''),
                    'data_source': 'Azure_Search_CSV'
                }
            )
        except Exception as e:
            logger.error(f"Failed to convert search result to product: {e}")
            logger.error(f"Search result data: {search_result}")
            return None
    
    async def close(self):
        """Close the search client"""
        if self.client:
            await self.client.close()
            logger.info("Azure Search client closed")