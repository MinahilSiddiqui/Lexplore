import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("MISTRAL_API_KEY")

# Check if the key is loaded correctly
if not api_key:
    print("❌ API key not loaded. Make sure your .env file has the correct key.")
    exit()

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"  # ✅ CORRECTED URL
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    # Send POST request
    response = requests.post(url, headers=headers, json=data)

    print(f"Status code: {response.status_code}")
    print(f"Response text (first 500 chars):\n{response.text[:500]}")

    try:
        response_json = response.json()
    except Exception as e:
        return f"❌ Failed to parse JSON. Error: {e}\nRaw response: {response.text[:500]}"

    # Check response content
    if response.status_code == 200:
        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return f"⚠️ Unexpected JSON structure: {response_json}"
    else:
        return f"❌ Error {response.status_code}: {response.text[:500]}"

