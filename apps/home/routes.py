
from jinja2 import TemplateNotFound
from flask import render_template, request, redirect, url_for, session, jsonify
from nylas import Client
from datetime import datetime, timedelta
from flask_session.__init__ import Session
import os
from apps.home  import blueprint
from apps.ai.cloudflare_llm import run_ai_llm
from datetime import datetime, timedelta
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
    { "role": "user", "content": f"Describe the email contents in 3 words {messages[1].subject}, respond with the 3 words only"}]
    ai_out = run_ai_llm(inputs)
    print(ai_out['result']['response'])
    return ai_out['result']['response']
  except Exception as e:
    return f'{e}'  


@blueprint.route('/', methods=["GET"])
def index():
  if session.get("grant_id") is None:
    return redirect('/auth')
  yesterday = datetime.today() - timedelta(hours=96)
  query_params = {"received_after": str(yesterday.strftime('%s'))}
  try:
    messages, _, _ = nylas.messages.list(session["grant_id"], query_params)
    keywords = list()
    message_dates = list()
    for message in messages:
      inputs = [{ "role": "system", "content": "You are a friendly assistant that helps sort emails" },
    { "role": "user", "content": f"Describe the email contents in upto 3 words {message.subject} {message.body}, respond with upto 3 words only without Quotes"}]
      keywords.append(run_ai_llm(inputs))
      message_dates.append(datetime.fromtimestamp(int(message.date)).strftime('%Y-%m-%d %H:%M:%S'))
    length = len(messages)
    return render_template('home/index.html', segment='index', emails=keywords,messages= messages,dates=message_dates,message_count=length)
  except Exception as e:
    return f'{e}'  
    

    