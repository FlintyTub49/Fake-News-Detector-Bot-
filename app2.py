from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name, URL
from preprocessing import preprocess_text

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
tokens = os.path.join(codePath, 'Models/90HighBias1D.h5')
model = load_model(tokens)

# ----------------------------------------
# Flag Value To Print Introductory Message
# ----------------------------------------
hello_flag = 0

def set_global_flag(value=1):
    global hello_flag
    hello_flag = 1

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
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = ''
    if any(hello in incoming_msg for hello in hello_list) and hello_flag == 0:
        set_global_flag(value=1)
        response = """_Hi, 
        I am *COVID19 Mythbuster*_ 👋🏻

        ◻️ _In these crazy hyperconnected times, there is a lot of FAKE NEWS spreading about the NOVEL CORONAVIRUS._

        ◻️ _I Can Help You In Differentiating the Fake News From The Real News_ 📰

        ◻️ _All you need to do is send me the news you get to verify if it Real or not._ 

        _It's that simple 😃
        Try it for yourself, simply send me a News About COVID19 and I'll try to tell if it is Fake Or Real_ ✌🏻✅
        """

    else: 
        # ----------------------------------------
        # To Preprocess and Print The Predictions
        # ----------------------------------------
        text = preprocess_text(text)
        pred = model.predict(text)[0][0]

        if pred > 0.5:
            response = "The given news is real"
        elif pred < 0.5:
            response = "The given news is fake"

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
    app.run(threaded=True)