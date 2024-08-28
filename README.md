# 3 word email : Browse through your E-mails quickly.


There are many ways one can categorize the mails, one common way is to categorize all the emails into seperate folders in the order of their priority.
However, this is more of a hassle where you need to check each folder to lookout for the email wrongly categorized, which could have been important you.
The idea of 3 word email is not to categorize but to summarize the contents mostly to 3 words, which along with the senders name and email address should be
a good indicator of whether the email is worth your time or not. Lastly to read the complete rendered email you can click on the card to view the email. This mechanism puts you in charge, where you decide which email is worthy of your time to read in depth. This can be a good excercise to do in the mornings where you can glance over the 3 words of each mail, decide which ones are important to you at that moment and read it at that moment.
This email app is not a replacement for the traditional email clients, but rather a companion which does not overwhelm you with lots of information, which does not
make categorization decisions for you, but lets you exercise that in a productive manner.

Another great feature to reduce the anxiety from lots of emails is time based filter options available on the top of the main screen. This ensures that you do not
get caught up Looking at old/irrelevant emails repeateadly.

## Features

1. Use of nylas email API using Python SDK to integrate email data securely into the flask web application.
2. No caching/storing of the email data to ensure best data security and regulatory compliances.
3. Use of cloudflare AI worker APIs using meta's llama 3.1 large language model for the generation of the 3 words and replies.
4. Simple, Intuitive and screen width responsive web interface.
5. View full body of the email with HTML markups.
6. Time based email viewer to reduce bombardment, while promoting habit to check email daily and excercise on the important emails on the same day.
7. Reply with 3 words ( or a few more if you want to) ! (LLM will automatically generate a mail for you !)
8. Revoke Nylas grant and clear session keys.

## Future Improvements

1. Caching and storing the results for faster load times.
2. Possibilities for many more enhancements remain open as it is a project built in a hackathon event.



## Environment Setup 

Store our nylas and cloudflare ai worker (REST API) tokens and credentials into the `.env` file.

```
NYLAS_CLIENT_ID="<<>>"
NYLAS_API_KEY="<<>>"
NYLAS_API_URI= "<<>>"


CLOUDFLARE_AI_TOKEN="<<>>"
CLOUDFLARE_ACCOUNT_ID="<<>>"

FLASK_APP="index.py"
```

## Install Dependencies

Install common Flask and Nylas dependencies from the `requirements.txt`.
No dependencies for cloudflare AI workers needed.


## Revoking Gmail/Email access from nylas

After you have tested the app and want to disconnect the nylas API from your Gmail/Email account, you can revoke access from 
Google/Provider account settings > Data from apps and services you use > Third-party apps & services > Nylas 


## Warning :

```
Use this project at your own risk, by using the project you fully understand the risks associated with linking email access to
third party projects. 
Read privacy policy of nylas/cloudflare at their respective websites.
This project is licensed under MIT License and is provided as is without any warranty.
As the author of this project I will not be liable for any damages/liabilities caused by using this project/app.
```

## License : MIT License