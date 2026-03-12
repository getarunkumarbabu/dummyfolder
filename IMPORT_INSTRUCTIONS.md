# How to Import the Databricks Monitoring Dashboard

## Prerequisites

### 1. System Tables Must Be Enabled
Before importing, verify System Tables are available:
```sql
-- Test query in a SQL Warehouse
SELECT COUNT(*) FROM system.lakeflow.jobs LIMIT 10;
```
If this fails, contact your Databricks Account Admin to enable System Tables.

### 2. Required Permissions
Your user or service principal needs:
- `SELECT` on `system.billing.*`
- `SELECT` on `system.lakeflow.*`
- `SELECT` on `system.compute.*`
- `CAN USE` on a Pro or Serverless SQL Warehouse

### 3. Databricks Environment
- **Platform**: Azure Databricks
- **Workspace**: Any workspace in your account (centralized monitoring)
- **SQL Warehouse**: Pro or Serverless tier (Classic not supported)

---

## Import Steps

### Step 1: Navigate to Lakeview Dashboards
1. Log into your Azure Databricks workspace
2. Click on **Dashboards** in the left sidebar (or go to `/sql/dashboards`)
3. You should see the Lakeview interface

### Step 2: Import the Dashboard File
1. Click the **Create** button in the top right
2. Select **Import dashboard from file**
3. Click **Choose file** or drag and drop
4. Select `Monitoring Dashboard.lvdash.json` from your local machine
5. Click **Import**

### Step 3: Initial Configuration
After import, the dashboard will appear but may not have data yet:

1. **Select a SQL Warehouse**:
   - Click on the dashboard settings (gear icon)
   - Under "SQL Warehouse", select a Pro or Serverless warehouse
   - Click **Save**

2. **Refresh Data**:
   - Click the **Refresh** button (circular arrow icon) in the top right
   - All dataset queries will execute
   - Wait for all queries to complete (typically 30 seconds - 2 minutes)

### Step 4: Verify Data
Check each page:
- **Overview**: Should show counters, charts, and workspace summary
- **Jobs**: Should list jobs with failures and costs
- **Pipelines**: Should show pipeline updates if you have DLT pipelines
- **Clusters**: Should list all active clusters

---

## Troubleshooting Import Issues

### Issue: "System catalog not found"
**Solution**: System Tables are not enabled
```
Contact your Databricks account admin to enable System Tables:
1. Go to Account Console
2. Navigate to Settings → System Tables
3. Enable System Tables
4. Wait 24-48 hours for initial data population
```

### Issue: "Permission denied on system.billing.usage"
**Solution**: Add SELECT permissions
```sql
-- As account admin, grant permissions:
GRANT SELECT ON SCHEMA system.billing TO `your-user@company.com`;
GRANT SELECT ON SCHEMA system.lakeflow TO `your-user@company.com`;
GRANT SELECT ON SCHEMA system.compute TO `your-user@company.com`;
```

### Issue: "No data in visualizations"
**Causes and Solutions**:
1. **System Tables recently enabled**: Wait 24-48 hours for data
2. **No activity in last 30 days**: Normal if this is a new environment
3. **Timezone issues**: Check if `CURRENT_DATE()` aligns with your timezone
4. **Warehouse access**: Ensure you're using a Pro/Serverless warehouse

### Issue: "Query failed with syntax error"
**Solution**: Check Databricks Runtime version
- Requires DBR 13.0+ or SQL Warehouse
- Some queries use modern SQL syntax (QUALIFY, GROUP BY ALL)
- Update to latest SQL Warehouse version

### Issue: "Dashboard import fails"
**Possible causes**:
1. **Invalid JSON**: Verify the file hasn't been corrupted
2. **File size**: Ensure complete file was downloaded (should be ~1500 lines)
3. **Format version**: Use Lakeview, not legacy SQL dashboards

---

## Post-Import Configuration

### 1. Set Refresh Schedule
**Recommended**: Hourly or daily refresh

Steps:
1. Open the dashboard
2. Click on **Schedule** in the top right
3. Configure:
   - **Frequency**: Hourly (for active monitoring) or Daily (for reporting)
   - **Time**: Off-peak hours if daily
   - **Email recipients**: Platform team emails
4. Click **Save**

### 2. Configure Alerts (Optional)
Create alerts for critical metrics:

**Example Alert: High Job Failure Rate**
1. Go to **SQL** → **Alerts**
2. Click **Create Alert**
3. Use query:
```sql
SELECT 
  COUNT(*) as failed_jobs
FROM system.lakeflow.job_run_timeline
WHERE result_state IN ('FAILED', 'ERROR')
  AND period_end_time >= CURRENT_TIMESTAMP() - INTERVAL 1 HOUR
```
4. Set condition: `failed_jobs > 10`
5. Add notification destinations

**Example Alert: Cost Spike**
```sql
SELECT 
  ROUND(SUM(usage_quantity * list_prices.pricing.default), 2) AS hourly_cost
FROM system.billing.usage t1
INNER JOIN system.billing.list_prices list_prices
  ON t1.cloud = list_prices.cloud
 AND t1.sku_name = list_prices.sku_name
 AND t1.usage_start_time >= list_prices.price_start_time
WHERE t1.usage_start_time >= CURRENT_TIMESTAMP() - INTERVAL 1 HOUR
```
Set condition: `hourly_cost > 500`

### 3. Share Dashboard
**Share with stakeholders**:
1. Click **Share** button
2. Add users or groups:
   - Platform Engineers: `CAN EDIT`
   - FinOps Team: `CAN RUN`
   - Executives: `CAN VIEW`
3. Enable **Link sharing** for broader access

### 4. Customize Branding (Optional)
Edit the title widget:
1. Go to **Overview** page
2. Click on the title text widget
3. Modify HTML to match your organization:
```html
<span style="text-align:center;display:block;">
  <span style="font-size:36px;line-height:1.4;font-family:Georgia;">
    🏢 YOUR COMPANY - Multi-Workspace Monitoring
  </span>
</span>
```

---

## Workspace-Level Deployment

### Option A: Import into Each Workspace
If you need the dashboard in multiple workspaces:
1. Import the `.lvdash.json` file into each workspace
2. Each workspace will show **all workspaces** (System Tables are account-level)
3. Useful for distributed teams

### Option B: Centralized Monitoring Workspace
**Recommended approach**:
1. Create a dedicated "Platform Monitoring" workspace
2. Import dashboard only there
3. Share dashboard with all platform team members
4. Reduces duplication and maintenance

### Option C: Add Workspace Filtering
Modify queries to show only current workspace:
```sql
WHERE workspace_id = current_workspace_id()
```
This makes each workspace's dashboard show only its own resources.

---

## Integration with Existing Dashboards

### Embed Widgets in Other Dashboards
You can copy individual widgets:
1. Open this monitoring dashboard
2. Click on any widget → **Copy**
3. Open your target dashboard
4. **Paste** the widget
5. The dataset will be copied automatically

### Link from Other Dashboards
Add navigation links:
```markdown
[View Multi-Workspace Monitoring](/sql/dashboards/<dashboard-id>)
```

---

## Maintenance and Updates

### Update Dashboard
When a new version is released:
1. **Export current dashboard** (backup):
   - Click **…** menu → **Download**
2. **Delete old dashboard** (or rename it)
3. **Import new version** using steps above
4. **Reconfigure** warehouse, schedules, and sharing

### Monitor Dashboard Health
Check:
- **Query execution times**: Should be < 60 seconds per dataset
- **Data freshness**: System Tables update every 30-60 minutes
- **Error notifications**: Set up alerts for query failures

---

## Security Best Practices

1. **Limit Edit Access**: Only platform admins should have `CAN EDIT`
2. **Row-Level Security**: System Tables have built-in access controls
3. **Audit Access**: Check who views the dashboard regularly
4. **Mask Sensitive Data**: Consider redacting user emails if needed
5. **Cost Data Visibility**: Restrict if cost data is confidential

---

## Support and Resources

### Documentation
- [Databricks System Tables](https://docs.databricks.com/administration-guide/system-tables/)
- [Lakeview Dashboards](https://docs.databricks.com/dashboards/lakeview.html)
- [SQL Warehouses](https://docs.databricks.com/sql/admin/sql-endpoints.html)

### Getting Help
- **Databricks Support**: Submit ticket via Account Console
- **Community**: [Databricks Community Forums](https://community.databricks.com/)
- **Internal**: Contact your Databricks account team

### Common Questions
**Q: Can I use this on AWS or GCP Databricks?**  
A: Yes, but you may need to adjust cloud-specific fields in queries.

**Q: How much does this cost to run?**  
A: Minimal - queries run on your SQL Warehouse and complete in seconds. Expect < $1/day for typical refresh schedules.

**Q: Can I export dashboard data?**  
A: Yes - each widget has a download option (CSV, Excel, JSON).

**Q: How far back does historical data go?**  
A: System Tables typically retain 1+ year of data, but this varies by table.

---

## Success Checklist

After import, verify:
- [ ] Dashboard opens without errors
- [ ] All 4 pages render correctly
- [ ] Overview page shows cost counters
- [ ] Jobs page shows failure and cost tables
- [ ] Pipelines page shows updates (if you have pipelines)
- [ ] Clusters page shows active cluster inventory
- [ ] Refresh completes successfully
- [ ] Schedule is configured
- [ ] Dashboard is shared with team
- [ ] Alerts are set up (optional)

---

**You're all set!** The dashboard should now provide comprehensive visibility into your Databricks platform across all workspaces.
