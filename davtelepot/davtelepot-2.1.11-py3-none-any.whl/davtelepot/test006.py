import sys
from davtelepot.bot import Bot
# from data.passwords import my_token, my_other_token
my_token = '197190910:AAGzsK6eliocHcgFu2WLl2baKQ8hGz0ORag'
my_other_token = '279769259:AAFGbTKEAwcuBCOXlXfbwy2iDaRl654wCtM'

long_polling_bot = Bot(token=my_token, database_url='my_db')
webhook_bot = Bot(token=my_other_token, hostname='example.com',
                  certificate='path/to/certificate.pem',
                  database_url='my_other_db')

@long_polling_bot.command('/foo')
async def foo_command(bot, update, user_record):
  return "Bar!"

@webhook_bot.command('/bar')
async def bar_command(bot, update, user_record):
  return "Foo!"

exit_state = Bot.run()
sys.exit(exit_state)
