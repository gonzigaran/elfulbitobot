import logging
import requests
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from config import token, api_url


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola soy el fulbito")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="que decí?")

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def info_jugador(update: Update, context: CallbackContext):
    url = api_url + "jugadores/" + "".join(context.args)
    print(url)
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Access-Control-Allow-Origin': '*'}
    r = requests.get(url, headers=headers)
    jugador_json = r.json()
    jugador_text = "Partidos jugados: %s \nPuntos: %s \nPromedio: %.2f \nGanados: %s \nEmpatados: %s \nPerdidos: %s " % (
        jugador_json['Partidos jugados'],
        jugador_json['Puntos'],
        float(jugador_json['Promedio']),
        jugador_json['Resultados']['Ganados'],
        jugador_json['Resultados']['Empatados'],
        jugador_json['Resultados']['Perdidos']
        ) 
    context.bot.send_message(chat_id=update.effective_chat.id, text=jugador_text)

info_jugador_handler = CommandHandler('info_jugador', info_jugador)
dispatcher.add_handler(info_jugador_handler)




def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="escribí bien el comando!")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()