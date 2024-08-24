
from flask import request, redirect, url_for, session, jsonify
from nylas import Client
from datetime import datetime, timedelta
from flask_session.__init__ import Session
import os
from apps.home  import blueprint
from apps.ai.cloudflare_llm import run_ai_llm

nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
  )

@blueprint.route("/nylas/recent-emails", methods=["GET"])
def recent_emails():
  query_params = {"limit": 5}

  try:
    messages, _, _ = nylas.messages.list(session["grant_id"], query_params)
    inputs = [
    { "role": "system", "content": "You are a friendly assistant that helps sort emails" },
    { "role": "user", "content": f"Describe the email contents in 3 words {messages[1].body}, respond with the 3 words only"}]
    ai_out = run_ai_llm(inputs)
    print(ai_out['result']['response'])
    return ai_out['result']['response']
  except Exception as e:
    return f'{e}'  
