from decouple import config
from telegram.ext import Updater, CommandHandler
from response_txt import symptoms_txt, propagation_txt
from bot_oop import ConnectionAPI
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
api = ConnectionAPI(base_url=config('BASE_URL_API'))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy BotCovid19, ¡Bienvenido!")


def symptoms(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=symptoms_txt)


def propagation(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=propagation_txt)


def globals_metrics(update, context):
    data = api.get_response(param='summary')
    global_data = data['Global']
    response_text = f'Nuevos casos: {global_data["NewConfirmed"]}.\n Total Confirmados: {global_data["TotalConfirmed"]}.\n Nuevas Muertes: {global_data["NewDeaths"]}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


def mexico_metrics(update, context):
    data = api.get_response(param='summary')
    countries = data['Countries']
    mexico_index = next((index for (index, d) in enumerate(countries) if d["Slug"] == "mexico"), None)
    data_mexico = countries[mexico_index]
    response_text = f'Casos confirmados:{data_mexico["TotalConfirmed"]},\n Muertes confirmadas: {data_mexico["TotalDeaths"]}'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


def main():
    # Create Updater object and attach dispatcher to it
    updater = Updater(config('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    print("Bot started")

    # Add command handler to dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Add commando handler to Symptoms
    symptoms_handler = CommandHandler('sintomas', symptoms)
    dispatcher.add_handler(symptoms_handler)

    # Add commando handler to propagation
    propagation_handler = CommandHandler('propagacion', propagation)
    dispatcher.add_handler(propagation_handler)

    # Add commando handler to Global Metrics
    metrics_handler = CommandHandler('metricasglobales', globals_metrics)
    dispatcher.add_handler(metrics_handler)

    # Add commando handler to Mexico Metrics
    mexico_handler = CommandHandler('confirmadosmexico', mexico_metrics)
    dispatcher.add_handler(mexico_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()


