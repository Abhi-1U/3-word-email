from flask import request, redirect, url_for, session
from nylas.models.auth import URLForAuthenticationConfig
from nylas.models.auth import CodeExchangeRequest
from nylas import Client
import os
from apps.auth  import blueprint
from flask import session,render_template


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
    return redirect('/') 


@blueprint.route("/oauth/exchange", methods=["GET"])
def authorized():
  if session.get("grant_id") is None:
    code = request.args.get("code")

    exchangeRequest = CodeExchangeRequest({"redirect_uri": "http://localhost:5000/oauth/exchange",
        "code": code, "client_id": os.environ.get("NYLAS_CLIENT_ID")})

    exchange = nylas.auth.exchange_code_for_token(exchangeRequest)
    session["grant_id"] = exchange.grant_id
    return redirect("/")

@blueprint.route("/revoke", methods=["GET","POST"])
def revoke():
  if request.method == "POST":
    if request.form['delete_confirmation'] == "TRUE":
      try:
        delete_response = nylas.grants.destroy(session["grant_id"])
        session.clear()
        return redirect('/')
      except Exception as e:
        return f"{e}"
    else:
      return redirect("/")
  if request.method == "GET":
    if session.get("grant_id") is None:
      return redirect('/')
    else:
      return render_template('auth/revoke.html') 