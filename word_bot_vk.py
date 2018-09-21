import sys
import os
import time
import json

from vk_api import VkApi
from word import MakeSquare, MakeCorner, MakeVerticals


class WordBot:
    config = {}

    commands = [
        {
            'type': 'command',
            'function': MakeSquare,
            'single': 'квадрат',
            'multiple': 'квадраты',
        },
         {
            'type': 'command',
            'function': MakeCorner,
            'single': 'угол',
            'multiple': 'углы',
        },
         {
            'type': 'command',
            'function': MakeVerticals,
            'single': 'вертикаль',
            'multiple': 0,
        },
    ]

    def execute(self, command):
        locals()[command]()

    def parseCommand(self, message):
        if "сделай квадрат " in message:
            # print("Message: {0}".format(word))
            word = message.split(' ')
            arg = word[-1]
            self.vk.method('messages.send', {'peer_id': self.getPeerId(), 'message': MakeSquare(arg)})
        elif "сделай квадраты" in message:
            # print("Making more than 1 square")
            words = message.split(" ")
            cmd_end_index = words.index("квадраты") + 1
            for w in words[cmd_end_index:len(words)]:
                self.vk.method('messages.send', {'peer_id': self.getPeerId(), 'message': MakeSquare(w)})
        elif "сделай угол " in message:
            word = message.split(' ')
            w = word[-1]
            self.vk.method('messages.send', {'peer_id': self.getPeerId(), 'message': MakeCorner(w)})
        elif "сделай углы" in message:
            words = message.split(" ")
            cmd_end_index = words.index("углы") + 1
            for w in words[cmd_end_index:len(words)]:
                self.vk.method('messages.send', {'peer_id': self.getPeerId(), 'message': MakeCorner(w)})
        elif "сделай вертикаль" in message:
            words = message.split(" ")
            cmd_end_index = words.index("вертикаль") + 1
            for word in MakeVerticals(words[-1]):
                self.vk.method('messages.send', {'peer_id': self.getPeerId(), 'message': word + '\n'})
        else:
            pass
    time.sleep(3)
                

    def getPeerId(self):
        if self.config['settings']['mode'] == "chat":
            return 2000000000 + int(self.chatId)
        else:
            return int(self.userId)

    def getDialogInfo(self):
        if self.config['settings']['mode'] == "user":
            self.requestParams = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': self.userId}
            user = self.vk.method('users.get', {'user_ids': self.userId})[0]
            userName = user['first_name'] + " " + user['last_name']
            print("Bot is started (for user \"{0}\" (id: {1})) !".format(
                userName, self.userId))
        else:
            self.requestParams = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': self.getPeerId()}
            chat = self.vk.method('messages.getChat', {'chat_id': self.chatId})
            chatTitle = chat['title']
            print("Bot is started (for chat \"{0}\" (chat_id: {1}))!".format(
                chatTitle, self.chatId))

    def loadConfig(self):
        with open(os.path.join(os.getcwd(), "config.json"), 'r', encoding='utf8') as jsonfile:
            self.config = json.loads("".join(jsonfile.readlines()))

    def getLatestMessageFromHistory(self):
        response = self.vk.method('messages.getHistory', self.requestParams)
        if response['items']:
            self.requestParams['last_message_id'] = response['items'][0]['id']
        return response

    def __init__(self):
        self.loadConfig()

        loggedIn = self.authenticate(
            self.config['credentials']['user'], self.config['credentials']['pwd'])
        if self.config['settings']['mode'] == "chat":
            self.chatId = input("Enter chat id (XX from &sel=cXX): ")
            print("Your chat id: {0}".format(self.chatId))
        else:
            self.userId = input("Enter user id (XX from &sel=cXX): ")

        self.getDialogInfo()

        while loggedIn:
            msg = self.getLatestMessageFromHistory()
            msgText = msg['items'][0]['text']
            self.parseCommand(msgText)

    def authenticate(self, user, pwd):
        try:
            self.vk = VkApi(login=user, password=pwd)
            self.vk.auth()
        except Exception as ex:
            print("Can't login to VK! Possible reason: {0}".format(ex))
            return False
        finally:
            print("Logged in")
            return True


if __name__ == "__main__":
    bot = WordBot()

'''
    send_type = "chat"
    get_id = sys.argv[4]
    username = ""

    response_body = "text"
    user_id = int(get_id)
    chat_id = 2000000000 + int(get_id)

    login = input("Enter login: ")
    pwd = input("Enter password: ")

    if login and pwd:
        authenticate(login, pwd)
        print("Stored login and password in config.json")

    if(send_type == "user"):
        values = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': user_id}
        user = vk.method('users.get', {'user_ids': get_id})[0]
        username = user['first_name'] + " " + user['last_name']
        print("Bot is started (for user \"{0}\" (id: {1})) !".format(
            username, get_id))
    else:
        values = {'out': 0, 'count': 1, 'time_offset': 60,
                  'peer_id': chat_id}
        chat = vk.method('messages.getChat', {'chat_id': get_id})
        chat_title = chat['title']
        print("Bot is started (for chat \"{0}\" (chat_id: {1}))!".format(
            chat_title, get_id))

    while True:
        response = vk.method('messages.getHistory', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            #print("dd {0}".format(item))
            # user_id = item['user_id']
            word = item[response_body]
            if("сделай квадрат " in word):
                # print("Message: {0}".format(word))
                word = word.split(' ')
                w = word[-1]
                if(send_type == "user"):
                    vk.method('messages.send', {
                        'peer_id': get_id, 'message': MakeSquare(w)})
                else:
                    vk.method('messages.send', {
                        'peer_id': 2000000000 + int(get_id), 'message': MakeSquare(w)})
            elif("сделай квадраты" in word):
                # print("Making more than 1 square")
                words = word.split(" ")
                cmd_end_index = words.index("квадраты") + 1
                for w in words[cmd_end_index:len(words)]:
                    if(send_type == "user"):
                        vk.method('messages.send', {
                            'peer_id': get_id, 'message': MakeSquare(w)})
                    else:
                        vk.method('messages.send', {
                            'peer_id': 2000000000 + int(get_id), 'message': MakeSquare(w)})
            elif("сделай угол " in word):
                word = word.split(' ')
                w = word[-1]
                if(send_type == "user"):
                    vk.method('messages.send', {
                        'peer_id': get_id, 'message': MakeCorner(w)})
                else:
                    vk.method('messages.send', {
                        'peer_id': 2000000000 + int(get_id), 'message': MakeCorner(w)})
            elif("сделай углы" in word):
                words = word.split(" ")
                cmd_end_index = words.index("углы") + 1
                for w in words[cmd_end_index:len(words)]:
                    if(send_type == "user"):
                        vk.method('messages.send', {
                            'peer_id': get_id, 'message': MakeCorner(w)})
                    else:
                        vk.method('messages.send', {
                            'peer_id': 2000000000 + int(get_id), 'message': MakeCorner(w)})
            elif("сделай вертикаль" in word):
                words = word.split(" ")
                cmd_end_index = words.index("вертикаль") + 1
                for word in words[cmd_end_index:len(words)]:
                    if(send_type == "user"):
                        print(" ".join(words[cmd_end_index:len(words)]))
                        vk.method('messages.send', {
                            'peer_id': get_id, 'message': MakeVerticals(word)})
                    else:
                        vk.method('messages.send', {
                            'peer_id': 2000000000 + int(get_id), 'message': MakeVerticals(word)})
            else:
                pass
        time.sleep(3)
'''
