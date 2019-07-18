"""Test webhooks integration with aiohttp web apps."""

# Standard library modules
import asyncio
import logging
import os

# Project modules
from bot import Bot
from data.config import (
    local_host, local_port, log_file_name, errors_file_name,
    server_certificate, webhook_url
)
from data.passwords import appbot_token
from utilities import make_button, make_inline_keyboard

# appbot_token = appbot_token.replace('7', '9')

if 1:
    path = os.path.dirname(__file__)
    log_file = "{}/data/{}".format(path, log_file_name)
    errors_file = "{}/data/{}".format(path, errors_file_name)

    # Outputs the log in console, log_file and errors_file
    # Log formatter: datetime, module name (filled with spaces up to 15
    # characters), logging level name (filled to 8), message
    log_formatter = logging.Formatter(
        "%(asctime)s [%(module)s.%(funcName)-10s %(levelname)-8s]     %(message)s",
        style='%'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    file_handler = logging.FileHandler(errors_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_formatter)
    consoleHandler.setLevel(logging.DEBUG)
    root_logger.addHandler(consoleHandler)


bot = Bot(
    appbot_token,
    # hostname='https://www.davte.it:8443/telegram',
    # certificate=server_certificate,
)

Davte = 63538990

# @bot.command(command='/ping')
# async def ping_command(update):
#     """Send a pong when users `/ping`."""
#     return "<i>Pong!</i>"


async def main():
    # result = await bot.sendVenue(
    #     63538990,
    #     45.309804, 8.843633, "chez-nadi", "Corso Torino 57 - Vigevano (PV)",
    #     foursquare_id="4c9bcb505e1a9521370b67f3",
    # )
    # bot.change_maintenance_status("Provone!")
    bot.set_unknown_command_message("Comando sconosciuto?!")
    bot.inline_query_handlers = dict()
    bot.inline_query_handlers[lambda query: query.startswith('a')] = dict(function=lambda update: "Eccolaaaaa")
    @bot.command('ping')
    async def ping_command(bot, update, user_record):
        print(bot.name, user_record)
        return "Pong!"
    # sent = await bot.send_message(Davte, 'ciao')
    # await bot.edit_message_text(update=sent, text="a"*25000)
    # bot.change_maintenance_status("Provone subacqueo.")
    # for i in range(2):
    #     await bot.send_photo(chat_id=63538990, photo='prova.jpg')
    # for i in range(3):
    #     asyncio.ensure_future(
    #         bot.send_message(
    #             chat_id=63538990,
    #             text=f"Message number {i}"
    #         )
    #     )
    #     print(bot.recently_sent_messages)
    await bot.send_message(
        chat_id=63538990,
        **{'text': '<b> Guida all\'uso di DavteTestBot</b>\nSeleziona la sezione della guida di interesse.\nAutore e amministratore del bot: <a href="tg://user?id=63538990">Davte</a>', 'parse_mode': 'HTML', 'reply_markup': {'inline_keyboard': [[{'text': 'Taccuino 📄', 'callback_data': 'help:///notes'}, {'text': 'Modalità inline 💭', 'callback_data': 'help:///inline'}, {'text': 'Doodle 🗳', 'callback_data': 'help:///doodles'}], [{'text': 'Promemoria 🕰', 'callback_data': 'help:///reminders'},{'text': 'CicloPi 🚲', 'callback_data': 'help:///ciclopi'}], [{'text': 'Comandi 🤖', 'callback_data': 'help:///commands'}]]}, 'disable_web_page_preview': True}
    )
    if 0:
        await bot.send_message(
            # text=f"{'Ciao!'*6}\n"*200,
            text=(
                "<b>Grassetto</b>\n"
                "<i>Corsivo</i>\n"
                "<code>7 < 4</code>"
            ),
            chat_id=63538990,
            # reply_markup=make_inline_keyboard(
            #     [make_button('ciao', 'ciao')]
            # )
        )
        with open('prova.txt') as _file:
            await bot.sendDocument(63538990, _file, caption="Prova")
    return


if __name__ == '__main__':
    asyncio.ensure_future(main())
    Bot.run(
        local_host=local_host,
        port=local_port
    )
