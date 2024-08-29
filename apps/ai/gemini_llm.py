import os
import google.generativeai as genai



def run_gemini_for_3_words(subject,body):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    generation_config = {
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config
                )

    chat_session = model.start_chat(
                            history=[
                                    ]
                    )
    inputs = "You are an email assistant that helps in summarizing emails" + f"Describe the email contents in upto 3 words {subject} {body}, respond with upto 3 words only without Quotes"
    response = chat_session.send_message(inputs)
    return response.text

def gemini_compose_reply(reply,body):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    generation_config = {
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config
                )

    chat_session = model.start_chat(
                            history=[
                                    ]
                    )
    inputs = "You are a friendly assistant that helps write reply for emails" + f"Write a email reply with the following reply {reply}, and the contents of the original mail are {body}. Write a email in a similar tone to the original email. Return just the plain text and do not say 'Here is the email reply:'."
    response = chat_session.send_message(inputs)
    return response.text