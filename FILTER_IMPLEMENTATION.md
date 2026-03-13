# Active Clusters Filter Implementation

## Overview
The "Active Clusters Across All Workspaces" table now includes **interactive filters** for **Workspace Name** and **Cluster Source** columns.

## ✅ Changes Implemented

### Dataset: `ds_clusters_active`

**Added Filter Parameters:**
1. **Workspace Name Filter** (`workspace_filter`)
   - Type: STRING
   - Default: "All"
   - Filters clusters by workspace name

2. **Cluster Source Filter** (`source_filter`)
   - Type: STRING
   - Default: "All"
   - Filters clusters by source (UI, API, JOB, etc.)

**Updated Query Logic:**
```sql
WHERE c.delete_time IS NULL
  AND ('{{ workspace_filter }}' = 'All' OR COALESCE(w.workspace_name, CAST(c.workspace_id AS STRING)) = '{{ workspace_filter }}')
  AND ('{{ source_filter }}' = 'All' OR c.cluster_source = '{{ source_filter }}')
```

## 🎯 How to Use the Filters

### In the Dashboard

Once you import the updated dashboard, you'll see filter dropdowns at the top of the Clusters page:

1. **Workspace Name Filter**
   - Dropdown showing all available workspace names
   - Select "All" to see all workspaces (default)
   - Select a specific workspace to filter clusters from that workspace only

2. **Cluster Source Filter**
   - Dropdown showing all cluster sources
   - Select "All" to see all sources (default)
   - Select specific source (UI, API, JOB, etc.) to filter

### Filter Behavior

**Default State:**
- Both filters set to "All"
- Shows all active clusters from all workspaces
- No filtering applied

**Single Filter:**
- Select workspace = "Production" → Shows only Production clusters
- Select source = "JOB" → Shows only job clusters

**Combined Filters:**
- Workspace = "Production" AND Source = "JOB"
- Shows only job clusters in Production workspace
- Both conditions must be met (AND logic)

## 📋 Common Filter Scenarios

### Scenario 1: View Clusters in Specific Workspace
```
Workspace Name: "Production"
Cluster Source: "All"
```
Result: All clusters in Production workspace

### Scenario 2: View Only Job Clusters
```
Workspace Name: "All"
Cluster Source: "JOB"
```
Result: All job clusters across all workspaces

### Scenario 3: View Interactive Clusters in Dev
```
Workspace Name: "Development"
Cluster Source: "UI"
```
Result: Only interactive (UI-created) clusters in Development

### Scenario 4: View All API-Created Clusters
```
Workspace Name: "All"
Cluster Source: "API"
```
Result: All clusters created via API across all workspaces

## 🔍 Available Cluster Sources

Common values you might see in the Source filter:
- **UI** - Interactive clusters created in Databricks UI
- **API** - Clusters created via REST API
- **JOB** - Job clusters (ephemeral)
- **PIPELINE** - Clusters for Delta Live Tables pipelines
- **SQL** - SQL Warehouse clusters
- **MODELS** - ML model serving clusters

## 💡 Filter Tips

### Getting Workspace Names
To see all available workspace names for filtering:
```sql
SELECT DISTINCT COALESCE(workspace_name, CAST(workspace_id AS STRING)) as workspace_name
FROM system.access.workspaces_latest
ORDER BY workspace_name;
```

### Getting Cluster Sources
To see all available cluster sources:
```sql
SELECT DISTINCT cluster_source
FROM system.compute.clusters
WHERE delete_time IS NULL
ORDER BY cluster_source;
```

## 🎨 Filter UI Appearance

After import, the Clusters page will display:

```
┌─────────────────────────────────────────────────────┐
│  Clusters Page                                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Workspace Name: [All ▼]    Cluster Source: [All ▼]│
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  Active Clusters Across All Workspaces       │ │
│  ├───────────────────────────────────────────────┤ │
│  │ Workspace | Cluster Name | Source | ...      │ │
│  │ Production| my-cluster   | JOB    | ...      │ │
│  │ Dev       | test-cluster | UI     | ...      │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## 🔄 How Filters Work Technically

### Parameter Substitution
Lakeview dashboards use template syntax `{{ parameter_name }}` to inject filter values into SQL queries.

**Before filter selection:**
```sql
WHERE c.delete_time IS NULL
  AND ('All' = 'All' OR workspace_name = 'All')  -- Always true
  AND ('All' = 'All' OR cluster_source = 'All')  -- Always true
```

**After selecting workspace = "Production":**
```sql
WHERE c.delete_time IS NULL
  AND ('Production' = 'All' OR workspace_name = 'Production')  -- Checks workspace
  AND ('All' = 'All' OR cluster_source = 'All')  -- Always true
```

**After selecting both filters:**
```sql
WHERE c.delete_time IS NULL
  AND ('Production' = 'All' OR workspace_name = 'Production')  -- Filters workspace
  AND ('JOB' = 'All' OR cluster_source = 'JOB')  -- Filters source
```

## 🚀 Performance Benefits

**Filtered queries are faster:**
- Reduces rows processed when workspace is selected
- Enables Databricks to optimize query execution
- Particularly beneficial in large multi-workspace environments

**Example:**
- Unfiltered: 10,000 clusters across 50 workspaces
- Filtered to 1 workspace: ~200 clusters
- Query time reduced significantly

## 📊 Use Cases

### 1. Platform Governance
**Goal:** Audit job clusters in production
```
Workspace: Production
Source: JOB
```

### 2. Cost Analysis
**Goal:** Identify UI-created clusters (often left running)
```
Workspace: All
Source: UI
```

### 3. Workspace-Specific Review
**Goal:** Review all resources in a specific workspace
```
Workspace: Analytics
Source: All
```

### 4. Compliance Check
**Goal:** Verify no API clusters in production
```
Workspace: Production
Source: API
```

## 🛠️ Troubleshooting

### Filter Not Appearing
**Issue:** Don't see filter dropdowns after import  
**Solution:** 
1. Ensure you're on the Clusters page
2. Refresh the dashboard
3. Check if parameters are defined in dataset

### No Results When Filtered
**Issue:** Filter applied but table is empty  
**Possible Causes:**
1. No clusters match the filter criteria (correct behavior)
2. Workspace name typo or mismatch
3. Cluster source value not exact match

**Solution:** 
- Reset both filters to "All" to see all data
- Check exact workspace names and sources in system tables

### Filter Values Not Populating
**Issue:** Dropdown is empty or shows unexpected values  
**Solution:**
- Databricks automatically populates dropdowns from query results
- If empty, ensure data exists in system.compute.clusters
- Check permissions on system tables

## 📝 Notes

### Filter vs. Search
- **Filters (dropdowns):** Pre-defined values, parameter-based filtering
- **Search (in table):** Free-text search within visible columns
- Both can be used together for powerful data exploration

### Case Sensitivity
- Workspace name filter is **case-sensitive**
- Cluster source filter is **case-sensitive**
- Use exact values from system tables

### "All" Option
- "All" is a special value that bypasses the filter
- Selecting "All" is equivalent to no filter applied
- Both filters default to "All" on page load

## 🎓 Best Practices

1. **Start broad, narrow down:** Begin with "All/All", then apply filters
2. **Use workspace filter for isolation:** Focus on one workspace at a time
3. **Combine with table search:** Use filters for categories, search for specifics
4. **Save filtered views:** Bookmark URLs with filter parameters applied
5. **Regular audits:** Weekly review with Source = "UI" to find idle clusters

## 📚 Related Documentation

- See `Dashboard_README.md` for complete dashboard documentation
- See `WORKSPACE_NAME_UPDATE.md` for workspace name implementation
- See `Query_Reference.md` for SQL query details

---

**Implementation Date:** March 12, 2026  
**Feature:** Interactive filters for Active Clusters table  
**Status:** ✅ Ready to use after dashboard import
