'''
Created on Saturday 01/06/2019

@author: yaztown
'''

from flask import send_from_directory#, request, redirect, url_for
from loopie.net.web_app import WebApp

web_app = WebApp.getWebApp()
# from . import api_routes


@web_app.route('/')
def index():
    return web_app.send_static_file('index.html')


@web_app.route('/<path:path>')
def send_file(path):
    return send_from_directory(web_app.static_folder, path)




# @flask_app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name = user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name = user))
# 
# 
# @flask_app.route('/success/<name>')
# def success(name):
#     return 'Welcome {}'.format(name)
