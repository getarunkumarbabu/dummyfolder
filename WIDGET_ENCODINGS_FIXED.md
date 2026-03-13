# Missing Widget Encodings - RESOLVED ✅

## Issue
Dashboard import failed with error:
> "Invalid widget definition is imported. The imported widget definition was invalid so it changed to the default. Here are the details: spec must have required property 'encodings'"

## Root Cause
The widget `w_long_running_jobs` had a table `spec` definition but was **missing the required `encodings` property** containing column definitions.

### Problem Structure (Before):
```json
{
  "name": "w_long_running_jobs",
  "queries": [...],
  "spec": {
    "version": 2,
    "widgetType": "table",
    "allowHTMLByDefault": false,
    "itemsPerPage": 25,
    // ❌ NO encodings property!
    "frame": {...}
  }
}
```

## Solution Applied
Added the complete `encodings` property with column definitions for all 8 fields in the widget.

### Fixed Structure (After):
```json
{
  "name": "w_long_running_jobs",
  "queries": [...],
  "spec": {
    "version": 2,
    "widgetType": "table",
    "encodings": {  // ✅ Added encodings with columns
      "columns": [
        { "fieldName": "name", "title": "Job Name", ... },
        { "fieldName": "workspace_name", "title": "Workspace", ... },
        { "fieldName": "job_id", "title": "Job ID", ... },
        { "fieldName": "total_runs", "title": "Total Runs", ... },
        { "fieldName": "avg_duration_minutes", "title": "Avg Duration (min)", ... },
        { "fieldName": "max_duration_minutes", "title": "Max Duration (min)", ... },
        { "fieldName": "p95_duration_minutes", "title": "P95 Duration (min)", ... },
        { "fieldName": "last_run_time", "title": "Last Run Time", ... }
      ]
    },
    "allowHTMLByDefault": false,
    "itemsPerPage": 25,
    "frame": {...}
  }
}
```

## Column Definitions Added

### 1. name (Job Name)
- **Type**: string
- **Display**: Left-aligned text
- **Searchable**: Yes

### 2. workspace_name (Workspace)
- **Type**: string
- **Display**: Left-aligned text
- **Searchable**: Yes

### 3. job_id (Job ID)
- **Type**: integer
- **Display**: Right-aligned number (format: "0")
- **Searchable**: No

### 4. total_runs (Total Runs)
- **Type**: integer
- **Display**: Right-aligned number (format: "0")
- **Searchable**: No

### 5. avg_duration_minutes (Avg Duration)
- **Type**: number
- **Display**: Right-aligned decimal (format: "0.00")
- **Searchable**: No

### 6. max_duration_minutes (Max Duration)
- **Type**: number
- **Display**: Right-aligned decimal (format: "0.00")
- **Searchable**: No

### 7. p95_duration_minutes (P95 Duration)
- **Type**: number
- **Display**: Right-aligned decimal (format: "0.00")
- **Searchable**: No

### 8. last_run_time (Last Run Time)
- **Type**: datetime
- **Display**: Left-aligned datetime (format: "YYYY-MM-DD HH:mm:ss")
- **Searchable**: No

## Azure Databricks Table Widget Requirements

For **table widgets** in Lakeview dashboards:
1. Must have `"widgetType": "table"`
2. Must have `encodings` property
3. Must have `encodings.columns` array
4. Each column must define:
   - `fieldName`: Matches query field name
   - `type`: Data type (string, integer, number, datetime, etc.)
   - `displayAs`: How to render (string, number, datetime, etc.)
   - `visible`: Whether to show the column
   - `order`: Column display order
   - `title`: Column header text
   - `displayName`: Internal reference name

## Verification Results
✅ Checked all widgets in the dashboard (13 widgets total)
✅ All widgets with `spec` now have proper `encodings`
✅ No more missing encodings errors

### Widget Type Breakdown:
- **Counter widgets**: 3 (all have encodings ✓)
- **Bar charts**: 2 (all have encodings ✓)
- **Line charts**: 1 (all have encodings ✓)
- **Table widgets**: 6 (all have encodings ✓)
- **Text widgets**: 1 (no spec required ✓)

## Impact
- ✅ Dashboard will now import without "invalid widget" errors
- ✅ Long Running Jobs table will render correctly with all 8 columns
- ✅ Table will be paginated (25 items per page)
- ✅ Table will have row numbers
- ✅ Columns will be searchable and properly formatted

## Status
**RESOLVED** - The `w_long_running_jobs` widget now has complete encodings with all 8 column definitions. Dashboard should import successfully without widget validation errors.

---
**Date**: March 12, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Widget Fixed**: w_long_running_jobs
**Lines Added**: ~120 lines (encodings definition)
**Location**: Jobs page, Long Running Jobs table widget
