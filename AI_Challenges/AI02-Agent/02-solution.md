# 📖 Solution to Challenge 02: Intelligent Agent with Cosmos DB (Recommendations)

## 🎯 Objective 
We have extended our Azure AI Foundry chatbot to integrate with Azure Cosmos DB, enabling it to provide on-the-fly product recommendations. The goal was to have the agent answer questions like “What should I buy with this product?” by querying a database of “frequently bought together” items. 

**Key steps accomplished:**  
- Created an Azure Cosmos DB container with sample recommendation data (product -> suggested items).  
- Connected Cosmos DB to our Foundry project (using a function call approach for fine control).  
- Modified the agent to detect when a recommendation is asked for and retrieve the relevant suggestions from Cosmos DB.  
- Tested that the agent’s answers are enriched with these dynamic suggestions, illustrating a fresh capability beyond basic Q&A.

Let’s go through the steps in detail.

## 🚀 Milestone #1: Setting up Cosmos DB and Data 

**1. Azure Cosmos DB Account:** We created a new Cosmos DB for NoSQL account named “contoso-cosmos” in the same resource group and region as previous resources. (In Azure Portal: Create Cosmos DB -> NoSQL -> fill in RG and name.)

- Sign in to the Azure Portal and click Create a resource. Search for "Azure Cosmos DB".
- Choose the Azure Cosmos DB for NoSQL option.
- Create a new account. Select your subscription and resource group, give the account a unique name (e.g., contoso-cosmos), and pick a region close to you.
- For this challenge, the default settings are fine. Click Review + create, then Create.

Why: Cosmos DB will store the "frequently bought together" recommendation data.

**2. Database and Container:** In the Cosmos DB account, under Data Explorer:  
- Once the Cosmos DB account is ready, go to it in the Azure Portal. In the left menu, find Data Explorer.
- Select the New Database from the drop down menu right above  **Home**. Name the database (for example, RetailData) and leave throughput as-is (we'll set it at the container level). Hit OK.
- Select the new DB and right click on the DB and select **+ New Container**.
- Select "Use existing" and select the DB which we created earlier
- Set the Container id to something like Recommendations.
- For Partition key, enter /productID . This means our data will be partitioned by the "productID" field in each document.
- Click OK to create the container.

![Cosmos DB](<Reference Pictures/cosmos_ss.png>)
Why: A container in Cosmos DB (like a table) will hold documents where each document maps one product to a list of recommended products.

**3. Import Recommendation Data from CSV:**
   - Use the provided CSV file (`tailwind_traders_challenge2_data.csv`) located one folder outside your current directory. This file contains product relationships (product, suggestions).
   - Convert the CSV to JSON using the following Python script:
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

   - Upload the resulting JSON to Cosmos DB using Data Explorer’s “Upload JSON” feature or the Azure SDK,Under ***Items*** ,use the ***Upload data*** and ***Select Json Files*** option
   - Ensure each document includes the partition key field (`Product`).

**4. Verify Data:** 
- Open the SQL Query tab then paste the below 
- `SELECT c.Product, c.suggestions FROM c`. It will return each product (by Product) with its suggestions array, confirming our entries. 

![Cosmos DB Query Output](<Reference Pictures/cosmos_query_ss.png>)

## 🚀 Milestone #1: Result

---
At this point we have the Cosmos DB with sample data ,for recommandations and the AI foundry also ready from our previous challenge and just completed Milestone #1 sucessfully 

---

---

## 🚀 Milestone #2:Integrating Cosmos DB with Foundry

We decided to use **OpenAI function calling** within the Foundry agent to query Cosmos DB, as this approach offers explicit control when testing the “fresh concept” of an agent performing actions. (Note: Foundry’s direct Cosmos connection will also be set up but function calling gives more transparency in this challenge.)

**1. Set up your Development Environment in VS Code:** 
- Python Installation: Ensure you have Python installed on your machine (Azure Functions supports 3.8 through 3.12 as of early 2025). On Windows, open a Command Prompt and run python --version to verify. If you have Python 3.13 installed, note that Azure Functions added support for 3.13 in mid-2025, but you may need the latest Azure Functions tools. If the tooling doesn’t recognize 3.13, consider installing Python 3.10 or 3.11 for compatibility during development. (The Azure Functions Python library officially supported up to 3.12 prior to 3.13’s preview.) 
- Azure Functions Core Tools & VS Code: Install the Azure Functions Core Tools and the Azure Functions extension for VS Code . This provides a local runtime and project scaffolding.

**2. Create A Function APP Project (inside VS Code):** 
- In VS Code, open the Command Palette (Ctrl+Shift+P or F1) and select "Azure Functions: Create New Project...."
- Choose or create a folder for your function project.
- Select Python as the language, then choose a Python version that matches your environment (e.g., Python 3.10). (If the drop-down only shows Python 3.9, ensure you installed a newer Python and restarted VS Code. You may manually specify a higher version in the project’s runtime.txt if needed.)
- When prompted for a template, choose HTTP trigger.
- Name the function (e.g., “GetRecommendations”) and set Authorization to Anonymous (so our bot can call it easily).
- VS Code will scaffold a project with a subfolder (e.g., GetRecommendations) containing __init__.py and function.json if it follows the old way ,and if it is the new method ,then it will be just a sample functions_app.py file only 
If using function APP V1 (Legacy Style) below will be the folder structure
![FunAPP V1 Dir Structure](<Reference Pictures/Funcapp_Folder_Struc.png>)

If using function APP V2 (Modern Decorator-Based) below will be the folder structure
 ![FunAPP V2 Dir Structure](<Reference Pictures/functionapp_v2_directory_structure.png>)


**3.Write the function Code:** 
- Open the __init__.py file (function_app.py file if you have FunctionAPP V2 ). We’ll replace its contents with code that queries Cosmos DB. First, add Azure Cosmos SDK to the project’s requirements. Open requirements.txt and add:

```Text
azure-functions
azure-cosmos
```
- Save the file (this ensures these packages will be installed in Azure). Now, use the following code for __init__.py (function_app.py file if you have that file and does not have this file ):
```python
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

```

- It reads COSMOS_URI and COSMOS_KEY from environment variables (we’ll set those in a moment). Using these, it creates a CosmosClient and gets a reference to our database and container.
- It expects an HTTP GET with a query parameter product. If ?product= is missing, it returns an error.
- It queries the container for documents whose product field contains the given name. We use CONTAINS(c.product, @name, true) in SQL to allow partial matches, case-insensitive. For example, if the product is “tent”, it would match a document with product “Tent”.
- We pass enable_cross_partition_query=True because the query needs to scan all partitions (since we don’t know the exact partition key upfront). 
-Configure the local settings, local.settings.json ,add the cosmos DB connection info under Values:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "COSMOS_URI": "https://YOUR-COSMOS-ACCOUNT.documents.azure.com:443/",
    "COSMOS_KEY": "<Your Cosmos DB Primary Key>",
    "COSMOS_DATABASE": "RetailData",
    "COSMOS_CONTAINER": "Recommendations"
  }
}

```
### 🧪 Local Testing: Running the Function App Locally
Before deploying to Azure, you should test your Function App locally to ensure everything works as expected.

#### 1. Install Python 3.12 and Set Up a Virtual Environment
If you have multiple Python versions installed, it's best to use a virtual environment (`venv`) to avoid conflicts.
- **Download Python 3.12:**  
    Visit [python.org/downloads/release/python-3120/](https://www.python.org/downloads/release/python-3120/) and install Python 3.12.  
    During installation, check “Add Python to PATH”.

- **Create and Activate a Virtual Environment:**  
    Open your terminal (e.g., PowerShell in VS Code) and run:

    ```powershell 
    py -3.12 -m venv .venv
    .\.venv\Scripts\activate.ps1

    # Verify the Python version inside the virtual environment
    py --version
    ```

#### 2. Test the Function App Locally

- With your virtual environment activated, start the Azure Function locally:

    ```powershell
    func start
    ```

    Or press **F5** in VS Code to launch the local debugger.
- Wait for the app to start (it may take a minute or two). Once running, test the endpoint in your browser or with a tool like `curl`:http://localhost:7071/api/GetRecommendations?product=Tent
    
- If you receive a JSON response with recommendations, your app logic is working correctly and you are ready to deploy to Azure.

![Func App VSCode local testing](<Reference Pictures/functionapp_v1_localtest.png>)

**4. Creat Azure Functions :** 
- Go to the Azure Portal, click Create a resource, search for Function App.
- Create a new Function App (name it something like contoso-recommend-func). Use the same resource group and region,Flex Consumption will do for this testing.
- For runtime, choose Python 3.12 and make sure you match what you have locally installed or used in your virtual environment
- Keep everthing default and create the function app


**5. Managed Identity Setup:** First, we ensured our Azure AI Services resource’s managed identity has access to Cosmos DB:  
   - In the **Cosmos DB account** IAM, we added a role assignment: **Cosmos DB Account Reader** (or Contributor) to the ContosoAIService managed identity. This allows it to read data.  
   - Because we are doing function calls in code, we also generated a **Primary Key** from Cosmos DB (available in Keys section) to use in the function. (Alternatively, one could use the Managed Identity token, but for simplicity we used the key in our Azure Function.)

**6. Deploy the Function to Azure :**
- GO to VS Code’s Azure extension. Find your subscription > Function Apps > your function app name. Right-click and choose Deploy to Function App.
- VS Code will package your code and deploy it. On first deployment, it may ask to overwrite – confirm yes (since the function app is empty).

![Fun App Deployment from VSCode](<Reference Pictures/fa_vscode_deploy_2_azure.png>)

### Add Cosmos DB Credentials to Function App Settings

- In the Azure Portal, navigate to your Function App.
- Go to **APP Settings** under the **Environment variables** section.
- Click on **Add**, and under "Add/Edit application setting", update the key-value pair.
- Click **+ New application setting** and add the following keys with their respective values:
    - `COSMOS_URI` – your Cosmos DB URI (e.g., `https://YOUR-COSMOS-ACCOUNT.documents.azure.com:443/`)
    - `COSMOS_KEY` – your Cosmos DB primary key
- Click **Apply** to apply the changes.
- Restart the Function App to ensure the new settings take effect.
- After deployment, in the Azure Portal, navigate to the Function App > Functions > GetRecommendations.Find out the function URL and go to your browser to test it

![Func App Portal Overview](<Reference Pictures/fa_portal_ss.png>)



![Fun App testing from Azure Portal](<Reference Pictures/function_app_testing_from_portal.png>)



```text
https://<your fuction app name>.azurewebsites.net/api/GetRecommendations?product=Lantern
```
the above querry will spit a json output with recommandations

![Fun App Browser testing](<Reference Pictures/functionapp_browsertest.png>)

**7. Foundry Agent Function Registration**

Azure AI Foundry currently doesn’t have a GUI to register custom functions to the GPT model, but you can implement this in the **prompt flow**. There are several integration options:

- **Prompt Flow Script:** Use prompt flow in AI Foundry for a low-code solution.
- **Direct Function Calling via SDK:** Package the agent as code and deploy using the UI.
- **Azure OpenAI Function Calling:** Expose the recommendation endpoint as a callable function for the model.

For this example, we'll use a prompt flow script to package everything as an AI Agent.

### Create a Prompt Flow

1. **Open your project in Azure AI Foundry.**
2. Navigate to the Prompt Flow section.
3. Create a new flow or open an existing one.
4. Ensure a compute session is running.

![Inital Prompt Flow Sample](<Reference Pictures/initial_prompt_flow_graph.png>)

### Define Flow Input

- Add an input variable named `user_message` of type string.
- This will hold the user’s query (e.g., “I bought a lantern, what else should I get?”).

![Prompt Flow Input-Output SS](<Reference Pictures/promptflow_input_output.png>)
### Add Python Tool – `detect_intent`

- Click **+ Add → Python Tool**.
- Name it `detect_intent`.
- Paste the following code:

    ```python
    from promptflow import tool
    import re

    @tool
    def detect_intent(user_message: str) -> dict:
        text = user_message.lower()
        triggers = ["what else should i", "also buy", "anything else", "in addition to"]
        do_recommend = any(key in text for key in triggers)
        product = ""
        if do_recommend:
            match = re.search(r"(bought|purchased|my)\s+([^,?.]+)", text)
            if match:
                product = match.group(2).strip()
                product = re.sub(r"^(a|an|the)\s+", "", product, flags=re.IGNORECASE)
                product = product.title()
        print(f"[detect_intent] do_recommend: {do_recommend}, product: '{product}'")
        return { "do_recommend": do_recommend, "product": product }
    ```

- Assign `user_message` input to `${inputs.user_message}`.
- This node checks for recommendation intent and extracts the product name.

![Detect Intent Node SS](<Reference Pictures/detect_intent_screenshot.png>)

### Add Python Tool – `get_recommendations`

- Click **+ Add → Python Tool**.
- Name it `get_recommendations`.
- Paste the following code:

    ```python
    from promptflow import tool
    import requests

    @tool
    def get_recommendations(product: str) -> list:
        if not product:
            return []
        try:
            url = "https://<Your Function APP FQDN>/api/GetRecommendations"
            params = {"product": product}
            resp = requests.get(url, params=params, timeout=5)
            print(f"[get_recommendations] Raw response: {resp.text}")
            data = resp.json()
            suggestions = data.get("suggestions", [])
            clean_suggestions = [
                s.replace('\u00a0', ' ').strip()
                for s in suggestions
                if s and s.strip()
            ]
            print(f"[get_recommendations] Clean suggestions: {clean_suggestions}")
            return clean_suggestions
        except Exception as e:
            print(f"[get_recommendations] Exception occurred: {e}")
            return []
    ```

- Replace `<Your Function APP FQDN>` with your actual Function App URL.
- Assign input `product` to `${detect_intent.output.product}`.
- Set conditional execution: run only if `${detect_intent.output.do_recommend} == True`.

![Get Recommendations  Node SS](<Reference Pictures/get_recommendations_screenshot.png>)

### Compose the Final Answer Using the Suggestions from LLM

- Add an LLM node (e.g., GPT-3.5-turbo).
- Connect inputs:
    - `user_message` → `${inputs.user_message}`
    - `detect_intent` → `${detect_intent.output}`
    - `get_recommendations` → `${get_recommendations.output}`

- In the LLM node’s prompt field, use Jinja2 syntax for dynamic content:

    ```jinja2
    system:
    You are a helpful assistant that provides product recommendations when available.

    user:
    {{ user_message }}

    assistant:
    {% set filtered_recommendations = get_recommendations | reject("equalto", detect_intent.product) | list %}
    {% if filtered_recommendations | length > 0 %}
    Customers who bought {{ detect_intent.product }} often also buy {{ filtered_recommendations | join(', ') }}.
    {% else %}
    I don’t have specific recommendations for that, but you might consider related accessories.
    {% endif %}
    ```

![LLM SS-PartI](<Reference Pictures/promptflow_llm_part1.png>)
![LLM SS-PartII](<Reference Pictures/promptflow_llm_part2.png>)


**How It Works:**

- If recommendations exist, the assistant replies with factual, retrieved data.
- If no recommendations are found, it responds with a fallback message.

![Final Prompt Flow Graph](<Reference Pictures/final_prompt_flow_graph.png>)

**Alternative:**  
You can format the response in a Python node if you prefer, but using the LLM allows for more natural replies.

### Final Flow Structure

- `detect_intent` (Python): Input: `user_message` → Output: `do_recommend`, `product`
- `get_recommendations` (Python): Input: `product` → Output: `suggestions` (runs only if `do_recommend == True`)
- LLM Node (GPT-3.5-turbo): Composes the final answer using all outputs.

## 🚀 Milestone #2: Result

---
At this point we have integrated the LLM with Function APP which inturn checks the CosmosDB and will give us recommendations on what to buy if we are planning to buy something from the e-commerce site ,with this we just completed Milestone #2 sucessfully 

---

---

## 🤖 Testing the Recommendation Agent (Milestone #3 & #4 )


After deploying the updated prompt flow, we tested the following interactions using actual product names and categories from the CSV:

- **Test 1 (Direct ask, Footwear):**Provide a Test Input: In the Prompt Flow testing panel, enter a sample user message that asks for a recommendation. For example:
  User message:“I bought a Tent, what else should I get for camping?”
  Run the flow , watch the execution and look for the output in each steps and watch the graph also you will see when each step gets sucessfully completed and how long it took to complete each stage

- ***Expected Result*** The LLM node will then generate an answer. You should see in the final output something like: “Customers who bought Tent often also buy Sleeping Bag and Lantern for camping trips.” (Wording may vary, but it should mention Sleeping Bag and Lantern). The model likely added “for camping trips” because the user mentioned camping – this shows it integrated the suggestions with the context smoothly

- **Test 2 (Non-Recommendation Query):** Try a different input where no recommendations are needed:
  For instance: “What is the price of the Tent?”
 This time, do_recommend would be False, so the call_function step is skipped (in trace, call_recommendation_api node status = “Bypassed”).

- ***Expected Result***  The LLM should answer the question with else option "I don’t have that information at the moment. Please check with a retailer or online for current pricing."


- **(Verify Conditional Behaviour):**  In the flow’s Outputs/Trace section, confirm:
  In the recommendation query run, the function node executed and returned data.
  In the non-recommendation query run, the function node was bypassed.
  The final answers make sense in each context.

- **Logs/Verification:**
- Inspect Azure Function logs or OpenAI function call traces to confirm the function is called only for recommendation queries.
- This real-time call to an external system demonstrates the “fresh” concept—answers are not limited to pre-ingested knowledge.


## 🚀 Milestone #3 & #4: Result

---
You have successfully integrated a live Azure Function call into your chat agent’s flow. Now your AI assistant can supplement its answers with real-time data from Cosmos DB, making its recommendations always up-to-date and grounded in fact ,with this we just completed Milestone #3 & #4 sucessfully 

---

---

## 💡 Insights and Learnings

- **Dynamic Knowledge:** By using Cosmos DB, the knowledge base for recommendations can be updated independently. If the marketing team decides to pair a new accessory with “Contoso Phone Model X”, they just update the Cosmos item — the chatbot will start recommending it on the very next query. This is more dynamic than the static search index (which would need re-indexing). It demonstrates how **LLMs + live databases** can work together.  
- **Function vs. Prompt Engineering:** We tried a direct approach of feeding the model the suggestions vs. letting it call a function. The function route gave deterministic results (we explicitly fetch and provide data). This is usually more reliable for factual insertions, whereas letting the model guess can lead to hallucinations (as seen when no data was found).  
- **Complex Query Understanding:** Our simple keyword triggers might miss some phrasings. In production, one might use a classification model or LLM itself to decide if a query is asking for recommendations. We kept it straightforward due to time.  
- **Foundry Integration:** Azure AI Foundry is evolving to simplify such tasks. There is mention of a direct Cosmos DB tool/connector (for example, storing conversation context or small knowledge pieces). In the future, one could imagine configuring, in the UI: “when user asks X, run query Y on data source Z” without writing code. For now, we used prompt flow code to achieve that.  

## 🔗 Useful Resources 
- Azure Cosmos DB documentation – particularly on querying in Python and using Contains, etc.  
- Azure AI Foundry blog (May 2025) on Cosmos DB integration – discusses using Cosmos as a “memory store” for agents, which is related to what we did.  
- Function Calling in OpenAI (Azure OpenAI) – the concept we utilized by bridging via an Azure Function.  

By completing Challenge 02, we have a chatbot that not only answers questions from documentation but also performs a mild form of **analysis/lookup** – retrieving related items. This showcases an **action-oriented agent** ability, moving closer to a true digital assistant that can both inform and act (in this case, act = query a database). 

In the next challenge, we will push this further by orchestrating **multiple agents** to handle even more complex scenarios (like checking inventory and suggesting alternatives). This will illustrate multi-agent cooperation in Azure AI Foundry. Great job so far taking the bot to the next level with Cosmos DB!
