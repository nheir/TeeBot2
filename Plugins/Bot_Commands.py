__author__ = 'rand()'

bot_binary = 'teebot'
bot_numbers = 4
bot_port = 3333
bot_config = 'managebot.cfg'
bot_passwd = "azerty"

bot_threshold = 8

server_port = 8303

import subprocess

import telnetlib

class BotTelnet(object):
    def __init__(self, port):
        self.passwd = bot_passwd
        self.host = '127.0.0.1'
        self.port = port
        self.initialize()

    def initialize(self):
        self.process = subprocess.Popen([bot_binary, '-f', bot_config, 'ec_port %d; ec_password %s' % (self.port,self.passwd,)], stdout=subprocess.DEVNULL)

    def connect(self):
        self.tn = telnetlib.Telnet(self.host, self.port)
        self.tn.read_until(b"Enter password:\n")
        self.tn.write(str(self.passwd).encode('utf-8') + b'\n')
        return self.tn

    def writeLine(self, line):
        try:
            self.tn.write(str(line).encode('utf-8') + b"\n")
        except:
            if self.process.poll() == None:
                self.connect()
                self.tn.write(str(line).encode('utf-8') + b"\n")
            else:
                self.initialize()

    def join(self):
        self.writeLine('connect 127.0.0.1:%d' % (server_port,))

    def leave(self):
        self.writeLine('disconnect')


class BotCommands:
    def __init__(self):
        self.handle_events = ["CHAT","CONNECTING", "LEAVE"]
        self.initialize()

    def initialize(self):
        self.bots = [ BotTelnet(bot_port+i) for i in range(bot_numbers)]

    def chat(self,event,bot):
        bot.debug("Bot_Commands is handling this.","PLUGIN")
        msg = event[1]
        nick = event[0]
        id = event[2]
        bot_list = [ t for t in bot.get_Teelista().values() if t.ip == b"127.0.0.1" ]
        player_list = [ t for t in bot.get_Teelista().values() if t.ip != b"127.0.0.1" ]
        if "/skynet" == msg.decode():
            bot.writeLine("set_team_all -1")
            for t in player_list:
                bot.writeLine("set_team %d 0" % t.id)
            for t in bot_list:
                bot.writeLine("set_team %d 1" % t.id)

    def connecting(self, event, bot):
        bc = len([ t for t in bot.get_Teelista().values() if t.ip == b"127.0.0.1" ])
        pc = len([ t for t in bot.get_Teelista().values() if t.ip != b"127.0.0.1" ])
        print(bc,pc)
        while bc > 0 and (bc + pc > bot_threshold or pc == 0):
            self.bots[bc-1].leave()
            bc -= 1
        while pc > 0 and bc < bot_numbers and bc+pc < bot_threshold:
            self.bots[bc].join()
            bc += 1
    def leave(self, event, bot):
        if len([ t for t in bot.get_Teelista().values() if t.ip != "127.0.0.1" ]) == 0:
            for bot in self.bots:
                bot.leave()


    def handle(self, event, bot):
        if event[-1] == "CHAT":
            self.chat(event,bot)
        if event[-1] == "CONNECTING":
            self.connecting(event, bot)
        if event[-1] == "LEAVE":
            self.leave(event, bot)

