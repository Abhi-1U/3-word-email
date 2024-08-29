from flask import render_template, request, redirect, session, jsonify
from nylas import Client
from datetime import datetime, timedelta
import os
from apps.home  import blueprint
from apps.ai.gemini_llm import run_gemini_for_3_words, gemini_compose_reply
from datetime import datetime, timedelta
nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
  )

@blueprint.route("/reply", methods=["GET","POST"])
def reply():
  if request.method == 'GET':
    return redirect('/')
  if request.method == 'POST':
    message_id = request.form['message_id']
    reply = request.form['reply']
    reply_type = request.form['reply_type']
    if reply_type == "DRAFT":
      try:
        message = nylas.messages.find(session["grant_id"], message_id)
        ai_generated_reply = gemini_compose_reply(reply,message.data.body)
        threewords = run_gemini_for_3_words("Re :"+message.data.subject,ai_generated_reply)
        date=datetime.fromtimestamp(int(message.data.date)).strftime('%d-%m-%Y %H:%M:%S')
        return render_template('home/reply.html',reply = ai_generated_reply,threewords= threewords,
                             message=message.data,folder=message.data.folders,date=date)
      except Exception as e:
        return f'{e}'  
    if reply_type == "FINAL":
      try:
        message = nylas.messages.find(session["grant_id"], message_id)
        draft = nylas.drafts.create(session["grant_id"],
                                    request_body={
                                      "to": message.data.from_,
                                      "reply_to": message.data.to,
                                      "subject":  message.data.subject,
                                      "body": reply,
                                      "thread_id": message.data.thread_id}
                                    )
        draftSent = nylas.drafts.send(session["grant_id"],draft[0].id)
        success_message = "Your reply has been sent successfully 🚀"
        date=datetime.fromtimestamp(int(draft.data.date)).strftime('%d-%m-%Y %H:%M:%S')
        return render_template('home/reply_success.html',success_message=success_message,threewords= request.form['threewords'],
                             message=draft.data,folder=draft.data.folders,date=date)
      except Exception as e:
        return f'{e}'
    if reply_type == "LATER":
      try:
        message = nylas.messages.find(session["grant_id"], message_id)
        message.data.from_
        draft = nylas.drafts.create(session["grant_id"],
                                    request_body={
                                      "to": message.data.from_,
                                      "reply_to": message.data.to,
                                      "subject": message.data.subject,
                                      "body": reply,
                                      "thread_id": message.data.thread_id}
                                    )
        success_message = "Your reply has been saved as draft successfully 🚀"
        date=datetime.fromtimestamp(int(draft.data.date)).strftime('%d-%m-%Y %H:%M:%S')
        return jsonify({"message":success_message})
      except Exception as e:
        return f'{e}'  

    


@blueprint.route('/', methods=["GET","POST"])
def index():
  if session.get("grant_id") is None:
    return redirect('/auth')
  td = 2
  if request.method == 'GET':
    if (request.args.get('timedelta') != None) :
      try:
        td =  int(request.args.get('timedelta'))
      except ValueError:
        td = 2
  yesterday = datetime.today() - timedelta(hours=td)
  query_params = {"received_after": str(yesterday.strftime('%s'))}
  try:
    messages, _, _ = nylas.messages.list(session["grant_id"], query_params)
    keywords = list()
    folder_categories=list()
    message_dates = list()
    for message in messages:
      keywords.append(run_gemini_for_3_words(message.subject,message.body))
      folder_categories.append(message.folders)
      message_dates.append(datetime.fromtimestamp(int(message.date)).strftime('%d-%m-%Y %H:%M:%S'))
    length = len(messages)
    return render_template('home/index.html', segment='index',
                           emails=keywords,messages= messages,
                           dates=message_dates,message_count=length,
                           td=td, folders=folder_categories)
  except Exception as e:
    return f'{e}'  