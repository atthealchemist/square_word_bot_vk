def make_square_word(word):
    square_word = ""
    if word != "":
        word = list(word)
        current_index = 0
        while current_index < len(word):
            for row_index, letter in enumerate(word):
                # print(word[row_index], end=" ")
                square_word += (word[row_index] + " ")
            first = word.pop(0)
            word.append(first)
            # print("")
            square_word += "\n"
            current_index += 1
    # print("")
    square_word += "\n"

    return square_word

def make_corner_word(word):
    corner_word = ""
    if word != "":
        word = list(word)
        for row_index, letter in enumerate(word):
            if(row_index < len(word)):
                corner_word += (word[row_index] + " ")
        corner_word += "\n"
        word.pop(0)
        for row_index, letter in enumerate(word):
            corner_word += (word[row_index] + "\n")

    return corner_word

def get_greatest_word_len(words):
    raw_words = words.split(' ')
    prev = 0
    new = 0
    for word in raw_words:
        if len(word) > new:
            prev = new
            new = len(word)
        else:
            continue
    return new


def make_vertical_words(words):
    raw_words = words.split(' ')
    vertical_words = []
    vertical_word = ""
    greatest_word_len = get_greatest_word_len(words)
    position_in_array = 0
    while len(vertical_words) < greatest_word_len:
        for raw_word in raw_words:
            try:
                for letter_index, letter in enumerate(raw_word[position_in_array]):
                    vertical_word += raw_word[position_in_array] + " "
            except Exception:
                space = " "
                vertical_word += space + " "
                continue
        vertical_words.append(vertical_word)
        if position_in_array < greatest_word_len - 1:
            position_in_array += 1
        vertical_word = ""
    return vertical_words

# if __name__ == '__main__':
#     for word in make_vertical_words("тюльпашки для ромашки"):
#         print(word + "\n")
    #print(make_vertical_words("ремонт обуви_ копир_ ключей"))