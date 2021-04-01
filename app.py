import os
from flask import Flask, request, render_template
import requests

from keras.models import load_model

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

app = Flask(__name__)


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


# --------------------------------------
# Reciever And Processor Output Function
# --------------------------------------
@app.route('/', methods=['POST'])
def output():

    # hello_list = ['hello', 'hey', 'start', 'hi']

    input_text = request.form["tweet"]
    input_button = request.form["button"]

    # Unused message, not required for webapp
    # --------------------------
    # First Time Welcome Message
    # --------------------------
    # if any(hello == input_text for hello in hello_list):

    #     hello_message = """_Hi,
    #     I am *COVID19 Mythbuster*_ 👋🏻

    #     ◻️ _In these crazy hyperconnected times, there is a lot of FAKE NEWS spreading about the NOVEL CORONAVIRUS._

    #     ◻️ _I Can Help You In Differentiating the Fake News From The Real News_ 📰

    #     ◻️ _All you need to do is send me the news you get to verify if it Real or not._

    #     _It's that simple 😃
    #     Try it for yourself, simply send me a News About COVID19 and I'll try to tell if it is Fake Or Real_ ✌🏻✅
    #     """

    #     msg.body(hello_message)
    #     responded = True

    # else:
    text = preprocess_text(input_text)
    pred = model.predict(text)[0][0]

    output = ''

    if pred > 0.5:
        output = "The given news is real"
    elif pred < 0.5:
        output = "The given news is fake"

    return render_template("index.html", pred=(output))


if __name__ == '__main__':
    app.run(debug=True)
