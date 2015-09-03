__author__ = 'Aleksi'
import threading
class Plugin_loader:
    def __init__(self, bot):
        self.teeBot = bot
        self.plugins = []
        self.initialize()
    def register(self, plugin):
        self.plugins.append(plugin)
        pass
    def event_handler(self, event):
        thread_list = []
        for x in self.plugins:
            if event[-1] in x.handle_events or "*" in x.handle_events:
                t = threading.Thread(target=x.handle, args=(event, self.teeBot,))
                thread_list.append(t)
                t.start()
        for x in thread_list:
            #x.start
            x.join()

    def initialize(self):
        from Plugins import Bot_Commands
        self.register(Bot_Commands.BotCommands())
