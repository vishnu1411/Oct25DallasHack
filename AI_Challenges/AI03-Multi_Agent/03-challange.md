<!-- File: 03-challenge.md -->
# 🏆 Challenge 03: Multi-Agent AI Application for Inventory Management

## 📖 Learning Objectives 
In this final challenge, you will design a **multi-agent** AI solution. Instead of a single agent handling everything, multiple specialized agents (or agent components) will collaborate. By the end, you will understand how to:  
- **Divide tasks** among different AI agents (or subsystems) for complex workflows.  
- **Orchestrate** agents so that one agent can invoke another when appropriate (agent-to-agent interaction).  
- **Detect** when a user’s request triggers a special workflow (in this case, an inventory check and alternative suggestion if item is unavailable).  
- Build a fresh, innovative AI application that goes beyond Q&A: a proactive assistant that handles an “out-of-stock” scenario gracefully using multiple steps.  

## ⚙️ Scenario 
Our retail company’s data is consolidated (via Fabric), and we have an AI chatbot that can answer questions and even suggest complementary products. Now, we address a common situation: a customer looks for a product that is **not in stock** or not carried. The AI assistant should not just say “Not available”; it should act smartly:

- **Agent A (Inventory Agent)**: Check if the product exists/in stock.  
- **Agent B (Alternative Agent)**: If not available, find a similar alternative product that *is* available (and possibly note the unavailability event).  
- **Agent C (Answer Agent)**: Convey the result to the user (apologize and suggest alternative, or confirm availability).  

This challenge is about implementing that multi-agent logic. In practice, you might do this with separate agents or a carefully structured prompt flow—either way, you are orchestrating multiple steps.

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


### Milestone #1: **Design Agent Workflow**  
1. **Identify Agent Roles**: Write down the roles and responsibilities of at least two agents: (A) Inventory Check Agent – decides if item is in stock or not, (B) Alternative Finder Agent – finds a replacement item if needed. (We might implicitly use our main chatbot as the one orchestrating these roles).  
2. **Decide Interaction Modalities**: Will Agent A directly call Agent B? Or will a central Orchestrator manage both? In Foundry’s context, often a prompt flow or chain-of-thought within one agent can simulate this. Outline the sequence:  
   - Step 1: Search the product index for the item.  
   - Step 2: If found, output a message “Yes, we have it.” (maybe including some details).  
   - Step 3: If not found, query for an alternative. This could be: search the index for a similar item (e.g., if user asked for “Contoso XYZ Camera” which we don’t carry, perhaps find “Fabrikam XYZ Camera” or “Contoso ABC Camera”). Or use the recommendations container in Cosmos from Challenge 02, if it contains a mapping for that item to an alternate suggestion.  
   - Step 4: Compile a response: “Sorry, X is not available. However, you might be interested in Y, which is similar.”  

3. **Prepare Alternative Finding Method**: Decide how to get a suggestion when an item is not found:  
   - **Approach 1**: Use the recommendations from Challenge 02 in a clever way (maybe pre-store an entry for the expected missing item pointing to an alt).  
   - **Approach 2**: Use semantic similarity via Cognitive Search: e.g., if “Contoso UltraCamera” isn’t found, search the index for “camera” or similar features to find the next best match. This leverages the vector search to get a similar item.  
   - Either approach is valid. (Approach 2 is truly fresh since it uses the vector similarity to find “closest” product in stock.)  

### Milestone #2: **Implement Multi-Agent Orchestration**  
1. **Use Prompt Flow (Recommended)**: Open Azure AI Studio > Prompt flow. Create a new flow (or extend the existing one) to incorporate the multi-step logic:  
   - Step: **Search Inventory** – Use the existing Cognitive Search index (`retail-index`) to search for the product name user asked. (This acts as Inventory Agent: if result found, item exists.)  
   - Step: **Check Result** – Add a small code step to examine the search results. If no results, set a variable `item_available=False`. If results exist, `item_available=True` and perhaps capture the product details from the result (like name or stock count if present).  
   - Step: **Find Alternative** – This step executes only if `item_available=False`. Here you implement Approach 1 or 2 from above. For example, use the recommendations function from Challenge 02: call `GetRecommendations` for the unavailable product (maybe we preloaded it with a known alternative suggestion). Or perform another search query: if the user asked for “Contoso XYZ Camera”, do a search for “camera” or simply a vector similarity search on the query itself but filter out exact matches (if none found, the vector search might already return something close). You might need to experiment: perhaps search the index for the product name anyway – if the index uses semantic similarity, it could return a near match even if exact doesn’t exist.  
   - Step: **Compile Answer** – Finally, a step to generate the answer to the user. This step will use conditional inputs: if `item_available` is True, the agent just confirms availability (and perhaps offers to help with anything else). If False, it uses the alternative from the previous step (if any found) to suggest to the user. If an alternative exists, phrase something like “We don’t have X, but we do have Y which is similar.” If even alternative search gave nothing, apologize that it’s not available and maybe suggest contacting support or checking later (to not leave user with nothing).  

2. **Agent-to-Agent API Call (Alternative)**: If you wanted to literally have separate agents, you could deploy one agent that does product search (exposed via an endpoint), and call it from another agent via an HTTP tool. This is more advanced and not necessary if prompt flow covers it, but conceptually: e.g., Agent B could be our Challenge 02 bot which given a product outputs recommendations (which could be used as alternatives too). However, due to time, we proceed with the prompt flow method which simulates multi-agent internally.  

3. **Logging (Optional)**: You could add a step to log the “not found” event. E.g., a call to another Azure Function to record that product X was searched for but not available. This could be useful feedback for inventory management. If you choose to, implement a small function or even use Application Insights logging. (Mark this step optional – mainly to demonstrate potential extension.)

### Milestone #3: **Testing the Multi-Agent System**  
1. **Test Available Item Query**: Ask the assistant for an item that you know is in the index (in stock). Example: “Do you have Contoso Phone Model X in stock?” The flow should find it in search results, mark item_available True, and answer along the lines of “Yes, Contoso Phone Model X is available.” Possibly it could even pull stock count if such data is in the index (not required, a confirmation is enough).  
2. **Test Unavailable Item Query**: Ask for a product that is not in your index (and thus not in stock). E.g., a made-up model or one you intentionally omitted. “Do you carry Contoso XYZ Camera?” The search will return nothing (`item_available=False`). Then the alt-finding step triggers. If we set up an alternative (say in Cosmos recommendations we added `product: "Contoso XYZ Camera", suggestions: ["Fabrikam 5X Zoom Camera"]`), the flow should retrieve that. If using vector search, it might return “Fabrikam 5X Zoom Camera” from index as the closest match. The final answer should apologize and suggest that camera.  
3. **Edge: No Alt Found**: Try an item that’s missing and perhaps we didn’t set up alt data for and is unique (so vector search doesn’t yield a good similar product). For example, “Do you have Contoso Refrigerator?” (assuming our index and recommender have nothing about appliances). The flow will have no search result, alt-finder might also return empty. Ensure your answer in this case is a polite: “Sorry, we don’t have that product at the moment.” Even without alternative, the assistant should handle it gracefully.  
4. **Multi-turn Check**: Follow up the not-available scenario with something like “What about something similar?” Our prompt flow design might not explicitly carry context between turns unless we integrated with the multi-round flow. If you combined this logic into the multi-round prompt flow from before, it would handle it in context (the user asking “something similar” after being told not available could re-trigger the alt search – but that’s optional complexity). At minimum, verify the single-turn behavior is correct.  

Throughout testing, observe how the two “agents” (inventory check and recommendation) worked in tandem. This multi-agent orchestration is the key takeaway: decomposing the problem avoided trying to have one giant prompt do everything. Instead, we did a structured approach.

---

By completing Challenge 03, you’ve built a **multi-agent AI application**: It takes a user request, runs it through a decision matrix (agent A: check inventory), then possibly through another knowledge source (agent B: find alternative), and finally gives a composed answer. This is a microcosm of how complex AI assistants can be built – e.g., a virtual shopping assistant that can check stock, recommend products, place orders, etc., each a separate function/agent working together.

This challenge’s concept is fresh and powerful: rather than an AI simply saying "I don't know" or "not found", the system proactively offers a solution, demonstrating a higher level of intelligence and usefulness. 

## 🚀 Next Steps (beyond the challenge)
- You could extend this further: integrate an agent or function to **place an order or notify** when an out-of-stock item is available (taking it into transactional territory).  
- Or add a **pricing agent** that, if the user asks price differences for alternatives, can fetch current prices from a database/API.  
- Consider using the new **Connected Agents** feature of Foundry when it becomes available, to formally separate these agents and let Foundry manage the routing.

You now have hands-on experience with Azure AI Foundry, Cognitive Search, Cosmos DB, and multi-step orchestration. You’ve essentially built a miniature “Copilot” for retail that can answer questions, give suggestions, and handle inventory queries – all using modern AI techniques and a robust architecture. Congratulations on completing the hackathon challenges! Feel free to experiment and enhance these solutions further. Happy building!  
