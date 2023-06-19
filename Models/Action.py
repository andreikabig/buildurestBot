class Action:
    def __init__(self, name, method, argsHandler):
        self.name = name
        self.isDone = False
        self.params = []
        self.method = method
        self.argsHandler = argsHandler

    def BeginInvoke(self, chatid):
        self.method(chatid)

    def EndInvoke(self, args):
        self.params = self.argsHandler(args)
        self.isDone = True
