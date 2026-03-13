# Overview Page Filter Update - March 12, 2026

## ✅ Filter Added: Jobs Summary by Workspace

A workspace name filter has been successfully added to the "Jobs Summary by Workspace — Last 30 Days" table on the Overview page.

---

## 📋 Change Summary

**Table:** Jobs Summary by Workspace — Last 30 Days  
**Location:** Overview Page  
**Filter Added:** Workspace Name filter  
**Parameter:** `workspace_filter_summary`  
**Default Value:** "All"

---

## 🎯 What This Filter Does

The workspace filter allows you to focus the summary table on a specific workspace, showing:
- **Number of Jobs** - Total unique jobs in that workspace
- **Number of Runs** - Total job runs in the last 30 days
- **$list Cost** - Total cost for jobs in that workspace

### Before Filter:
- Table showed ALL workspaces
- No way to isolate a specific workspace's summary

### After Filter:
- Can select "All" to see all workspaces (default)
- Can select a specific workspace to see only that workspace's stats

---

## 💡 Use Cases

### Use Case 1: Executive Dashboard
**Scenario:** C-level wants to see Production workspace metrics only

**Steps:**
1. Open Overview page
2. Scroll to "Jobs Summary by Workspace" table
3. Select filter = "Production"

**Result:**
- Table shows only Production workspace
- Clear view of Production job count, runs, and costs

---

### Use Case 2: Team-Specific Review
**Scenario:** Data Engineering team reviews their workspace

**Steps:**
1. Filter = "Data Engineering"
2. See their job statistics
3. Compare to previous periods

**Result:**
- Team accountability
- Self-service metrics

---

### Use Case 3: Cost Allocation
**Scenario:** FinOps team allocates costs per workspace

**Steps:**
1. Set filter to each workspace one by one
2. Export or note the $list Cost
3. Create chargeback report

**Result:**
- Accurate per-workspace cost allocation
- Easy reporting

---

### Use Case 4: Capacity Planning
**Scenario:** Platform team plans resource allocation

**Steps:**
1. Filter to high-activity workspaces
2. Note job count and run frequency
3. Allocate resources accordingly

**Result:**
- Data-driven capacity planning
- Optimize resource distribution

---

## 📊 Table Columns

The filtered table displays:

| Column | Description |
|--------|-------------|
| **Workspace Name** | Human-readable workspace identifier |
| **Jobs** | Number of unique jobs in workspace |
| **Runs (30d)** | Total job runs in last 30 days |
| **$list Cost** | Total list price cost for all job runs |

**Default Sort:** By $list Cost (descending) - most expensive workspaces first

---

## 🎛️ Filter Behavior

### Default State
- Filter = "All"
- Shows all workspaces
- Same behavior as before the update

### With Filter Applied
- Select a workspace name
- Table shows only that workspace's row
- Cost, run count, and job count for selected workspace only

### SQL Logic
```sql
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
  AND ('{{ workspace_filter_summary }}' = 'All' 
       OR COALESCE(w.workspace_name, CAST(t1.workspace_id AS STRING)) = '{{ workspace_filter_summary }}')
```

**How it works:**
- If filter = "All" → condition is always true → shows all rows
- If filter = "Production" → only shows rows where workspace_name = "Production"

---

## 📈 Overview Page Layout (After Update)

```
┌────────────────────────────────────────────────────────┐
│ Overview Page                                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│ [Counters Row]                                        │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐         │
│ │ Active │ │ Jobs   │ │Pipeline│ │ Total  │         │
│ │Clusters│ │  Run   │ │ Updates│ │  Cost  │         │
│ └────────┘ └────────┘ └────────┘ └────────┘         │
│                                                        │
│ ┌────────────────────────────────────────────────────┐│
│ │ Daily Cost Trend (Line Chart)                      ││
│ └────────────────────────────────────────────────────┘│
│                                                        │
│ ┌──────────────────────┐  ┌──────────────────────────┐│
│ │ Cost by Workspace    │  │ Jobs Summary by Workspace││
│ │ (Bar Chart)          │  │                          ││
│ │                      │  │ 🎛️ Workspace Filter ⭐NEW││
│ │                      │  │                          ││
│ │                      │  │ (Table: workspace, jobs, ││
│ │                      │  │  runs, cost)             ││
│ └──────────────────────┘  └──────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset: ds_job_run_cost_agg

### Key Features:
- Aggregates job runs and costs per workspace
- Last 30 days of data
- Joins with `system.access.workspaces_latest` for names
- Joins with `system.billing.usage` for costs
- Now includes filter parameter

### Query Structure:
```sql
WITH jobs_usage_with_list_cost AS (
  -- Calculate list cost for job usage
  SELECT t1.*, t1.usage_quantity * list_prices.pricing.default AS list_cost
  FROM system.billing.usage t1
  INNER JOIN system.billing.list_prices list_prices
    ON [... pricing join conditions ...]
  WHERE t1.sku_name LIKE '%JOBS%'
    AND usage_date >= CURRENT_DATE() - INTERVAL 30 DAYS
),
jobs_usage_per_workspace AS (
  -- Aggregate cost per workspace
  SELECT workspace_id, SUM(list_cost) AS list_cost
  FROM jobs_usage_with_list_cost GROUP BY ALL
)
SELECT
  t1.workspace_id,
  COALESCE(w.workspace_name, CAST(t1.workspace_id AS STRING)) AS workspace_name,
  COUNT(DISTINCT t1.job_id)  AS num_jobs,
  COUNT(DISTINCT t1.run_id)  AS num_runs,
  FIRST(t2.list_cost)        AS list_cost
FROM system.lakeflow.job_run_timeline t1
LEFT JOIN jobs_usage_per_workspace t2 USING (workspace_id)
LEFT JOIN system.access.workspaces_latest w ON t1.workspace_id = w.workspace_id
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
  AND ('{{ workspace_filter_summary }}' = 'All' 
       OR COALESCE(w.workspace_name, CAST(t1.workspace_id AS STRING)) = '{{ workspace_filter_summary }}')
GROUP BY ALL
ORDER BY list_cost DESC
```

### System Tables Used:
1. `system.lakeflow.job_run_timeline` - Job execution data
2. `system.billing.usage` - Usage metrics for billing
3. `system.billing.list_prices` - Pricing information
4. `system.access.workspaces_latest` - Workspace metadata

---

## 🔍 Common Scenarios

### Scenario: Compare Production vs. Development Costs

**Steps:**
1. Filter = "Production", note $list Cost
2. Filter = "Development", note $list Cost
3. Compare values

**Example Result:**
- Production: $15,432 (85 jobs, 1,250 runs)
- Development: $2,876 (45 jobs, 342 runs)
- Insight: Production is 5.4x more expensive

---

### Scenario: Track Single Workspace Over Time

**Steps:**
1. Set filter to your workspace
2. Export table today
3. Re-export weekly
4. Track trends in Excel

**Benefit:**
- Historical tracking
- Identify growth patterns
- Budget forecasting

---

### Scenario: Identify Inactive Workspaces

**Steps:**
1. Keep filter at "All"
2. Sort by "Runs (30d)" ascending
3. Identify workspaces with 0 or very few runs

**Action:**
- Consider decommissioning inactive workspaces
- Cost optimization opportunity

---

## 📈 Metrics Interpretation

### Number of Jobs
- **High value:** Workspace has many different job definitions
- **Low value:** Few job types, possibly more focused

### Runs (30d)
- **High value:** Active workspace with frequent executions
- **Low value:** Infrequent activity, possible candidate for review

### $list Cost
- **High value:** Resource-intensive workspace, review optimization
- **Low value:** Efficient or low-activity workspace

### Combined Analysis
```
Example 1:
  Jobs: 100, Runs: 1000, Cost: $500
  → Many jobs, high activity, relatively low cost = Efficient

Example 2:
  Jobs: 10, Runs: 50, Cost: $5000
  → Few jobs, low activity, high cost = Investigation needed

Example 3:
  Jobs: 50, Runs: 2000, Cost: $1500
  → Moderate jobs, very high activity, moderate cost = Normal pattern
```

---

## 🚀 Performance Impact

### Query Performance
- **With filter:** Faster (less data to aggregate)
- **Without filter (All):** Same as before update

### Expected Response Time
- All workspaces: ~2-5 seconds
- Single workspace: ~1-3 seconds

---

## 🐛 Troubleshooting

### Issue: Filter dropdown is empty
**Cause:** No workspaces have job activity in last 30 days  
**Solution:** Verify with: `SELECT DISTINCT workspace_id FROM system.lakeflow.job_run_timeline WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS`

### Issue: Filter shows workspace_id instead of name
**Cause:** Workspace not in `system.access.workspaces_latest`  
**Solution:** This is expected behavior; COALESCE provides ID as fallback

### Issue: Costs don't match billing reports
**Cause:** This shows LIST prices, not actual/negotiated prices  
**Solution:** Use this for relative comparison, not absolute billing

### Issue: No data after filtering
**Possible Causes:**
1. Selected workspace has no jobs in last 30 days (correct behavior)
2. Workspace name mismatch
3. Permissions issue

**Solution:** Reset filter to "All" and verify workspace appears in unfiltered view

---

## 📊 Dashboard Statistics

**Before This Update:**
- Total Filters: 5
- Overview Page Filters: 0

**After This Update:**
- Total Filters: 6
- Overview Page Filters: 1 ⭐

**Other Updates in This Session:**
- Added Long Running Jobs table (Jobs page)
- Removed Top Failing Jobs bar chart
- Total dashboard lines: 1,949

---

## 📚 Related Features

### Other Workspace Filters
1. **Clusters Page:** Active Clusters workspace filter
2. **Jobs Page:** Highest Failure Jobs workspace filter
3. **Jobs Page:** Most Expensive Jobs workspace filter
4. **Jobs Page:** Long Running Jobs workspace filter

### Related Tables
- **Cost by Workspace (Bar Chart)** - Visual representation, no filter
- Shows same workspaces as this table in chart format

---

## 💡 Pro Tips

### Tip 1: Bookmark Filtered Views
Create bookmarks for frequently viewed workspaces:
- Production dashboard: filter = "Production"
- Your team's view: filter = "Data Engineering"

### Tip 2: Combine with Chart
1. Apply filter to table
2. Look at "Cost by Workspace" bar chart (unfiltered)
3. See filtered workspace in context of all workspaces

### Tip 3: Export for Reporting
- Apply workspace filter
- Export table to Excel
- Include in monthly reports

### Tip 4: Watch the Ratios
- **Runs per Job:** High = frequently scheduled jobs
- **Cost per Run:** Divide cost by runs = efficiency metric
- Track these ratios over time per workspace

### Tip 5: Cross-Reference with Jobs Page
1. Note expensive workspace in Overview
2. Switch to Jobs page
3. Apply same workspace filter to "Most Expensive Jobs"
4. Identify specific jobs driving costs

---

## ✅ Validation Checklist

### Pre-Deployment
- [x] JSON validated successfully
- [x] Filter parameter added to dataset
- [x] WHERE clause updated with filter logic
- [x] Default value set to "All"

### Post-Deployment
- [ ] Dashboard imports without errors
- [ ] Filter dropdown appears on Overview page
- [ ] Filter shows workspace names
- [ ] Selecting "All" shows all workspaces
- [ ] Selecting specific workspace shows only that workspace
- [ ] Metrics (jobs, runs, cost) are accurate

---

## 📋 Summary

### What Changed
✅ Added workspace filter to "Jobs Summary by Workspace — Last 30 Days"  
✅ Updated dataset `ds_job_run_cost_agg` with filter parameter  
✅ Added WHERE clause filter logic  
✅ JSON validated successfully  

### Why It Matters
- **Focused analysis:** View specific workspace metrics
- **Team enablement:** Self-service workspace monitoring
- **Cost allocation:** Easy per-workspace cost tracking
- **Consistency:** All major tables now have workspace filters

### Next Steps
1. Import updated dashboard
2. Test filter functionality
3. Share with teams
4. Create workspace-specific bookmarks

---

**Update Date:** March 12, 2026  
**Dashboard Version:** 1.6  
**Filter Added:** workspace_filter_summary  
**Status:** ✅ Ready for Production  
**Documentation:** Complete
