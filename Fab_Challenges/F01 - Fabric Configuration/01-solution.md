# 📖 Solution to Challenge 1: Setting Up Fabric & Storage Solutions.

## 🔹 Objective  
In this challenge, you will:  

✅ Set up Microsoft Fabric Capacity  
✅ Create a OneLake Lakehouse to store transaction CSVs  
✅ Upload the CSVs to OneLake  
✅ Create & Configure a Service Principal for authentication  
✅ Assign permissions in Fabric & Azure Blob Storage  

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
   - **Security**: Enable **Private Link** (optional but recommended)  
5. Click **Review + Create**  
6. Wait for the deployment to complete.  

✅ **Best Practice**: Assign **Role-Based Access Control (RBAC)** to control access to the capacity.  

---

## 🚀 Step 2: Assign Fabric Capacity in Microsoft Fabric (skip if you already provisioned your Fabric Capacity or if you are using a free trial)  

### 1️⃣ Assign Fabric Capacity to Your Workspace  

1. Go to **Microsoft Fabric**  
2. Click **Admin Settings** (⚙️ gear icon) → **Fabric Capacity**  
3. Click **Assign Capacity**  
4. Select the Fabric Capacity you created (`YourFabricCapacity`)  
5. Click **Save**  

✅ **Outcome**: Your Fabric workspace is now connected to Microsoft Fabric Capacity.  

---

## 🚀 Step 3: Create a OneLake Lakehouse  

### 1️⃣ Create a new Fabric Workspace

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/cbc097fda45d32090f4d726b4fde8dc7ff3ba5ee/01-Data%20Ingestion/Reference%20Pictures/%7B57FFD2F6-A926-4079-A0A7-8CE696F2B0E5%7D.png)

1. In **Microsoft Fabric**, go to your **Workspace**  
2. Click **+ New item** → Select **Lakehouse**  

![alt text](https://github.com/DavidArayaS/AI-Powered-Insights-Fraud-Detection-Hackathon/blob/cbc097fda45d32090f4d726b4fde8dc7ff3ba5ee/01-Data%20Ingestion/Reference%20Pictures/%7B55843AA2-7852-48F4-9FF3-7A32BD832729%7D.png)

3. Fill in the details:  
   - **Name**: `YourLakehouse`  
   - **Description**: Storage for Financial CSVs  
   - Click **Create**  
   - **Security**: Assign **Admin & Reader** permissions  



✅ **Best Practice**: Keep a **structured folder hierarchy** in OneLake for organized data.  

---

## 🚀 Step 4: Download & Upload Financial Data to OneLake  
💡 **Why?** Your **AI models** need structured **financial CSVs** to analyze.  

### 1️⃣ Download and Extract the Financial Data  
🔹 Download the **financial data ZIP file** from the following link:  
   🔗 [Financial Data.zip](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip)  

🔹 Extract the **ZIP file** on your local machine.  


### 2️⃣ Upload Financial Data to OneLake  
🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.  
🔹 Click on **Files** (inside the Lakehouse).  
🔹 Click **Upload Folder** → Select the extracted Folder with the **CSV files**.  



✅ **Outcome**: Your **financial data** is now available to be uploaded to OneLake.  

---

