class OrderService:
    userOrders = dict()

    @staticmethod
    def GetUserOrders(user):
        try:
            return OrderService.userOrders[user.chat_id]
        except:
            return None

    @staticmethod
    def AddUserOrder(user, details):
        userOrders = OrderService.GetUserOrders(user)

        if userOrders is None:
            OrderService.userOrders[user.chat_id] = [details]
        else:
            OrderService.userOrders[user.chat_id].append(details)

    @staticmethod
    def GetUserOrdersText(user):
        text = "Нет актуального бронирования. Возможно произошла ошибка, обратитесь в тех. поддержку."

        userOrders = OrderService.GetUserOrders(user)

        if userOrders is not None:
            text = ""
            i = 1
            for details in userOrders:
                text += f"Заказ {i}\nДетали заказа: {details['details']}\nКол-во человек: {details['count']}"
                i += 1

        return text

