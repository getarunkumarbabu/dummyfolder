# Long Running Jobs Update - March 12, 2026

## 📋 Change Summary

**Removed:** "Top Failing Jobs (Bar)" visualization  
**Added:** "Long Running Jobs" table with performance metrics  
**Reason:** Bar chart was not providing useful information; replaced with actionable performance data

---

## ✅ What Was Changed

### 1. New Dataset Added: `ds_long_running_jobs`

**Purpose:** Identify jobs with long execution times to help with performance optimization

**SQL Query Features:**
- Analyzes last 30 days of job runs
- Calculates duration in minutes for each job run
- Aggregates performance metrics per job
- Includes workspace name for multi-workspace visibility
- Filters out jobs with avg duration < 10 minutes (focuses on meaningful data)

**Metrics Captured:**
- `name` - Job name
- `workspace_name` - Human-readable workspace identifier
- `job_id` - Unique job identifier
- `total_runs` - Number of times the job ran in last 30 days
- `avg_duration_minutes` - Average execution time
- `max_duration_minutes` - Longest execution time
- `p95_duration_minutes` - 95th percentile duration (filters out outliers)
- `last_run_time` - Most recent execution timestamp

**Filter Parameter:**
- `workspace_filter_longrunning` - Filter by workspace name (default: "All")

---

### 2. Widget Replaced on Jobs Page

**Old Widget:**
- Name: `w_top10_failure_bar`
- Type: Bar chart
- Data: Top 10 failing jobs (visual)
- Issue: Redundant with "Highest Failure Jobs" table above it

**New Widget:**
- Name: `w_long_running_jobs`
- Type: Table
- Data: Long-running jobs with performance metrics
- Position: Same location (x=0, y=20, width=6, height=10)
- Height: Increased from 7 to 10 for better readability

---

## 🎯 Use Cases

### Use Case 1: Performance Optimization
**Scenario:** Identify jobs that are consuming excessive compute time

**Steps:**
1. Open Jobs page
2. Review "Long Running Jobs" table
3. Sort by `avg_duration_minutes` (already default)
4. Identify top long-running jobs
5. Investigate query optimization opportunities

**Value:** Reduce costs by optimizing slow jobs

---

### Use Case 2: Workspace-Specific Performance Review
**Scenario:** Each team wants to optimize their workspace

**Steps:**
1. Apply workspace filter: Select your workspace
2. Review jobs specific to your team
3. Focus on jobs with high P95 duration (consistency issues)
4. Compare avg vs max duration (identify variance)

**Value:** Team-level accountability for performance

---

### Use Case 3: Cost-Performance Correlation
**Scenario:** Understand if long-running jobs are driving costs

**Steps:**
1. Review "Long Running Jobs" table
2. Note top 5 jobs by avg duration
3. Scroll up to "Most Expensive Jobs" table
4. Check if same jobs appear in both lists
5. Prioritize optimization of jobs in both lists

**Value:** Target optimization efforts for maximum ROI

---

### Use Case 4: Trend Analysis
**Scenario:** Monitor if job performance is degrading over time

**Steps:**
1. Export "Long Running Jobs" table today
2. Re-export after 1 week
3. Compare avg_duration_minutes for same jobs
4. Identify jobs with increasing duration trends

**Value:** Proactive detection of performance degradation

---

## 📊 Jobs Page Layout (After Update)

```
┌────────────────────────────────────────────────────────┐
│ Jobs Page                                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│ [Counter] Total Jobs Run                              │
│                                                        │
│ ┌────────────────────────────────────────────────────┐│
│ │ Job Run Timeline                                   ││
│ │ (Table: status, duration, workspace, timestamps)   ││
│ └────────────────────────────────────────────────────┘│
│                                                        │
│ ┌──────────────────────┐  ┌──────────────────────────┐│
│ │ Highest Failure Jobs │  │ Most Expensive Jobs      ││
│ │ — Last 30 Days       │  │ — Last 30 Days           ││
│ │                      │  │                          ││
│ │ 🎛️ Workspace Filter  │  │ 🎛️ Workspace Filter      ││
│ │                      │  │                          ││
│ │ (Table with failure  │  │ (Table with cost data)   ││
│ │  metrics)            │  │                          ││
│ └──────────────────────┘  └──────────────────────────┘│
│                                                        │
│ ┌────────────────────────────────────────────────────┐│
│ │ ⭐ NEW: Long Running Jobs — Last 30 Days          ││
│ │                                                    ││
│ │ 🎛️ Workspace Filter                                ││
│ │                                                    ││
│ │ (Table: job name, workspace, avg/max/P95 duration)││
│ │                                                    ││
│ └────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

---

## 📈 Interpreting the Metrics

### Average Duration
**What it means:** Typical execution time for this job  
**Use for:** Identifying consistently slow jobs  
**Action:** If > 60 minutes, consider optimization

### Max Duration
**What it means:** Longest execution time recorded  
**Use for:** Identifying outliers or data spikes  
**Action:** Compare to avg - large difference suggests variability

### P95 Duration
**What it means:** 95% of runs complete within this time  
**Use for:** Understanding "normal worst case"  
**Action:** Better indicator than max for SLAs

### Comparison Pattern
```
Job A:
  avg = 30 min
  max = 35 min
  p95 = 33 min
  → Consistent performance, predictable

Job B:
  avg = 30 min
  max = 180 min
  p95 = 40 min
  → Inconsistent, investigate outliers
```

---

## 🔍 Performance Optimization Workflow

### Step 1: Identify Targets
1. Open Long Running Jobs table
2. Filter to your workspace (if needed)
3. Note jobs with:
   - avg_duration > 60 minutes, OR
   - High variance (max >> p95), OR
   - Many runs with high duration

### Step 2: Investigate
1. Click job_id to open in Databricks
2. Review job configuration:
   - Cluster size
   - Number of tasks
   - Data volume processed
3. Check job run timeline for failure patterns

### Step 3: Optimize
**Common optimization strategies:**
- **Increase cluster size** for compute-bound jobs
- **Optimize queries** for data-bound jobs
- **Add caching** for repeated data access
- **Partition data** to enable parallelism
- **Remove unnecessary steps** in pipeline

### Step 4: Measure
1. Wait 1 week after optimization
2. Re-check Long Running Jobs table
3. Compare new avg_duration to baseline
4. Validate cost impact in Most Expensive Jobs

---

## 🎛️ Filter Usage

### Filter Parameter: `workspace_filter_longrunning`

**Display Name:** "Workspace Name"  
**Default Value:** "All"  
**Behavior:** Same as other workspace filters in the dashboard

**Examples:**
```
Filter = "All"
  → Shows long-running jobs from all workspaces
  → Use for: Platform-wide optimization priorities

Filter = "Production"
  → Shows only Production workspace jobs
  → Use for: Production performance review

Filter = "Analytics"
  → Shows only Analytics workspace jobs
  → Use for: Data engineering optimization
```

---

## 💡 Pro Tips

### Tip 1: Combine with Cost Data
Long duration doesn't always mean high cost - check both!
- High duration + High cost = Top priority
- High duration + Low cost = Lower priority (unless SLA issue)
- Low duration + High cost = Check cluster configuration

### Tip 2: Watch the P95
P95 is more actionable than max:
- Max can be skewed by one-off incidents
- P95 represents "typical worst case"
- Use P95 for capacity planning and SLAs

### Tip 3: Track Total Runs
Jobs with many runs have compound impact:
- 50 runs × 10 min avg = 500 min total
- 5 runs × 30 min avg = 150 min total
- First job is better optimization target despite shorter duration

### Tip 4: Filter for Focus
Use workspace filter during team reviews:
- Filter to team's workspace
- Each team owns their optimization
- Reduces noise from other teams' jobs

### Tip 5: Export for Trending
Export table monthly:
- Track duration trends over time
- Measure optimization impact
- Report to stakeholders

---

## 🔧 SQL Query Details

### Query Logic Explained

```sql
WITH job_runs AS (
  -- Calculate duration for each job run
  SELECT
    workspace_id,
    job_id,
    run_id,
    period_start_time,
    period_end_time,
    TIMESTAMPDIFF(MINUTE, period_start_time, period_end_time) AS duration_minutes,
    result_state
  FROM system.lakeflow.job_run_timeline
  WHERE period_end_time >= CURRENT_DATE() - INTERVAL 30 DAYS
    AND period_end_time IS NOT NULL
    AND period_start_time IS NOT NULL
    AND result_state IS NOT NULL
),
most_recent_jobs AS (
  -- Get current job names (jobs can be renamed)
  SELECT *, ROW_NUMBER() OVER(PARTITION BY workspace_id, job_id ORDER BY change_time DESC) AS rn
  FROM system.lakeflow.jobs QUALIFY rn = 1
)
SELECT
  FIRST(j.name) AS name,
  jr.workspace_id,
  COALESCE(w.workspace_name, CAST(jr.workspace_id AS STRING)) AS workspace_name,
  jr.job_id,
  COUNT(*) AS total_runs,
  ROUND(AVG(jr.duration_minutes), 2) AS avg_duration_minutes,
  MAX(jr.duration_minutes) AS max_duration_minutes,
  ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY jr.duration_minutes), 2) AS p95_duration_minutes,
  MAX(jr.period_end_time) AS last_run_time
FROM job_runs jr
LEFT JOIN most_recent_jobs j ON jr.workspace_id = j.workspace_id AND jr.job_id = j.job_id
LEFT JOIN system.access.workspaces_latest w ON jr.workspace_id = w.workspace_id
WHERE ('{{ workspace_filter_longrunning }}' = 'All' OR COALESCE(w.workspace_name, CAST(jr.workspace_id AS STRING)) = '{{ workspace_filter_longrunning }}')
GROUP BY jr.workspace_id, jr.job_id, workspace_name
HAVING AVG(jr.duration_minutes) >= 10  -- Focus on meaningful durations
ORDER BY avg_duration_minutes DESC
LIMIT 50
```

### Key Features:
- ✅ Uses `TIMESTAMPDIFF` for accurate duration calculation
- ✅ Joins with job metadata for current job names
- ✅ Joins with workspace table for human-readable names
- ✅ Uses `PERCENTILE_CONT` for P95 calculation
- ✅ Filters out very short jobs (< 10 min avg)
- ✅ Limits to top 50 to keep table manageable
- ✅ Supports workspace filtering via parameter

---

## 📊 Dashboard Statistics

**Before Update:**
- Total Datasets: 9
- Total Widgets: 13
- Jobs Page Widgets: 5

**After Update:**
- Total Datasets: 10 (added `ds_long_running_jobs`)
- Total Widgets: 13 (replaced, not added)
- Jobs Page Widgets: 5 (same count, different content)

**File Size:**
- Before: 1,895 lines
- After: 1,940 lines
- Increase: +45 lines (new dataset and widget definition)

---

## 🚀 Deployment

### Pre-Deployment
✅ JSON validated successfully  
✅ New dataset added  
✅ Old widget removed  
✅ New widget configured  
✅ Filter parameter defined  

### To Deploy
1. **Import** updated `Monitoring Dashboard.lvdash.json` into Databricks
2. **Replace** existing dashboard (or create new version)
3. **Refresh** dashboard to load data
4. **Test** workspace filter functionality
5. **Share** with teams

### Post-Deployment Validation
- [ ] Dashboard imports without errors
- [ ] Long Running Jobs table displays data
- [ ] Workspace filter works correctly
- [ ] Metrics are calculated correctly (avg, max, P95)
- [ ] Old bar chart is no longer visible

---

## 📝 Table Columns Reference

| Column | Type | Description | Sort Priority |
|--------|------|-------------|---------------|
| name | String | Job name | - |
| workspace_name | String | Workspace (human-readable) | - |
| job_id | Integer | Unique job identifier | - |
| total_runs | Integer | Number of executions | Secondary |
| avg_duration_minutes | Decimal | Average execution time | **Primary** |
| max_duration_minutes | Integer | Longest execution time | Tertiary |
| p95_duration_minutes | Decimal | 95th percentile duration | Secondary |
| last_run_time | Timestamp | Most recent execution | - |

**Default Sort:** `avg_duration_minutes DESC` (highest average at top)

---

## 🐛 Troubleshooting

### Issue: No data in table
**Possible Causes:**
1. No jobs have avg duration ≥ 10 minutes (HAVING clause)
2. No jobs ran in last 30 days
3. System tables have no data

**Solution:**
- Check `system.lakeflow.job_run_timeline` for recent data
- Verify jobs exist with: `SELECT COUNT(*) FROM system.lakeflow.job_run_timeline WHERE period_end_time >= CURRENT_DATE() - INTERVAL 30 DAYS`
- Consider lowering HAVING threshold if needed

### Issue: Durations seem incorrect
**Possible Causes:**
1. Job runs have NULL start/end times
2. Clock skew between nodes
3. Long-running background tasks

**Solution:**
- Check WHERE clause filters NULL timestamps
- Verify with: `SELECT period_start_time, period_end_time FROM system.lakeflow.job_run_timeline LIMIT 10`
- Cross-reference with Databricks UI job run times

### Issue: P95 equals avg (or seems wrong)
**Possible Causes:**
1. Job has very few runs (< 20)
2. Job has very consistent duration
3. Data aggregation issue

**Solution:**
- Check `total_runs` column - low run count affects P95
- Verify consistency by comparing avg, max, and P95
- Wait for more data to accumulate

### Issue: Filter not working
**Possible Causes:**
1. Workspace names not in `system.access.workspaces_latest`
2. Parameter not configured correctly
3. Dashboard not refreshed after import

**Solution:**
- Verify: `SELECT * FROM system.access.workspaces_latest`
- Check parameter name matches: `workspace_filter_longrunning`
- Refresh dashboard and clear browser cache

---

## 📚 Related Documentation

- **ALL_FILTERS_GUIDE.md** - Complete filter guide (includes this new filter)
- **Dashboard_README.md** - Full dashboard documentation
- **JOBS_FILTERS.md** - Other Jobs page filters
- **Query_Reference.md** - SQL patterns and best practices

---

## ✅ Summary

### What Changed
❌ Removed: Top Failing Jobs (Bar) - redundant visualization  
✅ Added: Long Running Jobs table - actionable performance data  
✅ Added: New dataset `ds_long_running_jobs` with performance metrics  
✅ Added: Workspace filter for long-running jobs  

### Why It Matters
- **Performance optimization** becomes data-driven
- **Cost reduction** opportunities identified
- **SLA management** enabled with P95 metrics
- **Team accountability** through workspace filtering
- **Trend analysis** supported with exportable data

### Next Steps
1. Import updated dashboard
2. Review long-running jobs in your workspaces
3. Start optimization efforts on top targets
4. Track improvements over time

---

**Update Date:** March 12, 2026  
**Dashboard Version:** 1.5  
**Status:** ✅ Ready for Production
