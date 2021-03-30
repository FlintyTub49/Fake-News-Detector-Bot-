import os
from flask import Flask, request, render_template
import requests

from keras.models import load_model
from twilio.twiml.messaging_response import MessagingResponse

from preprocessing import preprocess_text

codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
tokens = os.path.join(codePath, 'Models/90HighBias1D.h5')
model = load_model(tokens)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


# -----------------------------------
# Bot Command Reciever And Processor
# -----------------------------------
@app.route('/bot', methods=['POST'])
def bot():
    # input_text = request.form["tweet"]
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    # if 'quote' in incoming_msg:
    #     # return a quote
    #     r = requests.get('https://api.quotable.io/random')
    #     if r.status_code == 200:
    #         data = r.json()
    #         quote = f'{data["content"]} ({data["author"]})'
    #     else:
    #         quote = 'I could not retrieve a quote at this time, sorry.'
    #     msg.body(quote)
    #     responded = True
    # if 'cat' in incoming_msg:
    #     # return a cat pic
    #     msg.media('https://cataas.com/cat')
    #     responded = True

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
        msg.body('I only know about famous quotes and cats, sorry!')

    return str(resp)


# -----------------------------------
# Reciever And Processor Test Function
# -----------------------------------
@app.route('/', methods=['POST'])
def test():
    input_text = request.form["tweet"]
    input_button = request.form["button"]

    print(input_text)
    print(input_button)

    text = preprocess_text(input_text)
    pred = model.predict(text)

    return render_template("index.html", pred=str(pred))

# ---------------------------------
# Mostly To Be Deleted
# ---------------------------------


def main():
    x = input('Please Enter Some Text:')
    x = preprocess_text(x)
    pred = model.predict(x)
    print(pred)


if __name__ == '__main__':
    app.run(debug=True)
    # main()
