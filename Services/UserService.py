from DatabaseModels import Users

class UserService:
    _cache = {}

    @staticmethod
    def GetUserByChatId(chat_id: int):
        user = None
        try:
            user = UserService._cache[chat_id]
        except:
            try:
                user = Users.get(Users.chat_id == chat_id)
                UserService._cache[chat_id] = user
            except:
                return None

        return user

    @staticmethod
    def GetUserByContext(context: dict):
        chat_id = context["chat"]["id"]

        user = UserService.GetUserByChatId(chat_id)

        if user is None:
            return UserService.AddUser(context)

        return user

    @staticmethod
    def GetAdmins():
        admins = Users.select().where(Users.role == 2)
        return admins

    @staticmethod
    def AddUser(context: dict):
        chat_id = context["chat"]["id"]

        try:
            first_name = context['from']["first_name"]
        except:
            first_name = ""

        try:
            last_name = context['from']["last_name"]
        except:
            last_name = ""

        try:
            username = context['from']["username"]
        except:
            username = ""

        language_code = context['from']["language_code"]

        user = Users.create(chat_id=chat_id, is_bot=True, first_name=first_name, last_name=last_name, username=username,
                            language_code=language_code, role=1)
        user.save()

        return user