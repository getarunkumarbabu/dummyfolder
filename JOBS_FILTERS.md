# Jobs Page Filter Implementation

## ✅ Filters Added to Jobs Page

Workspace name filters have been successfully added to both job analysis tables on the Jobs page.

## 📊 Tables with Filters

### 1. Highest Failure Jobs — Last 30 Days
**Filter Added:** Workspace Name  
**Parameter:** `workspace_filter_failures`  
**Purpose:** Filter the failure analysis by specific workspace

### 2. Most Expensive Jobs — Last 30 Days
**Filter Added:** Workspace Name  
**Parameter:** `workspace_filter_expensive`  
**Purpose:** Filter the cost analysis by specific workspace

## 🎯 How to Use the Filters

### In the Dashboard

After importing the updated dashboard, the Jobs page will display:

```
┌──────────────────────────────────────────────────────┐
│ Jobs Page                                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│ ┌──────────────────────────────────────────────────┐│
│ │ Highest Failure Jobs — Last 30 Days              ││
│ │                                                  ││
│ │ 🎛️ Workspace Name: [All ▼]                      ││
│ │                                                  ││
│ │ Table showing filtered failure data...           ││
│ └──────────────────────────────────────────────────┘│
│                                                      │
│ ┌──────────────────────────────────────────────────┐│
│ │ Most Expensive Jobs — Last 30 Days               ││
│ │                                                  ││
│ │ 🎛️ Workspace Name: [All ▼]                      ││
│ │                                                  ││
│ │ Table showing filtered cost data...              ││
│ └──────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────┘
```

### Filter Behavior

**Default State:**
- Both filters set to "All"
- Shows jobs from all workspaces
- Same behavior as before the update

**With Filter Applied:**
- Select a specific workspace name
- Table updates to show only jobs from that workspace
- Independent filters for each table (can filter differently)

## 💡 Use Cases

### Use Case 1: Focus on Production Failures
**Scenario:** Platform team wants to review only production job failures

**Action:**
1. Go to Jobs page
2. In "Highest Failure Jobs" table
3. Select Workspace Name = "Production"

**Result:**
- See only jobs that failed in Production workspace
- Prioritize production issues
- Ignore dev/test failures for this analysis

### Use Case 2: Analyze Development Costs
**Scenario:** FinOps team wants to review development environment spending

**Action:**
1. Go to Jobs page
2. In "Most Expensive Jobs" table
3. Select Workspace Name = "Development"

**Result:**
- See only job costs from Development workspace
- Identify expensive dev jobs
- Optimize development resource usage

### Use Case 3: Compare Workspaces
**Scenario:** Compare failure rates between Production and Staging

**Action:**
1. Open Jobs page
2. Set "Highest Failure Jobs" filter to "Production"
3. Note the top failing jobs
4. Change filter to "Staging"
5. Compare the results

**Result:**
- Identify workspace-specific reliability issues
- Find patterns unique to each environment

### Use Case 4: Workspace-Specific Cost Optimization
**Scenario:** Each team manages their own workspace budget

**Action:**
1. Filter "Most Expensive Jobs" by team's workspace
2. Identify top cost drivers
3. Optimize those specific jobs

**Result:**
- Team-level cost accountability
- Targeted optimization efforts
- Clear cost attribution

## 🔍 Common Filtering Scenarios

### Scenario Matrix

| Highest Failure Jobs Filter | Most Expensive Jobs Filter | Use Case |
|----------------------------|---------------------------|----------|
| All | All | Overall platform health review |
| Production | Production | Production-only analysis |
| Development | Development | Dev environment review |
| Production | All | Focus failures, see all costs |
| All | Production | See all failures, focus prod costs |
| Analytics | Analytics | Single workspace deep dive |

## 📈 Query Logic

### Highest Failure Jobs Query
```sql
-- Filter applied in WHERE clause after JOIN
WHERE ('{{ workspace_filter_failures }}' = 'All' 
       OR workspace_name = '{{ workspace_filter_failures }}')
```

**How it works:**
- If filter = "All" → condition is always true → shows all workspaces
- If filter = "Production" → only shows rows where workspace_name = "Production"

### Most Expensive Jobs Query
```sql
-- Filter applied in WHERE clause after JOIN
WHERE ('{{ workspace_filter_expensive }}' = 'All' 
       OR workspace_name = '{{ workspace_filter_expensive }}')
```

**How it works:**
- Same logic as failure jobs filter
- Independent parameter allows different filtering per table

## 🎨 Filter Parameters

### ds_highest_failure_jobs
```json
{
  "name": "workspace_filter_failures",
  "displayName": "Workspace Name",
  "dataType": "STRING",
  "defaultValue": "All"
}
```

### ds_most_expensive_jobs
```json
{
  "name": "workspace_filter_expensive",
  "displayName": "Workspace Name",
  "dataType": "STRING",
  "defaultValue": "All"
}
```

## 🚀 Performance Benefits

**Filtered Queries Are Faster:**
- Reduces data volume processed
- Enables better query optimization
- Particularly beneficial with many workspaces

**Example Impact:**
- Unfiltered: Analyze 5,000 jobs across 20 workspaces
- Filtered to 1 workspace: Analyze ~250 jobs
- Query execution time reduced significantly

## 📊 Reporting Use Cases

### Executive Reporting
**Monthly Reliability Report:**
- Filter failures by "Production" workspace
- Export top 10 failing jobs
- Present to leadership

**Cost Review:**
- Filter expensive jobs by each workspace
- Compare month-over-month trends
- Identify optimization opportunities

### Team-Level Dashboards
**Development Team:**
- Filter both tables to "Development"
- Monitor team-specific metrics
- Track improvements over time

**Data Engineering Team:**
- Filter to "Analytics" workspace
- Review pipeline job costs
- Optimize data processing jobs

### Audit and Compliance
**Production-Only Audit:**
- Filter both tables to "Production"
- Verify SLA compliance
- Document failure patterns

**Cost Allocation:**
- Filter expensive jobs by each workspace
- Generate chargeback reports
- Allocate costs to business units

## 🛠️ Troubleshooting

### Filter Not Appearing
**Issue:** Don't see filter dropdown on Jobs page  
**Solution:**
1. Ensure dashboard is properly imported
2. Refresh the dashboard page
3. Check browser console for errors

### No Results When Filtered
**Issue:** Table is empty after selecting a workspace  
**Possible Causes:**
1. No jobs in that workspace (correct behavior)
2. Workspace name mismatch or typo
3. No data in last 30 days for that workspace

**Solution:**
- Reset filter to "All" to verify data exists
- Check exact workspace names in system tables
- Verify date range includes activity

### Different Results in Two Tables
**Issue:** Tables show different data when both filtered to same workspace  
**Explanation:** This is correct!
- Failure table: Shows jobs that **ran and had failures**
- Expensive table: Shows jobs that **incurred costs**
- A job can have failures but low cost, or high cost with no failures

## 💡 Best Practices

### 1. Start with "All", Then Narrow
- Begin with full data view
- Identify patterns
- Apply filters to investigate specific workspaces

### 2. Use Independent Filters Strategically
- Filter failures by Production to focus on critical issues
- Keep costs at "All" to maintain cost visibility
- Or vice versa based on your priorities

### 3. Combine with Table Search
- Apply workspace filter first
- Use in-table search for specific job names
- Powerful combination for targeted analysis

### 4. Export Filtered Data
- Apply desired filter
- Export table to CSV/Excel
- Use for offline analysis or reporting

### 5. Bookmark Common Views
- Filter to your team's workspace
- Bookmark the URL (includes filter parameters)
- Quick access to your relevant data

## 📚 Related Features

### Also Available on Other Pages

**Clusters Page:**
- Workspace Name filter
- Cluster Source filter
- See `FILTER_IMPLEMENTATION.md` for details

**Overview Page:**
- Workspace-level aggregations (no filters needed)
- Visual breakdown by workspace in charts

**Pipelines Page:**
- No filters currently (can be added if needed)

## 🔄 Filter Independence

**Important Note:**
The two filters on the Jobs page are **independent**:

- Setting "Highest Failure Jobs" to "Production" does NOT affect "Most Expensive Jobs"
- Each table has its own filter control
- This allows flexible analysis scenarios

**Example:**
```
Highest Failure Jobs: Filter = "Production"
  → Shows only Production job failures

Most Expensive Jobs: Filter = "All"
  → Shows expensive jobs from all workspaces

Purpose: Focus on Production reliability while maintaining 
         full visibility into costs across all workspaces
```

## 📝 Summary

### What Was Added
✅ Workspace Name filter for "Highest Failure Jobs — Last 30 Days"  
✅ Workspace Name filter for "Most Expensive Jobs — Last 30 Days"  
✅ Independent filters allow different selections per table  
✅ Default to "All" maintains existing behavior  

### Benefits
🎯 Workspace-focused analysis  
🎯 Faster queries with filtering  
🎯 Team-level accountability  
🎯 Flexible reporting options  
🎯 Better cost attribution  

### Files Updated
📄 `Monitoring Dashboard.lvdash.json` - Added filter parameters to both datasets  
📄 `JOBS_FILTERS.md` - This documentation file  

---

**Implementation Date:** March 12, 2026  
**Feature:** Workspace Name filters for Jobs page  
**Status:** ✅ Ready to use after dashboard import
