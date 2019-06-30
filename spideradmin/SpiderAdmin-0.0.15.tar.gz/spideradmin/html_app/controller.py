# -*- coding: utf-8 -*-

# @Date    : 2019-06-25
# @Author  : Peng Shiyu

from flask import Blueprint, send_file
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)

html_app = Blueprint(name="html_app", import_name=__name__)


@html_app.route("/")
def admin_vue():
    return send_file(os.path.join(base_dir, "templates/admin-vue.html"))


@html_app.route("/<template>")
def server_vue(template):
    return send_file(os.path.join(base_dir, "templates/{}.html".format(template)))
