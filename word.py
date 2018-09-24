class WordFactory:

    def __init__(self, config):
        self.config = config

    def item(self, item):
        print("self.factory.item ", item)
        for cmd in self.config['commands']:
            for word in cmd['name']['single']:
                if word in item:
                    print("self.factory.item.single ", item)
                    if word.strip() in ["квадрат", "square"]:
                        print("--> квадрат")
                        it = item.split(' ')[-1]
                        print(self.square(it))
                        return self.square(it)
            for word in cmd['name']['multiple']:
                if word in item:
                    print("self.factory.item.multi ", item)
                    if word.strip() in ["квадраты", "squares"]:
                        print("--> квадраты")

                        words = item.split(' ')
                        endOfCommandIndex = words.index(word.strip()) + 1
                        items = words[endOfCommandIndex:len(words)]
                        print(self.squares(items))
                        return self.squares(items)

    def squares(self, words):
        squares = []
        for word in words:
            squares.append(self.square(word))
        return squares

    def square(self, word):
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

    def corner(self, word):
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

    def corners(self, words):
        corners = []
        for word in words:
            corners.append(self.corner(word))
        return corners
    
    def verticals(self, words):
        rawWords = words.split(' ')
        verticalWords = []
        verticalWord = ""
        greatestWordLength = self.__getGreatestWordLength(words)
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

    def __getGreatestWordLength(self, words):
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

# if __name__ == '__main__':
#     factory = WordFactory()
#     print(factory.verticals("ремонт обуви копир ключей"))
