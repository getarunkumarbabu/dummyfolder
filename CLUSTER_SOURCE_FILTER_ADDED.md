# Cluster Source Filter Added - Interactive Cluster Filtering ✅

## User Question
"How can users see only interactive clusters in the 'Active Clusters Across All Workspaces' report? Is there any filter given to consumers to filter output in the report?"

## Solution Applied
Added a **Cluster Source Filter** parameter that allows users to filter clusters by their source type.

## How to Use the Filter

### Step 1: Locate the Filter
When you open the dashboard, you'll see a parameter dropdown at the top labeled:
- **"Cluster Source"**

### Step 2: Select Filter Value
Click the dropdown and choose from:

| Filter Option | What It Shows |
|--------------|---------------|
| **All** (Default) | Shows all clusters regardless of source |
| **UI** | Shows only clusters created through Databricks UI |
| **API** | Shows only clusters created via API |
| **JOB** | Shows only job clusters (ephemeral, created by jobs) |
| **INTERACTIVE** | Shows only interactive clusters (all-purpose clusters) |

### Step 3: View Filtered Results
The "Active Clusters Across All Workspaces" table will automatically update to show only clusters matching your selection.

## To See Only Interactive Clusters

**Users should select: `INTERACTIVE`** from the "Cluster Source" dropdown.

This will filter the report to show:
- ✅ All-purpose clusters (interactive)
- ✅ Clusters created for interactive use
- ❌ Excludes job clusters
- ❌ Excludes API-created clusters (unless they're interactive)

## Cluster Source Types Explained

### INTERACTIVE (All-Purpose Clusters)
- **Purpose**: Manual data exploration, notebook development, ad-hoc queries
- **Lifecycle**: Manually started/stopped by users
- **Cost**: Can be expensive if left running
- **Typical Users**: Data scientists, analysts, engineers doing development

### JOB (Job Clusters)
- **Purpose**: Automated job execution
- **Lifecycle**: Created when job starts, terminated when job ends
- **Cost**: More cost-efficient (only runs when needed)
- **Typical Users**: Automated workflows, scheduled ETL

### UI
- **Purpose**: Clusters created through Databricks workspace UI
- **Lifecycle**: Can be either interactive or job clusters
- **Use Case**: Manual cluster creation

### API
- **Purpose**: Clusters created programmatically
- **Lifecycle**: Created by external systems, CI/CD pipelines
- **Use Case**: Infrastructure as Code, automation

## Technical Implementation

### Parameter Definition:
```json
{
  "name": "cluster_source_filter",
  "keyword": "cluster_source_filter",
  "displayName": "Cluster Source",
  "dataType": "STRING",
  "defaultValue": "All"
}
```

### Query Filter Logic:
```sql
WHERE c.delete_time IS NULL
  AND (':cluster_source_filter' = 'All' 
       OR c.cluster_source = :cluster_source_filter)
```

This filter works by:
1. **If "All" is selected**: Shows all clusters (filter has no effect)
2. **If specific source selected**: Shows only clusters where `cluster_source` matches the selection

## Use Cases

### Scenario 1: Find Interactive Clusters for Cost Optimization
**Goal**: Identify all-purpose clusters that might be left running
**Action**: 
1. Select **"INTERACTIVE"** from Cluster Source filter
2. Review the list for clusters that could be terminated
3. Check `auto_termination_minutes` column

### Scenario 2: Audit Job Clusters
**Goal**: See which automated jobs are running
**Action**:
1. Select **"JOB"** from Cluster Source filter
2. Review job cluster configurations
3. Identify jobs with inefficient cluster settings

### Scenario 3: Monitor API-Created Clusters
**Goal**: Track clusters created by automation
**Action**:
1. Select **"API"** from Cluster Source filter
2. Review programmatically created clusters
3. Validate Infrastructure as Code deployments

## Benefits

### For Data Engineers:
✅ Quickly identify interactive vs job clusters
✅ Track cluster sources for governance
✅ Optimize costs by finding idle interactive clusters

### For FinOps Teams:
✅ Separate interactive cluster costs from job cluster costs
✅ Identify departments/users with expensive interactive clusters
✅ Set policies based on cluster source

### For Platform Admins:
✅ Monitor cluster creation patterns
✅ Identify shadow IT (unexpected API-created clusters)
✅ Enforce cluster policies by source type

## Filter Location in Dashboard
- **Page**: Clusters
- **Report**: "Active Clusters Across All Workspaces"
- **Filter Control**: Top of dashboard (global parameter)
- **Applies To**: Only the clusters table/report

## Important Notes

1. **Default Behavior**: Filter defaults to "All" - shows everything
2. **Case Sensitive**: The filter values are case-sensitive (use uppercase: INTERACTIVE, JOB, API, UI)
3. **Active Clusters Only**: Report only shows clusters where `delete_time IS NULL` (not deleted)
4. **Multi-Workspace**: Filter works across all workspaces in the report

## Next Steps for Users

1. **Save Bookmark**: After selecting "INTERACTIVE", save/bookmark the dashboard view
2. **Schedule Reports**: Set up scheduled reports with filter pre-selected
3. **Cost Analysis**: Combine with workspace filters for detailed cost breakdown
4. **Compliance**: Use for cluster governance and compliance reporting

---
**Date**: March 12, 2026
**Files Modified**: Monitoring Dashboard.lvdash.json
**Parameter Added**: cluster_source_filter
**Dataset Modified**: ds_clusters_active
**Feature**: Interactive cluster filtering capability
**Default Value**: "All" (shows all clusters)
**Available Values**: All, INTERACTIVE, JOB, API, UI
