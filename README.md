# 📊 Azure Databricks Multi-Workspace Monitoring Dashboard - Complete Package

## What's Included

This package contains a production-ready monitoring dashboard for Azure Databricks platform architects. The dashboard provides comprehensive visibility into jobs, pipelines, clusters, and costs across all Databricks workspaces using the System Catalog.

### Files in This Package

1. **Monitoring Dashboard.lvdash.json** (Main Dashboard)
   - Complete Lakeview dashboard with 9 datasets and 13+ widgets
   - 4 pages: Overview, Jobs, Pipelines, Clusters
   - Ready to import into any Azure Databricks workspace

2. **IMPORT_INSTRUCTIONS.md** (Start Here!)
   - Step-by-step import process
   - Prerequisites and permissions
   - Troubleshooting guide
   - Post-import configuration

3. **Dashboard_README.md** (User Guide)
   - Comprehensive documentation
   - Page-by-page breakdown
   - Widget descriptions
   - Customization options

4. **Query_Reference.md** (Technical Reference)
   - All 9 SQL queries with explanations
   - Common patterns and best practices
   - Performance optimization tips
   - Query modification examples

---

## Quick Start (3 Steps)

### 1️⃣ Verify Prerequisites
```sql
-- Run in Databricks SQL Warehouse:
SELECT COUNT(*) FROM system.lakeflow.jobs LIMIT 10;
```
✅ If this works, you're ready to proceed!  
❌ If it fails, System Tables need to be enabled (contact admin)

### 2️⃣ Import Dashboard
1. Open Azure Databricks → **Dashboards**
2. Click **Create** → **Import dashboard from file**
3. Select `Monitoring Dashboard.lvdash.json`
4. Choose a Pro/Serverless SQL Warehouse
5. Click **Refresh**

### 3️⃣ Start Monitoring
Navigate through the 4 pages to see:
- Real-time job execution status
- Cost trends and workspace spending
- Pipeline reliability metrics
- Active cluster inventory

---

## Dashboard Capabilities

### 🎯 What You Can Monitor

#### Jobs
- ✅ Run success/failure rates
- ✅ Most expensive jobs by cost
- ✅ Highest failure jobs by count
- ✅ Daily run status trends
- ✅ Workspace-level aggregations

#### Pipelines (Delta Live Tables)
- ✅ Pipeline update status over time
- ✅ Failed/canceled updates
- ✅ Pipeline reliability rankings

#### Clusters
- ✅ Complete active cluster inventory
- ✅ Node type and worker count
- ✅ Auto-termination settings
- ✅ DBR versions in use
- ✅ Owner/source tracking

#### Costs & Billing
- ✅ 30-day spend (jobs)
- ✅ Period-over-period growth
- ✅ Daily cost time series
- ✅ Cost by workspace
- ✅ Cost by product (jobs, SQL, notebooks, etc.)

### 🔍 Use Cases

**For Platform Architects:**
- Monitor platform health across all workspaces
- Identify reliability issues before users complain
- Track infrastructure usage patterns
- Enforce governance policies (autotermination, DBR versions)

**For FinOps Teams:**
- Track daily spending trends
- Identify cost optimization opportunities
- Allocate costs by workspace/team
- Budget forecasting with historical data

**For DevOps/SRE:**
- Alert on job/pipeline failures
- Monitor cluster sprawl
- Track deployment patterns
- Investigate incidents with historical data

**For Executive Reporting:**
- Platform adoption metrics
- Cost efficiency KPIs
- Reliability dashboards
- Cross-workspace comparisons

---

## Technical Highlights

### Multi-Workspace Architecture
- **Centralized monitoring**: One dashboard, all workspaces
- **System Catalog**: Leverages account-level system tables
- **No agents required**: Built-in Databricks telemetry
- **Real-time data**: Updates every 30-60 minutes automatically

### Data Sources
```
system.billing.*           → Cost and usage data
system.lakeflow.*         → Jobs and pipeline execution
system.compute.*          → Cluster configurations
```

### Query Optimization
- ✅ Window functions for latest records (ROW_NUMBER + QUALIFY)
- ✅ Efficient JOINs with list_prices for cost calculation
- ✅ 30-day lookback (configurable)
- ✅ GROUP BY ALL for cleaner syntax
- ✅ TRY_DIVIDE for safe calculations

### Visualization Features
- 📊 Counter widgets for KPIs
- 📈 Time series (line/bar charts)
- 📋 Sortable/searchable tables
- 🎨 Color-coded status indicators
- 🔢 Custom number formatting ($, %, dates)

---

## Dashboard Pages Overview

### Page 1: Overview 🏠
The executive summary page with:
- 3 KPI counters (30-day spend, 30-60 day spend, growth %)
- Daily job run status (stacked bar chart)
- Daily cost trends (line chart by workspace)
- Workspace summary table (jobs, runs, cost)

**Best for**: Morning standup, weekly reviews, executive reports

### Page 2: Jobs 💼
Detailed job performance analysis:
- Highest failure jobs table (sorted by failure count)
- Most expensive jobs table (sorted by cost)
- Top 10 failing jobs visualization (horizontal bar)

**Best for**: Reliability improvements, cost optimization, troubleshooting

### Page 3: Pipelines 🔄
Delta Live Tables monitoring:
- Daily pipeline update status (stacked bar)
- Top failing pipelines table

**Best for**: DLT pipeline developers, data engineers

### Page 4: Clusters 🖥️
Cluster governance and inventory:
- Complete active clusters table (11 columns)
- Sortable by workspace, owner, creation date, DBR version

**Best for**: Platform governance, cost control, compliance

---

## Requirements

### Minimum Requirements
- ✅ Azure Databricks account
- ✅ System Tables enabled
- ✅ Pro or Serverless SQL Warehouse
- ✅ SELECT permissions on system.* schemas

### Recommended Setup
- 🔹 Dedicated "Platform Monitoring" workspace
- 🔹 Hourly dashboard refresh schedule
- 🔹 Alerts on key metrics (failures, cost spikes)
- 🔹 Shared with platform team (CAN RUN access)

### Browser Support
- Chrome/Edge (recommended)
- Firefox
- Safari

---

## Customization Examples

### Filter to Specific Workspaces
```sql
WHERE workspace_id IN ('1234567890', '0987654321')
```

### Change Time Window to 7 Days
```sql
WHERE usage_date >= CURRENT_DATE() - INTERVAL 7 DAYS
```

### Add Cost Threshold Filter
```sql
HAVING list_cost > 100  -- Only show jobs costing > $100
```

### Group by Additional Dimensions
```sql
SELECT 
  workspace_id,
  owned_by,  -- Add owner dimension
  SUM(list_cost) as total_cost
FROM ...
GROUP BY workspace_id, owned_by
```

---

## Success Metrics

After deploying, measure:
- **MTTR**: Mean time to resolution for job failures
- **Cost efficiency**: $ per job run over time
- **Platform adoption**: # of jobs/workspaces growing
- **Reliability**: Job success rate trending up
- **Governance**: % clusters with proper autotermination

---

## Support and Next Steps

### Immediate Next Steps
1. ✅ Import dashboard (5 minutes)
2. ✅ Configure refresh schedule (2 minutes)
3. ✅ Share with team (1 minute)
4. ✅ Create 2-3 alerts (10 minutes)
5. ✅ Add to weekly review meeting agenda

### Ongoing Maintenance
- **Weekly**: Review failure trends, identify patterns
- **Monthly**: Analyze cost trends, optimize expensive jobs
- **Quarterly**: Update dashboard, add new metrics as needed

### Enhancement Ideas
- Add warehouse query performance metrics
- Include storage cost analysis
- Monitor Unity Catalog adoption
- Track user activity patterns
- Add predictive cost forecasting

### Get Help
- 📖 Read **IMPORT_INSTRUCTIONS.md** for detailed setup
- 📚 Review **Dashboard_README.md** for full documentation
- 🔧 Check **Query_Reference.md** for SQL query details
- 💬 Contact Databricks support for System Tables issues

---

## Version History

**Version 1.0** (March 2026)
- Initial release
- 4 pages, 9 datasets, 13+ widgets
- Support for jobs, pipelines, clusters, billing
- Multi-workspace monitoring
- 30-day default lookback

---

## License and Usage

This dashboard is provided as-is for use with Azure Databricks. Feel free to:
- ✅ Use in production environments
- ✅ Customize queries and visualizations
- ✅ Share within your organization
- ✅ Extend with additional pages/metrics

**Note**: Requires active Azure Databricks account and System Tables enabled.

---

## Quick Reference Card

| Feature | System Table | Key Metrics |
|---------|-------------|-------------|
| Job Runs | `system.lakeflow.job_run_timeline` | result_state, run_id, duration |
| Job Costs | `system.billing.usage` | usage_quantity, list_cost |
| Pipeline Updates | `system.lakeflow.pipeline_update_timeline` | update_state, duration |
| Clusters | `system.compute.clusters` | worker_count, node_type, owner |
| Billing | `system.billing.usage` + `list_prices` | daily cost, workspace spend |

---

## Feedback and Contributions

Have ideas for improvements? Consider adding:
- Warehouse performance metrics
- ML model training jobs
- Notebook execution tracking
- Unity Catalog governance
- User activity analytics

---

**🎉 You're ready to deploy! Start with IMPORT_INSTRUCTIONS.md**

For questions or issues, refer to the comprehensive documentation in the other `.md` files included in this package.
