from openai import OpenAI
from dotenv import load_dotenv
import telebot, assistant, os
from flask import Flask, request
from pyngrok import ngrok, conf
from waitress import serve
import time

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
bot = telebot.TeleBot(os.getenv("BIBLE_TOKEN"))
web_server = Flask(__name__)
voice_msg_activated = {}
voice = {}

@bot.message_handler(func = lambda message: "@EasyBible" in message.text)
def handle_message(message):
    print("Bot mencionado!")
    print(f"{message.from_user.username}: {message.text[12:]}")
    
    sms = f"El usuario {message.from_user.username} te ha mencionado en un grupo de telegram al que perteneces con el siguiente mensaje: {message.text}"
    data = {
        "id": message.chat.id, 
        "message": sms
    }
    ans = assistant.send_message(data)
    bot.reply_to(message, ans)


@web_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200


if __name__ == "__main__":
    print("Iniciando Bot")
    
    """ NGROK_TOKEN = os.getenv('NGROK_TOKEN')
    conf.get_default().config_path = "./config_ngrok.yml"
    conf.get_default().region = "eu"
    ngrok.set_auth_token(NGROK_TOKEN)
    ngrok_tunel = ngrok.connect(3031, bind_tls = True)
    ngrok_url = ngrok_tunel.public_url
    print(ngrok_url)
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url = ngrok_url) """
    
    bot.set_webhook(url = "https://telegram-bible.onrender.com")
    serve(web_server, host = "0.0.0.0", port = 3031)
    #web_server.run(host="0.0.0.0", port=5000)