from mindmeld import Application

app = Application(__name__)


@app.handle(intent='greet')
def welcome(request, responder):
    responder.slots['name'] = request.context.get('name', '')
    responder.reply('Hello, {name}. I can help you find store hours '
                    'for your local Kwik-E-Mart. How can I help?')
    responder.listen()


@app.handle(intent='exit')
def say_goodbye(request, responder):
    responder.reply(['Bye', 'Goodbye', 'Have a nice day.'])


@app.handle(default=True)
def default(request, responder):
    responder.reply('Sorry, not sure what you meant there. I can help you find '
                    'store hours for your local Kwik-E-Mart.')
    responder.listen()
