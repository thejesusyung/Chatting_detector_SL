import json
import base64

# Load your service account JSON key
with open('/Users/maxim/Downloads/vibe_streamlut_bot IAM Admin.json', 'r') as json_file:
    json_data = json.load(json_file)

# Convert JSON to string and then encode it
json_str = json.dumps(json_data)
encoded_json_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
st = encoded_json_str
print()
print(st)
print()
