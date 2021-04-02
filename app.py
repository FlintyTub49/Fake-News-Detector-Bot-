import os
from flask import Flask, request, render_template
import pickle as pk

# from tensorflow.keras.models import load_model
from preprocessing import preprocess_text

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


from rake_nltk import Rake
from googlesearch import search
import urllib.request as urllib

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

codePath = os.path.dirname(os.path.abspath('app.py'))
pipe = os.path.join(codePath, 'Models/100lenPipelineLem.pk')
pipeline = pk.load(open(pipe, 'rb'))

# hello_flag = 0

app = Flask(__name__)


# def set_global_flag(value=1):
#     global hello_flag
#     hello_flag = 1

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

    # vis = ['visualize', 'image', 'wordcloud', 'wordcount']
    # if len(incoming_msg.strip().split(' ')) > 1:
    #     first = incoming_msg.split(' ')[0]
    #     second = incoming_msg.split(' ')[1]

    put_links = False
    # global hello_flag

    # --------------------------
    # First Time Welcome Message
    # --------------------------
    if any(hello == incoming_msg for hello in hello_list):
        # and hello_flag == 0:
        # set_global_flag(value=1)

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

    # ------------------------------------
    # Visualizations Query
    # ------------------------------------
    # elif any(img == first.lower() for img in vis) and len(incoming_msg.strip().split(' ')) > 1:
    #     image = ''
    #     if second == 'fake':
    #         image = os.path.join(codePath, 'wordClouds/wcFake.jpg')

    #     else:
    #         image = os.path.join(codePath, 'wordClouds/wcReal.jpg')
        
    #     # bot.send_photo(chat_id = chat_id, photo = open(image, 'rb'), reply_to_message_id = msg_id)
    #     msg.media(open(image, 'rb'))
    #     responded = True

    else:
        text = preprocess_text(incoming_msg)
        pred = pipeline.predict([text])

        output = ''

        if pred > 0.5:
            output = "The Given News is Real. ✅"
            responded = True

        elif pred < 0.5:
            # ------------------------------------
            # Find Links Related to Keyword Search
            # ------------------------------------
            # sent = incoming_msg.split('.')
            # r = Rake()
            # r.extract_keywords_from_sentences(sent)
            # put_links = True
            # query = ' '.join(r.get_ranked_phrases()[:5])

            # links = []
            # for i in search(query, country = 'india', lang = 'en', num = 3, start = 0, stop = 3):
            #     links.append(i)
            if put_links:
                output = 'The Given News is Fake. ❌\nBelow are some links I found that might\
                     be useful.\n' + links[0] + '\n' + links[1] + '\n' + links[2]
            else:
                output = "The Given News is Fake. ❌"
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
