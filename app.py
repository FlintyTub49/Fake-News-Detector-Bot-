from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name, URL
from preprocessing import preprocess_text
# from keras.models import load_model
import pickle as pk
import os

from rake_nltk import Rake
from googlesearch import search
import urllib.request as urllib

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

codePath = os.path.dirname(os.path.abspath('app.py'))
pipe = os.path.join(codePath, 'Models/100lenPipelineLem.pk')
pipeline = pk.load(open(pipe, 'rb'))

# ----------------------------------------
# Flag Value To Print Introductory Message
# ----------------------------------------
# hello_flag = 0

# def set_global_flag(value=1):
#     global hello_flag
#     hello_flag = 1

app = Flask(__name__)


# ----------------------------------------
# To Get and Send Message
# ----------------------------------------

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    try:
        text = update.message.text.encode('utf-8').decode()
    except AttributeError as error:
        bot.sendMessage(chat_id=chat_id, text='No Response Received', reply_to_message_id=msg_id)
        return 'ok'

    print("got text message :", text)

    hello_list = ['hello', 'hey', 'start', 'hi']

    # vis = ['visualize', 'image', 'wordcloud', 'wordcount']
    # if len(text.strip().split(' ')) > 1:
    #     first = text.lower().split(' ')[0]
    #     second = text.lower().split(' ')[1]

    global hello_flag
    put_links = False
    response = 'No Response'
    if any(hello == text.lower() for hello in hello_list):
        #  and hello_flag == 0:
        # set_global_flag(value=1)
        response = """Hi, 
        I am COVID19 Mythbuster 👋🏻

        ◻️ In these crazy hyperconnected times, there is a lot of FAKE NEWS spreading about the NOVEL CORONAVIRUS.

        ◻️ I Can Help You In Differentiating the Fake News From The Real News 📰

        ◻️ All you need to do is send me the news you get to verify if it Real or not. 

        It's that simple 😃
        Try it for yourself, simply send me a News About COVID19 and I'll try to tell if it is Fake Or Real. ✌🏻✅
        """

    # ----------------------------------------
    # To Send Images
    # ----------------------------------------
    # elif any(img == first.lower() for img in vis) and len(text.strip().split(' ')) > 1:
    #     image = ''
    #     if second == 'fake':
    #         image = os.path.join(codePath, 'wordClouds/wcFake.jpg')

    #     else:
    #         image = os.path.join(codePath, 'wordClouds/wcReal.jpg')
        
    #     bot.send_photo(chat_id = chat_id, photo = open(image, 'rb'), reply_to_message_id = msg_id)
    #     return 'ok'


    else:
        # ----------------------------------------
        # To Preprocess and Print The Predictions
        # ----------------------------------------
        text_new = preprocess_text(text)
        pred = pipeline.predict([text_new])

        if pred > 0.5:
            response = "The given news is real. ✅"

        elif pred < 0.5:
            # ------------------------------------
            # Find Links Related to Keyword Search
            # ------------------------------------
            # sent = text.split('.')
            # r = Rake()
            # r.extract_keywords_from_sentences(sent)
            # put_links = True
            # query = ' '.join(r.get_ranked_phrases()[:5])

            # links = []
            # for i in search(query, country = 'india', lang = 'en', num = 3, start = 0, stop = 3):
            #     links.append(i)
            if put_links:
                response = 'The Given News is Fake. ❌\nBelow are some links I found that might\
                     be useful.\n' + links[0] + '\n' + links[1] + '\n' + links[2]
            else:
                response = "The Given News is Fake. ❌"

    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'


# ----------------------------------------
# Webhook To See If Our App Is Working
# ----------------------------------------
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    hello_flag = 0
    app.run(threaded=True)
