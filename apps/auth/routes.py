from flask import request, redirect, url_for, session, jsonify
from nylas.models.auth import URLForAuthenticationConfig
from nylas.models.auth import CodeExchangeRequest
from nylas import Client
from datetime import datetime, timedelta
from flask_session.__init__ import Session
import os
from apps.auth  import blueprint



nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
  )

@blueprint.route("/auth", methods=["GET"])
def login():
  
  if session.get("grant_id") is None:
    config = URLForAuthenticationConfig({"client_id": os.environ.get("NYLAS_CLIENT_ID"), 
        "redirect_uri" : "http://localhost:5000/oauth/exchange"})

    url = nylas.auth.url_for_oauth2(config)

    return redirect(url)
  else:
    return f'{session["grant_id"]}' 


@blueprint.route("/oauth/exchange", methods=["GET"])
def authorized():
  if session.get("grant_id") is None:
    code = request.args.get("code")

    exchangeRequest = CodeExchangeRequest({"redirect_uri": "http://localhost:5000/oauth/exchange",
        "code": code, "client_id": os.environ.get("NYLAS_CLIENT_ID")})

    exchange = nylas.auth.exchange_code_for_token(exchangeRequest)
    session["grant_id"] = exchange.grant_id
    return redirect(url_for("login"))

