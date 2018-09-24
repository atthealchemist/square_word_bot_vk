import sys
import os
import time
import json

from vk_api import VkApi, exceptions
from word import WordFactory


class WordBot:

    config = {}
    commands = []

    def __getUser(self):
        return self.vk.method('users.get', {'user_ids': self.userId})[0]

    def __getChat(self):
        return self.vk.method('messages.getChat', {'chat_id': self.chatId})

    def __sendMessage(self, text):
        self.vk.method('messages.send', {
                       'peer_id': self.getPeerId(), 'message': text})

    def parseCommand(self, message):
        
        for cmd in self.commands:
            if cmd['name']['single'] in message:
                count = message.index(cmd['name']['single'])
                words = message.split(' ')
                item = self.factory.item(words[-1])

                command = {
                    'count': words[count],
                    'raw': message,
                    'text': words.join(' ')
                }

                print("bot.parseCommand.command.single", command)

                self.__sendMessage(item)
            elif cmd['name']['multiple'] in message:
                count = message.index(cmd['name']['multiple'])
                words = message.split(' ')
                mult = words[count]

                command = {
                    'count': mult,
                    'raw': message,
                    'text': words[mult+1:len(words)]
                }

                print("bot.parseCommand.command.multi", command)

                endOfCommandIndex = words.index(cmd['name']['miltiple']) + 1
                items = words[endOfCommandIndex:len(words)]
                result = self.factory.item(items)
                self.__sendMessage(result)
    time.sleep(3)

    def getPeerId(self):
        if self.config['settings']['mode'] == "chat":
            return 2000000000 + int(self.chatId)
        else:
            return int(self.userId)

    def getDialogInfo(self):
        if self.config['settings']['mode'] == "user":
            self.requestParams = {'out': 0, 'count': 1,
                                  'time_offset': 60, 'peer_id': self.userId}
            user = self.__getUser()
            userName = user['first_name'] + " " + user['last_name']
            print("Bot is started (for user \"{0}\" (id: {1})) !".format(
                userName, self.userId))
        else:
            self.requestParams = {'out': 0, 'count': 1,
                                  'time_offset': 60, 'peer_id': self.getPeerId()}
            chat = self.__getChat()
            chatTitle = chat['title']
            print("Bot is started (for chat \"{0}\" (chat_id: {1}))!".format(
                chatTitle, self.chatId))

    def loadCommands(self):
        self.commands = self.__loadFromJsonFile("commands.json")

    def loadConfig(self):
        self.config = self.__loadFromJsonFile("config.json")

    def __loadFromJsonFile(self, fileName):
        with open(os.path.join(os.getcwd(), fileName), 'r', encoding='utf8') as jsonfile:
            return json.loads("".join(jsonfile.readlines()))

    def getLatestMessageFromHistory(self):
        response = self.vk.method('messages.getHistory', self.requestParams)
        if response['items']:
            self.requestParams['last_message_id'] = response['items'][0]['id']
        return response['items'][0]['text']

    def __init__(self):

        self.loadConfig()
        self.loadCommands()
        self.factory = WordFactory(self.config)

        loggedIn = self.authenticate(self.config)

        self.getDialogInfo()

        while loggedIn:
            try:
                msg = self.getLatestMessageFromHistory()
                self.parseCommand(msg)
            except exceptions.ApiError:
                pass
    def authenticate(self, config):
        try:
            self.vk = VkApi(
                login=config['credentials']['user'], password=config['credentials']['pwd'])
            self.vk.auth()
        except Exception as ex:
            print("Can't login to VK! Possible reason: {0}".format(ex))
            return False
        finally:
            print("Logged in.")
            if not config['settings']['id']:
                if config['settings']['mode'] == "chat":
                    self.chatId = input("Enter chat id (XX from &sel=cXX): ")
                    print("Your chat id: {0}".format(self.chatId))
                else:
                    self.userId = input("Enter user id (XX from &sel=cXX): ")
            else:
                if config['settings']['mode'] == "chat":
                    self.chatId = config['settings']['id']
                else:
                    self.userId = config['settings']['id']
            return True


if __name__ == "__main__":
    bot = WordBot()
