from telebot.types import ReplyKeyboardRemove
from dotenv import load_dotenv
from openai import OpenAI
import os, telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BIBLE_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def send_message(message, text, voice_msg_activated, voice):
    try:
        x = voice[message.chat.id]
    except KeyError as e:
        voice[message.chat.id] = "alloy"
        
    try:
        y = voice_msg_activated[message.chat.id]
    except KeyError as e:
        voice_msg_activated[message.chat.id] = False
        
    if voice_msg_activated[message.chat.id]:
        try:
            voice_path = text_to_voice(text, voice[message.chat.id], message.chat.id)
            with open(voice_path, 'rb') as audio:
                bot.send_chat_action(message.chat.id, "upload_audio")
                bot.send_voice(message.chat.id, audio, reply_markup=ReplyKeyboardRemove(), timeout=60)
        except Exception as e:
            print(e)
            bot.send_chat_action(message.chat.id, "typing")
            msg = "Lo siento, el envío del audio ha fallado. Le responderé esta vez con texto."
            bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(message.chat.id, text)
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())
        