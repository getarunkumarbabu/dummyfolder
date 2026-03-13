# Active Clusters Duplicate Records Fixed ✅

## Issue Reported
User saw **duplicate cluster_id entries** in the "Active Clusters Across All Workspaces" report.

Example:
```
| cluster_id       | cluster_name | workspace_name |
|------------------|--------------|----------------|
| 1234-567890-abc  | ETL Cluster  | Production     |
| 1234-567890-abc  | ETL Cluster  | Production     | ← DUPLICATE!
| 1234-567890-abc  | ETL Cluster  | Production     | ← DUPLICATE!
```

---

## Root Cause

The `system.compute.clusters` table is a **change tracking table** (CDC-style), not a snapshot table. It contains:

- **Multiple rows per cluster** tracking configuration changes over time
- Each row has a `change_time` timestamp indicating when the record was created
- Records for resize events, node type changes, autoscale adjustments, etc.

### Example: Why One Cluster Has 3 Records

```sql
SELECT cluster_id, cluster_name, change_time, worker_count, delete_time
FROM system.compute.clusters
WHERE cluster_id = '1234-567890-abc'
ORDER BY change_time;
```

**Results**:
```
| cluster_id      | change_time          | worker_count | delete_time |
|-----------------|----------------------|--------------|-------------|
| 1234-567890-abc | 2026-03-01 10:00:00 | 2            | NULL        | ← Created
| 1234-567890-abc | 2026-03-05 14:30:00 | 5            | NULL        | ← Resized
| 1234-567890-abc | 2026-03-10 09:15:00 | 3            | NULL        | ← Resized again
```

**The old query** filtered `WHERE delete_time IS NULL`, which returned **all 3 rows**! 

---

## Solution Applied

### Old Query (Incorrect - Shows Duplicates):
```sql
SELECT
  c.workspace_id,
  c.cluster_id,
  c.cluster_name,
  c.worker_count,
  ...
FROM system.compute.clusters c
LEFT JOIN system.access.workspaces_latest w ON c.workspace_id = w.workspace_id
WHERE c.delete_time IS NULL  -- ❌ Returns ALL records for each cluster
ORDER BY c.create_time DESC
```

**Problem**: Returns every configuration change record for active clusters.

---

### New Query (Correct - Deduplicates):
```sql
WITH latest_cluster_records AS (
  SELECT
    c.*,
    ROW_NUMBER() OVER (
      PARTITION BY c.cluster_id           -- ✅ Group by cluster
      ORDER BY c.change_time DESC         -- ✅ Sort by most recent change
    ) AS rn
  FROM system.compute.clusters c
  WHERE c.delete_time IS NULL
)
SELECT
  c.workspace_id,
  COALESCE(w.workspace_name, CAST(c.workspace_id AS STRING)) AS workspace_name,
  c.cluster_id,
  c.cluster_name,
  c.owned_by,
  c.cluster_source,
  c.driver_node_type,
  c.worker_node_type,
  c.worker_count,
  c.min_autoscale_workers,
  c.max_autoscale_workers,
  c.auto_termination_minutes,
  c.create_time,
  c.dbr_version
FROM latest_cluster_records c
LEFT JOIN system.access.workspaces_latest w ON c.workspace_id = w.workspace_id
WHERE c.rn = 1  -- ✅ Only the most recent record per cluster
ORDER BY c.create_time DESC
```

---

## How the Fix Works

### Step 1: CTE with ROW_NUMBER()
```sql
ROW_NUMBER() OVER (PARTITION BY c.cluster_id ORDER BY c.change_time DESC) AS rn
```

**What this does**:
- `PARTITION BY c.cluster_id` - Creates separate groups for each unique cluster
- `ORDER BY c.change_time DESC` - Sorts each group by most recent change first
- `ROW_NUMBER()` - Assigns rank 1 to the newest record, 2 to second newest, etc.

**Example**:
```
| cluster_id      | change_time          | worker_count | rn |
|-----------------|----------------------|--------------|-----|
| 1234-567890-abc | 2026-03-10 09:15:00 | 3            | 1   | ← LATEST!
| 1234-567890-abc | 2026-03-05 14:30:00 | 5            | 2   |
| 1234-567890-abc | 2026-03-01 10:00:00 | 2            | 3   |
```

### Step 2: Filter to rn = 1
```sql
WHERE c.rn = 1
```

**Only keeps the most recent record** for each cluster_id!

---

## Impact

### Before Fix:
```
| cluster_id       | cluster_name | worker_count | change_time          |
|------------------|--------------|--------------|----------------------|
| 1234-567890-abc  | ETL Cluster  | 2            | 2026-03-01 10:00:00 |
| 1234-567890-abc  | ETL Cluster  | 5            | 2026-03-05 14:30:00 |
| 1234-567890-abc  | ETL Cluster  | 3            | 2026-03-10 09:15:00 |
| 5678-123456-def  | ML Training  | 10           | 2026-02-15 08:00:00 |
```
❌ **4 rows total** (3 duplicates for cluster 1234-567890-abc)

### After Fix:
```
| cluster_id       | cluster_name | worker_count | change_time          |
|------------------|--------------|--------------|----------------------|
| 1234-567890-abc  | ETL Cluster  | 3            | 2026-03-10 09:15:00 | ← Latest config
| 5678-123456-def  | ML Training  | 10           | 2026-02-15 08:00:00 |
```
✅ **2 rows total** (one per unique cluster, showing current configuration)

---

## What This Report Shows Now

The **Active Clusters Across All Workspaces** report now displays:

1. ✅ **One row per unique cluster_id**
2. ✅ **Latest configuration** for each cluster (most recent worker count, node types, etc.)
3. ✅ **Only active clusters** (delete_time IS NULL)
4. ✅ **Current state** of each cluster, not historical changes

### Use Cases:
- **Cost monitoring**: See which clusters are currently running
- **Capacity planning**: Understand current resource allocation
- **Governance**: Identify clusters by owner, workspace, and source
- **Optimization**: Find clusters with autoscaling or auto-termination settings

---

## Technical Details

### Why `change_time` instead of `create_time`?

- `create_time`: When the cluster was **first created** (never changes)
- `change_time`: When this **specific record** was created (updates with each change)

For deduplication, we need `change_time` to get the **latest configuration state**.

### Alternative Approaches Considered:

#### Option 1: MAX(change_time) Subquery
```sql
-- More verbose, same result
SELECT c.*
FROM system.compute.clusters c
INNER JOIN (
  SELECT cluster_id, MAX(change_time) AS latest_change
  FROM system.compute.clusters
  WHERE delete_time IS NULL
  GROUP BY cluster_id
) latest ON c.cluster_id = latest.cluster_id 
        AND c.change_time = latest.latest_change
```

#### Option 2: QUALIFY Clause (Cleaner, if supported)
```sql
-- Simpler syntax, but requires QUALIFY support
SELECT c.*
FROM system.compute.clusters c
WHERE c.delete_time IS NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY c.cluster_id ORDER BY c.change_time DESC) = 1
```

**We chose ROW_NUMBER() with CTE** because:
- ✅ Widely supported in Databricks SQL
- ✅ Clear, readable logic
- ✅ Explicit step-by-step approach

---

## Performance Notes

- The CTE with ROW_NUMBER() is efficient on `system.compute.clusters` (relatively small table)
- Indexing on `cluster_id` and `change_time` helps performance
- No significant performance impact expected (table typically < 10K rows per workspace)

---

## Testing

To verify the fix works, run this query in Databricks:

```sql
-- Check for duplicates in old query
SELECT cluster_id, COUNT(*) AS record_count
FROM system.compute.clusters
WHERE delete_time IS NULL
GROUP BY cluster_id
HAVING COUNT(*) > 1
ORDER BY record_count DESC;
```

**Before fix**: Shows clusters with multiple records
**After fix**: Report shows only 1 row per cluster_id

---

## Files Modified
- `Monitoring Dashboard.lvdash.json`
  - Dataset: `ds_clusters_active`
  - Added CTE with ROW_NUMBER() deduplication
  - Added WHERE rn = 1 filter
  - Query now returns unique clusters only

---

**Date**: March 13, 2026
**Issue**: Duplicate cluster_id entries in Active Clusters report
**Root Cause**: `system.compute.clusters` tracks configuration changes over time
**Solution**: ROW_NUMBER() window function to get latest record per cluster
**Result**: One row per cluster showing current configuration
