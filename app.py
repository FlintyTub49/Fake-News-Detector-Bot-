import os
from flask import Flask, request, render_template
# import requests

from tensorflow.keras.models import load_model

from preprocessing import preprocess_text

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
tokens = os.path.join(codePath, 'Models/codalab_df_listone.h5')
model = load_model(tokens)

hello_flag = 0

app = Flask(__name__)


def set_global_flag(value=1):
    global hello_flag
    hello_flag = 1


# @app.before_request
# def init_global_flag():
#     g.hello_flag = 0


@app.route('/')
def home():
    return render_template("index.html")

# CODE FOR REQUESTS ONLINE ON SEARCH/ASKING FROM USER
    # # return a quote
    # r = requests.get('https://api.quotable.io/random')
    # if r.status_code == 200:
    #     data = r.json()
    #     quote = f'{data["content"]} ({data["author"]})'
    # else:
    #     quote = 'I could not retrieve a quote at this time, sorry.'

    # if 'cat' in incoming_msg:
    #     # return a cat pic
    #     msg.media('https://cataas.com/cat')
    #     responded = True



# -----------------------------------
# Bot Command Reciever And Processor
# -----------------------------------
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    hello_list = ['hello', 'hey', 'start', 'hi']
    global hello_flag

    # --------------------------
    # First Time Welcome Message
    # --------------------------
    if any(hello in incoming_msg for hello in hello_list) and hello_flag == 0:
        set_global_flag(value=1)

        hello_message = """_Hi,_ 
        _I am *COVID19 Mythbuster*_ 👋🏻

        ◻️ _In these crazy hyperconnected times, there is a lot of FAKE NEWS spreading about the NOVEL CORONAVIRUS._

        ◻️ _I Can Help You In Differentiating the Fake News From The Real News_ 📰

        ◻️ _All you need to do is send me the news you get to verify if it Real or not._ 

        _It's that simple_ 😃
        _Try it for yourself, simply send me a News About COVID19 and I'll try to tell if it is Fake Or Real_ ✌🏻✅
        """

        msg.body(hello_message)
        responded = True

    else:
        text = preprocess_text(incoming_msg)
        pred = model.predict(text)[0][0]

        output = ''

        if pred > 0.5:
            output = "The given news is real"
            responded = True
        elif pred < 0.5:
            output = "The given news is fake"
            responded = True

        msg.body(output)

    if not responded:
        msg.body(
            """That didn't quite work! Try some other text, or send a
            Hello to get started if you haven't already""")

    return str(resp)


if __name__ == '__main__':
    hello_flag = 0
    app.run(debug=True)
