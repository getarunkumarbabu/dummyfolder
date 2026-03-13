import json
import sys

try:
    with open('Monitoring Dashboard.lvdash.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("✅ JSON IS VALID!")
    print(f"\n📊 Dashboard Stats:")
    print(f"   • Datasets: {len(data.get('datasets', []))}")
    print(f"   • Pages: {len(data.get('pages', []))}")
    print(f"\n✅ File can be parsed successfully!")
    sys.exit(0)
    
except json.JSONDecodeError as e:
    print(f"❌ JSON PARSING ERROR!")
    print(f"\nError: {e.msg}")
    print(f"Line: {e.lineno}, Column: {e.colno}")
    print(f"Position: {e.pos}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    sys.exit(1)
