# Azure Fabric Hackathon Challenge: Data Engineering - From JSON to Silver Staging Layer

Welcome to the Azure Fabric Hackathon! In this challenge, participants will work through the foundational steps of building a modern data platform using Microsoft Fabric. The goal is to transform a raw JSON file into a silver staging layer ready for dimensional modeling and reporting in the next challenge.

## 📖 Objective

In this challenge, you will:

✅ Use two JSON data sources for source data. One uploaded directly to Fabric, and the other in a NoSQL instance.

✅ Set up an **Upload JSON to Fabric**

✅ Create a CosmosDB instance and **upload JSON to COSMOSDB**

✅ Move the data through a **Medallion Data Architecture** to a Silver staging layer for use in Challenge 3

✅ Assign **permissions** 

✅ **Produce a CSV version of the JSON file** for use with the AI workshop in day 2

##🗂️ Starting Dataset

The data for this excercise is available from the followling link. (Financial Data.zip) [https://github.com/vvenugopalan\_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip\]](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip%5D)

## 🧩 Challenge Steps & Outcomes

## 1\. Upload the JSON to Fabric (Bronze Layer)

**Challenge**:
Ingest the raw JSON file into Microsoft Fabric

**Expected Outcome**:

*   JSON file stored in the Lakehouse Files section
*   Folder structure follows naming conventions (e.g., /bronze/retail\_data/)

🔹 Open **Microsoft Fabric** → Navigate to **YourLakehouse**.
🔹 Click on **Files** (inside the Lakehouse).

🔹 Click on the ellipsis after **Files** and select **New subfolder** and create the folder **Bronze.**


🔹 Click  the ellipsis after the new **Bronze** subfolder and select upload files. Upload the file **tailwind**\_**traders\_retail\_data.json**.

## 2\. Move the JSON Data to Silver Staging Layer

**Challenge**:
Store the retail JSON data in the Silver layer as a structured format

**Considerations**:

*   Does the data require validation? Nulls removed, formats standardized
*   Stored in /silver/ as Delta tables

**Pointers**:

*   Use **Notebooks** or **Dataflows Gen2** for transformation

One possible method is to move this to a notebook to move this data. In this example the data is moved to a Delta table.

*   1.  Go to **Workspaces** and select the hackathon workspace.
    2.  In the upper left, select **New Item**
    3.  Select **Notebook**
    4.  Reference the sample code below.
    5.  Confirm that your File location for the json file is correct and also confirm the name of the silver layer staging table that you intend to use for your destination.

from pyspark.sql import SparkSession

import os

\# Initialize Spark session if not already available

spark = SparkSession.builder.getOrCreate()

\# Read JSON

df = spark.read.option("multiline", "true").json("Files/Bronze/tailwind\_traders\_retail\_data.json")

\# Write as Delta table (overwrite or 'append' as needed)

df.write.format("delta").mode("overwrite").saveAsTable("dbo.silverstaging")

## 3\. Create a CosmosDB NoSQL instance

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

\- For Partition key, enter /productID . This means our data will be partitioned by the "productID" field in each document.

\- Click OK to create the container.

## 4\. Upload the Sample JSON Data

**Challenge**: Upload the sample data to finish creating the second data source for Fabric

*   In the Azure Portal, navigate to your CosmosDB instance.
*   On the left menu select **Data Explorer**
*   From the **Data Explorer** window, expand your **Container** and **Database** and select **Items.**



*   From the top of the screen select **Upload Item**



*   Upload the file **tailwind\_traders\_challange2\_data.json**

\*\*Note: If you receive any permission errors with the upload, you may need to adjust your user permissions using Azure CLI

*   *   Open the CLI from the upper right in the portal and run the following command
        *   az resource update --resource-group "yourresourcegroup" --name "yourcosmosdbname" --resource-type "Microsoft.DocumentDB/databaseAccounts" --set properties.disableLocalAuth=false --set properties.disableKeyBasedMetadataWriteAccess=false

## 5\. Build the Data Integration from CosmosDB to Fabric**

**Challenge**: Using the newly uploaded data in CosmosDB, move this data to Fabric with the end goal of landing this data in a structured format in our silver layer.

**One possible method for this is using CosmosDB Mirroring, a shortcut and notebook**

Mirroring incrementally replicates Azure Cosmos DB data into Fabric OneLake in near real-time, without affecting the performance of transactional workloads or consuming Request Units (RUs).

1.  **Create the CosmosDB Mirror**

[Tutorial: Configure Microsoft Fabric Mirrored Databases From Azure Cosmos DB (Preview) - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/mirroring/azure-cosmos-db-tutorial)

\*\*Prerequisites:

1.  Networking must be set to Public Access – **All Networks**

![]()

1.  CosmosDB must be configured for continuous backup

[Provision an account with continuous backup and point in time restore in Azure Cosmos DB | Microsoft Learn](https://learn.microsoft.com/en-us/azure/cosmos-db/provision-account-continuous-backup#provision-portal)

**Create the Mirroring**

1.  Navigate to the [Fabric portal](https://fabric.microsoft.com/) home.
2.  Open an existing workspace or create a new workspace.
3.  In the navigation menu, select **Create**.
4.  Select **Create**, locate the **Data Warehouse** section, and then select **Mirrored Azure Cosmos DB (Preview)**.
5.  Provide a name for the mirrored database and then select **Create**.
6.  In the **New connection** section, select **Azure Cosmos DB for NoSQL**.
7.  Provide the Azure Cosmos DB Endpoint, the connection name, authentication method, account key, or alternatively, the organizational account. These can all be found on the **Keys** setting on the CosmosDB resource in the Azure portal.
8.  Select **Connect, then the database to mirror.**
9.  Select **Mirror Database**. The mirroring process now begins.
10.  In your lakehouse you will see two new items created, a Mirrored Database, and a corresponding SQL endpoint.
11.  **Create a Shortcut to the SQL Endpoint**

Next, use Lakehouse to extend the number of tools you can use to analyze your Cosmos DB data. In this step, create a lakehouse and connect it to your mirrored data.

1.  Navigate back to your lakehouse.
2.  Select the **Get data** option, and then select **New shortcut**.
3.  Follow the sequential instructions in the various **New shortcut** dialogs to select your existing mirrored Cosmos DB database, and then select your target table.
4.  **Move the Mirrored Data to a Silver Staging Table**

One method for doing this is with a notebook.

*   1.  Go to **Workspaces** and select the hackathon workspace.
    2.  In the upper left, select **New Item**
    3.  Select **Notebook**
    4.  Reference the sample code below. Correct the mirrored database and table names to your environment

#Read data from shortcut

df = spark.sql("SELECT \* FROM YourLakehouse. MirroredDatabaseName.TableName")

display(df)

#Write data to Silver staging table

df.write.format("delta").mode("overwrite").saveAsTable("dbo.SilverStagingAdditional")

**6\. Create a CSV file for Data Science**

**Challenge**: Using a file from Fabric location, transform to a single JSON file containing one record for each row of the CSV. Store this file in the silver layer of the medallion architecture.

Once again, a possible method for this is using a notebook.

*   1.  Go to **Workspaces** and select the hackathon workspace.
    2.  In the upper left, select **New Item**
    3.  Select **Notebook**
    4.  **The following code is an example of how this movement can be done. Please correct file paths and file names as needed.**

\# Step 1: Use Spark to read the JSON from Lakehouse mount

json\_path = "abfss://HackathonBeta@onelake.dfs.fabric.microsoft.com/YourLakehouse.Lakehouse/Files/Bronze/tailwind\_traders\_retail\_data.json"

df\_spark = spark.read.option("multiline", "true").json(json\_path)

\# Step 2: Convert Spark DataFrame to Pandas DataFrame

df\_pd = df\_spark.toPandas()

\# Step 3: Save as CSV using Pandas to a path in the Lakehouse (Fabric filesystem)

csv\_path = "abfss://HackathonBeta@onelake.dfs.fabric.microsoft.com/YourLakehouse.Lakehouse/Files/Silver/tailwind\_traders\_retail\_data.csv"

df\_pd.to\_csv(csv\_path, index=False)

**🔐 Security & Governance Considerations**

*   Enable **sensitivity labels** and **data loss prevention (DLP)** policies
*   Use **Microsoft Purview** for data cataloging and compliance
*   Audit access and transformations using Fabric’s built-in monitoring tools

**🛠️ Technology Stack**

*   **Microsoft Fabric**: Lakehouse, Dataflows Gen2, Notebooks, Power BI
*   **Storage Format**: CSV → Delta/Parquet → Semantic Model
*   **Security**: Entra ID, RBAC, Purview
*   **Optional Enhancements**: Data Activator, Power BI Copilot, Data Agents

**🏁 Final Deliverable**

A staged, silver relational model, ready for dimensional modeling and reporting. Participants should be able to explain each transformation step and justify their technology choices.

**🏁 Final Challenge Checkpoints**

✅ Silver stage data ready for gold modelling ✅ CSV file is created and ready for use in AI tasks

Once all steps are completed, you are ready to move on to **Challenge 3! 🚀**
