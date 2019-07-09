def welcome(request, responder):
    responder.slots['name'] = request.context.get('name', '')
    responder.reply('Hello, {name}. I can help you find store hours '
                    'for your local Kwik-E-Mart. How can I help?')
    responder.listen()
