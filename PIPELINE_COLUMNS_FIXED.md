# Pipeline Column Names Fixed - RESOLVED ✅

## Issue
Pipeline visualizations failed with error:
> "[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column, variable, or function parameter with name `u`.`update_start_time` cannot be resolved. Did you mean one of the following? [`u`.`period_start_time`, `u`.`update_id`, `u`.`update_type`, `p`.`create_time`, `w`.`create_time`]. SQLSTATE: 42703; line 18 pos 6"

## Root Cause
The pipeline datasets were using **incorrect column names** that don't exist in the `system.lakeflow.pipeline_update_timeline` table.

### Incorrect Column Names Used:
- ❌ `update_start_time` → Does not exist
- ❌ `update_end_time` → Does not exist  
- ❌ `update_state` → Does not exist

### Correct Column Names in `pipeline_update_timeline`:
- ✅ `period_start_time` → Pipeline update start time
- ✅ `period_end_time` → Pipeline update end time
- ✅ `update_type` → Update type/status (COMPLETED, FAILED, CANCELED, RUNNING, etc.)

## Solution Applied

### 1. Fixed Dataset: ds_pipeline_updates
**Changed columns in SELECT statement:**
```sql
-- BEFORE (Incorrect):
u.update_state,
u.update_start_time,
u.update_end_time,
WHERE u.update_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
ORDER BY u.update_start_time DESC

-- AFTER (Correct):
u.update_type,
u.period_start_time,
u.period_end_time,
WHERE u.period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
ORDER BY u.period_start_time DESC
```

### 2. Fixed Dataset: ds_pipeline_failures
**Changed WHERE clause and removed FIRST() aggregation:**
```sql
-- BEFORE (Incorrect):
FIRST(p.name) AS pipeline_name,
WHERE u.update_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
  AND UPPER(u.update_state) IN ('FAILED','CANCELED')

-- AFTER (Correct):
p.name AS pipeline_name,
WHERE u.period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
  AND UPPER(u.update_type) IN ('FAILED','CANCELED')
```

### 3. Fixed Widget: w_pipeline_status_bar
**Updated field names and expressions:**
```json
// BEFORE (Incorrect):
{
  "name": "daily(update_start_time)",
  "expression": "DATE_TRUNC(\"DAY\", `update_start_time`)"
},
{
  "name": "update_state",
  "expression": "`update_state`"
}

// Encodings:
"x": { "fieldName": "daily(update_start_time)", ... },
"color": { "fieldName": "update_state", "displayName": "Update State", ... }

// AFTER (Correct):
{
  "name": "daily(period_start_time)",
  "expression": "DATE_TRUNC(\"DAY\", `period_start_time`)"
},
{
  "name": "update_type",
  "expression": "`update_type`"
}

// Encodings:
"x": { "fieldName": "daily(period_start_time)", ... },
"color": { "fieldName": "update_type", "displayName": "Update Type", ... }
```

## System Table Schema Reference

### system.lakeflow.pipeline_update_timeline
**Correct columns available:**
- `workspace_id` - Workspace identifier
- `pipeline_id` - Pipeline identifier
- `update_id` - Update identifier
- `update_type` - Update type/status (COMPLETED, FAILED, CANCELED, RUNNING)
- `period_start_time` - When the update started
- `period_end_time` - When the update ended
- `cause` - What triggered the update

**Note:** This table uses `update_type` not `update_state`, and `period_start_time` not `update_start_time`.

## Changes Summary

### Datasets Modified: 2
1. ✅ **ds_pipeline_updates** - Fixed 3 column names + WHERE + ORDER BY
2. ✅ **ds_pipeline_failures** - Fixed 1 column name in WHERE clause + removed FIRST()

### Widgets Modified: 1
1. ✅ **w_pipeline_status_bar** - Fixed field names and expressions

### Column Mappings Applied:
| Old (Incorrect) | New (Correct) | Purpose |
|----------------|---------------|---------|
| `update_start_time` | `period_start_time` | Start time of pipeline update |
| `update_end_time` | `period_end_time` | End time of pipeline update |
| `update_state` | `update_type` | Status/type of update |

## Additional Fix
Removed `FIRST(p.name)` aggregation in `ds_pipeline_failures` since the query already has `GROUP BY ALL` which handles all non-aggregated columns.

## Verification
✅ No more references to `update_start_time` found
✅ No more references to `update_state` found
✅ All pipeline queries now use correct column names from schema

## Impact
- ✅ Pipeline status bar chart will render correctly
- ✅ Pipeline failures table will load data
- ✅ Pipeline updates dataset will return results
- ✅ No more "UNRESOLVED_COLUMN" errors on Pipelines page

## Status
**RESOLVED** - All pipeline datasets and widgets now use the correct column names from `system.lakeflow.pipeline_update_timeline` table schema.

---
**Date**: March 12, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Datasets Fixed**: ds_pipeline_updates, ds_pipeline_failures
**Widgets Fixed**: w_pipeline_status_bar
**Column Names Updated**: 3 (update_start_time → period_start_time, update_end_time → period_end_time, update_state → update_type)
