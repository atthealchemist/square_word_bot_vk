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