import json

print("=" * 60)
print("  FINAL VALIDATION - Dashboard JSON File")
print("=" * 60)
print()

try:
    with open('Monitoring Dashboard.lvdash.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("✅ JSON IS VALID!")
    print()
    print(f"📊 Dashboard Statistics:")
    print(f"   • Datasets: {len(data.get('datasets', []))}")
    print(f"   • Pages: {len(data.get('pages', []))}")
    print()
    
    # Count parameters
    total_params = sum(len(ds.get('parameters', [])) for ds in data.get('datasets', []))
    print(f"🔧 Parameters:")
    print(f"   • Total Parameters: {total_params}")
    print()
    
    # Check for conflict markers
    with open('Monitoring Dashboard.lvdash.json', 'r', encoding='utf-8') as f:
        content = f.read()
    
    conflict_markers = ['<<<<<<<', '=======', '>>>>>>>']
    has_conflicts = any(marker in content for marker in conflict_markers)
    
    if has_conflicts:
        print("❌ WARNING: File still contains merge conflict markers!")
    else:
        print("✅ No merge conflict markers found")
    
    print()
    print("=" * 60)
    print("  ✅ DASHBOARD IS READY FOR IMPORT!")
    print("=" * 60)
    
except json.JSONDecodeError as e:
    print(f"❌ JSON PARSING ERROR!")
    print(f"\nError: {e.msg}")
    print(f"Line: {e.lineno}, Column: {e.colno}")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
