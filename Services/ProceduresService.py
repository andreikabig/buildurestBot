from Services.UserService import UserService
from Models.Action import Action
from Models.Procedure import Procedure
from Services.OrderService import OrderService

class IProcedure:
    def __init__(self, app):
        self.app = app

class AboutProcedure(IProcedure):
    ACTION_NAME_ABOUT = "Инфо"

    def __init__(self, app):
        super(AboutProcedure, self).__init__(app)

    def ask_about(self, chatid):
        self.app.send_message(chatid, "В одном сообщении расскажите о себе, это поможет нашим умным алгоритмам подбирать вам отдых.")

    def about_procedure_end_handler(self, actions, chatid):
        about = ""

        for action in actions:
            if action.name == AboutProcedure.ACTION_NAME_ABOUT:
                about = action.params

        user = UserService.GetUserByChatId(chatid)

        user.about = about
        user.save()

        self.app.send_message(chatid,
                         f"Спасибо большое за информацию!")

        admins = UserService.GetAdmins()

        for admin in admins:
            self.app.send_message(admin.chat_id, f"Информация о пользователе: {user.username},{user.first_name},{user.last_name}\n{about}")


    def about_data_handler(self, text):
        return text


class OrderProcedure(IProcedure):
    ACTION_NAME_DETAILS = "Детали"
    ACTION_NAME_PERSONS = "Кол-во человек"

    def __init__(self, app):
        super(OrderProcedure, self).__init__(app)

    def ask_order_details(self, chatid):
        self.app.send_message(chatid, "Опишите детали отдыха, который вы бы хотели забронировать (одним сообщением). \nУкажите ваш номер телефона.")

    def ask_persoons(self, chatid):
        self.app.send_message(chatid, "Какое количество человек будет на отдыхе (одним сообщением)?")

    def order_procedure_end_handler(self, actions, chatid):
        details = ""
        count = ""

        for action in actions:
            if action.name == OrderProcedure.ACTION_NAME_DETAILS:
                details = action.params
            elif action.name == OrderProcedure.ACTION_NAME_PERSONS:
                count = action.params

        user = UserService.GetUserByChatId(chatid)

        order = {'details': details, 'count': count}

        OrderService.AddUserOrder(user, order)

        self.app.send_message(chatid,
                         f"Спасибо большое за информацию, в ближайшее время с Вами свяжется менеджер и обсудит детали.")

        admins = UserService.GetAdmins()

        for admin in admins:
            self.app.send_message(admin.chat_id, f"Новая бронь:\n{details}\nКол-во человек: {count}\n{user.username},{user.first_name},{user.last_name}")


    def persons_data_handler(self, count):
        return count

    def details_data_handler(self, details):
        return details

class ProcedureService:
    usersProcedures = dict()
    orderProcedure = None
    aboutProcedure = None

    @staticmethod
    def Initialize(app):
        ProcedureService.orderProcedure = OrderProcedure(app)
        ProcedureService.aboutProcedure = AboutProcedure(app)

    @staticmethod
    def StartOrderProcedure(user):
        procedure = Procedure('Бронирование', user.chat_id, ProcedureService.orderProcedure.order_procedure_end_handler)
        action1 = Action(OrderProcedure.ACTION_NAME_DETAILS, ProcedureService.orderProcedure.ask_order_details, ProcedureService.orderProcedure.details_data_handler)
        action2 = Action(OrderProcedure.ACTION_NAME_PERSONS, ProcedureService.orderProcedure.ask_persoons, ProcedureService.orderProcedure.persons_data_handler)
        procedure.actions = [action1, action2]
        ProcedureService.usersProcedures[user.chat_id] = procedure
        procedure.StartProcedure()

    @staticmethod
    def StartAboutProcedure(user):
        procedure = Procedure('Информация', user.chat_id, ProcedureService.aboutProcedure.about_procedure_end_handler)
        action1 = Action(AboutProcedure.ACTION_NAME_ABOUT, ProcedureService.aboutProcedure.ask_about, ProcedureService.aboutProcedure.about_data_handler)
        procedure.actions = [action1]
        ProcedureService.usersProcedures[user.chat_id] = procedure
        procedure.StartProcedure()

    @staticmethod
    def GetUserProcedure(user):
        try:
            return ProcedureService.usersProcedures[user.chat_id]
        except:
            return None

    @staticmethod
    def TryContinueProcedure(data, user):
        proc = ProcedureService.GetUserProcedure(user)
        if proc is not None:
            if proc.ContinueProcedure(data) is False:
                del ProcedureService.usersProcedures[user.chat_id]
            return True

        return False