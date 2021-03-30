import os
from flask import Flask, request
import requests

from keras.models import load_model
from twilio.twiml.messaging_response import MessagingResponse

from preprocessing import preprocess_text

codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
tokens = os.path.join(codePath, 'Models/90HighBias1D.h5')
model = load_model(tokens)


app = Flask(__name__)


# -----------------------------------
# Bot Command Reciever And Processor
# -----------------------------------
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


# ---------------------------------
# Mostly To Be Deleted
# ---------------------------------
def main():
    x = input('Please Enter Some Text:')
    x = preprocess_text(x)
    pred = model.predict(x)
    print(pred)


if __name__ == '__main__':
    # app.run()
    main()