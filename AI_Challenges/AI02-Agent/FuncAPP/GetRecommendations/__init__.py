import azure.functions as func
from azure.cosmos import CosmosClient
import os, json

# Initialize Cosmos DB client using credentials from environment variables
COSMOS_URI = os.environ["COSMOS_URI"]    # e.g., "https://YOUR-COSMOS-ACCOUNT.documents.azure.com:443/"
COSMOS_KEY = os.environ["COSMOS_KEY"]    # your Cosmos DB primary key
DATABASE_NAME = os.environ.get("COSMOS_DATABASE", "RetailData")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER", "Recommendations")

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
container = client.get_database_client(DATABASE_NAME).get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    product = req.params.get('product')
    if not product:
        return func.HttpResponse("Please pass a product name in the query string", status_code=400)
    # Query Cosmos DB: find the document where 'product' field contains the input (case-insensitive)
    query = "SELECT * FROM c WHERE CONTAINS(c.product, @name, true)"  # 'true' for case-insensitive contains
    items = list(container.query_items(
        query=query,
        parameters=[{"name": "@name", "value": product}],
        enable_cross_partition_query=True
    ))
    suggestions = []
    if items:
        # Take the first matching document's suggestions
        suggestions = items[0].get('suggestions', [])
    # Return the suggestions as a JSON response
    return func.HttpResponse(
        json.dumps({"suggestions": suggestions}),
        mimetype="application/json",
        status_code=200
    )