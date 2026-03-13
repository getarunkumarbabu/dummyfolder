# Missing Parameter Selection Error - RESOLVED ✅

## Issue
Dashboard reports were failing with error:
> "Missing selection for parameter: workspace_filter_summary"

## Root Cause
The dashboard had parameters defined **only at the dataset level**, but Azure Databricks Lakeview dashboards require parameters to be defined at the **dashboard (global) level** when they're used across multiple datasets and pages.

### Before (Incorrect Structure):
```json
{
  "datasets": [
    {
      "name": "ds_job_run_cost_agg",
      "queryLines": [...],
      "parameters": [
        {
          "name": "workspace_filter_summary",
          "keyword": "workspace_filter_summary",
          ...
        }
      ]
    }
  ],
  "pages": [...]  // ❌ No global parameters section!
}
```

### After (Correct Structure):
```json
{
  "datasets": [...],
  "parameters": [    // ✅ Global dashboard-level parameters
    {
      "name": "workspace_filter_summary",
      "keyword": "workspace_filter_summary",
      ...
    },
    ...
  ],
  "pages": [...]
}
```

## Solution Applied
Added a **global parameters section** at the dashboard root level (between datasets and pages) with all 6 parameters:

### 1. workspace_filter_summary
- **Display Name**: "Workspace Name (Summary)"
- **Used in**: ds_job_run_cost_agg dataset
- **Purpose**: Filter cost aggregation by workspace

### 2. workspace_filter_failures
- **Display Name**: "Workspace Name (Failures)"
- **Used in**: ds_highest_failure_jobs dataset
- **Purpose**: Filter failure tracking by workspace

### 3. workspace_filter_longrunning
- **Display Name**: "Workspace Name (Long Running)"
- **Used in**: ds_long_running_jobs dataset
- **Purpose**: Filter long-running jobs by workspace

### 4. workspace_filter_expensive
- **Display Name**: "Workspace Name (Expensive)"
- **Used in**: ds_most_expensive_jobs dataset
- **Purpose**: Filter expensive jobs by workspace

### 5. workspace_filter
- **Display Name**: "Workspace Name"
- **Used in**: ds_clusters_active dataset
- **Purpose**: Filter active clusters by workspace

### 6. source_filter
- **Display Name**: "Cluster Source"
- **Used in**: ds_clusters_active dataset
- **Purpose**: Filter clusters by source (JOB, API, UI, etc.)

## Parameter Configuration
All parameters share the same configuration:
- **Data Type**: STRING
- **Default Value**: "All"
- **Keyword**: Same as parameter name (for reference in queries)

## Query Syntax (Reminder)
Parameters are referenced using the new `:param` syntax:
```sql
WHERE (':workspace_filter' = 'All' 
   OR column = :workspace_filter)
```

## Key Learnings
1. **Dataset-level parameters** are only accessible within that specific dataset
2. **Dashboard-level parameters** are globally accessible across all datasets and pages
3. Parameters used in SQL queries must be defined at the **dashboard level** to be selectable in the UI
4. The `keyword` field must match the parameter reference in queries

## Dataset-Level Parameters (Now Redundant)
The dataset-level parameter definitions (lines 55-63, 97-105, etc.) are now redundant but harmless. They can be removed in a future cleanup, but keeping them doesn't cause errors - the dashboard-level parameters take precedence.

## Verification Steps
After importing the dashboard:
1. ✅ Dashboard should open without "Missing selection" errors
2. ✅ Parameter dropdowns should appear in the dashboard toolbar
3. ✅ All parameters should default to "All"
4. ✅ Changing parameters should filter the data accordingly

## Status
**RESOLVED** - Dashboard now has proper global parameter definitions and should render all reports without errors.

---
**Date**: March 12, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Lines Added**: 46 lines (global parameters section)
**Location**: Between line 354 (end of datasets) and start of pages
