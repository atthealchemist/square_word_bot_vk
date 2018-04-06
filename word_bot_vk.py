import sys
import time
import vk_api
from word import make_square_word, make_corner_word, make_vertical_words

vk = vk_api.VkApi(login=sys.argv[1], password=sys.argv[2])
vk.auth()
send_type = sys.argv[3]
get_id = sys.argv[4]
username = ""
if(send_type == "user"):
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
        if("сделай квадрат " in word):
            # print("Message: {0}".format(word))
            word = word.split(' ')
            w = word[-1]
            if(send_type == "user"):
                vk.method('messages.send', {
                          'peer_id': get_id, 'message': make_square_word(w)})
            else:
                vk.method('messages.send', {
                          'peer_id': 2000000000 + int(get_id), 'message': make_square_word(w)})
        elif("сделай квадраты" in word):
            # print("Making more than 1 square")
            words = word.split(" ")
            cmd_end_index = words.index("квадраты") + 1
            for w in words[cmd_end_index:len(words)]:
                if(send_type == "user"):
                    vk.method('messages.send', {
                              'peer_id': get_id, 'message': make_square_word(w)})
                else:
                    vk.method('messages.send', {
                              'peer_id': 2000000000 + int(get_id), 'message': make_square_word(w)})
        elif("сделай угол " in word):
            word = word.split(' ')
            w = word[-1]
            if(send_type == "user"):
                vk.method('messages.send', {
                          'peer_id': get_id, 'message': make_corner_word(w)})
            else:
                vk.method('messages.send', {
                          'peer_id': 2000000000 + int(get_id), 'message': make_corner_word(w)})
        elif("сделай углы" in word):
            words = word.split(" ")
            cmd_end_index = words.index("углы") + 1
            for w in words[cmd_end_index:len(words)]:
                if(send_type == "user"):
                    vk.method('messages.send', {
                              'peer_id': get_id, 'message': make_corner_word(w)})
                else:
                    vk.method('messages.send', {
                              'peer_id': 2000000000 + int(get_id), 'message': make_corner_word(w)})
        elif("сделай вертикаль" in word):
            words = word.split(" ")
            cmd_end_index = words.index("вертикаль") + 1
            for word in words[cmd_end_index:len(words)]):
                if(send_type == "user"):
                    print(" ".join(words[cmd_end_index:len(words)]))
                    vk.method('messages.send', {
                                'peer_id': get_id, 'message': make_vertical_words(word)
                else:
                    vk.method('messages.send', {
                                'peer_id': 2000000000 + int(get_id), 'message': make_vertical_words(word)
        else:
            pass
    time.sleep(3)
