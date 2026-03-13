# Pricing Discount Update - March 12, 2026

## 📊 Summary
Updated all cost calculations in the monitoring dashboard to reflect your negotiated DBU discount rate.

## 💰 Pricing Details
- **Your Rate**: $730,000 for 1,000,000 DBUs
- **Effective Rate**: $0.73 per DBU
- **Discount**: 27% off list price (0.73 multiplier)

## 🔧 Technical Changes
All occurrences of `list_prices.pricing.default` have been updated to `list_prices.pricing.default * 0.73`

### Datasets Updated (4 total):

#### 1. **ds_job_run_cost_agg** (Jobs Summary by Workspace)
- **Line**: 27
- **Query**: Job run cost aggregation for last 30 days
- **Updated Formula**: 
  ```sql
  t1.usage_quantity * list_prices.pricing.default * 0.73 AS list_cost
  ```
- **Impact**: Overview page "Jobs Summary by Workspace" table now shows discounted costs

#### 2. **ds_most_expensive_jobs** (Most Expensive Jobs)
- **Line**: 165
- **Query**: Cost analysis per job with failure tracking
- **Updated Formula**: 
  ```sql
  SUM(t1.usage_quantity * list_prices.pricing.default * 0.73) AS list_cost
  ```
- **Impact**: Jobs page "Most Expensive Jobs" table reflects actual costs

#### 3. **ds_billing_30_60_days** (Billing Comparison)
- **Line**: 214
- **Query**: Compare spending between last 30-60 days
- **Updated Formula**: 
  ```sql
  t1.usage_quantity * list_prices.pricing.default * 0.73 AS list_cost
  ```
- **Impact**: Billing trend analysis uses accurate pricing

#### 4. **ds_billing_daily_timeseries** (Daily Billing Timeseries)
- **Line**: 335
- **Query**: Daily cost tracking by product and workspace
- **Updated Formula**: 
  ```sql
  ROUND(SUM(usage_quantity * list_prices.pricing.default * 0.73), 2) AS list_cost
  ```
- **Impact**: Overview page timeseries chart displays correct daily costs

## ✅ Validation
- ✅ JSON structure validated
- ✅ All 4 dataset queries updated
- ✅ No syntax errors
- ✅ Dashboard ready for import

## 📈 Impact Areas

### Overview Page
- Jobs Summary by Workspace table → Shows discounted costs
- Daily billing timeseries chart → Reflects actual spending

### Jobs Page
- Most Expensive Jobs table → Accurate cost rankings
- All cost-related metrics → Based on discounted rates

### Financial Analysis
- 30-day vs 60-day comparisons → True cost trends
- Cost per job calculations → Reflects negotiated pricing
- Budget tracking → Aligned with actual billing

## 🔄 Before vs After

### Before
```sql
usage_quantity * list_prices.pricing.default
```
Showed **list price** (100% of standard rates)

### After
```sql
usage_quantity * list_prices.pricing.default * 0.73
```
Shows **actual cost** (73% of list price = 27% discount)

## 📋 Important Notes

1. **Consistent Discount**: The 0.73 multiplier is applied uniformly across:
   - Job compute costs
   - All SKU types (JOBS, ALL_PURPOSE, etc.)
   - All time periods (30-day, 60-day comparisons)

2. **List Price Reference**: The `list_prices.pricing.default` still uses Azure Databricks list prices from `system.billing.list_prices`, but the 0.73 multiplier adjusts it to your contracted rate.

3. **Future Updates**: If your discount rate changes:
   - Search for `* 0.73` in the dashboard JSON
   - Replace with new multiplier (e.g., `* 0.70` for 30% discount)
   - All cost calculations will update automatically

4. **Validation**: Always validate JSON after changes:
   ```powershell
   Get-Content "Monitoring Dashboard.lvdash.json" -Raw | ConvertFrom-Json
   ```

## 🎯 Next Steps

1. **Import Dashboard**: Import the updated dashboard into Azure Databricks
2. **Verify Costs**: Compare dashboard costs with actual billing statements
3. **Monitor**: Use the dashboard to track actual spending vs budgets
4. **Optimize**: Identify high-cost jobs/workspaces with accurate pricing

## 📞 Support

If you need to adjust the discount rate or have questions about cost calculations:
- All pricing formulas are in the datasets queries
- Each dataset uses the same `* 0.73` multiplier pattern
- Changes require JSON editing and re-import

---

**Update Date**: March 12, 2026  
**Dashboard Version**: 1,950 lines  
**Discount Applied**: 27% (0.73 multiplier)  
**Status**: ✅ Ready for Production
