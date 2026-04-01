import requests
import json

print("Testing batch update endpoint...")
r = requests.post('http://localhost:5000/api/update', json={'update_type': 'test_batch'}, timeout=120)
print('status:', r.status_code)
data = r.json()
print('result:', json.dumps(data, indent=2))
