# 🏆 Challenge 1: Setting Up Fabric 

## 📖 Scenario  
 This challenge focuses on **building the foundation** for data storage and access using **Microsoft Fabric**.  

Your goal is to set up the **necessary infrastructure** to support a scalable data pipeline.  The following is a simplied view of the architecture of this set of challanges.

![Architecture Overview](Architecture/details.png)

> **Note:** If you **already completed the Fabric Capacity setup** as per the **prerequisites email**, you can **skip those steps** and proceed with the rest of the challenge.  

---

## 🎯 Your Mission  
By completing this challenge, you will:  

✅ Set up **Microsoft Fabric Capacity** *(skip if completed in prerequisites)*  
✅ Create a **OneLake Lakehouse** to store financial transactions  
✅ Download, unzip, and upload **financial data** to **OneLake**  
✅ Assign appropriate **permissions** in Fabric  
 

> **Reminder:** This challenge is about **building the data pipeline**. You will not process the documents yet.  

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

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric *(Skip if completed in prerequisites)*  
💡 **Why?** The Fabric workspace must be **assigned to a capacity** before you can use it.  

### 1️⃣ Assign Fabric Capacity  
🔹 In **Microsoft Fabric**, assign the **Fabric Capacity** to your workspace.  

🔹 **Hint:** Where in the Fabric UI can you manage capacity assignments?  

#### ✅ Success Checkpoint
- Workspace shows assigned capacity in admin settings
- Capacity utilization metrics appear in monitoring  

---

## 🚀 Step 3: Create a OneLake Lakehouse  
💡 **Why?** A **OneLake Lakehouse** is needed to store **financial transactions** before AI processing.  

### 1️⃣ Create a Fabric Lakehouse  
🔹 In **Microsoft Fabric**, create a **new Lakehouse** inside your workspace.  

🔹 **Hint:** What folder structure would be best for organizing financial data?  

✅ **Best Practice**: Keep a **structured folder hierarchy** for better organization.  

#### ✅ Success Checkpoint
- Lakehouse appears in workspace with correct naming
- Folder structure is visible in Files explorer
- Proper permissions assigned (Admin/Reader roles)
---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **JSON** to analyze.  

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
- File integrity maintained (size/format checks pass)
- Data accessible through Fabric SQL endpoint

---
### Step 5: Configure Security & Permissions 🔐

**Objective:** Establish proper access controls and security governance

#### 1️⃣ RBAC Configuration
1. Navigate to lakehouse **Settings** → **Security**
2. Configure role assignments:
   ```
   Admin Role: Your account + project team leads
   Reader Role: Data analysts and consumers
   Contributor Role: Data engineers and developers
   ```

#### 2️⃣ Data Access Validation
1. Test read access with different user roles
2. Verify proper permission inheritance
3. Document access patterns for governance

#### ✅ Success Checkpoint
- Security roles properly assigned
- Access controls verified through testing
- Audit logging enabled for compliance


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
- [ ] Data accessible through Fabric SQL endpoints
- [ ] Proper data governance structure established

**Operational Readiness:**
- [ ] Workspace operational with assigned capacity
- [ ] Admin access configured for management tasks
- [ ] Monitoring and alerting capabilities available
- [ ] Documentation updated for team reference

### 🏆 Challenge Completion Indicators

✅ **Bronze Data Layer** populated with financial transaction JSON data  
✅ **Lakehouse SQL Endpoint** providing data access  
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
 
