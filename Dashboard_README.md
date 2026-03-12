# Azure Databricks Multi-Workspace Monitoring Dashboard

## Overview
This comprehensive monitoring dashboard provides visibility into Jobs, Pipelines, Clusters, and Billing across all Databricks workspaces using the System Catalog.

## Dashboard Specifications

### Data Sources
The dashboard leverages the following System Catalog schemas:
- **system.billing** - Cost and usage data
- **system.lakeflow** - Jobs and pipeline execution data
- **system.compute** - Cluster configuration and status

### Dashboard Structure

#### 📊 Page 1: Overview
**Purpose:** High-level summary of multi-workspace operations and costs

**Datasets:**
- `ds_job_run_timeline` - Job execution timeline (last 30 days)
- `ds_job_run_cost_agg` - Aggregated job costs by workspace
- `ds_billing_30_60_days` - Spend comparison between 30-day periods
- `ds_billing_daily_timeseries` - Daily cost trends

**Widgets:**
1. **Title Header** - Dashboard branding and description
2. **Counter: 30-Day Spend** - Total list cost for jobs (last 30 days)
3. **Counter: 30-60 Day Spend** - Previous period comparison
4. **Counter: 30-Day Growth %** - Spend growth percentage
5. **Bar Chart: Daily Job Run Status** - Stacked bar showing run outcomes by day
   - Color-coded: Success (green), Failed (red), Error (red), Timed Out (gray), Skipped (blue)
6. **Line Chart: Daily Cost by Workspace** - Multi-line time series by workspace_id
7. **Table: Jobs Summary by Workspace** - Aggregated metrics per workspace
   - Columns: Workspace ID, Job Count, Run Count, List Cost

#### 💼 Page 2: Jobs
**Purpose:** Detailed job performance and cost analysis

**Datasets:**
- `ds_highest_failure_jobs` - Jobs with highest failure rates
- `ds_most_expensive_jobs` - Jobs ranked by cost

**Widgets:**
1. **Table: Highest Failure Jobs** - Jobs sorted by failure count
   - Columns: Workspace ID, Job Name, Job ID, Runs, Failures, Success Ratio %, Last Seen
   - Shows failure patterns across all workspaces
   
2. **Table: Most Expensive Jobs** - Cost analysis by job
   - Columns: Workspace ID, Job Name, Job ID, Runs, Run As, List Cost, Last Seen
   - Identifies cost optimization opportunities
   
3. **Bar Chart: Top Failing Jobs** - Visual representation of failure counts
   - Horizontal bar chart with color gradient (red scheme)
   - Sorted by failure count descending

#### 🔄 Page 3: Pipelines
**Purpose:** Delta Live Tables / Pipeline monitoring

**Datasets:**
- `ds_pipeline_updates` - Pipeline update execution timeline
- `ds_pipeline_failures` - Failed pipeline updates aggregated

**Widgets:**
1. **Bar Chart: Daily Pipeline Update Status** - Stacked bar by update state
   - Color-coded: Completed (green), Failed (red), Canceled (gray), Running (blue)
   - Shows pipeline health trends over 30 days
   
2. **Table: Top Failing Pipelines** - Pipelines with most failures
   - Columns: Workspace ID, Pipeline Name, Pipeline ID, Failed Updates
   - Helps identify problematic pipelines

#### 🖥️ Page 4: Clusters
**Purpose:** Cluster inventory and configuration monitoring

**Datasets:**
- `ds_clusters_active` - All active (non-deleted) clusters

**Widgets:**
1. **Table: Active Clusters Across All Workspaces** - Complete cluster inventory
   - Columns:
     - Workspace ID
     - Cluster Name
     - Cluster ID
     - Owner
     - Source (UI, API, JOB, etc.)
     - Driver Node Type
     - Worker Node Type
     - Worker Count
     - Auto-Termination Minutes
     - Create Time
     - DBR Version
   - Useful for governance, cost control, and compliance

## Key Features

### Multi-Workspace Support
- All queries aggregate data across workspaces
- Workspace ID is included in most visualizations
- Enables central platform monitoring

### Time-Based Analysis
- 30-day default lookback period
- Supports trend analysis and growth calculations
- Daily granularity for detailed insights

### Cost Tracking
- List price calculations using `system.billing.list_prices`
- Join patterns that handle price changes over time
- Spend growth calculations (30-day vs. 30-60 day)

### Failure Detection
- Job failure tracking with success ratio calculations
- Pipeline failure aggregation
- Visual indicators for different failure states

### Query Optimization Techniques
Used throughout the dashboard:
- Window functions for "most recent" record selection
- CTEs for complex calculations
- Proper JOIN strategies with list_prices
- GROUP BY ALL for cleaner aggregations
- DATE_TRUNC for time-series grouping

## Import Instructions

1. **Open Azure Databricks Workspace**
   - Navigate to any workspace in your environment
   - Go to **SQL** → **Dashboards**

2. **Import Dashboard**
   - Click **Create** → **Import Dashboard**
   - Select the `Monitoring Dashboard.lvdash.json` file
   - The dashboard will be created with all pages, datasets, and widgets

3. **Verify Data Access**
   - Ensure you have SELECT permissions on:
     - `system.billing.usage`
     - `system.billing.list_prices`
     - `system.lakeflow.jobs`
     - `system.lakeflow.job_run_timeline`
     - `system.lakeflow.pipelines`
     - `system.lakeflow.pipeline_update_timeline`
     - `system.compute.clusters`

4. **Run Queries**
   - Click **Refresh** on the dashboard
   - All datasets will execute and populate the widgets
   - Queries typically complete in seconds to minutes depending on data volume

## Customization Options

### Adjust Time Windows
Modify the date filters in any dataset query:
```sql
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
```
Change `30 DAYS` to `7 DAYS`, `60 DAYS`, or `90 DAYS` as needed.

### Add Workspace Filters
Add workspace filtering to any query:
```sql
WHERE workspace_id IN ('workspace-id-1', 'workspace-id-2')
```

### Additional Metrics
Consider adding:
- **Warehouse monitoring** from `system.query.history`
- **Storage metrics** from `system.storage.*`
- **User activity** from `system.access.audit`

### Custom Color Schemes
Modify the color mappings in chart encodings:
```json
"mappings": [
  { "value": "SUCCEEDED", "color": "#00A972" },
  { "value": "FAILED", "color": "#FF3621" }
]
```

## Troubleshooting

### No Data Appearing
- Verify System Tables are enabled in your account
- Check that data has been ingested (can take 24-48 hours initially)
- Confirm SELECT permissions on all system schemas

### Query Errors
- Ensure you're on a **Pro or Serverless SQL Warehouse**
- System tables require appropriate DBR/SQL Warehouse versions
- Check for any schema changes in recent Databricks releases

### Performance Issues
- Add WHERE clauses to filter by specific workspaces
- Reduce time window for large environments
- Consider materializing frequently-used CTEs as tables

## Best Practices

1. **Schedule Refresh**: Set up automatic refresh (hourly or daily)
2. **Alert Configuration**: Create alerts on key metrics (failure rates, cost spikes)
3. **Access Control**: Share with platform admins and finance teams
4. **Regular Review**: Monitor trends weekly for optimization opportunities
5. **Documentation**: Keep track of any custom modifications

## Additional Resources

- [System Tables Documentation](https://docs.databricks.com/administration-guide/system-tables/index.html)
- [Lakeview Dashboard Guide](https://docs.databricks.com/dashboards/lakeview.html)
- [Billing Usage Patterns](https://docs.databricks.com/administration-guide/system-tables/billing.html)

## Version Information

- **Dashboard Version**: 1.0
- **Created**: March 2026
- **Compatible With**: Azure Databricks (System Tables enabled)
- **Dashboard Format**: Lakeview (.lvdash.json)

---

**Note**: This dashboard requires System Tables to be enabled in your Databricks account. Contact your Databricks account team if you don't have access to the `system` catalog.
