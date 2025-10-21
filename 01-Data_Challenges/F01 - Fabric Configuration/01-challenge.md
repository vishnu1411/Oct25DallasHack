# 🏆 Challenge 1: Setting Up Fabric 

## 📖 Scenario  
 This challenge focuses on **building the foundation** for data storage and access using **Microsoft Fabric**.  

Your goal is to set up the **necessary infrastructure** to support a scalable data pipeline.  The following is a simplied view of the architecture of this set of challanges.

![Architecture Overview](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Architecture/details.png)

> **Note:** If you **already completed the Fabric Capacity setup** as per the **prerequisites email**, you can **skip those steps** and proceed with the rest of the challenge.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Set up **Microsoft Fabric Capacity** *(skip if completed in prerequisites)*  
✅ Create a **OneLake Lakehouse** to store financial transactions  
✅ Download, unzip, and upload **financial data** to **OneLake**  
✅ Assign appropriate **permissions** in Fabric  
 



---

## 🚀 Step 1: Create Microsoft Fabric Capacity *(Skip if completed in prerequisites)*  
💡 **Why?** Microsoft Fabric provides the necessary **capacity to store and process large datasets**.  

### 1️⃣ Create Fabric Capacity in Azure  
🔹 Use the **Azure Portal** to create a **Fabric Capacity** resource.  

🔹 **Things to consider:**  
   - What **SKU** is required for this challenge?  
   - Should **security features** like Private Link be enabled?  

✅ **Best Practice**: Configure **RBAC (Role-Based Access Control)** to manage access.

#### ✅ Success Checkpoint
- Fabric Capacity resource appears in Azure Portal
- Status shows as "Succeeded"
- Capacity is available for workspace assignment

---

## 🚀 Step 2: Create a Fabric Workspace 
💡 **Why?** The Fabric workspace must be **assigned to a capacity** before you can use it.  



#### ✅ Success Checkpoint
- Workspace shows assigned capacity in admin settings
 

---

## 🚀 Step 3: Create a OneLake Lakehouse  
💡 **Why?** A **OneLake Lakehouse** is needed to store **financial transactions** before AI processing.  

### 1️⃣ Create a Fabric Lakehouse  
🔹 In **Microsoft Fabric**, create a **new Lakehouse** inside your workspace.  

🔹 **Hint:** What folder structure would be best for organizing financial data?  Remember we are building for a medallion architecture.

✅ **Best Practice**: Keep a **structured folder hierarchy** for better organization.  

#### ✅ Success Checkpoint
- Lakehouse appears in workspace with correct naming
- Folder structure is visible in Files explorer
- Proper permissions assigned (Workspace or object roles)
---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **data** to analyze.  

### 1️⃣ Download and Extract the Financial Data  
🔹 Download the **financial data ZIP file** from the following link:  
   🔗 [Financial Data.zip](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip)  

🔹 Extract the **ZIP file** on your local machine.  
🔹 Locate the extracted **Financial Data** folder containing the transaction JSON files.  

### 2️⃣ Upload Financial Data to OneLake  
🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.  
🔹 Click on **Files** (inside the Lakehouse).  
🔹 Click **Upload File** → Select the extracted Folder with the **JSON files**, and the file **tailwind_traders_retail_data.JSON**.  


#### ✅ Success Checkpoint
- Data accessible through Fabric SQL endpoint

---
### Step 5: Configure Security & Permissions 🔐

**Objective:** Establish proper access controls and security governance

#### 1️⃣ RBAC Configuration
1. Navigate to lakehouse **Manage Access**
2. Configure role assignments:

Admin, Member, Contributor, or Viewer as approriate

   🔗 [Security Roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)


#### 2️⃣ Data Access Validation
1. Test access with different user roles
2. Document access patterns for governance

#### ✅ Success Checkpoint
- Security roles properly assigned


## ✅ Success Criteria

### 🎯 Technical Validation

**Infrastructure Readiness:**
- [ ] Fabric Capacity provisioned and assigned (or free trial active)
- [ ] OneLake Lakehouse created with proper naming
- [ ] Organized folder structure implemented
- [ ] Security permissions configured correctly

**Data Pipeline Foundation:**
- [ ] Financial data successfully uploaded to Bronze layer
- [ ] File integrity validated (all JSON files present)

**Operational Readiness:**
- [ ] Workspace operational with assigned capacity
- [ ] Admin access configured for management tasks
- [ ] Documentation updated for team reference

### 🏆 Challenge Completion Indicators

✅ **Bronze Data Layer** populated with financial transaction JSON data  
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
2. **Explore data** - Use SQL endpoint to query uploaded JSONs
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
 
