# 📖 Solution to AI Challenge 01: Setting Up LLMs for a Chatbot and its Dependencies

## 🔹 Objective
In this challenge, you will:

✅ Create, Define, and Explore LLMs for a Chatbot and the Resources Needed to Set Up the Same.  

✅ Add Custom Data to Your Project and Explore the Response of Chatbot Post Indexing and Grounding.  

✅ Build & Customize – Create, Iterate, and Debug Your Orchestration Flows.

✅ Learn how to use frameworks to programatically create AI agents and achive tailormade solutions for complex use cases with more flexiblity

---

## 🚀 Generic TIPS:

- Try to keep all resources and RG in the same Region for ease of understanding and standardization.
- Most companies have organizational policies on auto-creation of Key Vault & Storage account, so here we will be creating all resources separately and will stitch them together.
- Add a tag to the Resources and resource group when you create them so that we can identify them later for cost management or other aspects.
- Ensure that all necessary resource providers are registered. For example, you might need to register Microsoft.PolicyInsights and Microsoft.Cdn policies by selecting them and clicking the register button in the Azure Portal.
- Make sure the location or region for each of the resources is preferably one of the following, to ensure smooth testing of all resources:
  - Australia East
  - Canada East
  - East US
  - East US 2
  - France Central
  - Japan East
  - North Central US
  - Sweden Central
  - Switzerland
- Check the TPM quota for your subscription for the LLMs `text-embedding-ada-002` and `gpt-35-turbo`. If you are already familiar with the same, request a quota addition if the current quota is in the 2-digit range (10k–90k) and increase it to whatever is maximum for each model.

---

## 🚀 Milestone #1: Create, Define, and Explore LLMs for a Chatbot and the Resources Needed to Set Up the Same

### 1️⃣ Create the Resource Group (RG)

**Steps:**
1. Sign in to the Azure portal.  
2. Select **Resource groups**.  
3. Select **Create**.  
4. Enter the following details:
   - **Subscription**:
   - **Resource group**:
   - **Region**:
5. Select **Review + Create**.

![Create Resource Group](<Reference Pictures/1.png>)

---

### 2️⃣ Create/Use the existing Storage account (this will be source of our custom data)

1. On the **Storage accounts** page, select **Create**.  
2. Fill in the required details.  
3. Enter the following details:
   - **Subscription**  
   - **Resource group**  
   - **Storage account name**  
   - **Region**  
   - **Performance**: select **Standard**  
   - **Redundancy**: **LRS**  
   - **Networking**: enable public access from all networks (to avoid isolated environment-specific issues)  
   - Keep everything else default  
4. Select **Review + Create**  
5. Click **Create**

![Create Storage Account](<Reference Pictures/2.png>)

6. Once the storage account is created, create a container `refined-data` and upload the CSV file for first challange [Challange01 Data source folder](../Data_Source/01_CSV/tailwind_traders_retail_data.csv) into the container (inside a folder named `csv-data` or `txt-data`). By the end of this step, you will have:
   - A **storage account** with a **container** inside
   - A **subfolder** in that container
   - All the files in CSV format inside that subfolder

When everything is done, it will look like this:

![Container with CSV Files](<Reference Pictures/3.png>)

---

### 3️⃣ Create the Key Vault

1. On the **Key Vault** page, select **Create**.  
2. Fill in the required details.  
3. Enter the following:
   - **Subscription**  
   - **Resource group**  
   - **Key Vault Name**  
   - **Region**  
   - **Pricing tier**: **Standard**  
   - Keep everything else default
4. Select **Review + Create**  
5. Click **Create**

![Key Vault Creation](<Reference Pictures/kv4.png>)

---

### 4️⃣ Create a Search Service Connection to Index the Sample Product Data

1. On the **home page**, select **+ Create a resource** and search for **Azure AI Search**. Then create a new Azure AI Search resource with the following:
   - **Subscription**  
   - **Resource group**  
   - **Service name**  
   - **Location**: pick from any region mentioned in the Tips  
   - **Pricing tier**: **Standard**  
   - **Scale**: Increase the search unit by 4 to enhance query performance
2. Wait for deployment to complete

![Azure AI Search Creation](<Reference Pictures/search5.png>)
---

### 5️⃣ Create an Azure Open AI Service

1. On the **home page**, select **+ Create a resource** and search for **Azure OpenAI**. Create a new service using:
   - **Subscription**  
   - **Resource group**  
   - **Region**: pick from the recommended regions in the Tips  
   - **Name**  
   - **Pricing tier**: **StandardS0**  
   - **Scale**: Increase search unit by 4 for better performance
2. Wait for deployment to complete

![Azure AI Services Creation](<Reference Pictures/aiservice6.png>)

**Remarks**: By now, you have everything needed (Hub, Project) in **AI Foundry**.

---

### 6️⃣ Create a Hub

1. On the **AI Foundry** page at [https://portal.azure.com](https://portal.azure.com), select **+ Create** and **Hub**. Provide:
   - **Subscription**  
   - **Resource group**  
   - **Region**: choose one from the Tips  
   - **Name**  
   - **Connect AI Services incl. OpenAI**: pick the Open AI service you made  before this step
   - **Storage Tab**: select your storage account  
   - **Key Vault Tab**: pick your key vault  
   - **Networking**: default (public)  
   - Everything else default  
   - **Create + Review**, then **Create**
2. Wait for deployment to finish

![Hub Creation](<Reference Pictures/hub7.png>)

---

### 7️⃣ Create a Project

1. On the **AI Foundry** page at [https://portal.azure.com](https://portal.azure.com), select **+ Create** and **Project**. Provide:
   - **Subscription**  
   - **Resource group**  
   - **Region**: choose from the recommended regions  
   - **Name**  
   - **Hub**: pick the Hub you created  
   - Keep other defaults  
   - **Create + Review**, then **Create**
2. Wait for deployment

![Project Creation](<Reference Pictures/project8.png>)

**Remarks**: This shouldn’t take more than 20 minutes. Once done, head to [https://ai.azure.com](https://ai.azure.com). Choose your project, and we’ll proceed inside that environment.

**TIP**: With no organizational constraints, you can sign up at [https://ai.azure.com](https://ai.azure.com) and create the project directly. All other resources will be created automatically. You just need an AI search service resource.

---

### 8️⃣ Deploy Models

You need two models:
- **An embedding model** (text-embedding-ada-002)
- **A generative model** (like gpt-35-turbo)


1. In **Azure AI Foundry**, open your **project** → **My assets** → **Models + endpoints**.
2. **New deployment** of `text-embedding-ada-002` (click **Customize**):
   - **Deployment name**: `text-embedding-ada-002`
   - **Type**: Standard
   - **Model version**: default
   - **AI resource**: the AI service you created
   - **Tokens per Minute**: max
   - **Content filter**: DefaultV2
   - **Enable dynamic quota**: optional  
   > If insufficient quota, you'll be asked to choose a different location; a new AI resource will be created.

3. **Repeat** the deployment for `gpt-35-turbo` under the name `gpt-35-turbo`.
4. **Select** `gpt-35-turbo` → **Open in playground**.
5. Test with "What do you do?" to see the default response.
6. **Now change** instructions/context:

![Model Instructions](<Reference Pictures/model9.png>)

**Objective**: Provide Retails advice as a custom knowledgeable advisor.

**Capabilities**:
- Analyze and discuss customer purchase history and transaction details  
- Recommend products and offers based on loyalty tier, preferences, and past purchases  
- Provide insights on loyalty program benefits and tier upgrades  
- Answer questions about previous orders, returns, and account activity  
- Suggest personalized deals, bundles, and shopping tips  
- Help with budgeting, saving, and maximizing rewards  
- Address common retail issues (order status, payment, delivery, etc.)  

**Instructions**:
1. Engage as a friendly, knowledgeable retail advisor.
2. Use customer profile, transaction history, and loyalty data to provide accurate recommendations.
3. Tailor responses to each customer's preferences, loyalty tier, and shopping behavior.
4. Be practical, prioritize safety, and respect customer privacy at all times.
5. Encourage follow-up questions and ongoing engagement with the customer.

6. **Apply changes**.
7. **Test the chatbot** with the question "What do you do?" to see a context-specific response. Notably, if you asked the same question before updating the context, the answer would have been more generic.

## 🚀 Milestone #1: Result

---
You can test the model by opening the **playground** and chatting with it. Ask some generic questions, and you’ll get generic answers. At this point, the model is looking for data it was originally trained on and is **not yet grounded** in **your custom data**. However, we did manage to tailor the instructions and context to yield more specific responses.

---

---

## 🚀 Milestone #2: Add Data to Your Project and Explore the Response of the Chatbot Post Indexing and Grounding

1. **Enable Managed Identity**  
   - **(a)** Enable **Managed Identity (MI)** for both the **AI service** and the **AI search service**.  
   - **(b)** In the **Search service** resource (in the Azure portal):  
     1. Go to **Settings** → **Identity**  
     2. Switch **Status** to **On**  
     3. Select **Save**  
   - **(c)** In the **Azure AI services** resource (in the Azure portal):  
     1. Go to **Resource Management** → **Identity**  
     2. Switch **Status** to **On**  
     3. Select **Save**

2. **Set API Access Control for Search**  
   - **(a)** In the **Search service** resource (in the Azure portal):  
     1. Go to **Settings** → **Keys**  
     2. Under **API Access control**, select **Both**  
     3. When prompted, select **Yes** to confirm

3. **Assign Roles**  
   - **(a)** The general pattern for assigning role-based access control (RBAC) is:  
     1. In the **Azure portal**, open the relevant resource  
     2. Select **Access control (IAM)** from the left pane  
     3. Click **+ Add > Add role assignment**  
     4. Search for the role, select it, then **Next**  
     5. When assigning a role to yourself:
        - Choose **User, group, or service principal**
        - **Select members**
        - Search for your name, select it
     6. When assigning a role to another resource:
        - Choose **Managed identity**
        - **Select members**
        - Pick the target resource type (e.g., Azure AI services or Search service)
        - Select your resource from the list
     7. Click **Review + assign** to finalize  
   - **(b)** Use these steps for each resource in this tutorial:
     1. **Search service** (Azure portal):
        - **Search Index Data Reader** → Azure AI services managed identity  
        - **Search Service Contributor** → Azure AI services managed identity  
        - **Contributor** → yourself (switch to **Privileged administrator roles** if needed)
     2. **Azure AI services** (Azure portal):
        - **Cognitive Services OpenAI Contributor** → Search service managed identity  
        - **Contributor** → yourself (if not already)
     3. **Azure Blob storage** (Azure portal):
        - **Storage Blob Data Contributor** → Search services managed identity & Azure AI services managed identity  
        - **Contributor** → yourself (if not already)

   > **TIP**: If you’re using identity-based authentication, **Storage Blob Data Contributor**, **Storage File Privileged Contributor** (inside Storage account), and **Cognitive Services OpenAI Contributor** (inside AI services) must be assigned to any user or managed identity needing storage access.

4. **Storage Account Datastore Configuration**  
   - **(a)** Best practice: **Microsoft Entra Authentication**  
   - **(b)** Enable the **Account Key** for the storage account (only if you can’t do #a) so you have it for future steps.

   > **TIP**: You can also create SAS URLs or use Entra ID in various ways. We’re using **Entra ID** for simplicity below.

### 5️⃣ Create Connections to the Blob Storage & AI Search

1. A straightforward option is to open the **Management Center** at [ai.azure.com](https://ai.azure.com) or [ml.azure.com](https://ml.azure.com) and create connections under **Connected resources** → **+ New connection**.  
2. Add **Azure AI Search** as an internal connection.

3. For loading custom data (if not uploading directly to AI Foundry), we'll use **Azure Blob storage**:

   - **a.** Click **+ New connection**  
   - **b.** Choose **Blob storage**  
   - **c.** Select the **subscription ID**, **storage account**, and **blob container** (the main container)

   **Option 4.a**:
   - Under **authentication method**, select **Microsoft Entra ID based**
   - Name the connection, click **Save**

   **Option 4.b**:
   - Under **authentication method**, select **Credential based**
   - Under **authentication type**, select **Account key**, then paste your storage account key
   - Name the connection, click **Save**

![Connection to Blob Storage](<Reference Pictures/conn10.png>)

---

### 6️⃣ Add the Custom Data to AI Foundry

1. Go to your **project** in **Azure AI Foundry**  
2. Select **Data + Indexes**  
3. Click **+ New Data**  
4. From the drop-down, pick the **data source** (the new connection). If configured right, you’ll see **Browse to storage path**; if not, you might see only **Enter storage path manually** (indicates an access or key issue)  
5. Choose the **subfolder** you need and click **Next**  
6. Provide a **friendly name** for this data

![Data Addition in AI Foundry](<Reference Pictures/data11.png>)
7. Once it’s created, verify it’s **readable** and shows **file count** and **total size**. A quick preview helps confirm correct ingestion.

8. Now create the **Index**:
   - a. Go to **Indexes**
   - b. Click **+ New Index**
   - c. Under **Data Source**, pick **Data in Azure AI Foundry**  and then pick the **Data** (the data you just set up)
   - d. Select the data
   - e. **Index configuration**: pick your **AI Search** service, name the vector index, optionally choose higher compute  
   - f. Select the **AOAI Service** **Embedding model** & **Embedding model deployment**  connection from when you created the project  
   - g. Click **Create vector index**  
   - h. Status will show "In progress" while indexing completes

![Creating a Vector Index](<Reference Pictures/vector12.png>)

> **TIP**: Click **job details** to see the indexing job in [https://ml.azure.com](https://ml.azure.com). Times may vary by data size/resources.

![Vector Indexing Status](<Reference Pictures/vector13.png>)

---

### 7️⃣ Add Your Custom Data to Your Chat Model

1. In your **Azure AI Foundry** project, under **Playgrounds**, open **try the chat playground**  
2. Click **Add your data**  
3. Pick the **project index** from the previous step  
4. For **Search type**, keep **hybrid**  
5. No other changes; your chatbot now includes **custom data**  
6. After refreshing, ask specific questions like:
   - “What is the Address of Customer_1354?”
   - “im looking for everything related to Customer_1354”
   - “how many loyaltyTier does this customer went through? and when all?”


**Congratulations!**  
You’ve trained the model with **your data**, giving domain-specific answers. Note:

> **TIP**:Create seperate folder for JSON,CSV and TXT and upload those files to the storage container (refined-data as an example) and then create the data and index out of all 3 formats and detach/attach each type of Indexes with the LLM to see the difference in output the LLM will give you

- **Best Way** the best way is to directly use AI search and upload the CSV file directly using the code [Upload the CSV entries directly to Search Index](../AI_Scripts/03_search_direct_upload.py)
- **csv** might cause inconsistent answers
- **txt** format often yields better responses
- **Json** format is the best to out of all 3 formats

- **Our recomendation is to use TXT format for MS2 ,even though you will get inconsistent results ,you will learn why it happens and how it is getting fixed at MS4, but if you do not have time to go till MS4 use JSON file and you will see consistent results**
- **Refined data yeilds more refined answers**


- **Your AI application is as reliable as your Data**


**Milestone #4** will introduce an **AI agent** approach to tackle these inconsistencies.

If you used **csv** data, consider **txt** for better results. You’ll also see it’s easy to get single-record details but harder to do **bulk** responses—this setup needs more advanced frameworks or custom solutions for bigger queries.

## 🚀 Milestone #2: Result

---

You can **Build & Customize** a Generative AI app with your **own custom data**. Now, when you ask the same question as before, it references **your** data. Check the **References** button to see the underlying details.

---

---

## 🚀 Milestone #3: Build & Customize – Create, Iterate, and Debug Your Orchestration Flows

**Context**: This sample **prompt flow** manages a **multi-round conversation**, retaining history for each new user request. It uses a set of tools to:
1. **Append** the conversation history to form a contextual question  
2. **Retrieve** data from your index  
3. **Generate** prompt context using the retrieved data  
4. **Create** prompt variants (system message, structured history)  
5. **Submit** the final prompt to a language model to get a natural language response

### 1️⃣ Save the Current Prompt Flow

1. In **Azure AI Foundry**, open your **project** → **Playgrounds** → **chat model**  
2. Click **prompt flow** and save it with a name like `default-flow`  
3. Review the steps in the flow; you'll soon clone it so the chat can include conversation history

### 2️⃣ Use the Index in a Prompt Flow

1. Your **vector index** is already stored in your **AI Foundry** project, making it simple to include in a prompt flow  
2. In the **AI Foundry** portal, open your **project** → **Build and customize** → **Prompt flow**  
3. **Create a new prompt flow** by cloning the **Multi-Round Q&A on Your Data** sample  
4. Save that clone in a folder named `product-flow`  
5. Click **Start compute session** to launch the runtime; wait until it’s ready  
6. In **Inputs**, confirm:
   - `chat_history`
   - `chat_input`  
   (The default sample includes some AI conversation.)

7. In **Outputs**, ensure:
   - `chat_output` = `${chat_with_context.output}`

8. In **modify_query_with_history**:
   - **Connection** = default Azure OpenAI
   - **Api** = `chat`
   - **deployment_name** = `gpt-35-turbo`
   - **response_format** = `{"type":"text"}`

9. Once the compute session starts, go to **lookup**:
   - `mlindex_content`: click the blank field → **Generate** pane  
     - **index_type**: **Registered Index**  
     - **mlindex_asset_id**: `<your_vector_index>:1`  
     - **save**
   - `queries`: `${modify_query_with_history.output}`
   - `query_type`: **Hybrid** (vector + keyword)
   - `top_k`: 2

10. In **generate_prompt_context**, confirm `search_result (object)` = `${lookup.output}`

11. In **Prompt_variants**:
   - `contexts (string)` = `${generate_prompt_context.output}`
   - `chat_history (string)` = `${inputs.chat_history}`
   - `chat_input (string)` = `${inputs.chat_input}`

12. In **chat_with_context**:
   - **Connection** = `Default_AzureOpenAI`
   - **Api** = `Chat`
   - **deployment_name** = `gpt-35-turbo`
   - **response_format** = `{"type":"text"}`
   - `prompt_text (string)` = `${Prompt_variants.output}`

13. On the **toolbar**, click **Save** to finalize changes in the prompt flow  
14. On the **toolbar**, select **Chat**. A pane opens with sample conversation history and default input (you can ignore it).  
15. Replace the default question with **how many clients does Wayne Enterprises company have?** and submit  
16. Examine the response, which should be sourced from your index  
17. Review the output of each tool in the flow  
18. Enter additional queries, for example:

    What products did Customer_1354 purchase?
    What is the loyalty tier of Customer_1354?
    How much did Customer_2048 spend in total?
    What are the most popular product categories?
    Which customers have Gold loyalty tier?
    Can you show me all transactions from the Electronics category?
    What recommendations can you make for frequent buyers?

19. Notice how it uses **index data** and **chat history**  
20. Observe each tool’s transformations to build a contextual prompt

### 3️⃣ Deploy the Flow

1. On the **toolbar**, select **Deploy**  
2. Use the following settings:
- **Basic**:
  - Endpoint: **New**
  - Endpoint name: auto-generated or unique
  - Deployment name: auto-generated or unique
  - Virtual machine: `Standard_DS3_v2`
  - Instance count: 3
  - Inferencing data collection: selected
- **Advanced**: defaults

3. In the **Azure AI Foundry** portal, open your **project** → **My assets** → **Models + endpoints**. Watch for the new deployment to appear as **succeeded** under your new endpoint (can take time).  
4. When done, select it → **Test** page to check the response  
5. Enter a follow-up prompt and review the output  
6. Go to **Consume**, where you'll find connection details and sample code to integrate this prompt flow as a copilot in your application

**Congratulations!** You’ve trained the model with your own data and created a new prompt flow so users can chat iteratively while retaining history. The conversation context is included each time.

### Milestone #3: Result

---
The sample prompt flow you are using implements the prompt logic for a chat application in which the user can iteratively submit text input to the chat interface. The conversational history is retained and included in the context for each iteration. With this, the challenge #3 is completed; we still have not solved the problem of bulk response query or rather SQL-formatted queries in human language. Hungry for more? Let’s explore further!

---

---

## 🚀 Milestone #4: Query Multiple CSV Files Using Azure OpenAI & Langchain Framework

**Context**: At the end of Milestone #2, we observed the model handling certain questions (e.g., specific data fields). But for **SQL-formatted queries** or more complex data in a **human-readable** format, our chat app isn’t fully autonomous yet. Larger or semi-structured data (like CSV or Excel) can be challenging. This is where an **AI Agent** using an **AI Model framework like Langchain**  and  **OpenAI Service** comes in, enabling powerful, flexible queries on more complex data.

### 1️⃣ Create an Azure OpenAI Resource from the Portal (for the sake of the Milestone please create a new )

1. Sign in to the **Azure portal**.  
2. Search/Select **Azure OpenAI**.  
3. Click **+Create**.  
4. Provide details:
   - **Subscription**  
   - **Resource group**  
   - **Region**  
   - **Name**  
   - **Pricing tier**: `Standard S0`
5. Keep other defaults.  
6. Select **Review + Create**.  
7. When deployment is done, open the resource to note the keys/endpoints (for later).  
8. Click **Go to Azure AI Foundry portal**, and we'll continue our setup there.

![Azure OpenAI Resource Creation](<Reference Pictures/openai14.png>)

### 2️⃣ Deploy Model

You need a model capable of generating **natural language responses** from your data.

**Steps**:

1. In the **Azure AI Foundry** portal, within your **Azure OpenAI** resource, go to **Deployments** → **Model deployments** → **Deploy base model**.
2. Create a new deployment of `gpt-35-turbo` by selecting **Customize** after confirming:
   - **Deployment name**: `gpt-35-turbo`
   - **Deployment type**: Standard
   - **Model version**: default
   - **Resource location**: keep the default
   - **Tokens per Minute**: slide to maximum
   - **Enable dynamic quota**: optional
3. **Test** your chatbot with a quick question like "What do you do?" to confirm it responds.

Now we’ll move to our local environment so this OpenAI service can connect with our CSV data in a **human-readable** manner.

**TIP**: We’re using **VSCode** as our editor. It’s helpful to have the following extensions:

```markdown
Azure Account  
Azure CLI Tools  
Azure Developer CLI  
Azure Machine Learning  
Jupyter  
Jupyter Notebook Renderers  
jupyter-notebook-vscode  
Linter  
Pylance  
Python  
Python Debugger  
Python snippets
```

### 3️⃣ Write the python Code using Langchain framework and read the csv from storage account ,combine and get it ready for querying using an agent,deploy an agent and invoke the agent to get answers

1. Install the various python packages we will be using during this coding session.open up a new file with .ipynb extension,this will help us run the code in cells and seperate functions ,this is better for troubleshooting and learning the python coding also

```python
%pip install openai
%pip install langchain
%pip install pandas
%pip install langchain_experimental
%pip install langchain_openai
%pip install tabulate
%pip install azure-storage-blob
```

2. Import the necessary packages and also connect to the Azure subscription, gather the details, get the CSV files in a loop, and combine them together using dataframes and place it in a single file

```python
import openai
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient
connection_string = "<<connectionstrong of your storage account>>"
container_name = "refined-data"
blob_names = ["tailwind_traders_retail_data.csv"]
# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
dataframes = []
for blob_name in blob_names:
    blob_client = container_client.get_blob_client(blob_name)

    # Download the blob content
    blob_content = blob_client.download_blob().content_as_text()

    # Read the content into a pandas DataFrame
    df = pd.read_csv(StringIO(blob_content))
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
print(combined_df.head())
```

3. Save the combined DataFrame to a CSV file and save locally

```python
combined_csv_path = "combined.csv"
combined_df.to_csv(combined_csv_path, index=False)
```

4. Connect to the OpenAI resource and the deployment which we created earlier

```python
from langchain_openai import AzureOpenAI

llm = AzureOpenAI(
    deployment_name="gpt-35-turbo",
    openai_api_type="azure",
    openai_api_key="your_azure_openai_key_here",
    azure_endpoint="<<your openAI resource end point>>",
    api_version="<<gather this from the foundry>>"
)
```

6. Create the CSV agent using Langchain and combine the same to a single file and save locally to get the results faster

```python
%pip install langchain_experimental
from langchain_experimental.agents import create_csv_agent

agent = create_csv_agent(
    llm=llm, 
    path='combined.csv', 
    verbose=True, 
    low_memory=False, 
    allow_dangerous_code=True
)
```

7. Invoke the agent and ask the questions which are structured queries but in human-readable format

```python
agent.invoke("im looking for everything related to Customer_1354?")
```

8. Invoke the agent and ask more complicated questions which are structured queries but in human-readable format which also did not give us the right answers in the past milestones

```python
agent.invoke("how many loyaltyTier does this customer went through? and when all")
```

Congratulations! 🎉 You are now able to talk to the CSV using the OpenAI resources programmatically. The last two questions weren't answered in the first 3 milestones, and we started getting the correct responses for the questions we asked in the format we want! 🏆

These 4 milestones represent the journey of GenAI apps over the last 24-36 months. 🕰️ At this point, we can converse with any type of data using OpenAI ML frameworks and Foundry offerings. 💬

## 🚀 Milestone #4: Result ✨

---
Your results are **significantly more accurate**, enabling you to query semi-structured or unstructured data in **human-readable prompts** without memorizing any syntax. 🤩 Next, you can explore different frameworks and create other **agents** to fulfill various organizational needs. 🎯 These can include multi-agent systems, single agents working across multiple frameworks or data sources, and potentially deploying your solution as a **web app** or simple site (e.g., using Azure Web Apps), or via Python-based lightweight deployment packages. 🌐

Having addressed all the use cases of reading different source files to retrieve domain-specific answers, 🥳 you’ve extended your application’s intelligence to match the expertise of the prompt engineer’s queries. But how do we push it further? **Enter multi-agent applications**! 🧠 These are small, autonomous subsystems that operate in parallel, in series, or back-and-forth to deliver a refined product—work that might otherwise require hours of manual analysis. 🚀  
Stay tuned to learn more about **multi-agent AI applications** in upcoming challenges! 📚

**Congratulations** once again! 👏
---

### Extra Credits 🌟

- **Deploy your web app** using the new deployment. Test it to see how it behaves in a real environment. 🚀  
- **Deploy your app using cosmos DB** so that the emeddings and vector data and actual data will both be stored in the same place 🚀
- **Enable CICD Pipeline** enable contnious integration and deployment using gitops for LLM models 🚀    
- Experiment with **Temperature** and **P value** to understand how they influence response creativity and variability. 🌡️  
- **Customize** the model’s context or instructions with a humorous or thematic style—maybe channel your favorite movie character’s voice. 🎭  
- Investigate how **Microsoft Fabric** can act as a data source for your AI app,which all features are in preview and what all are GA. 🧵 