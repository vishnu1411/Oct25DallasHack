# 🏆 Challenge 03: Advanced Multi-Agent AI System

## 📖 Learning Objectives 
In this final challenge, you will design a **production-ready multi-agent** AI solution that demonstrates enterprise-level capabilities. You'll build a sophisticated conversational AI system with:
- **🧠 5 Specialized AI Agents** working in harmony
- **💭 Advanced Conversation Memory** that persists across sessions  
- **🔄 Smart Context Switching** with confirmatory response handling
- **⚡ Real Azure Service Integration** for live inventory and recommendations
- **🎨 Beautiful Console Interface** with rich formatting and analytics

By the end, you will understand how to:  
- **Architect** complex multi-agent systems with clean separation of concerns
- **Orchestrate** agents with sophisticated conversation flow management
- **Implement** persistent session context and conversation memory
- **Handle** confirmatory responses and context switching naturally
- Build a **production-ready** AI application that rivals commercial systems

## 🎯 Project Overview

This solution demonstrates how to build a **production-ready multi-agent AI system** for intelligent retail assistance. Unlike basic chatbots, this system features:

- **🧠 5 Specialized AI Agents** working in harmony
- **💭 Advanced Conversation Memory** that persists across sessions  
- **🔄 Smart Context Switching** with confirmatory response handling
- **⚡ Real Azure Service Integration** for live inventory and recommendations
- **🎨 Beautiful Console Interface** with rich formatting and analytics

### What Makes This Solution Special?

This isn't just a multi-agent system—it's a **conversational AI that thinks**:
- Remembers what you've discussed ("I already showed you those routers")
- Understands confirmatory responses ("yes" means show the routers we just talked about)
- Provides intelligent alternatives when products aren't available
- Tracks conversation patterns and provides detailed session analytics

---

## 🐍 Python Version Requirements & Setup

**⚠️ IMPORTANT: This project requires Python 3.12 specifically for optimal compatibility with Azure services and dependencies.**

### Check Your Python Installation
```powershell
# Check which Python versions you have installed
py -0
# OR
python --version
python3.12 --version
```

### Installing Python 3.12 (If Not Present)
If you don't have Python 3.12, download and install it from:
- **Official Python**: https://www.python.org/downloads/release/python-3120/
- **Microsoft Store**: Search "Python 3.12"

### Using Python 3.12 with Multiple Versions
```powershell
# Use py launcher to specify Python 3.12
py -3.12 --version        # Verify Python 3.12 is available
py -3.12 -m pip --version # Verify pip for Python 3.12

# Find Python 3.12 installation path
py -3.12 -c "import sys; print(sys.executable)"
# Example output: C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe
```

**For all commands in this challenge, use either:**
- `python` (if Python 3.12 is your default)
- `py -3.12` (to explicitly use Python 3.12)

---

## 🚀 Getting Started: Three Paths to Success

### Path 1: 🆕 Starting Fresh (Brand New Participants)

#### Step 1: Download and Setup
```powershell
# Clone the repository
git clone https://github.com/your-hackathon-repo/AIHack-Oct-2025.git
cd "AIHack-Oct-2025/03-Multi Agent/Multi_Agent_App"

# Create virtual environment with Python 3.12
python -m venv venv
# OR with py launcher
py -3.12 -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Verify you're using Python 3.12 in the virtual environment
python --version
# Should show: Python 3.12.x

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Step 2: Configure Azure Services
You'll need these Azure services (create them in Azure Portal):

1. **Azure OpenAI Service**
   - Create deployment with GPT-4 or GPT-3.5-turbo
   - Note endpoint and API key

2. **Azure Cognitive Search**
   - Create search service
   - Import the retail data index
   - Note endpoint and admin key

3. **Update .env file**:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_openai_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Azure Search Configuration  
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your_search_api_key_here
AZURE_SEARCH_INDEX=csv-retail-index

# Application Settings
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

### Path 2: 🔗 Continuing from Challenge 02 (Recommended)

If you completed Challenge 02, you already have:
- ✅ Azure OpenAI service configured
- ✅ Azure Cognitive Search with retail index
- ✅ Azure Function for recommendations

#### Quick Setup:
```powershell
# Navigate to Multi-Agent folder
cd "03-Multi Agent/Multi_Agent_App"

# Use your existing .env from Challenge 02
copy "../../02-AI Agent/.env" ".env"

# Create virtual environment with Python 3.12
python -m venv venv
# OR with py launcher
py -3.12 -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install new dependencies for multi-agent system
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 📝 Challenge Tasks 

✅ **Set up inventory data** – Ensure you have a way to determine if a product is available. This could be a flag in the product index or a separate list of out-of-stock items. (For simplicity, we might assume the search index from Challenge 01 contains only available products. So a search miss = not available.) Alternatively, use another Cosmos DB container or simple dictionary for inventory status.  

✅ **Implement multi-step logic** – Use Azure AI Foundry’s tools (prompt flow, connected agents, or external orchestration) to split the task: first an inventory check, then an alternative lookup, then response formulation. This can be done in a prompt flow with conditional steps or by one agent calling another via an API.  

✅ **Leverage previous components** – Reuse what you built: e.g., use the Cognitive Search index to search for the product (inventory check). Use the Cosmos DB recommendations from Challenge 02 to find a similar product if the item is not found. The “fresh concept” here is having one agent’s outcome (no search result) trigger another action (search for alt product).  

✅ **User experience** – The final answer from the assistant should handle the situation smoothly: if unavailable, it suggests a specific alternative item and maybe offers to notify or something (we won’t implement notification, just noting we could log it).  

## 🤖 What Are Embeddings and Why Use Them?

**Embeddings** are numerical representations of text (or other data) that capture semantic meaning. Instead of relying on keywords, information is encoded as vectors (arrays of numbers) in a high-dimensional space. The key advantage: similar meanings produce vectors that are close together in this space.

### 🔍 Role in Semantic Search

Embeddings enable search systems to find results based on meaning, not just exact wording. For example, a keyword search might treat “5K” and “4K” as unrelated, but an embedding model understands both refer to display resolutions and are related to “monitor.” This allows a vector search to retrieve a “4K monitor” document for a “5K monitor” query if it’s the closest semantic match. Embeddings surface conceptually relevant alternatives where normal search fails.

### ⚡ Azure Cognitive Search Capabilities

By default, **Azure Cognitive Search (ACS)** is a keyword search engine. It supports fuzzy matching and synonym maps, but these require manual configuration. ACS also offers a “semantic search” mode, which improves snippet extraction and passage ranking for natural language queries. However, semantic search still relies on lexical overlap—if the document doesn’t contain related terms, it won’t be retrieved. For example, if “Contoso 5K” isn’t in any document, semantic mode alone won’t return a “4K” result. In short, ACS semantic search ≠ true semantic similarity search.

### 🚀 What Embeddings Add

With embeddings and vector search, your assistant can handle queries that use different terminology than the documents. This enables “conceptual likeness” matching—such as “dog” vs “canine” or “sneakers” vs “running shoes.” In your scenario, the bot could find a “gaming laptop” when asked for a “high-end notebook,” if those map to similar feature vectors. This capability is not possible with plain keyword search unless you explicitly pre-link those terms.


This challenge consists of **4 comprehensive milestones** to build your multi-agent system:

### 1️⃣ Milestone 1: **Project Setup and Configuration**

**Goal**: Set up the foundation for your multi-agent system with proper Azure service integration.

#### 1.1 Core Agent Roles to Design:
1. **🕵️ Intent Detector Agent**: Analyzes user queries to determine intent (product search, general inquiry, alternatives request)
2. **📦 Inventory Agent**: Searches Azure Cognitive Search index for products  
3. **🔄 Alternatives Agent**: Finds smart alternatives when items are unavailable
4. **💡 Recommendations Agent**: Provides AI-powered product suggestions
5. **📝 Response Formatter**: Creates natural, conversational responses

#### 1.2 Architecture Requirements: Will Agent A directly call Agent B? Or will a central Orchestrator manage both? In Foundry’s context, often a prompt flow or chain-of-thought within one agent can simulate this. Outline the sequence:  
   - Step 1: Search the product index for the item.  
   - Step 2: If found, output a message “Yes, we have it.” (maybe including some details).  
   - Step 3: If not found, query for an alternative. This could be: search the index for a similar item (e.g., if user asked for “Contoso XYZ Camera” which we don’t carry, perhaps find “Fabrikam XYZ Camera” or “Contoso ABC Camera”). Or use the recommendations container in Cosmos from Challenge 02, if it contains a mapping for that item to an alternate suggestion.  
   - Step 4: Compile a response: “Sorry, X is not available. However, you might be interested in Y, which is similar.”  

3. **Prepare Alternative Finding Method**: Decide how to get a suggestion when an item is not found:  
   - **Approach 1**: Use the recommendations from Challenge 02 in a clever way (maybe pre-store an entry for the expected missing item pointing to an alt).  
   - **Approach 2**: Use semantic similarity via Cognitive Search: e.g., if “Contoso UltraCamera” isn’t found, search the index for “camera” or similar features to find the next best match. This leverages the vector search to get a similar item.  
   - Either approach is valid. (Approach 2 is truly fresh since it uses the vector similarity to find “closest” product in stock.)  

### 2️⃣ Milestone 2: **Multi-Agent System Implementation**

**Goal**: Build the core multi-agent orchestration system with proper coordination.

#### 2.1 Agent Development Tasks: Open Azure AI Studio > Prompt flow. Create a new flow (or extend the existing one) to incorporate the multi-step logic:  
   - Step: **Search Inventory** – Use the existing Cognitive Search index (`retail-index`) to search for the product name user asked. (This acts as Inventory Agent: if result found, item exists.)  
   - Step: **Check Result** – Add a small code step to examine the search results. If no results, set a variable `item_available=False`. If results exist, `item_available=True` and perhaps capture the product details from the result (like name or stock count if present).  
   - Step: **Find Alternative** – This step executes only if `item_available=False`. Here you implement Approach 1 or 2 from above. For example, use the recommendations function from Challenge 02: call `GetRecommendations` for the unavailable product (maybe we preloaded it with a known alternative suggestion). Or perform another search query: if the user asked for “Contoso XYZ Camera”, do a search for “camera” or simply a vector similarity search on the query itself but filter out exact matches (if none found, the vector search might already return something close). You might need to experiment: perhaps search the index for the product name anyway – if the index uses semantic similarity, it could return a near match even if exact doesn’t exist.  
   - Step: **Compile Answer** – Finally, a step to generate the answer to the user. This step will use conditional inputs: if `item_available` is True, the agent just confirms availability (and perhaps offers to help with anything else). If False, it uses the alternative from the previous step (if any found) to suggest to the user. If an alternative exists, phrase something like “We don’t have X, but we do have Y which is similar.” If even alternative search gave nothing, apologize that it’s not available and maybe suggest contacting support or checking later (to not leave user with nothing).  

2. **Agent-to-Agent API Call (Alternative)**: If you wanted to literally have separate agents, you could deploy one agent that does product search (exposed via an endpoint), and call it from another agent via an HTTP tool. This is more advanced and not necessary if prompt flow covers it, but conceptually: e.g., Agent B could be our Challenge 02 bot which given a product outputs recommendations (which could be used as alternatives too). However, due to time, we proceed with the prompt flow method which simulates multi-agent internally.  

3. **Logging (Optional)**: You could add a step to log the “not found” event. E.g., a call to another Azure Function to record that product X was searched for but not available. This could be useful feedback for inventory management. If you choose to, implement a small function or even use Application Insights logging. (Mark this step optional – mainly to demonstrate potential extension.)

### 3️⃣ Milestone 3: **Test Implementation & Unit Testing**

**Goal**: Comprehensive testing of all agent interactions and edge cases.

#### 3.1 Core Testing Scenarios: Ask the assistant for an item that you know is in the index (in stock). Example: “Do you have Contoso Phone Model X in stock?” The flow should find it in search results, mark item_available True, and answer along the lines of “Yes, Contoso Phone Model X is available.” Possibly it could even pull stock count if such data is in the index (not required, a confirmation is enough).  
2. **Test Unavailable Item Query**: Ask for a product that is not in your index (and thus not in stock). E.g., a made-up model or one you intentionally omitted. “Do you carry Contoso XYZ Camera?” The search will return nothing (`item_available=False`). Then the alt-finding step triggers. If we set up an alternative (say in Cosmos recommendations we added `product: "Contoso XYZ Camera", suggestions: ["Fabrikam 5X Zoom Camera"]`), the flow should retrieve that. If using vector search, it might return “Fabrikam 5X Zoom Camera” from index as the closest match. The final answer should apologize and suggest that camera.  
3. **Edge: No Alt Found**: Try an item that’s missing and perhaps we didn’t set up alt data for and is unique (so vector search doesn’t yield a good similar product). For example, “Do you have Contoso Refrigerator?” (assuming our index and recommender have nothing about appliances). The flow will have no search result, alt-finder might also return empty. Ensure your answer in this case is a polite: “Sorry, we don’t have that product at the moment.” Even without alternative, the assistant should handle it gracefully.  
4. **Multi-turn Check**: Follow up the not-available scenario with something like “What about something similar?” Our prompt flow design might not explicitly carry context between turns unless we integrated with the multi-round flow. If you combined this logic into the multi-round prompt flow from before, it would handle it in context (the user asking “something similar” after being told not available could re-trigger the alt search – but that’s optional complexity). At minimum, verify the single-turn behavior is correct.  

Throughout testing, observe how the two “agents” (inventory check and recommendation) worked in tandem. This multi-agent orchestration is the key takeaway: decomposing the problem avoided trying to have one giant prompt do everything. Instead, we did a structured approach.

---

By completing Challenge 03, you’ve built a **multi-agent AI application**: It takes a user request, runs it through a decision matrix (agent A: check inventory), then possibly through another knowledge source (agent B: find alternative), and finally gives a composed answer. This is a microcosm of how complex AI assistants can be built – e.g., a virtual shopping assistant that can check stock, recommend products, place orders, etc., each a separate function/agent working together.

This challenge's concept is fresh and powerful: rather than an AI simply saying "I don't know" or "not found", the system proactively offers a solution, demonstrating a higher level of intelligence and usefulness. 

### 4️⃣ Milestone 4: **Production Application Testing**

**Goal**: Test your main.py application from VS Code terminal to validate the complete multi-agent system.

#### 4.1 VS Code Terminal Testing:
1. **Launch Application**: Run your main.py from VS Code integrated terminal
2. **Interactive Testing**: Test all agent interactions through the console interface
3. **Validation Scenarios**: Verify agent coordination and response quality
4. **Performance Monitoring**: Check response times and system behavior
5. **Error Handling**: Test edge cases and error recovery

#### 4.2 Production Testing Requirements:
- **Agent Coordination**: Verify all 5 agents work together seamlessly
- **Conversation Flow**: Test natural dialogue progression
- **Memory Persistence**: Validate conversation context retention
- **Alternative Suggestions**: Confirm smart alternative recommendations
- **System Reliability**: Ensure consistent performance across sessions

### 5️⃣ Milestone 5: **Enhanced Features & Production Readiness**

**Goal**: Add advanced features that make your system production-ready.

#### 5.1 Advanced Features to Implement:
1. **Conversation Memory System**: Track products shown to avoid repetition
2. **Session Analytics**: Monitor user behavior and interests  
3. **Confidence Scoring**: Each agent returns confidence levels
4. **Fallback Mechanisms**: Handle service failures gracefully
5. **Performance Optimization**: Implement caching and async processing

#### 5.2 Production Enhancements:
- **Comprehensive Error Handling**: Robust exception management
- **Logging System**: Track system performance and user interactions  
- **Test Suite**: Unit tests for each agent and integration tests
- **Configuration Management**: Environment-based settings
- **Documentation**: Complete API documentation and usage guides

#### 5.3 Final Testing Scenarios:
1. **Performance Tests**: Test with multiple concurrent requests
2. **Stress Tests**: Verify system behavior under high load
3. **Integration Tests**: End-to-end testing of complete agent pipeline
4. **User Acceptance Tests**: Validate natural conversation flow
5. **Production Readiness**: Verify all monitoring and logging works

---

## 🎯 Success Criteria

By completing Challenge 03, you've built a **sophisticated multi-agent AI system** that demonstrates advanced AI orchestration and intelligence.

## 🚀 Next Steps (Beyond the Challenge)

- **Order Integration**: Add agents to place orders or notify when items are back in stock
- **Analytics Dashboard**: Track alternative suggestion success rates over time
- **Customer Service Integration**: Deploy as part of a larger customer service architecture
- **Personalization**: Add user preference learning and personalized recommendations
- **Connected Agents**: Use Azure AI Foundry's Connected Agents feature for formal agent separation

You now have hands-on experience with advanced AI orchestration, Azure AI services, and production-ready multi-agent systems. You've built a sophisticated "AI Copilot" for retail that demonstrates the future of intelligent customer service. Congratulations on completing this advanced challenge!
