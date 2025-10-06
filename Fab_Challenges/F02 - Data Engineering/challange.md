# Azure Fabric Hackathon Challenge: Data Engineering - From JSON to Silver Staging Layer

Welcome to the Azure Fabric Hackathon! In this challenge, participants will work through the foundational steps of building a modern data platform using Microsoft Fabric. The goal is to transform a raw JSON file into a silver staging layer ready for dimensional modeling and reporting in the next challenge.


## 📖 Objective  

In this challenge, you will:  

✅ Use two JSON data sources for source data.  One uploaded directly to Fabric, and the other in a NoSQL instance.
✅ Set up an Upload JSON to Fabric
✅ Create a CosmosDB instance and upload JSON to COSMOSDB
✅ Move the data through a Medallion Data Architecture to a Silver staging layer for use in Challenge 3
✅ Assign permissions 
✅ Produce a CSV version of the JSON file for use with the AI workshop in day 2 


---

## 🗂️ Starting Dataset

The data for this excercise is available from the followling link.  (Financial Data.zip) https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip]

---

**🧩 Challenge Steps & Outcomes**
1. Upload the JSON to Fabric (Bronze Layer)
Challenge:
Ingest the raw JSON file into Microsoft Fabric

**Expected Outcome:**
•	JSON file stored in the Lakehouse Files section
•	Folder structure follows naming conventions (e.g., /bronze/retail_data/)


**Pointers**:
- Use **OneLake** for unified storage
- Validate schema and file integrity
- Consider using **Data Activator** for real-time alerts if applicable

---

### 2. Move the JSON Data to Silver Staging Layer

**Challenge**:  
Cleanse and enrich the data, then store it in the Silver layer as a structured format (e.g., Parquet or Delta).

**Considerations**:
- Does the data require validation? Nulls removed, formats standardized
- Stored in `/silver/` as Delta tables

**Pointers**:
- Use **Notebooks** or **Dataflows Gen2** for transformation
- Consider converting to **JSON** if required for downstream compatibility

---

### 3. Create a CosmosDB NoSQL instance

**Challenge**:  
Create a CosmosDB no SQL instance to be used for the second data source in this challenge.

**Expected Outcome**:
- CosmosDB create with NoSQL container

**Pointers**:
- Apply **role-based access control (RBAC)**


---

### 4. Upload the Sample JSON Data

**Challenge**:  
 Upload the sample data to finish creating the second data source for Fabric

**Expected Outcome**:
- JSON data uploaded successfully to the NoSQL database ready to be used as a Fabric datasource
- What is a logical partition ID?

---

### 5. Build the Data Integration from CosmosDB to Fabric

**Challenge**:  Using the newly uploaded data in CosmosDB, move this data to Fabric with the end goal of landing this data in a structured format in our silver layer.

**Expected Outcome**:
- Both JSON files will now be in Fabric in a silver layer and ready for transformation and modeling in the Gold layer.


---

### 6. Create a CSV file for Data Science

**Challenge:** Using a file from Fabric location, transform to a single JSON file containing one record for each row of the CSV. Store this file in the silver layer of the medallion architecture.



---

## 🔐 Security & Governance Considerations

- Enable **sensitivity labels** and **data loss prevention (DLP)** policies
- Use **Microsoft Purview** for data cataloging and compliance
- Audit access and transformations using Fabric’s built-in monitoring tools






## 🛠️ Technology Stack

- **Microsoft Fabric**: Lakehouse, Dataflows Gen2, Notebooks, Power BI
- **Storage Format**: CSV → Delta/Parquet → Semantic Model
- **Security**: Entra ID, RBAC, Purview
- **Optional Enhancements**: Data Activator, Power BI Copilot, Data Agents

---

## 🏁 Final Deliverable

A fully functional semantic model built from a raw CSV file, ready for reporting and insights. Participants should be able to explain each transformation step and justify their technology choices.

---

## 🏁 Final Challenge Checkpoints  
✅ Semantic model is available for use in PowerbI 
✅ JSON file is created and ready for use in AI tasks 



Once all steps are completed, you are ready to move on to **Challenge 3! 🚀**  

