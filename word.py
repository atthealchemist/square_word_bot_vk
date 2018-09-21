def MakeSquare(word):
    squareWord = ""
    if word != "":
        word = list(word)
        currentIndex = 0
        while currentIndex < len(word):
            for rowIndex, letter in enumerate(word):
                # print(word[row_index], end=" ")
                squareWord += (word[rowIndex] + " ")
            firstLetter = word.pop(0)
            word.append(firstLetter)
            # print("")
            squareWord += "\n"
            currentIndex += 1
    # print("")
    squareWord += "\n"

    return squareWord

def MakeCorner(word):
    cornerWord = ""
    if word != "":
        word = list(word)
        for rowIndex, letter in enumerate(word):
            if(rowIndex < len(word)):
                cornerWord += (word[rowIndex] + " ")
        cornerWord += "\n"
        word.pop(0)
        for rowIndex, letter in enumerate(word):
            cornerWord += (word[rowIndex] + "\n")

    return cornerWord

def __getGreatestWordLength(words):
    rawWords = words.split(' ')
    prev = 0
    new = 0
    for word in rawWords:
        if len(word) > new:
            prev = new
            new = len(word)
        else:
            continue
    return new


def MakeVerticals(words):
    rawWords = words.split(' ')
    verticalWords = []
    verticalWord = ""
    greatestWordLength = __getGreatestWordLength(words)
    positionInArray = 0
    while len(verticalWords) < greatestWordLength:
        for rawWord in rawWords:
            try:
                for letter_index, letter in enumerate(rawWord[positionInArray]):
                    verticalWord += rawWord[positionInArray] + " "
            except Exception:
                space = " "
                verticalWord += space + " "
                continue
        verticalWords.append(verticalWord)
        if positionInArray < greatestWordLength - 1:
            positionInArray += 1
        verticalWord = ""
    return verticalWords

if __name__ == '__main__':
    for word in MakeVerticals("тюльпашки для ромашки"):
        print(word + "\n")
    print(MakeVerticals("ремонт обуви копир ключей"))
