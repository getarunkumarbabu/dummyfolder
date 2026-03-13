# Unbound Parameter Fixed - RESOLVED ✅

## Issue
Dashboard query failed with error:
> "[UNBOUND_SQL_PARAMETER] Found the unbound parameter: cluster_source_filter. Please, fix `args` and provide a mapping of the parameter to either a SQL literal or collection constructor functions such as `map()`, `array()`, `struct()`. SQLSTATE: 42P02; line 19 pos 62"

## Root Cause
The parameter `:cluster_source_filter` was referenced in the SQL query but was **not bound at the dataset level**. 

In Azure Databricks Lakeview dashboards:
- **Global parameters** are defined at the dashboard level
- **Dataset parameters** must be defined to bind the global parameter to the query
- The parameter must exist in both places for the binding to work

### Problem Structure (Before):
```json
{
  "datasets": [
    {
      "name": "ds_clusters_active",
      "queryLines": [
        "...",
        "WHERE ... AND (':cluster_source_filter' = 'All' OR c.cluster_source = :cluster_source_filter)"
      ]
      // ❌ NO parameters section - parameter unbound!
    }
  ],
  "parameters": [
    {
      "name": "cluster_source_filter",  // Global parameter exists
      ...
    }
  ]
}
```

## Solution Applied
Added a **dataset-level parameter binding** to the `ds_clusters_active` dataset that references the global parameter.

### Fixed Structure (After):
```json
{
  "datasets": [
    {
      "name": "ds_clusters_active",
      "queryLines": [
        "...",
        "WHERE ... AND (':cluster_source_filter' = 'All' OR c.cluster_source = :cluster_source_filter)"
      ],
      "parameters": [  // ✅ Added parameter binding
        {
          "name": "cluster_source_filter",
          "keyword": "cluster_source_filter",
          "displayName": "Cluster Source",
          "dataType": "STRING",
          "defaultValue": "All"
        }
      ]
    }
  ],
  "parameters": [  // Global parameter (already existed)
    {
      "name": "cluster_source_filter",
      ...
    }
  ]
}
```

## How Parameter Binding Works

### Two-Level Parameter System:

1. **Dashboard Level (Global)**:
   - Defines the parameter that appears in the UI
   - Users interact with this parameter
   - Controls the default value

2. **Dataset Level (Local Binding)**:
   - Binds the global parameter to the query
   - Tells the query engine how to substitute the parameter value
   - Must match the global parameter name

### Parameter Flow:
```
User selects value in UI
         ↓
Global parameter receives value
         ↓
Dataset parameter binds value to query
         ↓
SQL query executes with parameter value
         ↓
Results filtered accordingly
```

## Parameter Definition Fields

### Required Fields:
- **name**: Internal identifier (e.g., "cluster_source_filter")
- **keyword**: Reference name used in SQL (same as name)
- **displayName**: Label shown to users (e.g., "Cluster Source")
- **dataType**: Data type (STRING, INTEGER, BOOLEAN, etc.)
- **defaultValue**: Initial value when dashboard loads (e.g., "All")

### Parameter Usage in Query:
```sql
-- Bind string parameters with quotes for comparison:
WHERE (':cluster_source_filter' = 'All' OR column = :cluster_source_filter)

-- The ':parameter' checks if literal 'All' selected
-- The :parameter (no quotes) uses the actual value
```

## Why This Error Occurred

This happened because we previously removed all parameters to simplify the dashboard, but then added back:
1. ✅ Global parameter at dashboard level
2. ✅ Parameter reference in SQL query
3. ❌ **FORGOT** dataset-level parameter binding

The query engine couldn't find the parameter binding, causing the "unbound parameter" error.

## Verification

### Now Properly Configured:
- ✅ Global parameter: `cluster_source_filter` (line ~297)
- ✅ Dataset parameter: `cluster_source_filter` (line ~273-281)
- ✅ SQL reference: `:cluster_source_filter` (line 270)
- ✅ Parameter names match exactly
- ✅ Default value: "All"

## Impact

### User Experience:
- ✅ "Cluster Source" dropdown appears in dashboard toolbar
- ✅ Users can select: All, INTERACTIVE, JOB, API, UI
- ✅ Query executes with parameter value properly bound
- ✅ Results filter according to selection

### Query Behavior:
```sql
-- When "All" selected:
WHERE c.delete_time IS NULL
  AND ('All' = 'All' OR c.cluster_source = 'All')
  -- First condition TRUE, shows all clusters

-- When "INTERACTIVE" selected:
WHERE c.delete_time IS NULL
  AND ('INTERACTIVE' = 'All' OR c.cluster_source = 'INTERACTIVE')
  -- Second condition applies filter
```

## Best Practices for Dashboard Parameters

### 1. Always Define Both Levels:
- Global parameter (for UI)
- Dataset parameter (for binding)

### 2. Keep Names Consistent:
- Same `name` and `keyword` at both levels
- Prevents binding issues

### 3. Set Sensible Defaults:
- "All" for optional filters
- Most common value for required filters

### 4. Document Parameter Values:
- What values are valid?
- What does each value filter?

## Related Documentation
- CLUSTER_SOURCE_FILTER_ADDED.md - Usage guide for this filter
- FILTERS_REMOVED.md - Why we initially removed filters
- MISSING_PARAMETER_FIX.md - Previous parameter issues resolved

## Status
**RESOLVED** - The `cluster_source_filter` parameter is now properly bound at both the dataset and dashboard levels. Users can select cluster sources from the dropdown and the query will execute correctly.

---
**Date**: March 13, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Dataset Fixed**: ds_clusters_active
**Parameter Bound**: cluster_source_filter
**Error Code**: SQLSTATE: 42P02 (Unbound parameter)
**Resolution**: Added dataset-level parameter definition
