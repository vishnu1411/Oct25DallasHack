# 🏆 Challenge 1: Setting Up Fabric 

## 📖 Scenario  
 This challenge focuses on **building the foundation** for data storage and access using **Microsoft Fabric**.  

Your goal is to set up the **necessary infrastructure** to support a scalable data pipeline.  

![Architecture Overview](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Architecture/details.png)

> **Note:** If you **already completed the Fabric Capacity setup** as per the **prerequisites email**, you can **skip those steps** and proceed with the rest of the challenge.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Set up **Microsoft Fabric Capacity** *(skip if completed in prerequisites)*  
✅ Create a **OneLake Lakehouse** to store financial transactions  
✅ Use two JSON data sources for source data. One uploaded directly to Fabric, and the other in a NoSQL instance.   
✅ Download, unzip, and upload **financial data** to **OneLake**  
✅ Create a CosmosDB instance and **upload JSON to COSMOSDB**  
✅ Assign appropriate **permissions** in Fabric  
 

> **Reminder:** This challenge is about **building the data pipeline**. You will not process the documents yet.  
  

---

## 🚀 Step 1: Create Microsoft Fabric Capacity  

### 1️⃣ Create Fabric Capacity in Azure (skip if you already provisioned your Fabric Capacity or if you are using a free trial)

1. Go to **Azure Portal** → Microsoft Azure  
2. Search for **Microsoft Fabric** → Select **Fabric Capacity**  
3. Click **Create**  
4. Fill in the details:  
   - **Resource Group**: `YourUniqueResourceGroup`  
   - **Capacity Name**: `YourFabricCapacity`  
   - **SKU**: `F32` (minimum recommended)  
   - **Region**: Closest to your location  
5. Click **Review + Create**  
6. Wait for the deployment to complete.  

✅ **Best Practice**: Assign **Role-Based Access Control (RBAC)** to control access to the capacity.  

---

## 🚀 Step 2: Create a Fabric Workspace

### 1️⃣ Create a Fabric Workspace and assign it to the new capacity

1. Go to **Microsoft Fabric**  
2. Click **New Workspace**
3. Give the workapce a name
4. Scroll down and expand the **Advanced** options
5. From the license modes, select **Fabric Capacity**
6. Select the Fabric Capacity you created (`YourFabricCapacity`)  
7. Click **Save**  

✅ **Outcome**: Your Fabric workspace is now connected to Microsoft Fabric Capacity.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  

### 1️⃣ Create a new Fabric Lakehouse

1. In **Microsoft Fabric**, go to your **Workspace**  
2. Click **+ New item** → Select **Lakehouse**  
3. Fill in the details:  
   - **Name**: `YourLakehouse`  
   - **Location**:  Select the hackathon workspace
   - **Check** the box for Lakehouse Schemas
   - Click **Create**  
  

✅ **Best Practice**: Keep a **structured folder hierarchy** in OneLake for organized data.  

---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **financial CSVs** to analyze.  

### 1️⃣ Download and Extract the Financial Data  
🔹 Download the **financial data ZIP file** from the following link:  
   🔗 [Financial Data.zip](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip)  

🔹 Extract the **ZIP file** on your local machine.  This should contain two JSON files


### 2️⃣ Upload Financial Data to OneLake  

The goal here is to build the **Bronze** layer of the medallion architecture.  For this, create a bronze folder and load JSON data.  In future challanges folders and tables for silver and gold will be built.

🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.  
🔹 Click on **Files** (inside the Lakehouse).  
🔹 Click the **Ellipsis** behind the **Files** and select **New Subfolder**
🔹 Create a **Bronze** folder.
🔹 Right-click the new Bronze folder and select **Upload** and update the file **tailwind_traders_retail_data.json**



✅ **Outcome**: Your **financial data** is now available to be uploaded to OneLake.  

---
## 🚀Step 5: Create a CosmosDB NoSQL instance

**Challenge**: Create a Cosmos TB no SQL instance to be used for the second data source in this challenge.

**Setting up Cosmos DB**

1\. Create a new Cosmos DB for NoSQL account named “contoso-cosmos” in the same resource group and region as previous resources. (In Azure Portal: Create Cosmos DB -> NoSQL -> fill in RG and name.)

\- Sign in to the Azure Portal and click Create a resource. Search for "Azure Cosmos DB".

\- Choose the Azure Cosmos DB for NoSQL option.

\- Create a new account. Select your subscription and resource group, give the account a unique name (e.g., contoso-cosmos), and pick a region close to you.

\- For this challenge, the default settings are fine. Click Review + create, then Create.

2\. Database and Container: In the Cosmos DB account, under Data Explorer:

\- Once the Cosmos DB account is ready, go to it in the Azure Portal. In the left menu, find Data Explorer.

\- Select the New Database from the drop down menu right above \*\*Home\*\*. Name the database (for example, RetailData) and leave throughput as-is (we'll set it at the container level). Hit OK.

\- Select the new DB and right click on the DB and select \*\*+ New Container\*\*.

\- Select "Use existing" and select the DB which we created earlier

\- Set the Container id to something like Recommendations.

\- For Partition key, enter /ProductCategory . This means our data will be partitioned by the "ProductCategory" field in each document.

\- Click OK to create the container.

## 🚀Step 6: Upload the Sample JSON Data

**Challenge**: Upload the sample data to finish creating the second data source for Fabric

*   In the Azure Portal, navigate to your CosmosDB instance.
*   On the left menu select **Data Explorer**
*   From the **Data Explorer** window, expand your **Container** and **Database** and select **Items.**



*   From the top of the screen select **Upload Item**



*   Upload the file **tailwind_traders_challange2_data.json**

\*\*Note: If you receive any permission errors with the upload, you may need to adjust your user permissions using Azure CLI

*   *   Open the CLI from the upper right in the portal and run the following command
```
         az resource update --resource-group "yourresourcegroup" --name "yourcosmosdbname" --resource-type "Microsoft.DocumentDB/databaseAccounts" --set properties.disableLocalAuth=false --set properties.disableKeyBasedMetadataWriteAccess=false
```


---
### 🚀Step 7: Configure Security & Permissions 🔐

**Objective:** Establish proper access controls and security governance

#### 1️⃣ RBAC Configuration
1. Navigate to workspace **Manage Access**
2. Configure role assignments:

Admin, Member, Contributor, or Viewer as approriate

   🔗 [Security Roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)




## ✅ Success Criteria

### 🎯 Technical Validation

**Infrastructure Readiness:**
- [ ] Fabric Capacity provisioned and assigned (or free trial active)
- [ ] OneLake Lakehouse created with proper naming
- [ ] Organized folder structure implemented
- [ ] CosmosDB provisoned and data uploaded
- [ ] Security permissions configured correctly

**Data Pipeline Foundation:**
- [ ] Financial data successfully uploaded to Bronze layer
- [ ] File integrity validated (all CSV files present)

**Operational Readiness:**
- [ ] Workspace operational with assigned capacity
- [ ] Admin access configured for management tasks
- [ ] Documentation updated for team reference

### 🏆 Challenge Completion Indicators

✅ **Bronze Data Layer** populated with financial transaction JSON 
✅ **Security Governance** implemented with proper RBAC  
✅ **Architecture Foundation** ready for next challenge  

## 🆘 Troubleshooting

### Common Issues & Solutions

**🔴 Capacity Assignment Issues**
```
Problem: Cannot assign Fabric Capacity to workspace
Solution: 
- Verify sufficient Azure subscription quota
- Check RBAC permissions (Contributor required)
- Ensure capacity is in same region as workspace
```

**🔴 Data Upload Failures**
```
Problem: JSON files fail to upload to OneLake
Solution:
- Check file size limits (max 100MB per file)
- Verify network connectivity and bandwidth
- Use folder upload instead of individual files
- Clear browser cache and retry
```

**🔴 Permission Denied Errors**
```
Problem: Cannot access lakehouse or uploaded data
Solution:
- Verify workspace member permissions
- Check Fabric capacity assignment
- Validate Azure AD authentication
- Review lakehouse security settings
```

**🔴 Missing Data After Upload**
```
Problem: Files uploaded but not visible in lakehouse
Solution:
- Refresh lakehouse explorer view
- Check upload job status in notification center
- Verify correct target folder path
- Wait for metadata synchronization (5-10 minutes)
```

**🔴Unable to Connect to Spark Session**
```
Problem: Cannot connect a new notebook to a spark session with error to stop existing session or scale up the Fabric capacity
Solution: Try the following:
-	Open a new code cell in the notebook. Run the following command: 
# Stop the Spark session
spark.stop()
-	Try to connect the notebook to a New standard session
-	Once connected, click on Stop session button  
-	After session is stopped, connect to standard session again 
-	This will ensure spark context is also started and running in the background
```

**🔴Copilot Authoring Disabled**
```
Problem: If getting message "Copilot authoring is currently disabled."
Solution: To enable it, go to Power BI Settings and turn on Q&A for this semantic model” when creating report using Copilot (e.g. using prompt: Create a report using table gold*….), enable Q&A as follow:
-	Open your workspace 
-	Locate the semantic model you want to enable Copilot for from the list
-	Click on the three dots (More options) next to your semantic model and select Settings
-	Enable Q&A and Copilot: Toggle the switch to enable Q&A and Copilot for this semantic model.
-	Hit Apply
```


### 📞 Support Resources

**Microsoft Documentation:**
- [Fabric Capacity Management](https://learn.microsoft.com/en-us/fabric/admin/capacity-settings)
- [OneLake Overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)
- [Lakehouse Tutorial](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-introduction)

**Community Support:**
- Microsoft Fabric Community Forums
- Azure Support Portal (for capacity issues)
- Challenge documentation in repository

## 📚 Additional Resources

### 🎓 Learning Materials

**Microsoft Fabric Fundamentals:**
- [What is Microsoft Fabric?](https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview)
- [Fabric Workspace Management](https://learn.microsoft.com/en-us/fabric/admin/workspace-admin-settings)
- [OneLake Security Model](https://learn.microsoft.com/en-us/fabric/onelake/security-model)

**Best Practices:**
- [Data Organization in OneLake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-best-practices)
- [Fabric Capacity Planning](https://learn.microsoft.com/en-us/fabric/admin/capacity-planning)
- [Security and Governance](https://learn.microsoft.com/en-us/fabric/governance/governance-overview)

### 🔧 Development Tools

**Essential Browser Extensions:**
- Azure Account (for authentication)
- Developer Tools (for debugging upload issues)

**Helpful PowerShell Commands:**
```powershell
# Check Azure subscription
Get-AzContext

# List Fabric resources
Get-AzResource -ResourceType "Microsoft.Fabric/*"

# Monitor resource usage
Get-AzMetric -ResourceId <fabric-capacity-id>
```

### 🎯 Next Steps

**After Challenge Completion:**
1. **Review architecture** - Understand how components interact
2. **Explore data** - Use SQL endpoint to query uploaded JSON
3. **Plan Challenge 2** - Consider medallion architecture requirements
4. **Document learnings** - Note any customizations or challenges faced

**Advanced Extensions:**
- Enable **Data Activator** for real-time monitoring
- Configure **Power BI** workspace integration
- Set up **Microsoft Purview** for data cataloging
- Implement **sensitivity labels** for data classification

---

## 🎯 Ready for Challenge 2?

Once you've completed all success criteria, you're ready to proceed to **F02 - Data Engineering** challenge, where you'll:

- Transform raw JSON data through medallion architecture
- Configure a second data source
- Build dimensional models in the Silver layer
- Generate CSV outputs for AI/ML workflows

**Congratulations on completing the Fabric Configuration challenge! 🚀**

---

*Built with ❤️ for the Dallas MTC Fabric Hackathon - October 2025*
 
