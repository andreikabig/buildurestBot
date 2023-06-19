import time

from telebot_router import TeleBot
from DatabaseModels import con
from Services.UserService import *
from Services.ProceduresService import ProcedureService
from Services.OrderService import OrderService
from Services.RoleValidatorService import RoleValidatorService
from Services.RestsService import RestsService
from Services.AutoPickUpService import AutoPickUpService

app = TeleBot("BuildurestBot")
ProcedureService.Initialize(app)

@app.route('(?!/).+')
def data_handler(context):
    user = UserService.GetUserByContext(context)
    data = context['text']
    if not ProcedureService.TryContinueProcedure(data, user):
        app.send_message(user.chat_id, "Я вас не понимаю, посмотрите принцип работы с ботом через команду /help.")

@app.route('/help')
def help_handler(context):
    user = UserService.GetUserByContext(context)

    text = "Привет, добро пожаловать в сервис подбора доступного отдыха BUILDUREST!\n\n" \
           "Мы с радостью поможем тебе подробрать именно тот отдых, который тебе нужен.\n" \
           "Наши специалисты готовы ответить в любое время суток.\n\n" \
           "Если ты еще не заполнил информацию о себе, то рекомендуем это сделать через " \
           "команду /about - это поможет нашим алгоритмам более качественно подобрать твой " \
           "незабываемый отдых.\n\n" \
           "Для того, чтобы посмотреть список доступных комманд нажми /cmds.\n"

    app.send_message(user.chat_id, text)

@app.route('/cmds')
def cmds_handler(context):
    user = UserService.GetUserByContext(context)
    text = "Список доступных команд:\n"
    text += "* /help - общая информация,\n" \
            "* /order - оформить бронь,\n" \
            "* /details - информация о бронировании,\n" \
            "* /about - заполнение информации о себе,\n" \
            "* /auto - автоматический подбор отдыха,\n" \
            "* /rests - просмотр всех вариантов активностей.\n"

    app.send_message(user.chat_id, text)

@app.route('/order')
def order_handler(context):
    user = UserService.GetUserByContext(context)
    ProcedureService.StartOrderProcedure(user)

@app.route('/details')
def details_handler(context):
    user = UserService.GetUserByContext(context)
    result = OrderService.GetUserOrdersText(user)
    app.send_message(user.chat_id, result)

@app.route("/orders")
def order_handler(context):
    user = UserService.GetUserByContext(context)

    if RoleValidatorService.ValidateAdminRole(user):
        app.send_message(user.chat_id, "Пока что команда не доступна.")
    else:
        app.send_message(user.chat_id, "Команда доступна только администратору.")

@app.route("/about")
def order_handler(context):
    user = UserService.GetUserByContext(context)
    ProcedureService.StartAboutProcedure(user)

@app.route("/auto")
def auto_handler(context):
    user = UserService.GetUserByContext(context)
    result = AutoPickUpService.PickUp(user)

    app.send_message(user.chat_id, result)

@app.route("/rests")
def rests_handler(context):
    user = UserService.GetUserByContext(context)
    result = RestsService.GetAllRestsText()

    split = result.split("\n\n")

    for res in split:
        app.send_message(user.chat_id, res)
        time.sleep(1)

with open("data/bot.auth", 'r') as file:
    token = file.readline()
    app.config['api_key'] = token

app.poll(debug=True)

con.close()