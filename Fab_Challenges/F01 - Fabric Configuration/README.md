# 🏗️ F01 - Fabric Configuration Challenge

**Setting up Microsoft Fabric Foundation for Data Platform**

Welcome to the first Fabric challenge! This foundational challenge focuses on establishing the core infrastructure needed for modern data platform operations using Microsoft Fabric.

## 📋 Table of Contents

- [🎯 Challenge Overview](#-challenge-overview)
- [🏆 Learning Objectives](#-learning-objectives)
- [🛠️ Prerequisites](#️-prerequisites)
- [📐 Architecture Overview](#-architecture-overview)
- [🚀 Challenge Steps](#-challenge-steps)
- [✅ Success Criteria](#-success-criteria)
- [🆘 Troubleshooting](#-troubleshooting)
- [📚 Additional Resources](#-additional-resources)

## 🎯 Challenge Overview

This challenge establishes the **foundational infrastructure** for a scalable data pipeline using Microsoft Fabric. You'll set up the essential components needed to support enterprise-grade data storage, processing, and governance.

### 🎯 What You'll Build
- Microsoft Fabric Capacity for computational resources
- OneLake Lakehouse for unified data storage
- Proper security configurations with RBAC
- Data ingestion pipeline for financial datasets

### ⏱️ Estimated Time
**1-2 hours** (depending on prior Fabric experience)

## 🏆 Learning Objectives

By completing this challenge, you will understand:

✅ **Fabric Capacity Management** - How to provision and configure compute resources  
✅ **OneLake Architecture** - Unified data lake concepts and best practices  
✅ **Data Organization** - Implementing folder structures for data governance  
✅ **Security Configuration** - Setting up RBAC and access controls  
✅ **Data Ingestion** - Loading structured data into Fabric ecosystem  

## 🛠️ Prerequisites

### Azure Requirements
- **Azure Subscription** with Contributor or Owner permissions
- **Sufficient quota** for Fabric Capacity (F32 minimum recommended)
- **Resource provider registration** for Microsoft.Fabric

### Knowledge Prerequisites
- Basic understanding of Azure services
- Familiarity with data lake concepts
- Understanding of CSV/structured data formats

### Optional (Skip if completed in prerequisites)
- Pre-provisioned Fabric Capacity from hackathon setup email

## 📐 Architecture Overview

### 🏗️ Fabric Configuration Architecture

```mermaid
graph TB
    subgraph "Azure Subscription"
        subgraph "Azure Portal"
            AzPortal[Azure Portal<br/>Resource Management]
            FabCapacity[Fabric Capacity<br/>F32 SKU<br/>Compute Resources]
        end
        
        subgraph "Security & Identity"
            AAD[Azure Active Directory<br/>Identity Provider]
            RBAC[Role-Based Access Control<br/>Permissions Management]
            SP[Service Principal<br/>Authentication]
        end
    end
    
    subgraph "Microsoft Fabric Platform"
        subgraph "Fabric Workspace"
            Workspace[Fabric Workspace<br/>Project Container]
            Admin[Admin Settings<br/>Capacity Assignment]
        end
        
        subgraph "OneLake Storage"
            Lakehouse[Lakehouse<br/>Unified Data Storage]
            
            subgraph "Folder Structure"
                Files[/Files/<br/>Raw Data Storage]
                Bronze[/Bronze/<br/>Ingested Data]
                Metadata[Metadata & Schema<br/>Data Catalog]
            end
        end
    end
    
    subgraph "Data Sources"
        LocalData[Local Machine<br/>Financial Data ZIP]
        CSVFiles[CSV Files<br/>Transaction Data]
    end
    
    subgraph "Data Flow"
        Upload[Data Upload<br/>Folder Upload]
        Validation[Data Validation<br/>Schema Check]
        Organization[Data Organization<br/>Structured Storage]
    end

    %% Relationships
    AzPortal --> FabCapacity
    AAD --> RBAC
    RBAC --> SP
    FabCapacity --> Workspace
    Admin --> FabCapacity
    Workspace --> Lakehouse
    Lakehouse --> Files
    Files --> Bronze
    
    %% Data Flow
    LocalData --> CSVFiles
    CSVFiles --> Upload
    Upload --> Files
    Files --> Validation
    Validation --> Organization
    Organization --> Bronze
    
    %% Security Flow
    SP --> Lakehouse
    RBAC --> Files
    
    style FabCapacity fill:#e3f2fd
    style Lakehouse fill:#e8f5e8
    style Files fill:#fff3e0
    style Bronze fill:#f3e5f5
    style CSVFiles fill:#ffebee
```

### 🔄 Architecture Components

**Azure Layer:**
- **Fabric Capacity**: Dedicated compute resources for Fabric workloads
- **RBAC**: Role-based security for resource access
- **Azure AD**: Identity and authentication management

**Fabric Layer:**
- **Workspace**: Logical container for Fabric resources
- **OneLake**: Unified data lake storage with automatic replication
- **Lakehouse**: Data storage combining data lake and data warehouse features

**Data Organization:**
- **Bronze Layer**: Raw data ingestion point
- **File Management**: Structured folder hierarchy
- **Metadata**: Automatic schema detection and cataloging

## 🚀 Challenge Steps

### Step 1: Create Microsoft Fabric Capacity ⚡

> **Note:** Skip this step if you completed Fabric Capacity setup in prerequisites email

**Objective:** Provision dedicated compute resources for Fabric workloads

#### 1️⃣ Azure Portal Configuration
1. Navigate to **Azure Portal** → Search "Microsoft Fabric"
2. Select **Fabric Capacity** → Click **Create**
3. Configure resource details:
   ```
   Resource Group: YourUniqueResourceGroup
   Capacity Name: YourFabricCapacity  
   SKU: F32 (minimum recommended)
   Region: Choose closest to your location
   Security: Enable Private Link (optional)
   ```
4. Review settings → **Create**
5. Wait for deployment completion

#### ✅ Success Checkpoint
- Fabric Capacity resource appears in Azure Portal
- Status shows as "Succeeded"
- Capacity is available for workspace assignment

---

### Step 2: Assign Fabric Capacity ⚙️

> **Note:** Skip this step if using Fabric free trial

**Objective:** Connect your workspace to provisioned compute capacity

#### 1️⃣ Workspace Capacity Assignment
1. Open **Microsoft Fabric** portal
2. Navigate to **Admin Settings** (⚙️ gear icon)
3. Select **Fabric Capacity** 
4. Click **Assign Capacity**
5. Choose your created capacity (`YourFabricCapacity`)
6. Apply to your workspace → **Save**

#### ✅ Success Checkpoint
- Workspace shows assigned capacity in admin settings
- Capacity utilization metrics appear in monitoring

---

### Step 3: Create OneLake Lakehouse 🏗️

**Objective:** Establish unified data storage for financial transaction data

#### 1️⃣ Lakehouse Creation
1. In **Microsoft Fabric** → Navigate to your **Workspace**
2. Click **+ New Item** → Select **Lakehouse**
3. Configure lakehouse:
   ```
   Name: FinancialDataLakehouse
   Description: Storage for Financial Transaction CSVs
   ```
4. Click **Create**

#### 2️⃣ Folder Structure Setup
1. Access your new lakehouse
2. Navigate to **Files** section
3. Create organized folder structure:
   ```
   /Files/
   ├── Bronze/
   │   └── FinancialData/
   ├── Raw/
   │   └── Uploads/
   └── Archive/
   ```

#### ✅ Success Checkpoint
- Lakehouse appears in workspace with correct naming
- Folder structure is visible in Files explorer
- Proper permissions assigned (Admin/Reader roles)

---

### Step 4: Download & Upload Financial Data 📊

**Objective:** Ingest financial transaction data into OneLake storage

#### 1️⃣ Data Acquisition
1. Download financial data from repository:
   🔗 [Financial Data.zip](https://github.com/vvenugopalan_microsoft/HackathonOct25/blob/main/Data/financial%20data.zip)
2. Extract ZIP file to local machine
3. Locate extracted folder containing CSV transaction files
4. Verify data format and file count

#### 2️⃣ Data Upload Process
1. Return to **Microsoft Fabric** → **FinancialDataLakehouse**
2. Navigate to **Files** → **Bronze/FinancialData/**
3. Click **Upload** → **Upload Folder**
4. Select extracted financial data folder
5. Monitor upload progress and verify completion

#### 3️⃣ Data Validation
1. Confirm all CSV files uploaded successfully
2. Check file sizes match source data
3. Verify folder structure maintained:
   ```
   /Files/Bronze/FinancialData/
   ├── transactions_2023.csv
   ├── transactions_2024.csv
   └── account_data.csv
   ```

#### ✅ Success Checkpoint
- All financial CSV files visible in OneLake
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
- [ ] File integrity validated (all CSV files present)
- [ ] Data accessible through Fabric SQL endpoints
- [ ] Proper data governance structure established

**Operational Readiness:**
- [ ] Workspace operational with assigned capacity
- [ ] Admin access configured for management tasks
- [ ] Monitoring and alerting capabilities available
- [ ] Documentation updated for team reference

### 🏆 Challenge Completion Indicators

✅ **Bronze Data Layer** populated with financial transaction CSVs  
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
Problem: CSV files fail to upload to OneLake
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
2. **Explore data** - Use SQL endpoint to query uploaded CSVs
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

- Transform raw CSV data through medallion architecture
- Build dimensional models in the Gold layer
- Create semantic models for business intelligence
- Generate JSON outputs for AI/ML workflows

**Congratulations on completing the Fabric Configuration challenge! 🚀**

---

*Built with ❤️ for the Dallas MTC Fabric Hackathon - October 2025*