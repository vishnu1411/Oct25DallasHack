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

**Pointers:**

*   Focus on the data coming from the uploaded JSON document first.
*   What information should be your fact?
*   How does the data that came from CosmosDB relate to this data?

**3\. Create a New Semantic Model**

**Challenge**: Create a new semantic model for the lakehouse. Include gold layer data.

**Expected Outcome**:

*   Semantic Model based on Gold layer data ready for reporting

**4\. Bonus Challenge - Create a New PowerBI Report**

**Objective**: Get creative. Explore the automatic and manual methods for generating reports on our new semantic model. Consider Copilot for enhancing the report with suggested visualizations and report summaries.

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