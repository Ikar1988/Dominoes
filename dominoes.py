from random import randint

class Domino:

    stock_pieces = []  # не сыгранные домино
    computer_pieces = []  # домино у компьютера
    player_pieces = []  # домино у игрока
    domino_snake = []  # выложенные домино
    status = 'computer'  # указывает, кто сейчас делает ход (computer / player)

    def __init__(self):
        self.stock_pieces = self.create_basic_set()
        self.computer_pieces = self.split_set(self.stock_pieces, 7)
        self.player_pieces = self.split_set(self.stock_pieces, 7)

        computer_piece = self.get_max_piece(self.computer_pieces)
        player_piece = self.get_max_piece(self.player_pieces)

        self.domino_snake = [player_piece]

        if sum(computer_piece) > sum(player_piece):
            self.status = 'player'
            self.computer_pieces.remove(computer_piece)
            self.domino_snake = [computer_piece]
        else:
            self.player_pieces.remove(player_piece)


    def display(self):
        print('=' * 70)
        print("Stock size:", len(self.stock_pieces))
        print("Computer pieces:", len(self.computer_pieces))
        print()
        domino_snake_str = ''

        i = 0
        if len(self.domino_snake) <= 6:
            for item in self.domino_snake:
                domino_snake_str += str(item)
        else:
            for i in (range(0, 3)):
                domino_snake_str += str(self.domino_snake[i])

            domino_snake_str += '...'

            for i in (range(len(self.domino_snake) - 3, len(self.domino_snake))):
                domino_snake_str += str(self.domino_snake[i])

        print(domino_snake_str)
        print()
        print("Your pieces:")
        for i in range(len(self.player_pieces)):
            print(str(i + 1) + ":" + str(self.player_pieces[i]))
        print()


    def create_basic_set(self):
        basic_set = []

        for i in range(4):
            for j in range(7):
                basic_set.append([i, j])

        return basic_set


    def split_set(self, main_set, count):
        new_set = []

        for i in range(count):
            rand_index = randint(0, len(main_set) - 1)
            new_set.append(main_set.pop(rand_index))

        return new_set

    def get_max_piece(self, pieces):
        max_value = None
        max_pair_value = None

        for i in range(len(pieces)):
            item = pieces[i]
            item_sum = sum(item)
            if not max_value or sum(max_value) < item_sum:
                max_value = item

            if item[0] == item[1] and (not max_pair_value or sum(max_pair_value) < item_sum):
                max_pair_value = item

        if max_pair_value:
            return max_pair_value
        else:
            return max_value

    # проверяет, закончена ли игра
    def get_status(self):

        if len(self.player_pieces) == 0:
            print('Status: The game is over. You won!')
            return True
        elif len(self.computer_pieces) == 0:
            print('Status: The game is over. The computer won!')
            return True

        first_symbol = str(self.domino_snake[0][0])
        if (str(self.stock_pieces)).count(first_symbol) == 8 and first_symbol == str(self.stock_pieces)[-1]:
            print("Status: The game is over. It's a draw!")
            return True


        if self.status == 'computer':
            print("Status: Computer is about to make a move. Press Enter to continue...")
        else:
            print("Status: It's your turn to make a move. Enter your command.")
        return False

    # осуществляет ход
    def motion(self, key):
        element = None

        if not(key == 0 and len(self.stock_pieces) == 0):
            if self.status == 'computer':
                if key == 0:
                    self.computer_pieces.append(self.stock_pieces.pop())
                else:
                    element = self.computer_pieces.pop(abs(key) - 1)
            else:
                if key == 0:
                    self.player_pieces.append(self.stock_pieces.pop())
                else:
                    element = self.player_pieces.pop(abs(key) - 1)

            if key > 0:
                if element[0] != self.domino_snake[-1][1]:
                    element.reverse()
                self.domino_snake.insert(len(self.domino_snake), element)
            elif key < 0:
                if element[1] != self.domino_snake[0][0]:
                    element.reverse()
                self.domino_snake.insert(0, element)

        if self.status == 'computer':
            self.status = 'player'
        else:
            self.status = 'computer'

    def check_motion(self, key):
        left_domino = self.domino_snake[0][0]
        right_domino = self.domino_snake[-1][1]

        #if key == 0 and len(self.stock_pieces) == 0:
        #    if self.status == 'player':
        #        print("Invalid input. Please try again.")
        #    return False
        if self.status == 'computer' and not (-len(self.computer_pieces) <= key <= len(self.computer_pieces)):
            return False
        elif self.status == 'player' and not (-len(self.player_pieces) <= key <= len(self.player_pieces)):
            print("Invalid input. Please try again.")
            return False

        if key != 0:
            user_domino = None
            if self.status == 'computer':
                user_domino = self.computer_pieces[abs(key)-1]
            else:
                user_domino = self.player_pieces[abs(key)-1]

            if key < 0 and left_domino not in user_domino:
                if self.status == 'player':
                    print("Illegal move. Please try again.")
                return False
            if key > 0 and right_domino not in user_domino:
                if self.status == 'player':
                    print("Illegal move. Please try again.")
                return False

        return True

    # эмулирует ход компьютера
    def emulate_computer_motion(self):
        weight = self.__get_weight(self.domino_snake)
        weight_2 = self.__get_weight(self.computer_pieces)
        for i in range(7):
            weight[i] += weight_2[i]

        total_weight = {}
        for i in range(len(self.computer_pieces)):
            total_weight[i + 1] = weight[self.computer_pieces[i][0]] + weight[self.computer_pieces[i][1]]

        # сортировка словаря с весами
        total_weight_sort = {}
        while (len(total_weight) > 0):
            max_key = -1
            max_value = -1
            for key in total_weight.keys():
                if max_key == -1 or total_weight[key] > max_value:
                    max_key = key
                    max_value = total_weight[max_key]

                if (self.check_motion(max_key)):
                    return max_key
                if (self.check_motion(-max_key)):
                    return -max_key

            total_weight_sort[max_key] = max_value
            del total_weight[max_key]

        #return randint(-len(self.computer_pieces), len(self.computer_pieces))
        return 0

    def __get_weight(self, pieces):
        res = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for i in range(len(pieces)):
            res[pieces[i][0]] += 1
            res[pieces[i][1]] += 1

        return res


domino = Domino()
domino.display()
while not domino.get_status():

    if domino.status == 'player':
        key = input()
        while not key.replace('-', '').isdigit() or not domino.check_motion(int(key)):
            key = input()
        domino.motion(int(key))
    else:
        input()
        key = domino.emulate_computer_motion()
        while not domino.check_motion(key):
            key = domino.emulate_computer_motion()
        domino.motion(key)

    domino.display()