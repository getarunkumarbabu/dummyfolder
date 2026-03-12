# Query Reference Guide - Databricks Monitoring Dashboard

## Dataset Queries Quick Reference

### 1. Job Run Timeline (`ds_job_run_timeline`)
```sql
SELECT workspace_id, job_id, run_id, period_start_time, period_end_time, result_state
FROM system.lakeflow.job_run_timeline
WHERE result_state IS NOT NULL
  AND period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
```
**Purpose**: Track all job run outcomes over time  
**Key Fields**: result_state (SUCCEEDED, FAILED, ERROR, TIMED_OUT, SKIPPED)  
**Use Case**: Status trending and failure detection

---

### 2. Job Run Cost Aggregation (`ds_job_run_cost_agg`)
```sql
WITH jobs_usage_with_list_cost AS (
  SELECT t1.*, t1.usage_quantity * list_prices.pricing.default AS list_cost
  FROM system.billing.usage t1
  INNER JOIN system.billing.list_prices list_prices
    ON t1.cloud = list_prices.cloud
   AND t1.sku_name = list_prices.sku_name
   AND t1.usage_start_time >= list_prices.price_start_time
   AND (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)
  WHERE t1.sku_name LIKE '%JOBS%'
    AND usage_date >= CURRENT_DATE() - INTERVAL 30 DAYS
),
jobs_usage_per_workspace AS (
  SELECT workspace_id, SUM(list_cost) AS list_cost
  FROM jobs_usage_with_list_cost GROUP BY ALL
)
SELECT
  t1.workspace_id,
  COUNT(DISTINCT t1.job_id)  AS num_jobs,
  COUNT(DISTINCT t1.run_id)  AS num_runs,
  FIRST(t2.list_cost)        AS list_cost
FROM system.lakeflow.job_run_timeline t1
LEFT JOIN jobs_usage_per_workspace t2 USING (workspace_id)
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY ALL
ORDER BY list_cost DESC
```
**Purpose**: Aggregate job metrics and costs per workspace  
**Key Metrics**: Number of jobs, runs, and total cost  
**Use Case**: Workspace-level cost allocation and comparison

---

### 3. Highest Failure Jobs (`ds_highest_failure_jobs`)
```sql
WITH terminal_statuses AS (
  SELECT workspace_id, job_id,
    CASE WHEN result_state IN ('ERROR','FAILED','TIMED_OUT') THEN 1 ELSE 0 END AS is_failure,
    period_end_time AS last_seen_date
  FROM system.lakeflow.job_run_timeline
  WHERE result_state IS NOT NULL
    AND period_end_time >= CURRENT_DATE() - INTERVAL 30 DAYS
),
most_recent_jobs AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, job_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.jobs QUALIFY rn = 1
)
SELECT
  FIRST(t2.name) AS name,
  t1.workspace_id,
  t1.job_id,
  COUNT(*) AS runs,
  SUM(is_failure) AS failures,
  (1 - COALESCE(TRY_DIVIDE(SUM(is_failure), COUNT(*)), 0)) * 100 AS success_ratio,
  MAX(t1.last_seen_date) AS last_seen_date
FROM terminal_statuses t1
LEFT JOIN most_recent_jobs t2 USING (workspace_id, job_id)
GROUP BY ALL
ORDER BY failures DESC
```
**Purpose**: Identify jobs with highest failure counts  
**Key Metrics**: Total runs, failures, success ratio percentage  
**Pattern**: ROW_NUMBER() window function to get most recent job metadata  
**Use Case**: Reliability improvements and troubleshooting priorities

---

### 4. Most Expensive Jobs (`ds_most_expensive_jobs`)
```sql
WITH list_cost_per_job AS (
  SELECT
    t1.workspace_id,
    t1.usage_metadata.job_id,
    COUNT(DISTINCT t1.usage_metadata.job_run_id) AS runs,
    SUM(t1.usage_quantity * list_prices.pricing.default) AS list_cost,
    FIRST(identity_metadata.run_as, TRUE) AS run_as,
    MAX(t1.usage_end_time) AS last_seen_date
  FROM system.billing.usage t1
  INNER JOIN system.billing.list_prices list_prices
    ON t1.cloud = list_prices.cloud
   AND t1.sku_name = list_prices.sku_name
   AND t1.usage_start_time >= list_prices.price_start_time
   AND (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)
  WHERE t1.sku_name LIKE '%JOBS%'
    AND t1.usage_metadata.job_id IS NOT NULL
    AND t1.usage_date >= CURRENT_DATE() - INTERVAL 30 DAY
  GROUP BY ALL
),
most_recent_jobs AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, job_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.jobs QUALIFY rn = 1
)
SELECT
  t2.name,
  t1.job_id,
  t1.workspace_id,
  t1.runs,
  t1.run_as,
  SUM(t1.list_cost) AS list_cost,
  t1.last_seen_date
FROM list_cost_per_job t1
LEFT JOIN most_recent_jobs t2 USING (workspace_id, job_id)
GROUP BY ALL
ORDER BY list_cost DESC
```
**Purpose**: Rank jobs by cost for optimization  
**Key Fields**: usage_metadata.job_id, identity_metadata.run_as  
**Cost Calculation**: usage_quantity × list_price  
**Use Case**: Cost optimization and chargeback

---

### 5. Billing 30-60 Day Comparison (`ds_billing_30_60_days`)
```sql
WITH jobs_usage_with_list_cost AS (
  SELECT t1.*, t1.usage_quantity * list_prices.pricing.default AS list_cost
  FROM system.billing.usage t1
  INNER JOIN system.billing.list_prices list_prices
    ON t1.cloud = list_prices.cloud
   AND t1.sku_name = list_prices.sku_name
   AND t1.usage_start_time >= list_prices.price_start_time
   AND (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)
  WHERE t1.sku_name LIKE '%JOBS%'
)
SELECT
  sku_name,
  SUM(list_cost) AS spend,
  SUM(CASE WHEN usage_end_time BETWEEN DATE_ADD(CURRENT_DATE(), -30) AND CURRENT_DATE() 
           THEN list_cost ELSE 0 END) AS Last30DaySpend,
  SUM(CASE WHEN usage_end_time BETWEEN DATE_ADD(CURRENT_DATE(), -60) AND DATE_ADD(CURRENT_DATE(), -31) 
           THEN list_cost ELSE 0 END) AS Last30to60DaySpend,
  TRY_DIVIDE(
    SUM(CASE WHEN usage_end_time BETWEEN DATE_ADD(CURRENT_DATE(), -30) AND CURRENT_DATE() 
             THEN list_cost ELSE 0 END)
    - SUM(CASE WHEN usage_end_time BETWEEN DATE_ADD(CURRENT_DATE(), -60) AND DATE_ADD(CURRENT_DATE(), -31) 
             THEN list_cost ELSE 0 END),
    SUM(CASE WHEN usage_end_time BETWEEN DATE_ADD(CURRENT_DATE(), -60) AND DATE_ADD(CURRENT_DATE(), -31) 
             THEN list_cost ELSE 0 END)
  ) * 100 AS Last30DayGrowth
FROM jobs_usage_with_list_cost
GROUP BY ALL
```
**Purpose**: Period-over-period cost comparison  
**Metrics**: Current spend, previous spend, growth percentage  
**Pattern**: CASE statements for time bucketing  
**Use Case**: Budget tracking and forecast validation

---

### 6. Pipeline Update Timeline (`ds_pipeline_updates`)
```sql
WITH most_recent_pipelines AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, pipeline_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.pipelines QUALIFY rn = 1
)
SELECT
  u.workspace_id,
  u.pipeline_id,
  FIRST(p.name) AS pipeline_name,
  u.update_id,
  u.update_state,
  u.update_start_time,
  u.update_end_time,
  u.cause
FROM system.lakeflow.pipeline_update_timeline u
LEFT JOIN most_recent_pipelines p USING (workspace_id, pipeline_id)
WHERE u.update_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
ORDER BY u.update_start_time DESC
```
**Purpose**: Track DLT pipeline executions  
**Key Fields**: update_state (COMPLETED, FAILED, CANCELED, RUNNING), cause  
**Use Case**: Pipeline reliability monitoring

---

### 7. Pipeline Failures (`ds_pipeline_failures`)
```sql
WITH most_recent_pipelines AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, pipeline_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.pipelines QUALIFY rn = 1
)
SELECT
  u.workspace_id,
  u.pipeline_id,
  FIRST(p.name) AS pipeline_name,
  COUNT(*) AS failed_updates
FROM system.lakeflow.pipeline_update_timeline u
LEFT JOIN most_recent_pipelines p USING (workspace_id, pipeline_id)
WHERE u.update_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
  AND UPPER(u.update_state) IN ('FAILED','CANCELED')
GROUP BY ALL
ORDER BY failed_updates DESC
```
**Purpose**: Identify problematic pipelines  
**Filter**: Failed and Canceled states only  
**Use Case**: Prioritize pipeline fixes

---

### 8. Active Clusters (`ds_clusters_active`)
```sql
SELECT
  workspace_id,
  cluster_id,
  cluster_name,
  owned_by,
  cluster_source,
  driver_node_type,
  worker_node_type,
  worker_count,
  min_autoscale_workers,
  max_autoscale_workers,
  auto_termination_minutes,
  create_time,
  dbr_version
FROM system.compute.clusters
WHERE delete_time IS NULL
ORDER BY create_time DESC
```
**Purpose**: Cluster inventory across all workspaces  
**Filter**: Only active clusters (not deleted)  
**Use Case**: Governance, cost control, compliance audits

---

### 9. Daily Billing Time Series (`ds_billing_daily_timeseries`)
```sql
SELECT
  DATE_TRUNC('DAY', usage_start_time) AS day,
  billing_origin_product,
  workspace_id,
  ROUND(SUM(usage_quantity * list_prices.pricing.default), 2) AS list_cost
FROM system.billing.usage t1
INNER JOIN system.billing.list_prices list_prices
  ON t1.cloud = list_prices.cloud
 AND t1.sku_name = list_prices.sku_name
 AND t1.usage_start_time >= list_prices.price_start_time
 AND (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)
WHERE t1.usage_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY 1, 2, 3
ORDER BY 1
```
**Purpose**: Daily cost trending by workspace and product  
**Key Fields**: billing_origin_product (JOBS, SQL, NOTEBOOKS, etc.)  
**Pattern**: DATE_TRUNC for daily aggregation  
**Use Case**: Cost trend analysis and anomaly detection

---

## Common Query Patterns

### Getting Most Recent Records
```sql
WITH most_recent AS (
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, entity_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.entity QUALIFY rn = 1
)
```

### Joining with List Prices
```sql
INNER JOIN system.billing.list_prices list_prices
  ON t1.cloud = list_prices.cloud
 AND t1.sku_name = list_prices.sku_name
 AND t1.usage_start_time >= list_prices.price_start_time
 AND (t1.usage_end_time <= list_prices.price_end_time OR list_prices.price_end_time IS NULL)
```

### Calculating Success Ratios
```sql
(1 - COALESCE(TRY_DIVIDE(SUM(is_failure), COUNT(*)), 0)) * 100 AS success_ratio
```

### Time-Based Filtering (30 days)
```sql
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
```

### Safe Division
```sql
TRY_DIVIDE(numerator, denominator)  -- Returns NULL if denominator is 0
```

## Performance Tips

1. **Use WHERE clauses** to filter by workspace_id when possible
2. **Limit time windows** - shorter periods = faster queries
3. **Avoid SELECT *** - specify only needed columns
4. **Use QUALIFY** instead of subqueries with ROW_NUMBER
5. **Consider materialized views** for frequently-run queries
6. **Index on** workspace_id, job_id, cluster_id, usage_date

## Query Modification Examples

### Filter to Specific Workspaces
```sql
WHERE workspace_id IN ('1234567890123456', '6543210987654321')
  AND period_start_time >= CURRENT_DATE() - INTERVAL 30 DAYS
```

### Change Time Window to 7 Days
```sql
WHERE period_start_time >= CURRENT_DATE() - INTERVAL 7 DAYS
```

### Add User/Owner Filtering
```sql
WHERE owned_by = 'user@company.com'
```

### Filter by Job Name Pattern
```sql
WHERE name LIKE 'prod_%'
```

### Exclude System Jobs
```sql
WHERE cluster_source NOT IN ('SYSTEM', 'INTERNAL')
```

---

**Note**: All queries use System Tables which require:
- System Tables enabled on your Databricks account
- SELECT permissions on system.* schemas
- Pro or Serverless SQL Warehouse
