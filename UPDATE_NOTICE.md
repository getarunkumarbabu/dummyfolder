# ⚠️ IMPORTANT UPDATE - Workspace Names

## Dashboard Updated to Show Workspace Names

The dashboard has been **updated** to display **workspace names instead of workspace IDs** throughout all visualizations.

### What Changed?
✅ All queries now join with `system.access.workspaces_latest`  
✅ Workspace names appear in all tables and charts  
✅ Fallback to workspace_id if name is not available  
✅ User-friendly, human-readable workspace identification  

### Example Query Pattern (Updated)
```sql
SELECT 
  t1.workspace_id,
  COALESCE(w.workspace_name, CAST(t1.workspace_id AS STRING)) AS workspace_name,
  -- other fields
FROM system.lakeflow.job_run_timeline t1
LEFT JOIN system.access.workspaces_latest w ON t1.workspace_id = w.workspace_id
WHERE ...
```

### Required Table Access
You now need SELECT permission on:
- `system.access.workspaces_latest` ← **NEW**

### For Complete Details
See **WORKSPACE_NAME_UPDATE.md** for:
- Detailed change log
- Testing recommendations
- Troubleshooting guide
- Verification checklist

---

**Re-import the dashboard** to see workspace names instead of IDs!

---

*This update was made on March 12, 2026*
