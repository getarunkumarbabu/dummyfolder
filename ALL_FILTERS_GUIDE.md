# Complete Filter Guide - Azure Databricks Monitoring Dashboard

## 📋 Overview

This dashboard now includes **5 interactive filters** across 3 different pages, enabling workspace-specific and cluster-source analysis.

## 🎛️ All Filters at a Glance

| Page | Table/Widget | Filter | Parameter Name | Values |
|------|--------------|--------|----------------|--------|
| **Clusters** | Active Clusters Across All Workspaces | Workspace Name | `workspace_filter` | All, [workspace names] |
| **Clusters** | Active Clusters Across All Workspaces | Cluster Source | `source_filter` | All, [API, JOB, UI, PIPELINE, SQL] |
| **Jobs** | Highest Failure Jobs — Last 30 Days | Workspace Name | `workspace_filter_failures` | All, [workspace names] |
| **Jobs** | Most Expensive Jobs — Last 30 Days | Workspace Name | `workspace_filter_expensive` | All, [workspace names] |

## 📊 Filters by Page

### Clusters Page (2 Filters)

#### Filter 1: Workspace Name
- **Applied to:** Active Clusters table
- **Purpose:** Show clusters from specific workspace
- **Default:** All

#### Filter 2: Cluster Source
- **Applied to:** Active Clusters table
- **Purpose:** Show clusters created by specific source
- **Default:** All
- **Options:**
  - `API` - Created via REST API
  - `JOB` - Created by job execution
  - `UI` - Created through UI
  - `PIPELINE` - Created by Delta Live Tables
  - `SQL` - Created for SQL warehouse

**Filter Combination:**
- Both filters work together (AND logic)
- Example: Workspace = "Production" AND Source = "JOB"
- Shows only job-created clusters in Production

**Use Case Example:**
```
Scenario: Find all manually-created clusters in Production
Filter 1: Workspace Name = "Production"
Filter 2: Cluster Source = "UI"
Result: Only interactive clusters in Production workspace
```

### Jobs Page (2 Independent Filters)

#### Filter 1: Highest Failure Jobs Workspace Filter
- **Applied to:** Highest Failure Jobs table only
- **Purpose:** Focus failure analysis on specific workspace
- **Default:** All
- **Independent:** Does not affect other tables

#### Filter 2: Most Expensive Jobs Workspace Filter
- **Applied to:** Most Expensive Jobs table only
- **Purpose:** Focus cost analysis on specific workspace
- **Default:** All
- **Independent:** Does not affect other tables

**Independent Behavior:**
- Each table has its own filter
- Can analyze failures in Production while viewing costs across All workspaces
- Maximum flexibility for different analysis needs

**Use Case Example:**
```
Scenario: Production reliability review + full cost visibility
Table 1 Filter: Workspace Name = "Production"
  → Shows Production failures only
Table 2 Filter: Workspace Name = "All"
  → Shows all workspace costs
Result: Focus on critical environment while maintaining cost oversight
```

## 🎯 Common Analysis Scenarios

### Scenario 1: Single Workspace Deep Dive
**Goal:** Comprehensive view of one workspace

**Steps:**
1. **Clusters Page:**
   - Workspace Name = "Production"
   - Cluster Source = "All"
   - Review: All Production clusters

2. **Jobs Page:**
   - Highest Failure Jobs filter = "Production"
   - Most Expensive Jobs filter = "Production"
   - Review: Production job health and costs

**Result:** Complete Production workspace analysis

---

### Scenario 2: Cost Optimization Focus
**Goal:** Identify expensive resources across all workspaces

**Steps:**
1. **Clusters Page:**
   - Workspace Name = "All"
   - Cluster Source = "All"
   - Review: All active clusters

2. **Jobs Page:**
   - Highest Failure Jobs filter = "All"
   - Most Expensive Jobs filter = "All"
   - Review: Highest cost jobs across platform

**Result:** Platform-wide cost insights

---

### Scenario 3: Job Cluster Investigation
**Goal:** Analyze automatically-created clusters

**Steps:**
1. **Clusters Page:**
   - Workspace Name = "All"
   - Cluster Source = "JOB"
   - Review: All job-created clusters

2. **Jobs Page:**
   - Highest Failure Jobs filter = "All"
   - Review: Which jobs are failing

**Result:** Correlation between job clusters and job failures

---

### Scenario 4: Manual Cluster Audit
**Goal:** Review all manually-created clusters

**Steps:**
1. **Clusters Page:**
   - Workspace Name = "All"
   - Cluster Source = "UI"
   - Review: All interactive clusters

**Action Items:**
- Identify long-running interactive clusters
- Check if they should be scheduled jobs instead
- Optimize costs by converting to job clusters

---

### Scenario 5: Development Environment Review
**Goal:** Analyze Development workspace health

**Steps:**
1. **Clusters Page:**
   - Workspace Name = "Development"
   - Cluster Source = "All"

2. **Jobs Page:**
   - Highest Failure Jobs = "Development"
   - Most Expensive Jobs = "Development"

**Result:** Complete Development workspace health check

---

### Scenario 6: Production-Only Monitoring
**Goal:** Executive dashboard for Production environment

**Steps:**
1. Set all filters to "Production"
2. Bookmark the URL
3. Share with leadership

**Result:** Production-focused view without dev/test noise

## 🔄 Filter Interaction Rules

### Same Page Filters (AND Logic)
**Clusters Page Example:**
```
Workspace Name = "Production"  
    +  
Cluster Source = "API"  
    =  
Shows: API-created clusters in Production only
```

**Rule:** Filters on the same page combine with AND logic
- Must match ALL filter conditions
- More selective = fewer results

### Different Page Filters (Independent)
**Jobs Page Example:**
```
Highest Failure Jobs: Workspace = "Production"
Most Expensive Jobs: Workspace = "All"
```

**Rule:** Filters on different tables are independent
- Each table can have different filter settings
- Enables flexible multi-faceted analysis

## 📈 Filter Performance Impact

### Query Optimization Benefits

| Scenario | Unfiltered | Filtered to 1 Workspace | Performance Gain |
|----------|-----------|------------------------|------------------|
| Active Clusters | 500 clusters | 25 clusters | 20x data reduction |
| Failure Jobs | 10,000 jobs | 500 jobs | 20x data reduction |
| Expensive Jobs | 10,000 jobs | 500 jobs | 20x data reduction |

**Recommendation:** Use filters when working with large multi-workspace environments

### Best Performance Practices

1. **Start Broad, Narrow Down**
   - Begin with "All" to see full picture
   - Apply filters to investigate specific areas

2. **Use Filters for Large Environments**
   - 10+ workspaces: Filtering significantly improves performance
   - 5 or fewer workspaces: Filtering less critical but still useful

3. **Combine Filters Strategically**
   - Multiple filters = smaller result set = faster queries
   - Example: Workspace + Source filter on Clusters page

## 🎨 Filter Parameter Reference

### Technical Details

```json
{
  "Clusters Page": {
    "workspace_filter": {
      "displayName": "Workspace Name",
      "dataType": "STRING",
      "defaultValue": "All",
      "appliesTo": "ds_clusters_active"
    },
    "source_filter": {
      "displayName": "Cluster Source",
      "dataType": "STRING",
      "defaultValue": "All",
      "appliesTo": "ds_clusters_active"
    }
  },
  "Jobs Page": {
    "workspace_filter_failures": {
      "displayName": "Workspace Name",
      "dataType": "STRING",
      "defaultValue": "All",
      "appliesTo": "ds_highest_failure_jobs"
    },
    "workspace_filter_expensive": {
      "displayName": "Workspace Name",
      "dataType": "STRING",
      "defaultValue": "All",
      "appliesTo": "ds_most_expensive_jobs"
    }
  }
}
```

### Query Pattern

All filters use the same SQL pattern:

```sql
WHERE ('{{ parameter_name }}' = 'All' OR field_name = '{{ parameter_name }}')
```

**How it works:**
- If parameter = 'All' → WHERE clause is always TRUE → shows all data
- If parameter = specific value → WHERE clause filters to that value
- Elegant solution that handles both filtered and unfiltered states

## 💡 Advanced Use Cases

### Use Case 1: Workspace Comparison
**Goal:** Compare metrics across workspaces

**Method:**
1. Filter to Workspace A, note metrics
2. Change filter to Workspace B, note metrics
3. Compare results

**Benefit:** Identify workspace-specific issues or patterns

---

### Use Case 2: Source-Based Cost Analysis
**Goal:** Understand costs by cluster creation method

**Steps:**
1. Clusters Page: Source = "JOB", note cluster count
2. Clusters Page: Source = "UI", note cluster count
3. Compare: Are interactive clusters costing more?

**Action:** If UI clusters are excessive, consider job conversions

---

### Use Case 3: Team Accountability
**Goal:** Each team monitors their own workspace

**Setup:**
1. Create bookmark with team's workspace filter applied
2. Share bookmark with team
3. Team uses pre-filtered view for daily monitoring

**Benefit:** Self-service monitoring, reduced support requests

---

### Use Case 4: Incident Investigation
**Goal:** Debug Production job failures

**Steps:**
1. **Jobs Page:** Filter Highest Failure Jobs to "Production"
2. Identify failing job name
3. **Clusters Page:** Filter to "Production" + "JOB" source
4. Check if related clusters have issues

**Result:** Correlation between job failures and cluster health

---

### Use Case 5: Cost Allocation
**Goal:** Chargeback to business units

**Steps:**
1. **Jobs Page:** Filter Most Expensive Jobs by each workspace
2. Export results for each workspace
3. Generate chargeback reports

**Benefit:** Accurate cost attribution to teams/projects

## 🛠️ Troubleshooting

### Problem: Filter dropdown is empty
**Cause:** No data in system tables  
**Solution:**
- Verify system tables have data: `SELECT * FROM system.access.workspaces_latest`
- Check Databricks system table permissions
- Ensure workspace metadata is populated

### Problem: Filter shows wrong workspace names
**Cause:** Workspace name mismatch  
**Solution:**
- Check exact names in: `SELECT workspace_name FROM system.access.workspaces_latest`
- Names are case-sensitive
- Verify workspace hasn't been renamed

### Problem: Filters not working together
**Cause:** Misunderstanding filter logic  
**Solution:**
- **Same page:** Filters use AND logic (both must match)
- **Different tables:** Filters are independent
- Review section: "Filter Interaction Rules"

### Problem: Filtered results seem incorrect
**Cause:** Data lag in system tables  
**Solution:**
- System tables may have 1-2 hour lag
- Recent changes might not appear immediately
- Wait and refresh, or check system table timestamps

## 📊 Reporting Best Practices

### Daily Monitoring Dashboards

**Production Team View:**
```
Clusters Page:
  - Workspace = "Production"
  - Source = "All"

Jobs Page:
  - Highest Failure Jobs = "Production"
  - Most Expensive Jobs = "Production"

Action: Bookmark this filtered view for daily standup
```

**Platform Team View:**
```
All filters = "All"

Purpose: Platform-wide oversight
Review: Overall health across all workspaces
```

### Weekly Cost Reviews

**By Workspace:**
```
Week 1: Filter all to "Analytics"
Week 2: Filter all to "Development"
Week 3: Filter all to "Production"
Week 4: Filter all to "All" for comparison
```

**By Cluster Type:**
```
Review 1: Clusters Source = "UI" → Check interactive costs
Review 2: Clusters Source = "JOB" → Check automation costs
Review 3: Compare and optimize
```

### Monthly Executive Reports

**Production Health:**
- Jobs page → Production failures only
- Export top 10 failing jobs
- Present mitigation plans

**Cost Trends:**
- Jobs page → Most expensive across all workspaces
- Show month-over-month changes
- Highlight optimization opportunities

## 📚 Related Documentation

- **FILTER_IMPLEMENTATION.md** - Clusters page filters (detailed)
- **JOBS_FILTERS.md** - Jobs page filters (detailed)
- **Dashboard_README.md** - Complete dashboard guide
- **IMPORT_INSTRUCTIONS.md** - How to import and set up
- **Query_Reference.md** - Technical SQL details

## 📝 Quick Reference Card

### Filter Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│ CLUSTERS PAGE                                           │
├─────────────────────────────────────────────────────────┤
│ • Workspace Name filter (all clusters in that workspace)│
│ • Cluster Source filter (API/JOB/UI/PIPELINE/SQL)      │
│ • Filters combine with AND logic                       │
│ • Use for: cluster inventory, source analysis          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ JOBS PAGE                                               │
├─────────────────────────────────────────────────────────┤
│ • Highest Failure Jobs: Independent workspace filter   │
│ • Most Expensive Jobs: Independent workspace filter    │
│ • Filters work independently                           │
│ • Use for: failure analysis, cost optimization         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ COMMON PATTERNS                                         │
├─────────────────────────────────────────────────────────┤
│ Single workspace analysis: Filter all to workspace X   │
│ Platform-wide view: Set all filters to "All"          │
│ Focused investigation: Combine multiple filters        │
│ Team dashboards: Bookmark with team's workspace        │
└─────────────────────────────────────────────────────────┘
```

## ✅ Filter Implementation Status

| Feature | Status | Date Added |
|---------|--------|------------|
| Cluster Workspace Filter | ✅ Complete | March 12, 2026 |
| Cluster Source Filter | ✅ Complete | March 12, 2026 |
| Failure Jobs Workspace Filter | ✅ Complete | March 12, 2026 |
| Expensive Jobs Workspace Filter | ✅ Complete | March 12, 2026 |
| Documentation | ✅ Complete | March 12, 2026 |

**All filters tested and validated** ✅

---

**Document Version:** 1.0  
**Last Updated:** March 12, 2026  
**Dashboard File:** `Monitoring Dashboard.lvdash.json`  
**Status:** Ready for production use
