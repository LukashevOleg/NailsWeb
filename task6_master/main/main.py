import json
from os import path

from werkzeug.utils import redirect

from task6_master.main.bot.bot import Bot

from flask import Flask, render_template, request, make_response, url_for
from task6_master.main.data_base.base_connect import BaseConnect

app = Flask(__name__)

menu = [{"name": "Авторизация", "url": "login"},
        {"name": "Бот", "url": "second"}]

# arrMessage = [
#     {'id': 1, 'mes': "Привет, с моей помощью Вы сможете записаться на ноготочки!"},
#     {'id': 2, 'mes': "Second"},
#     {'id': 3, 'mes': "third"}]

bot = Bot()
db = BaseConnect()


@app.route("/")
def root():
    return render_template("root.html", title="Olegofriend", menu=menu)


@app.route("/login", methods=['GET', 'POST'])
def index():
    cookie = ""
    res = make_response(render_template("first.html", title="Olegofriend", menu=menu))
    if request.method == 'POST':
        data = request.form.get('name_user')
        # Processor().add_user(name=cookie)
        #     cookie = data.get('name')
        print(data)
        res.set_cookie('name', data, max_age=60 * 60 * 24 * 365)
        # return redirect(url_for('second'))

    return res


@app.route("/first", methods=['GET', 'POST'])
def first():
    # if request.method == 'GET':
    #     Processor().add_user(request.cookies.get('name'))
    return render_template('second.html', title="Olegofriend", menu=menu)


@app.route("/second", methods=['GET', 'POST'])
def second():
    # print(request.cookies.get('name'))
    # print("name " + str(request.cookies.get('name')))
    arr_message = []
    name = request.cookies.get('name')
    id = BaseConnect().find_user_by_name(name)
    if id is None:
        BaseConnect().add_user(name)
        id = BaseConnect().find_user_by_name(name)

    if request.method == 'POST':
        arr_message = bot.get_answer(id, str(request.form.get('message')), get_link_from_json())
        # print()
    # else:
    #     print("loser")
    return render_template('second.html', title="Second", menu=menu, arrMessage=arr_message)




def get_link_from_json():
    with open("config.json") as json_data_file:
        link = (json.load(json_data_file))['link']
    return str(link)


if __name__ == '__main__':
    # get_link_from_json()
    app.run(host='0.0.0.0', port=4556)
    # BaseConnect().delete_user()

    # db.add_client("AbuAbu")
    # db.get_list_client()
