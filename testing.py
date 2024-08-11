import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer key",
  },
  data=json.dumps({
    "model": "neversleep/llama-3-lumimaid-70b", # Optional
    "messages": [
      { "role": "user", "content": "What is the meaning of life?" }
    ]
  })
)
print(response.json())