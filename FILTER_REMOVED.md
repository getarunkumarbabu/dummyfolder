# Cluster Source Filter Removed ✅

## Change Summary
Removed the `cluster_source_filter` parameter completely from the dashboard as requested by user.

## What Was Removed

### 1. SQL WHERE Clause Filter
**Location**: `ds_clusters_active` dataset query

**Removed Line**:
```sql
AND (':cluster_source_filter' = 'All' OR c.cluster_source = :cluster_source_filter)
```

**New Query**:
```sql
WHERE c.delete_time IS NULL
ORDER BY c.create_time DESC
```

Now shows **all active clusters** without any filtering.

---

### 2. Dataset-Level Parameter Binding
**Location**: `ds_clusters_active` dataset parameters section

**Removed Block** (9 lines):
```json
"parameters": [
  {
    "name": "cluster_source_filter",
    "keyword": "cluster_source_filter",
    "displayName": "Cluster Source",
    "dataType": "STRING",
    "defaultValue": "All"
  }
]
```

---

### 3. Global Dashboard Parameter
**Location**: Dashboard-level parameters array

**Removed Block** (17 lines):
```json
"parameters": [
  {
    "name": "cluster_source_filter",
    "keyword": "cluster_source_filter",
    "displayName": "Cluster Source",
    "dataType": "STRING",
    "defaultValue": "All",
    "possibleValues": {
      "values": [
        "All",
        "INTERACTIVE",
        "JOB",
        "API",
        "UI"
      ]
    }
  }
]
```

**New Structure**:
```json
"parameters": []
```

---

## Impact

### Before (With Filter):
- ✅ Dropdown to filter by cluster source
- ✅ Could show only INTERACTIVE or JOB clusters
- ❌ Required user to select value
- ❌ Caused "Missing selection" error

### After (No Filter):
- ✅ Shows all active clusters automatically
- ✅ No dropdown in UI
- ✅ No parameter errors
- ✅ Simpler user experience
- ❌ Cannot filter by cluster source type

---

## Dashboard Status

**Active Filters**: None (all removed)

**Clusters Query**: Now returns all active clusters across all workspaces where `delete_time IS NULL`

**User Experience**: 
- No filters/dropdowns in the toolbar
- All visualizations show complete unfiltered data
- Faster load time (no parameter validation)

---

## Files Modified
- `Monitoring Dashboard.lvdash.json`
  - Removed 1 SQL filter condition
  - Removed 9 lines (dataset parameter block)
  - Removed 17 lines (global parameter definition)
  - **Total reduction**: ~27 lines

---

## Related Documentation
- CLUSTER_SOURCE_FILTER_ADDED.md - Previous filter addition (now obsolete)
- PARAMETER_VALUES_ADDED.md - Previous dropdown fix (now obsolete)
- FILTERS_REMOVED.md - Original filter removal documentation

---

**Date**: March 13, 2026
**Action**: Filter Removal
**Files Modified**: Monitoring Dashboard.lvdash.json
**Lines Removed**: 27
**Parameters Remaining**: 0
