import requests
import os

def run_ai_llm(inputs):
    CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_AI_TOKEN = os.environ.get("CLOUDFLARE_AI_TOKEN")
    MODEL = "@cf/meta/llama-3-8b-instruct"
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_AI_TOKEN}"}
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{MODEL}", headers=headers, json=input)
    return response.json()