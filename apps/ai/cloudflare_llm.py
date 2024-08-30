import requests
import os

def run_llama(subject,body):
    CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_AI_TOKEN = os.environ.get("CLOUDFLARE_AI_TOKEN")
    MODEL = "@cf/meta/llama-3-8b-instruct"
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_AI_TOKEN}"}
    inputs = [{ "role": "system", "content": "You are a friendly assistant that helps sort emails" },
    { "role": "user", "content": f"Describe the email contents in upto 3 words {subject} {body}, respond with upto 3 words only without Quotes"}]
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{MODEL}", headers=headers, json=input)
    return response.json()['result']['response']

def compose_reply(reply,body):
    CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_AI_TOKEN = os.environ.get("CLOUDFLARE_AI_TOKEN")
    MODEL = "@cf/meta/llama-3-8b-instruct"
    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_AI_TOKEN}"}
    inputs = [{ "role": "system", "content": "You are a friendly assistant that helps write reply for emails" },
    { "role": "user", "content": f"Write a email reply with the following reply {reply}, and the contents of the original mail are {body}. Write a email in a similar tone to the original email. Return just the plain text and do not say 'Here is the email reply:'."}]
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{MODEL}", headers=headers, json=input)
    return response.json()['result']['response']