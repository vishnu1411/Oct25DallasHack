**Azure Fabric Hackathon Challenge: Data Modeling and Reporting**

Welcome to the Azure Fabric Hackathon! In this challenge, participants will work through the final steps of creating an analytics solution using Microsoft Fabric. The goal is to take data in the silver staging layer and create dimensional modeling and reporting.

**📖 Objective**

In this challenge, you will:

✅ Use the Silver layer data to generate a Gold layer of data that has been cleansed and transformed.

✅ Build a Semantic model from the Gold data

✅ Create a PowerBI report from the Semantic model

**🧩 Challenge Steps & Outcomes**

**1\. Generate a Gold layer of the Data in a Dimensional Model**

**Challenge**:  
Take the silver layer staging data and develop a dimensional model. Transform the staging data into fact and dimension tables.

**Expected Outcome**:

*   Gold layer of structured data consisting of fact and dimension tables

\-----------------------------------------

One possible solution to this would be to build the following table structure.

GoldSalesFact – This table structure holds individual sales from the data

GoldCustomerDim – Customer information

GoldDateDim - Date dimension

GoldProductDim – Product details

GoldStoreDim – Store details

To build is structure out:

*   1.  Go to **Workspaces** and select the hackathon workspace.
    2.  In the upper left, select **New Item**
    3.  Select **Notebook**
    4.  Reference the sample code below, correcting for file and table locations.

The following script builds the tables and populates them with data from the staging table.

#Step-by-step PySpark ETL Notebook Code

import pyspark.sql.functions as F

\# 1. LOAD source data from stagingsales

sales\_df = spark.sql("SELECT \* FROM YourLakehouse.dbo.silverstagingsales")

\# 2. BUILD and SAVE Customer Dimension

customer\_dim = (

    sales\_df.select("CustomerID", "CustomerName", "EmailAddress", "LoyaltyTier")

    .dropDuplicates()

    .withColumn("CustomerKey", F.monotonically\_increasing\_id())

)

customer\_dim = customer\_dim.select(

    "CustomerKey", "CustomerID", "CustomerName", "EmailAddress", "LoyaltyTier"

)

customer\_dim.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.GoldCustomerDim")

\# 3. BUILD and SAVE Product Dimension

product\_dim = (

    sales\_df.select("ProductName", "ProductCategory")

    .dropDuplicates()

    .withColumn("ProductKey", F.monotonically\_increasing\_id())

)

product\_dim = product\_dim.select("ProductKey", "ProductName", "ProductCategory")

product\_dim.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.GoldProductDim")

\# 4. BUILD and SAVE Store Dimension

store\_dim = (

    sales\_df.select("StoreLocation")

    .dropDuplicates()

    .withColumn("StoreKey", F.monotonically\_increasing\_id())

)

store\_dim = store\_dim.select("StoreKey", "StoreLocation")

store\_dim.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.GoldStoreDim")

\# 5. BUILD and SAVE Date Dimension

date\_dim = (

    sales\_df.select(F.to\_date("PurchaseDate", "M/d/yyyy").alias("PurchaseDate"))

    .dropDuplicates()

    .withColumn("DateKey", F.monotonically\_increasing\_id())

)

date\_dim = date\_dim.select("DateKey", "PurchaseDate")

date\_dim.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.GoldDateDim")

\# 6. CREATE SALES FACT TABLE with keys

fact\_df = (

    sales\_df

    .join(customer\_dim, \["CustomerID", "CustomerName", "EmailAddress", "LoyaltyTier"\], "left")

    .join(product\_dim, \["ProductName", "ProductCategory"\], "left")

    .join(store\_dim, \["StoreLocation"\], "left")

    .join(date\_dim, F.to\_date(sales\_df.PurchaseDate, "M/d/yyyy") == date\_dim.PurchaseDate, "left")

    .select(

        "CustomerKey",

        "ProductKey",

        "StoreKey",

        "DateKey",

        "Quantity",

        "UnitPrice",

        "TotalAmount",

        "PaymentMethod"

    )

)

fact\_df.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.GoldSalesFact")

Additional consideration needs to be given to the additional sales data file. While this file does provide information on associated sales, it does not provide it in context of _specific sales_. So we do not have the additional data to join the information together.

The Product and ProductCategory columns do correspond to similar columns in the GoldProductDim table, however this will not relate directly back to the fact table. This will be accounted for in the semantic model.

Correct table and file names as needed.

import pyspark.sql.functions as F

sales\_df = spark.sql("SELECT \* FROM YourLakehouse.dbo.silverstagingadditional")

Productadditional\_dim = (

    sales\_df.select("ProductID", "Product", "ProductCategory", "Price", "Description", "AlsoBought1", "AlsoBought2", "AlsoBought3")

    .dropDuplicates()

)

Productadditional\_dim = Productadditional\_dim.select(

    "ProductID", "Product", "ProductCategory", "Price", "Description", "AlsoBought1", "AlsoBought2", "AlsoBought3"

)

Productadditional\_dim.write.mode("overwrite").option("overwriteSchema", "true").format("delta").saveAsTable("Yourlakehouse.dbo.goldprodadddim")

**3\. Create a New Semantic Model**

**Challenge**: Create a new semantic model for the lakehouse.

1\. To create a Power BI semantic model using Direct Lake mode, follow these steps:

1.  In the **Fabric portal**, create a new semantic model based on the desired item:
    *   Open the lakehouse and select **New Power BI semantic model** from the ribbon.
    *   Alternatively, open the relevant item, such as your warehouse or SQL analytics endpoint, select **New semantic model**.
2.  Enter a name for the new semantic model, select a workspace to save it in, and pick the tables to include. Then select **Confirm**.
3.  The new Power BI semantic model can be [edited in the workspace](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models), where you can add relationships, measures, rename tables and columns, choose how values are displayed in report visuals, and much more. If the model view does not show after creation, check the pop-up blocker of your browser.
4.  In this particular example, relationships will need to be added for the fact and dimension tables. Each dimension table has key that needs to correspond to a key in the fact table.

One method for creating these relationships is to highlight the table in the PowerBI relationship view, click on the table value, and drag this to the corresponding table and key that it relates to. A window will then open to provide relationship details. For these relationships, they will be many to one as the fact table may reference the dimensions many times.

[Edit semantic models in the Power BI service - Power BI | Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models)

1.  To edit the Power BI semantic model later, select **Open data model** from the semantic model context menu or item details page to edit the semantic model further.

**4\. Bonus Challenge - Create a New PowerBI Report**

Objective: Get creative. Explore the automatic and manual methods for generating reports on our new semantic model.

Power BI reports can be created in the workspace by selecting **New report** from web modeling, or in Power BI Desktop by live connecting to this new semantic model. To learn more on how to [connect to semantic models in the Power BI service from Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-report-lifecycle-datasets)

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

Multiple sources of data, brought together and prepared for both reporting and separating for AI/ML workloads. Data has moved through a medallion architecture resulting in a semantic model and PowerBI report. Participants should be able to explain each transformation step and justify their technology choices.

**🏁 Final Challenge Checkpoints**

✅ Gold dimensional model

✅ Semantic model ready for PowerBI modeling

Once all steps are completed, you are ready to move on to **Optional Challenge 4! 🚀**