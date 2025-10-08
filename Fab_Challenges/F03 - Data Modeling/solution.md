
# F03 - Azure Fabric Hackathon Challenge: Data Modeling and Reporting

Welcome to the Azure Fabric Hackathon! In this challenge, participants will work through the final steps of creating an analytics solution using Microsoft Fabric. The goal is to take data in the silver staging layer and create dimensional modeling and reporting.

- [🎯 Challenge Overview](#-challenge-overview)
- [🏆 Learning Objectives](#-learning-objectives)
- [🛠️ Prerequisites](#️-prerequisites)
- [📐 Architecture Overview](#-architecture-overview)
- [🚀 Challenge Steps](#-challenge-steps)
- [✅ Success Criteria](#-success-criteria)
- [🆘 Troubleshooting](#-troubleshooting)
- [📚 Additional Resources](#-additional-resources)

## 📖 Challenge Overview  

In this challenge, you will:

✅ Use the Silver layer data to generate a Gold layer of data that has been cleansed and transformed.
✅ Build a Semantic model from the Gold data
✅ Create a PowerBI report from the Semantic model

---

### ⏱️ Estimated Time
**2-3 hours** (depending on data complexity and modeling experience)

---

## 🏆 Learning Objectives

By completing this challenge, you will master:

✅ **Medallion Architecture** - Bronze, Silver, and Gold data layer implementation  
✅ **Data Transformation** - Cleansing, enrichment, and standardization techniques  
✅ **Dimensional Modeling** - Star schema design with facts and dimensions  
✅ **Semantic Layer** - Business-friendly models for analytics consumption  
✅ **Multi-Format Output** - CSV, Parquet, Delta, and JSON for different use cases  
✅ **Data Governance** - Security, quality, and lineage management  

---

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

---

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

---

Additional consideration needs to be given to the additional sales data file. While this file does provide information on associated sales, it does not provide it in context of _specific sales_. So we do not have the additional data to join the information together.

The Product and ProductCategory columns do correspond to similar columns in the GoldProductDim table, however this will not relate directly back to the fact table. This will be accounted for in the semantic model.

Correct table and file names as needed.

---

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

---

**3\. Create a New Semantic Model**

**Challenge**: Create a new semantic model for the lakehouse.

1\. To create a Power BI semantic model using Direct Lake mode, follow these steps:

1.  In the **Fabric portal**, create a new semantic model based on the desired item:
    *   Open the lakehouse and select **New Power BI semantic model** from the ribbon.
    *   Alternatively, open the relevant item, such as your warehouse or SQL analytics endpoint, select **New semantic model**.
2.  Enter a name for the new semantic model, select a workspace to save it in, and pick the tables to include. Then select **Confirm**.
3.  The new Power BI semantic model can be [edited in the workspace](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models), where you can add relationships, measures, rename tables and columns, choose how values are displayed in report visuals, and much more. If the model view does not show after creation, check the pop-up blocker of your browser.
4.  In this particular example, relationships will need to be added for the fact and dimension tables. Each dimension table has key that needs to correspond to a key in the fact table.

One method for creating these relationships is to highlight the table in the PowerBI relationship view, click on the table value, and drag this to the corresponding table and key that it relates to. A window will then open to provide relationship details. For these relationships, they will be many to one as the fact table may reference the dimensions many times.

[Edit semantic models in the Power BI service - Power BI | Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/service-edit-data-models)

1.  To edit the Power BI semantic model later, select **Open data model** from the semantic model context menu or item details page to edit the semantic model further.

---

**4\. Bonus Challenge - Create a New PowerBI Report**

Objective: Get creative. Explore the automatic and manual methods for generating reports on our new semantic model.

Power BI reports can be created in the workspace by selecting **New report** from web modeling, or in Power BI Desktop by live connecting to this new semantic model. To learn more on how to [connect to semantic models in the Power BI service from Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-report-lifecycle-datasets)

---

**🔐 Security & Governance Considerations**

*   Enable **sensitivity labels** and **data loss prevention (DLP)** policies
*   Use **Microsoft Purview** for data cataloging and compliance
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

Once all steps are completed, you are ready to move on to **Optional Challenge 4! 🚀**

## ✅ Success Criteria

### 🎯 Technical Implementation

**Medallion Architecture:**
- [ ] Bronze layer with raw CSV data ingestion
- [ ] Silver layer with cleansed Delta tables
- [ ] Gold layer with dimensional star schema
- [ ] JSON exports optimized for AI/ML consumption

**Data Quality & Governance:**
- [ ] Data validation rules implemented
- [ ] Quality metrics documented and monitored
- [ ] Security roles and permissions configured
- [ ] Data lineage tracked across all layers

**Business Intelligence Ready:**
- [ ] Power BI semantic model deployed
- [ ] Table relationships configured correctly
- [ ] Business measures and calculations defined
- [ ] Sample reports demonstrate analytical capabilities

### 🏆 Challenge Completion Indicators

✅ **Semantic Model** accessible and functional in Power BI  
✅ **JSON Dataset** available for AI Challenge consumption  
✅ **Data Pipeline** processes data with quality validation  
✅ **Documentation** completed for team handover  

---

Once all steps are completed, you are ready to move on to **Optional Challenge 4! 🚀**


---

## 🆘 Troubleshooting

### Common Issues & Solutions

**🔴 Delta Table Creation Failures**
```
Problem: Cannot create Delta tables in Silver/Gold layers
Solution: 
- Verify lakehouse permissions (Admin role required)
- Check available compute capacity
- Ensure proper Spark session configuration
- Validate folder path permissions in OneLake
```

**🔴 Power BI Connection Issues**
```
Problem: Cannot connect Power BI to Fabric SQL Endpoint
Solution:
- Verify SQL Analytics Endpoint is active
- Check authentication credentials
- Ensure workspace access permissions
- Try direct SQL endpoint URL connection
```

**🔴 JSON Export Problems**
```
Problem: JSON files not generated or corrupted
Solution:
- Use coalesce(1) to create single output file
- Verify output path permissions
- Check for special characters in data
- Monitor Spark job execution logs
```

**🔴 Dimensional Model Issues**
```
Problem: Fact table relationships not working correctly
Solution:
- Verify foreign key integrity
- Check dimension table unique keys
- Validate join conditions in transformation logic
- Test with small dataset first
```

### 📞 Support Resources

**Microsoft Documentation:**
- [Fabric Data Engineering](https://learn.microsoft.com/en-us/fabric/data-engineering/)
- [Delta Lake in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-lake-overview)
- [Power BI Semantic Models](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-understand)

**Best Practices:**
- [Medallion Architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)
- [Dimensional Modeling](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

## 📚 Additional Resources

### 🎓 Advanced Learning

**Data Engineering Patterns:**
- [Modern Data Warehouse Architecture](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/data/modern-data-warehouse)
- [Data Mesh Concepts](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/data-management/architectures/data-mesh)
- [Real-time Analytics](https://learn.microsoft.com/en-us/fabric/real-time-analytics/)

**Performance Optimization:**
- [Delta Lake Performance Tuning](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)
- [Power BI Model Optimization](https://learn.microsoft.com/en-us/power-bi/guidance/import-modeling-data-reduction)

### 🔧 Development Tools

**Notebook Templates:**
```python
# Template for data transformation notebook
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta import configure_spark_with_delta_pip

# Initialize Delta-enabled Spark session
spark = configure_spark_with_delta_pip(
    SparkSession.builder
    .appName("DataEngineering")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
).getOrCreate()
```

**SQL Templates:**
```sql
-- Template for dimension table creation
CREATE TABLE DimProduct (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY,
    product_id STRING NOT NULL,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) USING DELTA
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);
```

### 🎯 Next Steps

**Immediate Actions:**
1. **Test your semantic model** with various business scenarios
2. **Document data lineage** for governance and compliance
3. **Set up monitoring** for data pipeline health
4. **Prepare datasets** for Day 2 AI challenges

**Advanced Extensions:**
- **Real-time streaming** data integration
- **Machine learning** model training on Gold data
- **Advanced analytics** with Python/R in Fabric
- **Data mesh** pattern implementation

---

## 🎯 Ready for Day 2 AI Challenges?

Your data engineering pipeline now provides:

**For AI Challenge 01 (RAG ChatBot):**
- JSON datasets ready for vector embedding
- Clean, structured data for knowledge base
- Optimized format for Azure AI Search indexing

**For AI Challenge 02 (Intelligent Agent):**
- Dimensional model for recommendation algorithms
- Customer and product relationships established
- Real-time data access through SQL endpoints
