
# 🏆AI Challenge 02: Intelligent Agent with Azure Cosmos DB (Recommendations)

## 📖 Learning Objectives 
In this challenge, you will extend your AI agent’s capabilities by integrating it with an external database. Specifically, you’ll use **Azure Cosmos DB** to provide dynamic, data-driven responses (like product recommendations). By the end, you will know how to:  
- **Connect** an Azure Cosmos DB (NoSQL) container to **Azure AI Foundry** as a tool or data source.  
- **Implement** function calling or tool use in the AI agent to query Cosmos DB during a conversation.  
- **Build** an agent that can suggest related items (e.g., “frequently bought together” recommendations) by retrieving information from Cosmos DB.  
- **Understand** the pattern of combining LLMs with live database queries for fresh, context-specific answers (a “fresh concept” beyond static Q&A).  

## ⚙️ Prerequisites
- Completed **Challenge 01** (or have an Azure AI Foundry project with a working chat agent and an Azure OpenAI model deployment).  
- **Azure Cosmos DB** account with the ability to create a new database and container (or permissions to create one).  
- Basic familiarity with JSON and database concepts.  
- (Data prerequisite) A dataset of product relationships (e.g., which products are commonly bought together). If not readily available, you will create a small sample in this challenge.  

---

## 📝 Challenge Overview 
Continuing with the retail scenario, the company wants the AI assistant to not only answer questions but also make smart **product recommendations**. For example, when a customer is looking at a product or adds it to cart, the assistant should suggest complementary products (“Customers who bought X also buy Y”). We’ll achieve this by storing product recommendation data in Azure **Cosmos DB** and enabling the AI agent to query it. 

Key tasks:  

✅ **Set up Cosmos DB** – Create a Cosmos DB (NoSQL) container and insert sample recommendation data (e.g., for a given product, list other products often bought together). We can use GitHub sample data or create our own.  
✅ **Integrate Cosmos DB with Foundry** – Enable the Foundry agent to access Cosmos DB. This could be done via Foundry’s built-in data connection or by implementing a custom **function** that the agent can call (using OpenAI function calling).  
✅ **Implement Agent logic for suggestions** – Configure the agent’s behavior: when a user asks for recommendations (or when the context implies it), the agent will fetch data from Cosmos DB and use it in its answer.  
✅ **Test the enhanced agent** – Ask the chatbot things like “I’m buying a [Product]. What else should I get?” and verify it returns suggestions based on the Cosmos DB data. Ensure the concept is fresh and interesting to users.  

Milestones:

## 🚀 Milestone #1: **Prepare Azure Cosmos DB with Recommendation Data**  

### 1️⃣ **Create** an Azure Cosmos DB account (NoSQL API) in your resource group (e.g., "contoso-cosmos"). If you already have one, you can use it. Choose the same region as before for consistency.  

### 2️⃣ **Create** a Database (e.g., `RetailData`) and a Container (e.g., `Recommendations`) within the Cosmos DB account. Set a partition key (e.g., `/productId` or `/product`). Throughput: for hackathon, a small fixed throughput (like 400 RU/s) or the new serverless option is fine.  

### 3️⃣ **Insert recommendation data from CSV** into the container. Instead of manually entering sample documents, you can use your CSV file (`tailwind_traders_challenge2_data.csv`) located one folder outside your current directory. This file should contain product relationships, such as which products are frequently bought together.

### Importing Data from CSV

- **Prepare your CSV file:** Ensure your CSV has columns like `product`, `suggestions` (where `suggestions` is a comma-separated list).
- **Convert CSV to JSON:** Use a script (Python example below) to read the CSV and generate JSON documents for Cosmos DB.

```python
import csv, json

docs = []
with open('tailwind_traders_challange2_data.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, start=1):
        # Clean non-breaking spaces and strip whitespace
        product = row["Product"].replace('\u00a0', ' ').strip()
        suggestions = [
            row["AlsoBought1"].replace('\u00a0', ' ').strip(),
            row["AlsoBought2"].replace('\u00a0', ' ').strip(),
            row["AlsoBought3"].replace('\u00a0', ' ').strip()
        ]
        # Remove empty suggestions
        suggestions = [s for s in suggestions if s]
        doc = {
            "id": f"rec{idx}",
            "product": product,
            "suggestions": suggestions
        }
        docs.append(doc)

with open('recommendations.json', 'w', encoding='utf-8') as out:
    json.dump(docs, out, indent=2, ensure_ascii=False)
``` 

Upload the resulting JSON documents to the Cosmos DB container (use the Data Explorer's Upload Items or an SDK/script) so that each product has a corresponding document with its suggestions.

### 4️⃣ Verify Data in Cosmos DB
In Data Explorer, run a query like SELECT * FROM c on the Recommendations container. You should see the inserted documents. Verify that each document contains the expected product name and suggestions array. This ensures your Cosmos DB is correctly populated with recommendation data before moving on.

## 🚀 Milestone #2: Integrate Cosmos DB with Azure AI Foundry

### 1️⃣ Enable Managed Identity and Assign Roles
Enable Managed Identity on your Azure AI Services resource (the one hosting your OpenAI model) and on the Azure Cosmos DB account (via the Azure Portal’s Identity blade for each). Then assign the necessary RBAC roles:

In the Cosmos DB account IAM, assign Cosmos DB Account Reader (or Contributor) to the AI Services managed identity, so it can read data.
In the Cosmos DB IAM, also assign Cosmos DB Data Reader or Cosmos DB Built-in Data Contributor to the AI Service identity for data access (use the appropriate Data role for NoSQL).
In the Azure AI Services resource IAM, assign Cognitive Services OpenAI Contributor to the Cosmos DB managed identity (if you enabled MI on Cosmos) or ensure your user has Owner/Contributor access as needed.

These steps allow the Foundry project (which uses the AI Service's identity under the hood) to access Cosmos DB securely without needing keys.

### 2️⃣ Deploy an Azure Function for Recommendations
To let the chat agent query Cosmos DB, implement a simple API that the agent can call. One approach is using Azure Functions. Create an HTTP-triggered Azure Function (in Python or C#) that accepts a product name and returns suggested products from Cosmos DB. For example, in Python:

```python
import azure.functions as func
from azure.cosmos import CosmosClient
import os, json

# Cosmos DB connection (using the account URI and key from settings)
client = CosmosClient(os.environ["COSMOS_URI"], credential=os.environ["COSMOS_KEY"])
container = client.get_database_client('RetailData').get_container_client('Recommendations')

def main(req: func.HttpRequest) -> func.HttpResponse:
    product = req.params.get('product')
    if not product:
        return func.HttpResponse("Please pass a product name", status_code=400)
    # Query Cosmos DB for the given product
    query = "SELECT * FROM c WHERE CONTAINS(c.product, @name)"
    items = list(container.query_items(
        query=query,
        parameters=[{"name": "@name", "value": product}],
        enable_cross_partition_query=True
    ))
    suggestions = []
    if items:
        suggestions = items[0].get('suggestions', [])
    return func.HttpResponse(
        body=json.dumps({"suggestions": suggestions}),
        mimetype="application/json"
    )
``` 

Deploy this function (e.g., via Azure Functions Core Tools or VS Code) and note its URL (e.g., https://functionapp.azurewebsites.net/api/GetRecommendations). Set up environment variables (COSMOS_URI, COSMOS_KEY) for the function or use Azure Managed Identity within the function to access Cosmos (which would require adding a Managed Identity to the function and granting it Cosmos DB Data Reader role).

### 3️⃣ Register the Function in Azure AI Foundry
In Azure AI Studio (your Foundry project), integrate this API as a function the agent can call. In the Prompt Flow or Agent configuration, you can use OpenAI’s function calling. For example, define a function schema like:

```json
{
  "name": "GetRecommendations",
  "description": "Get product recommendations from Cosmos DB",
  "parameters": {
    "type": "object",
    "properties": {
      "product": {"type": "string", "description": "Product name"}
    },
    "required": ["product"]
  }
}
``` 


---

#### Configure the Agent to Call the Function

- In the prompt flow code or Foundry UI, configure the agent to call the Azure Function’s URL when the function is invoked.
- In a prompt flow, use a Python step to call the HTTP endpoint with the product parameter and capture the JSON response (list of suggestions).
- Ensure your Azure AI Services managed identity or function URL has permission (you might use a function key). For hackathon scenarios, anonymous access or a function key is acceptable.

**Agent Logic:**
- Update the chatbot’s logic so that when a user asks for recommendations, the bot uses the Cosmos DB function.
- This can be done via OpenAI function calling: provide the model with the GetRecommendations function schema (from step 3) in the system message or via the Foundry interface. The model will decide to call it when appropriate.
- Alternatively, in a prompt flow, explicitly detect a recommendation query and execute the function. For example, if the user query contains phrases like “what should I get with” or “also buy”, you can have a condition to trigger the GetRecommendations call.
- Pass the product name (from user’s query or conversation context) to the function and retrieve the suggestions.

#### Ensure Fresh Data Usage

- Because the recommendations come from a live database, any updates in Cosmos DB will reflect immediately in the agent’s answers.
- This “live” aspect is a fresh concept beyond static Q&A.
- To highlight this freshness: after integrating, try changing a suggestion directly in the Cosmos DB container and ask the question again – the new suggestion should appear without redeploying the model.
- This is mostly a mental check; there's no coding in this step, just an understanding that our agent now pulls data at runtime, ensuring up-to-date responses.

---

## 🚀 Milestone #3: Implement Agent Recommendation Logic

### 1️⃣ **Trigger Recommendations on Relevant Queries**  
    Configure the agent to detect when a user is seeking product recommendations. Use simple keyword matching (e.g., “recommend”, “anything else with”, “also buy”) in the user’s input to trigger the Cosmos DB function. In Azure AI Foundry, this can be implemented as a condition or classifier within your prompt flow. For production, consider more advanced intent detection, but for this challenge, keyword checks are sufficient.

### 2️⃣ **Incorporate Suggestions in Responses**  
    When the agent receives recommended products from Cosmos DB, format the reply to clearly present them. For example:  
    > Customers who bought **Tent** often also buy **Sleeping Bag**, **Lantern**, and **Camping Stove**.  
    Use a consistent answer template and ensure the suggestions are included in the agent’s response. If using prompt flow, store the suggestions in a variable and append them to the assistant’s answer.

### 3️⃣ **Provide a Safe Fallback for No Data**  
    If no recommendations are found (the suggestions list is empty), the agent should avoid guessing or hallucinating. Instead, respond with a general helpful statement or acknowledge the lack of specific recommendations. For example:  
    > I don’t have specific recommendations for that item, but you might consider accessories related to it.  
    This approach maintains factual accuracy and user trust.

## 🚀 Milestone #4: Test the Enhanced Agent

### 1️⃣ **Ask a Direct Recommendation Question**  
        Example: “I bought a Tent. What else should I get?”  
        - The chatbot should recognize the intent, call the Cosmos DB function, and respond with relevant product suggestions (e.g., “Sleeping Bag and Lantern”) based on the data for “Tent”.

### 2️⃣ **Ask an Implicit Recommendation Question**  
        Example: “Do I need anything in addition to the Headlamp?”  
        - The agent should interpret this as a request for related items and provide suggestions (e.g., “You might also consider Running Shoes and a Hiking Backpack with your Headlamp.”).  
        - If not, adjust your keyword triggers or function-calling logic.

### 3️⃣ **Ask a Non-Recommendation Question**  
        Example: “What is the price of the Tent?”  
        - The bot should answer using its knowledge sources and not trigger the Cosmos DB function.  
        - Ensure regular Q&A works as expected.

### 4️⃣ **Test a "No Data" Scenario**  
Example: "I just bought a Solar Charger. What else do I need?"  
- If "Solar Charger" is not in your Cosmos DB container, the function may return an empty list.  
- The agent should use the fallback response (from Milestone #3) and avoid guessing, providing a generic helpful suggestion or politely stating no specific recommendations.

### 5️⃣ **Verify Function Calls and Logs**  
- Optionally, review Azure Function logs or Foundry traces to confirm the GetRecommendations function is called for recommendation queries and not for unrelated questions.

    By completing these tests, you’ll confirm that your agent uses live Cosmos DB data to deliver fresh, relevant recommendations. 🎉