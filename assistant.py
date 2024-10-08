from dotenv import load_dotenv
import os, requests, telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BIBLE_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_message(data):
    bot.send_chat_action(data["id"], "typing")
    URL_API = os.getenv("URL_API")
    headers = {
        "token": os.getenv('TOKEN_API')
    }
    response = requests.post(URL_API, headers=headers, data=data)
    print(f"Codigo de respuesta: {response.status_code}")
    ans = response.json()

    if ans["status_code"] == 200:
        print(f"-Assistant: {ans['message']}")
        #bot.send_message(data["id"], ans["message"], reply_markup=ReplyKeyboardRemove())
        return ans["message"]
    else:
        error = f"Error {ans['status_code']}: {ans['error']}, {ans['message']}"
        print(error)
        #bot.send_message(data["id"], error)
        return error