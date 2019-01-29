class Player(object):
    """Участники игры."""
    def __init__(self,name,score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep

def ask_yes_no(question):
    """Задает вопрос с ответом да или нет."""
    response = None
    while response not in ("y","n"):
        response = input(question).lower()
    return response

def ask_number(question,low,high):
    """Просит ввести число из заданного диапозона."""
    response = None
    while response not in range(low,high):
        response = int(input(question))
    return response

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую , а не импортировали его.")
    input("Нажмите Enter , чтобы выйти.")
    
