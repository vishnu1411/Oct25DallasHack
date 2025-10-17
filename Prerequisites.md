# 🚀 Dallas MTC Hackathon: Prerequisites & Preparation Guide  

This hackathon is designed to be a **fun, collaborative, and hands-on learning experience**, bringing together **cutting-edge technologies** like **Microsoft Fabric, Azure AI, OpenAI**, and more to solve **real-world challenges**.

---

## 🔹 Preparing for the Hackathon 

To ensure you have the best possible experience, please review and complete all **prerequisites** before the event.  

---

## ✅ Personal Requirements  

Each participant must have:  

- 💻 **A laptop** with a modern web browser (**Chrome, Edge, Firefox, or Safari**).  
- 🐍 **Python 3.12 ** → [Download here](https://www.python.org/downloads/)  
- 🖥 **Visual Studio Code** → [Download here](https://code.visualstudio.com/download)  

### 🔹 Optional Tools (Recommended) 

- ☁ **Azure Storage Explorer** → [Download here](https://azure.microsoft.com/en-us/products/storage/storage-explorer#Download-4)  
  *(Useful for managing Azure Storage resources efficiently)*  
- 📊 **Power BI Desktop** → [Download here](https://powerbi.microsoft.com/en-us/downloads/)  
  *(Required for F02 Data Engineering challenge)*
- 🔧 **Git** → [Download here](https://git-scm.com/downloads)  
  *(For version control and repository management)*

---

## ✅ Azure Subscription & Access 

### 🔹 Subscription Requirements  
Participants must have access to an **Azure subscription** with the following:  

- **Shared Subscription or Resource Group** in your Company's Tenant (Dev, Test, SandBox): Ideally, your **team should leverage the same subscription or resource group** for seamless collaboration.  
- **RBAC Role**:  
  - At least **one team member** must have **Contributor + User Access Administrator** permissions.  
  - The rest of the team should have **Contributor access** to the subscription or a dedicated resource group.  
- **GitHub Account (Optional)**: Ideally, each participant should have a **GitHub account** for accessing repository resources and collaboration.  

### 🔹 Azure Setup Best Practices

**🏗️ Resource Organization:**
- **Keep all resources and Resource Groups in the same Region** for ease of understanding and standardization
- **Add tags to Resources and Resource Groups** when creating them for cost management and identification
- Most companies have organizational policies on auto-creation of Key Vault & Storage accounts, so **create all resources separately** and stitch them together

**📍 Recommended Regions:**
Ensure the location/region for each resource is preferably one of the following for smooth testing:
- **Australia East**
- **Canada East**  
- **East US**
- **East US 2**
- **France Central**
- **Japan East**
- **North Central US**
- **Sweden Central**
- **Switzerland North**

### 🔹 Azure Credit Considerations
- **Cost Optimization**: We'll provide guidance on managing costs and using free tiers where available
- **Resource Cleanup**: Instructions will be provided for cleaning up resources after the event

---

## ✅ Resource Provider Registration  

Ensure the following **resource providers** are registered within your Azure subscription:  

- `Microsoft.PolicyInsights`  
- `Microsoft.Cdn`  
- `Microsoft.StreamAnalytics`  
- `Microsoft.CognitiveServices`
- `Microsoft.Fabric`
- `Microsoft.MachineLearningServices`

📌 **How to register**:  

- Navigate to **Azure Portal** → **Subscription Settings** → **Resource Providers**  
- Select each provider and **click Register**  

**⚠️ Important**: Ensure that all necessary resource providers are registered. For example, you might need to register **Microsoft.PolicyInsights** and **Microsoft.Cdn** policies by selecting them and clicking the register button in the Azure Portal.  

---

## ✅ Identity & Authentication  

### 🔹 Service Principal & Authentication  
Each team must create a **Service Principal (App Registration in Entra ID)** with:  

- ✅ **Client ID & Secret** (expires no earlier than **one week after the event**)  
- ✅ **Participants must have their Client ID and Secret available during the hackathon.**  
- ✅ **Proper RBAC permissions** assigned to the Service Principal for resource access

### 🔹 Authentication Setup Steps
1. Navigate to **Azure Portal** → **Entra ID** → **App Registrations**
2. Click **New Registration** and provide a meaningful name
3. Generate a **Client Secret** under **Certificates & Secrets**
4. Assign **Contributor** role to the Service Principal at subscription/resource group level
5. **Document and securely store** the Application (Client) ID and Secret

---

## ✅ Microsoft Fabric Prerequisites  

### 🔹 Fabric Access  
Participants can either:  
- **Create a new Microsoft Fabric Free Trial** → [Sign up here](https://app.fabric.microsoft.com/)  
- **Leverage an existing Fabric Capacity provisioned in their Azure Subscription**.  

### 🔹 Fabric Setup Requirements  
Each team must have:  
- ✅ **At least one team member assigned as a Microsoft Fabric Administrator**.  
- ✅ **A Microsoft Fabric Workspace assigned to the team**.  
- ✅ **The ability to create Lakehouses & Semantic Models in Fabric**.  
- ✅ **Access to Fabric Storage OneLake for file uploads**.  

### 🔹 Fabric Capacity Planning (for Production Environments)
- **F32 minimum** for smooth performance during challenges
- **Region considerations**: Choose regions with Fabric availability
- **Cost management**: Understand Fabric pricing model and pause capabilities

---

## ✅ Azure OpenAI Requirements  

### 🔹 TPM Quota for OpenAI Models  
Check the **TPM quota** for your **Azure subscription** for the following **Large Language Models (LLMs)**:  

- `text-embedding-ada-002` → **Minimum 120k TPM**
- `gpt-35-turbo` → **Minimum 120k TPM**  
- `gpt-4o` → **Optional, minimum 30k TPM** (for advanced scenarios)

📌 **Critical Quota Management**: 

- **Check Current Quota**: If you are already familiar with Azure OpenAI, check your current quota for each model
- **Request Increase**: If the current quota is in the 2-digit range (10k–90k), request a quota addition to increase it to whatever is maximum for each model
- **Processing Time**: Quota increases typically take **24-48 hours for approval**, so it is **critical to complete this step in advance**

📌 **If the current quota is less than 120k**, request a **quota increase** before the event to ensure availability.  

- 🔹 **Check your current quota** → [Azure OpenAI Quota Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/quota?tabs=rest)  
- 🔹 **Request a quota increase** → [Request Quota Increase](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu)  

### 🔹 Supported Regions for OpenAI
Ensure your Azure subscription can deploy OpenAI resources in these regions:
- **Primary**: East US, East US 2, West Europe
- **Secondary**: Australia East, Canada East, Sweden Central
- **Avoid**: Regions with limited OpenAI model availability

---

## ✅ Network & Access Requirements  

### 🔹 Ensure **Unrestricted Access** to the Following Platforms:  

- 🌐 [**Azure AI Foundry**](https://ai.azure.com/)  
- 🏭 [**Azure Data Factory**](https://adf.azure.com/)  
- 📄 [**Document Intelligence Studio**](https://documentintelligence.ai.azure.com/)  
- ☁ [**Azure Portal**](https://portal.azure.com/)  
- 🔹 [**Microsoft Fabric**](https://app.fabric.microsoft.com/)  
- 📊 [**Power BI Service**](https://app.powerbi.com/)
- 🤖 [**OpenAI Playground**](https://oai.azure.com/) (through Azure OpenAI)

### 🔹 Corporate Network Considerations
- Ensure **WebSocket connections** are allowed (required for real-time AI features)
- Verify **HTTPS traffic** to *.azure.com, *.microsoft.com, *.fabric.microsoft.com domains
- Test **file upload capabilities** to Azure services
- Confirm **API access** for REST endpoints

---

## ✅ Visual Studio Code Requirements  

### 🔹 Required VS Code Extensions  
Teams must have **Visual Studio Code installed** with the following **extensions**:  

- 🐍 **Python** → Essential for AI challenge development
- 🔹 **Azure Tools** → For Azure resource management  
- 🧠 **Azure Machine Learning** → For AI model development
- 📊 **Jupyter** → For notebook-based data analysis
- 🔧 **GitHub Pull Requests and Issues** → For collaboration
- 📝 **Pylance** → Enhanced Python language support

### 🔹 Recommended VS Code Settings
```json
{
    "python.defaultInterpreterPath": "python",
    "jupyter.askForKernelRestart": false,
    "python.terminal.activateEnvironment": true
}
```

---

## ✅ Programming Environment Setup

### 🔹 Python Package Requirements
Pre-install these essential packages for Day 2 AI challenges:

```bash
# Core AI and Data packages
pip install openai==1.12.0
pip install langchain==0.1.13
pip install azure-ai-inference
pip install azure-search-documents
pip install azure-storage-blob
pip install pandas
pip install numpy
pip install jupyter

# Optional but recommended
pip install azure-cosmos
pip install azure-functions
pip install python-dotenv
pip install requests
```

### 🔹 Environment Configuration
- Create a **dedicated project folder** for hackathon work
- Set up **Python virtual environment** for package isolation
- Test **Azure CLI authentication**: `az login` and verify subscription access
- Verify **Python-Azure SDK connectivity** with a simple test script

---

## ✅ Data & File Requirements

### 🔹 Sample Data Access
- Ensure ability to **download ZIP files** from GitHub (corporate firewall consideration)
- Verify **file extraction capabilities** (7-Zip, WinRAR, or built-in OS tools)
- Test **large file upload** to Azure Blob Storage (sample datasets ~50-100MB)

### 🔹 File Format Support
- **CSV reading/writing** capabilities in Python/Excel
- **JSON processing** tools and libraries
- **PDF viewing** for documentation and reference materials
- **Image viewing** for architecture diagrams and screenshots

---

## 🎯 **What to Expect During the Event**  

### 🔹 Day 1: Microsoft Fabric Foundation
- 🏗️ **Infrastructure Setup** - Fabric capacity and OneLake configuration
- 🔄 **Data Engineering** - Medallion architecture implementation
- 📊 **Business Intelligence** - Power BI semantic model creation
- ⚙️ **Integration** - Preparing datasets for AI consumption

### 🔹 Day 2: AI Application Development  
- 🤖 **RAG ChatBot** - Conversational AI with custom data
- 🧠 **Intelligent Agents** - Database-connected AI systems
- 🚀 **Advanced Patterns** - Multi-agent and production deployment
- 🎯 **Integration** - Leveraging Day 1 data platform for AI

### 🔹 Learning Outcomes
- 🔥 **Hands-on technical challenges** with real-world applications
- 🤝 **Collaboration with like-minded professionals** in cross-functional teams
- 🧠 **Live problem-solving and expert guidance** from Microsoft experts
- 🚀 **Level up your skills** and brainstorm innovative use cases

---

## 🚀 **Final Checklist**  

### ✅ **Pre-Event Verification**
- [ ] **Azure subscription** with sufficient credits and permissions verified
- [ ] **Microsoft Fabric** workspace created and accessible
- [ ] **Azure OpenAI** quota confirmed (120k+ TPM for required models)
- [ ] **Development environment** set up with VS Code and extensions
- [ ] **Python environment** configured with required packages
- [ ] **Network access** confirmed to all required Azure services
- [ ] **Service Principal** created with proper RBAC permissions

### ✅ **Day-of-Event Preparation**  
- [ ] **Laptop charged** with power adapter available
- [ ] **Authentication credentials** (Service Principal details) securely stored
- [ ] **GitHub repository** bookmarked for quick access
- [ ] **Azure Portal** and **Microsoft Fabric** login tested
- [ ] **Team collaboration** tools agreed upon (Teams, Slack, etc.)

### ✅ **Backup Plans**
- [ ] **Alternative Azure subscription** available if needed
- [ ] **Mobile hotspot** or alternative internet access
- [ ] **Local Python environment** working offline for development
- [ ] **Downloaded sample datasets** available locally

---

## 🎉 **See You at the Hackathon!**  

We're looking forward to an **engaging and inspiring event**—and most importantly, an **enjoyable learning journey for everyone!**  

### 📞 **Need Help?**
- 📧 **Technical Questions**: Contact event organizers
- 🔧 **Azure Issues**: Use Azure Support portal
- 💬 **General Questions**: Event Slack/Teams channels
- 📖 **Documentation**: This repository contains comprehensive guides

### 🚀 **Success Tips**
- **Start early** with prerequisite setup - don't wait until the event day
- **Test everything** - verify your setup works end-to-end
- **Document issues** - note any problems for quick resolution during the event
- **Collaborate** - work with teammates on prerequisite completion
- **Stay curious** - come prepared with questions and use cases to explore

🚀 **Get ready to innovate, collaborate, and build AI-powered solutions with Microsoft Fabric!** 🎉