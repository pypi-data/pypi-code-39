def default(request, responder):
    responder.reply('Sorry, not sure what you meant there. I can help you find '
                    'store hours for your local Kwik-E-Mart.')
    responder.listen()
