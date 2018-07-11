import sys
import time
import vk_api
from PyQt5.QtCore import QRunnable, pyqtSlot

from word import MakeSquare, MakeCorner, MakeVerticals


class Bot(QRunnable):

    def getChatTitle(self, chatId):
        if not self.isUser:
            chat = self.__getChat(chatId)
            return chat["title"]

    def getUserName(self, userId):
        if self.isUser:
            user = self.__getUser(userId)
            return f"{user['name']} {user['last_name']}"

    def sendSquare(self, word):
        aliases = ("квадрат", "квадр", "sqr", "square", "sqrt")

        if word in aliases:
            self.__performCommand(function=MakeSquare(word), keyword=word)

    def sendCorner(self, keyword, word):
        aliases = ("угол", "углы")

        if keyword in aliases:
            self.__performCommand(keyword, MakeCorner(word))

    def sendVertical(self, keyword, word):
        aliases = ("вертикаль", "вертикали")

        if keyword in aliases:
            self.__performCommand(keyword, MakeVerticals(word))

    def __getUser(self, userId):
        return self.vk.method('users.get', {'user_ids': userId})[0]

    def __getChat(self, chatId):
        return self.vk.method('messages.getChat', {'chat_id': chatId})

    def __performCommand(self, keyword, function):
        if self.isUser:
            self.requestParams = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': int(self.vkId)}
        else:
            self.requestParams = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': 2000000000 + int(self.vkId)}
        historyResponse = self.vk.method('messages.getHistory', self.requestParams)
        if historyResponse['items']:
            self.requestParams['last_message_id'] = historyResponse['items'][0]['id']
        for historyMessage in historyResponse['items']:
            userId = historyMessage['user_id']
            message = historyMessage['body']
            if keyword in message:
                lastWord = message.split(' ')[-1]
                self.__sendMessage(function(lastWord))
        time.sleep(3)

    def __sendMessage(self, text):
        self.vk.method('messages.send', {'peer_id': self.vkId, 'message': text})

    def start(self):
        try:
            self.vk = vk_api.VkApi(login=self.login, password=self.passwd)
            self.vk.auth()
        except Exception as ex:
            print(f"Can't login to vk! Possible reason: {ex}")
        finally:
            self.run()

    def setVkId(self, id, isUser):
        self.isUser = isUser
        if self.isUser:
            self.vkId = id
        else:
            self.vkId = 2000000000 + int(id)

    def setCredentials(self, login, passwd):
        self.login = login
        self.passwd = passwd

    @pyqtSlot()
    def run(self):
        while True:
            response = self.vk.method('messages.getHistory', self.requestParams)
            if response['items']:
                self.requestParams['last_message_id'] = response['items'][0]['id']
            for item in response['items']:
                message = item['body']
                if "сделай квадрат " in message:
                    self.sendSquare(message)
                elif "сделай квадраты" in message:
                    words = message.split(" ")
                    cmd_end_index = words.index("квадраты") + 1
                    for word in words[cmd_end_index:len(words)]:
                        self.sendSquare(word)
                elif "сделай угол " in message:
                    self.sendCorner(message)
                elif "сделай углы" in message:
                    self.sendCorner(message)
                elif "сделай вертикаль" in message:
                    words = message.split(" ")
                    cmd_end_index = words.index("вертикаль") + 1
                    for word in words[cmd_end_index:len(words)]:
                        self.sendVertical(word)
                else:
                    pass
            time.sleep(3)

    def __init__(self):
        super(Bot, self).__init__()
        self.isUser = False
        self.vkId = 0


'''
vk = vk_api.VkApi(login=sys.argv[1], password=sys.argv[2])
vk.auth()
send_type = sys.argv[3]
get_id = sys.argv[4]
username = ""
if send_type is "user":
    values = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': int(get_id)}
    user = vk.method('users.get', {'user_ids': get_id})[0]
    username = user['first_name'] + " " + user['last_name']
    print("Bot is started (for user \"{0}\" (id: {1})) !".format(
        username, get_id))
else:
    values = {'out': 0, 'count': 1, 'time_offset': 60,
              'peer_id': 2000000000 + int(get_id)}
    chat = vk.method('messages.getChat', {'chat_id': get_id})
    chat_title = chat['title']
    print("Bot is started (for chat \"{0}\" (chat_id: {1}))!".format(
        chat_title, get_id))

while True:
    response = vk.method('messages.getHistory', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        user_id = item['user_id']
        word = item['body']
        if ("сделай квадрат " in word):
            # print("Message: {0}".format(word))
            word = word.split(' ')
            w = word[-1]
            if (send_type == "user"):
                vk.method('messages.send', {
                    'peer_id': get_id, 'message': MakeSquare(w)})
            else:
                vk.method('messages.send', {
                    'peer_id': 2000000000 + int(get_id), 'message': MakeSquare(w)})
        elif ("сделай квадраты" in word):
            # print("Making more than 1 square")
            words = word.split(" ")
            cmd_end_index = words.index("квадраты") + 1
            for w in words[cmd_end_index:len(words)]:
                if (send_type == "user"):
                    vk.method('messages.send', {
                        'peer_id': get_id, 'message': MakeSquare(w)})
                else:
                    vk.method('messages.send', {
                        'peer_id': 2000000000 + int(get_id), 'message': MakeSquare(w)})
        elif "сделай угол " in word:
            word = word.split(' ')
            w = word[-1]
            if send_type is "user":
                vk.method('messages.send', {
                    'peer_id': get_id, 'message': MakeCorner(w)})
            else:
                vk.method('messages.send', {
                    'peer_id': 2000000000 + int(get_id), 'message': MakeCorner(w)})
        elif "сделай углы" in word:
            words = word.split(" ")
            cmd_end_index = words.index("углы") + 1
            for w in words[cmd_end_index:len(words)]:
                if send_type is "user":
                    vk.method('messages.send', {
                        'peer_id': get_id, 'message': MakeCorner(w)})
                else:
                    vk.method('messages.send', {
                        'peer_id': 2000000000 + int(get_id), 'message': MakeCorner(w)})
        elif "сделай вертикаль" in word:
            words = word.split(" ")
            cmd_end_index = words.index("вертикаль") + 1
            for word in words[cmd_end_index:len(words)]:
                if send_type is "user":
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
