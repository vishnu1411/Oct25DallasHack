# 🏆 Challenge 1: Setting Up Fabric 

## 📖 Scenario  
 This challenge focuses on **building the foundation** for data storage and access using **Microsoft Fabric**.  

Your goal is to set up the **necessary infrastructure** to support a scalable data pipeline.  

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

---

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric *(Skip if completed in prerequisites)*  
💡 **Why?** The Fabric workspace must be **assigned to a capacity** before you can use it.  

### 1️⃣ Assign Fabric Capacity  
🔹 In **Microsoft Fabric**, assign the **Fabric Capacity** to your workspace.  

🔹 **Hint:** Where in the Fabric UI can you manage capacity assignments?  

✅ **Outcome**: Your **Fabric workspace** should now be connected to a **Fabric Capacity**.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  
💡 **Why?** A **OneLake Lakehouse** is needed to store **financial transactions** before AI processing.  

### 1️⃣ Create a Fabric Lakehouse  
🔹 In **Microsoft Fabric**, create a **new Lakehouse** inside your workspace.  

🔹 **Hint:** What folder structure would be best for organizing financial CSVs?  

✅ **Best Practice**: Keep a **structured folder hierarchy** for better organization.  

---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **JSON** to analyze.  

### 1️⃣ Download and Extract the Financial Data  
🔹 Download the **financial data ZIP file** from the following link:  
   🔗 [Financial Data.zip](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip)  

🔹 Extract the **ZIP file** on your local machine.  
🔹 Locate the extracted **Financial Data** folder containing the transaction PDFs.  

### 2️⃣ Upload Financial Data to OneLake  
🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.  
🔹 Click on **Files** (inside the Lakehouse).  
🔹 Click **Upload Folder** → Select the extracted Folder with the **CSV files**.  


✅ **Outcome**: Your **financial data** is now **organized and available** in OneLake.  

---


## 🏁 Final Challenge Checkpoints  
✅ Is **Fabric Capacity** assigned correctly? *(Skip if already done in prerequisites)*  
✅ Do all **financial CSVs** appear in **OneLake** under **/Files/Bronze/**?  


Once all steps are completed, you are ready to move on to **Challenge 2! 🚀**  

---

## ❓ Troubleshooting Tips  
🔹 If you cannot **upload files to OneLake**, verify the assigned **capacity and workspace settings**.  
 
