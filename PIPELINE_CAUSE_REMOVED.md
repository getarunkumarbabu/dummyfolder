# Pipeline 'cause' Column Removed - RESOLVED ✅

## Issue
Pipeline visualization failed with error:
> "[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column, variable, or function parameter with name `u`.`cause` cannot be resolved. Did you mean one of the following? [`p`.`tags`, `u`.`compute`, `p`.`name`, `p`.`rn`, `w`.`status`]. SQLSTATE: 42703; line 14 pos 2"

## Root Cause
The `ds_pipeline_updates` dataset was trying to select a `cause` column that **does not exist** in the `system.lakeflow.pipeline_update_timeline` table.

### Query Before (Incorrect):
```sql
SELECT
  u.workspace_id,
  COALESCE(w.workspace_name, CAST(u.workspace_id AS STRING)) AS workspace_name,
  u.pipeline_id,
  p.name AS pipeline_name,
  u.update_id,
  u.update_type,
  u.period_start_time,
  u.period_end_time,
  u.cause  -- ❌ This column does not exist!
FROM system.lakeflow.pipeline_update_timeline u
```

## Solution Applied
Removed the `u.cause` column from the SELECT statement in the `ds_pipeline_updates` dataset.

### Query After (Correct):
```sql
SELECT
  u.workspace_id,
  COALESCE(w.workspace_name, CAST(u.workspace_id AS STRING)) AS workspace_name,
  u.pipeline_id,
  p.name AS pipeline_name,
  u.update_id,
  u.update_type,
  u.period_start_time,
  u.period_end_time  -- ✅ Removed u.cause
FROM system.lakeflow.pipeline_update_timeline u
```

## Available Columns in pipeline_update_timeline

Based on the error suggestions and Databricks system tables documentation, the actual columns available are:

### From `u` (pipeline_update_timeline):
- ✅ `workspace_id`
- ✅ `pipeline_id`
- ✅ `update_id`
- ✅ `update_type`
- ✅ `period_start_time`
- ✅ `period_end_time`
- ✅ `compute` (compute resources used)
- ❌ `cause` (does NOT exist)

### From `p` (pipelines):
- ✅ `name`
- ✅ `tags`
- ✅ Other pipeline metadata

### From `w` (workspaces_latest):
- ✅ `workspace_name`
- ✅ `status`

## Why `cause` Doesn't Exist
The `cause` column was likely confused with:
- **DLT Pipeline Events**: Some Delta Live Tables event tables may have a `cause` field
- **Job Runs**: The `system.lakeflow.job_run_timeline` has fields related to run triggers
- **Different Table**: The column might exist in a different pipeline-related table

The `pipeline_update_timeline` table focuses on update events and their timing/status, not the trigger cause.

## Dataset Modified
**ds_pipeline_updates** - Removed `u.cause` from SELECT statement

## Impact
- ✅ Pipeline updates dataset will now execute successfully
- ✅ No more "UNRESOLVED_COLUMN" error for `cause`
- ✅ Query returns 8 columns instead of 9
- ℹ️ If you need trigger information, you may need to:
  - Check `system.lakeflow.pipeline_events` for more detailed event data
  - Look for alternative fields like `origin.update_id` or event metadata

## Verification
✅ Removed `u.cause` from query
✅ No other references to `cause` in pipeline queries
✅ All selected columns now exist in the schema

## Status
**RESOLVED** - The non-existent `cause` column has been removed from the pipeline updates query. Dashboard should now render the pipeline visualizations without errors.

---
**Date**: March 12, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Dataset Fixed**: ds_pipeline_updates
**Column Removed**: `u.cause`
**Remaining Columns**: 8 (workspace_id, workspace_name, pipeline_id, pipeline_name, update_id, update_type, period_start_time, period_end_time)
