# Azure Databricks Multi-Workspace Monitoring Dashboard# 📊 Azure Databricks Multi-Workspace Monitoring Dashboard - Complete Package



A comprehensive Lakeview dashboard for monitoring jobs, pipelines, clusters, and costs across all Azure Databricks workspaces.## What's Included



---This package contains a production-ready monitoring dashboard for Azure Databricks platform architects. The dashboard provides comprehensive visibility into jobs, pipelines, clusters, and costs across all Databricks workspaces using the System Catalog.



## 📊 Dashboard Overview### Files in This Package



### Purpose1. **Monitoring Dashboard.lvdash.json** (Main Dashboard)

Monitor and optimize Azure Databricks resources across multiple workspaces with real-time insights into:   - Complete Lakeview dashboard with 9 datasets and 13+ widgets

- Job execution performance and failures   - 4 pages: Overview, Jobs, Pipelines, Clusters

- Pipeline updates and error rates   - Ready to import into any Azure Databricks workspace

- Active cluster inventory

- Cost analysis with 27% discount applied (0.73 multiplier)2. **IMPORT_INSTRUCTIONS.md** (Start Here!)

   - Step-by-step import process

### Pages   - Prerequisites and permissions

1. **Overview** - High-level metrics and trends   - Troubleshooting guide

2. **Jobs** - Job performance, failures, and cost analysis   - Post-import configuration

3. **Pipelines** - Pipeline status and failure tracking

4. **Clusters** - Active cluster inventory3. **Dashboard_README.md** (User Guide)

   - Comprehensive documentation

---   - Page-by-page breakdown

   - Widget descriptions

## 🗄️ Data Sources   - Customization options



### System Tables Used4. **Query_Reference.md** (Technical Reference)

- `system.billing.usage` - Usage data for cost calculation   - All 9 SQL queries with explanations

- `system.billing.list_prices` - Pricing information   - Common patterns and best practices

- `system.lakeflow.job_run_timeline` - Job execution history   - Performance optimization tips

- `system.lakeflow.pipeline_update_timeline` - Pipeline updates   - Query modification examples

- `system.lakeflow.pipelines` - Pipeline metadata

- `system.compute.clusters` - Cluster configurations---

- `system.access.workspaces_latest` - Workspace information

## Quick Start (3 Steps)

### Time Ranges

- Jobs: Last 30 days### 1️⃣ Verify Prerequisites

- Pipelines: Last 30 days```sql

- Clusters: Currently active (delete_time IS NULL)-- Run in Databricks SQL Warehouse:

- Billing: Last 30-60 daysSELECT COUNT(*) FROM system.lakeflow.jobs LIMIT 10;

```

---✅ If this works, you're ready to proceed!  

❌ If it fails, System Tables need to be enabled (contact admin)

## 📈 Key Reports

### 2️⃣ Import Dashboard

### Overview Page1. Open Azure Databricks → **Dashboards**

- **Job Run Success Rate** - Success vs failure percentage2. Click **Create** → **Import dashboard from file**

- **Pipeline Update Status** - Update type distribution3. Select `Monitoring Dashboard.lvdash.json`

- **Daily Job Costs** - Time series of job execution costs4. Choose a Pro/Serverless SQL Warehouse

5. Click **Refresh**

### Jobs Page

- **Jobs with Highest Failure Rate** - Top 10 failing jobs### 3️⃣ Start Monitoring

- **Long Running Jobs** - Jobs with high P95 durationNavigate through the 4 pages to see:

- **Most Expensive Jobs Last 30 Days** - Cost leaders- Real-time job execution status

- Cost trends and workspace spending

### Pipelines Page- Pipeline reliability metrics

- **Pipeline Update Status Over Time** - Daily trend by update type- Active cluster inventory

- **Pipeline Failures Last 30 Days** - Failed pipeline details

---

### Clusters Page

- **Active Clusters Across All Workspaces** - Current cluster inventory (deduplicated by latest configuration)## Dashboard Capabilities



---### 🎯 What You Can Monitor



## 🚀 Installation#### Jobs

- ✅ Run success/failure rates

### Prerequisites- ✅ Most expensive jobs by cost

- Azure Databricks workspace with Unity Catalog enabled- ✅ Highest failure jobs by count

- System tables accessible- ✅ Daily run status trends

- Permissions to query `system.*` schema- ✅ Workspace-level aggregations



### Import Steps#### Pipelines (Delta Live Tables)

1. Open Azure Databricks workspace- ✅ Pipeline update status over time

2. Go to **Dashboards** section- ✅ Failed/canceled updates

3. Click **Import**- ✅ Pipeline reliability rankings

4. Upload `Monitoring Dashboard.lvdash.json`

5. Select a SQL Warehouse#### Clusters

6. Click **Refresh** to load data- ✅ Complete active cluster inventory

- ✅ Node type and worker count

---- ✅ Auto-termination settings

- ✅ DBR versions in use

## 🔧 Key Technical Details- ✅ Owner/source tracking



### P95 Duration Explained#### Costs & Billing

- **P95 (95th percentile)**: 95% of runs complete within this time- ✅ 30-day spend (jobs)

- More reliable than average (ignores rare outliers)- ✅ Period-over-period growth

- Used for SLA planning and performance monitoring- ✅ Daily cost time series

- Example: P95 = 45 min means 95% of runs finish in ≤45 minutes- ✅ Cost by workspace

- ✅ Cost by product (jobs, SQL, notebooks, etc.)

### Pricing Formula

All cost calculations use:### 🔍 Use Cases

```sql

list_prices.pricing.default * 0.73**For Platform Architects:**

```- Monitor platform health across all workspaces

- Applies **27% enterprise discount**- Identify reliability issues before users complain

- Consistent across all cost reports- Track infrastructure usage patterns

- Update multiplier if your discount differs- Enforce governance policies (autotermination, DBR versions)



### Cluster Deduplication**For FinOps Teams:**

`system.compute.clusters` tracks configuration changes over time, creating multiple rows per cluster. The query deduplicates using:- Track daily spending trends

```sql- Identify cost optimization opportunities

ROW_NUMBER() OVER (PARTITION BY cluster_id ORDER BY change_time DESC)- Allocate costs by workspace/team

WHERE rn = 1  -- Keep only latest configuration- Budget forecasting with historical data

```

**For DevOps/SRE:**

### Pipeline Column Names- Alert on job/pipeline failures

**Important**: Use correct column names from `system.lakeflow.pipeline_update_timeline`:- Monitor cluster sprawl

- ✅ Use `period_start_time` (NOT update_start_time)- Track deployment patterns

- ✅ Use `period_end_time` (NOT update_end_time)- Investigate incidents with historical data

- ✅ Use `update_type` (NOT update_state)

- ❌ Column `cause` does not exist in this table**For Executive Reporting:**

- Platform adoption metrics

---- Cost efficiency KPIs

- Reliability dashboards

## 📊 Datasets (10 Total)- Cross-workspace comparisons



| Dataset | Purpose | Time Range |---

|---------|---------|------------|

| ds_job_run_timeline | Job execution timeline | 30 days |## Technical Highlights

| ds_job_run_cost_agg | Aggregated job costs | 30 days |

| ds_highest_failure_jobs | Top 10 failing jobs | 30 days |### Multi-Workspace Architecture

| ds_long_running_jobs | Jobs with high P95 duration | 30 days |- **Centralized monitoring**: One dashboard, all workspaces

| ds_most_expensive_jobs | Top 10 cost leaders | 30 days |- **System Catalog**: Leverages account-level system tables

| ds_pipeline_updates | Pipeline update timeline | 30 days |- **No agents required**: Built-in Databricks telemetry

| ds_pipeline_failures | Failed pipeline updates | 30 days |- **Real-time data**: Updates every 30-60 minutes automatically

| ds_clusters_active | Active clusters (deduplicated) | Current |

| ds_billing_30_60_days | Billing summary | 30-60 days |### Data Sources

| ds_billing_daily_timeseries | Daily cost time series | 30 days |```

system.billing.*           → Cost and usage data

---system.lakeflow.*         → Jobs and pipeline execution

system.compute.*          → Cluster configurations

## 🛠️ Troubleshooting```



### Dashboard Won't Import### Query Optimization

- Verify JSON file is valid- ✅ Window functions for latest records (ROW_NUMBER + QUALIFY)

- Check Unity Catalog is enabled- ✅ Efficient JOINs with list_prices for cost calculation

- Ensure system tables are accessible- ✅ 30-day lookback (configurable)

- ✅ GROUP BY ALL for cleaner syntax

### No Data Showing- ✅ TRY_DIVIDE for safe calculations

- Verify activity exists in last 30 days

- Check permissions to system schema### Visualization Features

- Test system table access with sample query:- 📊 Counter widgets for KPIs

```sql- 📈 Time series (line/bar charts)

SELECT COUNT(*) FROM system.lakeflow.job_run_timeline;- 📋 Sortable/searchable tables

```- 🎨 Color-coded status indicators

- 🔢 Custom number formatting ($, %, dates)

### Incorrect Costs

- Verify 0.73 multiplier matches your discount---

- Check `system.billing.list_prices` is populated

- Ensure usage data exists in `system.billing.usage`## Dashboard Pages Overview



### Duplicate Clusters### Page 1: Overview 🏠

- Should be fixed with ROW_NUMBER() deduplicationThe executive summary page with:

- Verify `change_time` column exists in your system.compute.clusters- 3 KPI counters (30-day spend, 30-60 day spend, growth %)

- Daily job run status (stacked bar chart)

---- Daily cost trends (line chart by workspace)

- Workspace summary table (jobs, runs, cost)

## 🎯 Best Practices

**Best for**: Morning standup, weekly reviews, executive reports

### Cost Optimization

- Review "Most Expensive Jobs" weekly### Page 2: Jobs 💼

- Check for idle clustersDetailed job performance analysis:

- Identify jobs that can use smaller clusters- Highest failure jobs table (sorted by failure count)

- Most expensive jobs table (sorted by cost)

### Performance Optimization- Top 10 failing jobs visualization (horizontal bar)

- Monitor P95 duration trends

- Investigate long-running jobs**Best for**: Reliability improvements, cost optimization, troubleshooting

- Track success rates for reliability

### Page 3: Pipelines 🔄

### Capacity PlanningDelta Live Tables monitoring:

- Use active clusters report for resource allocation- Daily pipeline update status (stacked bar)

- Track daily cost trends for budgeting- Top failing pipelines table

- Monitor job/pipeline volume growth

**Best for**: DLT pipeline developers, data engineers

---

### Page 4: Clusters 🖥️

## 🔄 CustomizationCluster governance and inventory:

- Complete active clusters table (11 columns)

### Change Discount Rate- Sortable by workspace, owner, creation date, DBR version

Find and replace `* 0.73` with your discount multiplier:

```sql**Best for**: Platform governance, cost control, compliance

-- Example: 30% discount = 0.70

list_prices.pricing.default * 0.70---

```

## Requirements

### Extend Time Range

Change from 30 days to different period:### Minimum Requirements

```sql- ✅ Azure Databricks account

-- Current: 30 days- ✅ System Tables enabled

WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS- ✅ Pro or Serverless SQL Warehouse

- ✅ SELECT permissions on system.* schemas

-- Example: 90 days

WHERE period_start_time >= CURRENT_DATE() - INTERVAL 90 DAYS### Recommended Setup

```- 🔹 Dedicated "Platform Monitoring" workspace

- 🔹 Hourly dashboard refresh schedule

### Add Filters (Optional)- 🔹 Alerts on key metrics (failures, cost spikes)

To add parameter filters:- 🔹 Shared with platform team (CAN RUN access)

1. Add parameter to `parameters` array at dashboard level with `possibleValues`

2. Add dataset-level parameter binding in relevant dataset### Browser Support

3. Update SQL WHERE clause to use `:param_name` syntax- Chrome/Edge (recommended)

- Firefox

---- Safari



## 📌 Report Details---



### Jobs with Highest Failure Rate## Customization Examples

```sql

failure_rate = failed_runs / total_runs### Filter to Specific Workspaces

``````sql

Shows jobs where failure_rate > 0, ordered by failure countWHERE workspace_id IN ('1234567890', '0987654321')

```

### Long Running Jobs

Uses `PERCENTILE_CONT(0.95)` for P95 duration### Change Time Window to 7 Days

Filtered to jobs with avg_duration > 10 minutes```sql

WHERE usage_date >= CURRENT_DATE() - INTERVAL 7 DAYS

### Most Expensive Jobs```

Aggregates: DBU usage × list price × 0.73

Shows top 10 by total cost### Add Cost Threshold Filter

```sql

### Active ClustersHAVING list_cost > 100  -- Only show jobs costing > $100

Deduplicated by cluster_id showing only latest configuration```

Includes: workspace, owner, source, node types, autoscaling settings

### Group by Additional Dimensions

---```sql

SELECT 

## ✅ Dashboard Status  workspace_id,

  owned_by,  -- Add owner dimension

**Current State**: Production-ready  SUM(list_cost) as total_cost

- ✅ All queries validatedFROM ...

- ✅ No parameter dependencies (shows all data)GROUP BY workspace_id, owned_by

- ✅ Proper column names used```

- ✅ Cluster deduplication implemented

- ✅ Cost calculations correct---

- ✅ Widget encodings complete

## Success Metrics

**Configuration**:

- No filters/parameters (simplified UX)After deploying, measure:

- 30-day lookback period- **MTTR**: Mean time to resolution for job failures

- 27% enterprise discount applied- **Cost efficiency**: $ per job run over time

- Multi-workspace support- **Platform adoption**: # of jobs/workspaces growing

- **Reliability**: Job success rate trending up

---- **Governance**: % clusters with proper autotermination



## 📄 File Information---



**Filename**: `Monitoring Dashboard.lvdash.json`  ## Support and Next Steps

**Format**: Lakeview Dashboard JSON  

**Line Count**: ~2000+ lines  ### Immediate Next Steps

**Version**: Production-ready  1. ✅ Import dashboard (5 minutes)

**Last Updated**: March 13, 20262. ✅ Configure refresh schedule (2 minutes)

3. ✅ Share with team (1 minute)

---4. ✅ Create 2-3 alerts (10 minutes)

5. ✅ Add to weekly review meeting agenda

## 🔗 Resources

### Ongoing Maintenance

- [Azure Databricks System Tables](https://learn.microsoft.com/azure/databricks/administration-guide/system-tables/)- **Weekly**: Review failure trends, identify patterns

- [Lakeview Dashboard Documentation](https://learn.microsoft.com/azure/databricks/dashboards/)- **Monthly**: Analyze cost trends, optimize expensive jobs

- [Unity Catalog Documentation](https://learn.microsoft.com/azure/databricks/data-governance/unity-catalog/)- **Quarterly**: Update dashboard, add new metrics as needed



---### Enhancement Ideas

- Add warehouse query performance metrics

**Dashboard Purpose**: Multi-workspace monitoring and cost optimization for Azure Databricks platform architects.- Include storage cost analysis

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
