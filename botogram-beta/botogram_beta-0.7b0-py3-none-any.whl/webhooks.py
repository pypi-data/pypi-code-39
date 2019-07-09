from flask import Flask, request
app = Flask(__name__)

class Webhook:
    def __init__(self, port, ):
        pass
@app.route('/')
def index():
    print(request)
    return 'hello world'
