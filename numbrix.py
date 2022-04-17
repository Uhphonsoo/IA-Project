# Grupo 39:
# 90398 Joao Silva
# 95633 Maria Varanda

#v10

import sys
import copy
""" from turtle import position """
from search import InstrumentedProblem, Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # O(1)
    def get_sequential_values(self, adjacent_values):

        max = self.board.N ** 2
        result = []

        # O(1)
        for value in adjacent_values:
            if value + 1 < max + 1:
                result.append(value + 1)
            if value - 1 > 0:
                result.append(value - 1)
        return result

    # O(1)
    def get_possible_values(self, position, adjacentValues):

        possibleValues = []

        # O(1)
        filledValues = self.board.filled_values

        max = self.board.N ** 2

        # O(1)
        sequential_values = self.get_sequential_values(adjacentValues)

        # O(1)
        for i in sequential_values:

            """ if i in sequential_values and i not in filledValues: """
            if i not in filledValues:
                
                # O(1)
                number_of_blank_positions_adjacent_to_position = self.board.get_number_of_blank_positions_adjacent_to_position(position)
                if i == 1 or i == max:
                    possibleValues.append(i)
                elif number_of_blank_positions_adjacent_to_position != 0:
                    possibleValues.append(i)
                elif self.at_least_two_adjacent_numbers_are_sequential(i, position):
                    possibleValues.append(i)

        return possibleValues

    # O(1)
    def at_least_two_adjacent_numbers_are_sequential(self, number, position):

        # O(1)
        horizontal_adjacent_numbers = self.board.adjacent_horizontal_numbers(position[0], position[1])
        vertical_adjacent_numbers = self.board.adjacent_vertical_numbers(position[0], position[1])

        # O(1)
        return self.board.at_least_two_adjacent_numbers_are_sequential(number, horizontal_adjacent_numbers, vertical_adjacent_numbers)

    # < O(N) - WWW
    def set_board_value(self, row, col, value):
        """ return NumbrixState(self.board.set_value(row, col, value))  """
        # < O(N)
        self.board.set_value(row, col, value)

    def to_string(self):
        return("board:\n" + self.board.to_string() + "\nid:\n" + str(self.id))


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, lines):

        # a primeira linha de linhas e' da forma [N]
        N = lines[0][0]

        # Validar input
        if N < 1:
            raise Exception("N deve ser maior ou igual a 1.")
        if len(lines) != N + 1:
            raise Exception("O input nao tem o numero correto de linhas.")

        self.N = N
        self.lines = lines[1:]

        self.filled_values = self.get_filled_values()
        self.blank_positions_adjacent_to_values = self.get_blank_positions_adjacent_to_values()
        self.max = N**2
        self.last_changed_position = (-1, -1)
        self.last_set_value = 0
    
    # O(1)
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """

        # O(1)
        return self.lines[row][col]
    
    # O(1)
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        # Caso N == 1
        if self.N == 1:
            return (None, None)

        # Caso N > 1
        elif self.N > 1:

            # Caso primeira linha
            if row == 0:
                return (self.get_number(row + 1, col), None)
            # Caso ultima linha
            elif row == self.N - 1:
                return (None, self.get_number(row - 1, col))
            # Caso linha intermedia
            else:
                return (self.get_number(row + 1, col), self.get_number(row - 1, col))

    # O(1)
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """

        # Caso N == 1
        if self.N == 1:
            return (None, None)

        # Caso N > 1
        elif self.N > 1:

            # Caso primeira coluna
            if col == 0:
                return (None, self.get_number(row, col + 1))
            # Caso ultima coluna
            elif col == self.N - 1:
                return (self.get_number(row, col - 1), None)
            # Caso coluna intermedia
            else:
                return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """

        # Abrir ficheiro e ler conteudo
        file = open(filename, "r")
        lines_strings = file.readlines()

        # Coverter linhas de strings para linhas de ints
        lines_ints = []
        for line in lines_strings:
            line_ints = [int(string_number) for string_number in line.split()]
            lines_ints.append(line_ints)

        # Criar e retornar board
        board = Board(lines_ints)
        return board
        
    # O(N^2)
    def get_blank_positions_adjacent_to_values(self):
        """ Retorna uma lista em que cada elemento e' composto por uma 
        posicao vazia que esteja adjacente a pelo menos uma posicao nao
        vazia (posicao com um valor) e por o conjunto de valores que 
        lhe sao adjacentes """

        blankPositionsAdjacentToValues = []

        # O(N^2)
        for line in range(self.N):
            for col in range(self.N):
                adjacentValuesOfThisPosition = set()

                if self.lines[line][col] != 0: # se a posicao nao esta vazia
                    continue
                else:
                    adjacentToNonBlankPosition = False
                    verticalAdjacentValues = self.adjacent_vertical_numbers(line, col)
                    horizontalAdjacentValues = self.adjacent_horizontal_numbers(line, col)

                    # O(1)
                    for verticalValue in verticalAdjacentValues:
                        if verticalValue != 0 and verticalValue != None:
                            adjacentToNonBlankPosition = True
                            adjacentValuesOfThisPosition.add(verticalValue)

                    # O(1)
                    for horizontalValue in horizontalAdjacentValues:
                        if horizontalValue != 0 and horizontalValue != None:
                            adjacentToNonBlankPosition = True
                            adjacentValuesOfThisPosition.add(horizontalValue)
                    
                    if adjacentToNonBlankPosition:
                        blankPositionsAdjacentToValues.append([(line, col), adjacentValuesOfThisPosition])
                        
        return blankPositionsAdjacentToValues

    # O(1)
    def get_number_of_blank_positions_adjacent_to_position(self, position):

        row = position[0]
        col = position[1]

        number_of_blank_positions = 0

        # O(1)
        horizontal_values = self.adjacent_horizontal_numbers(row, col)
        vertical_values = self.adjacent_vertical_numbers(row, col)

        # O(1)
        for value in horizontal_values:
            if value != None and value == 0:
                number_of_blank_positions += 1
        for value in vertical_values:
            if value != None and value == 0:
                number_of_blank_positions += 1

        return number_of_blank_positions

    # O(N^2)
    def get_filled_values(self):

        filledValues = []
        
        for line in self.lines:
            for element in line:
                if element != 0:
                    filledValues.append(element)

        return filledValues

    # < O(N) - WWW
    def set_value(self, row, col, value):
        self.lines[row][col] = value
        self.filled_values.append(value)
        self.last_changed_position = (row, col)
        self.last_set_value = value

        # Update self.blank_positions_adjacent_to_values
        # Remove old
        # < O(N) ??? DA PARA MELHORAR ???
        self.remove_old_blank_position_adjacent_to_value(row, col)

        # Add new
        horizontal_adjacent = self.adjacent_horizontal_numbers(row, col)
        vertical_adjacent = self.adjacent_vertical_numbers(row, col)

        """ for value in horizontal_adjacent:
            if value != 0:
                horizontal_adjacent_aux = 
                blank_positions_adjacent_to_values.append() """
        if row == 0:
            if col == 0:
                # O(1)
                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    # O(1)
                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    # O(1)
                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col > 0 and col < self.N - 1:
                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col == self.N - 1:
                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

        elif row > 0 and row < self.N - 1:      
            if col == 0:
                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col > 0 and col < self.N - 1:
                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col == self.N - 1:
                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row+1, col) == 0:
                    new_blank_position = [(row+1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row+1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row+1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

        elif row == self.N-1:
            if col == 0:
                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col > 0 and col < self.N - 1:
                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row, col+1) == 0:
                    new_blank_position = [(row, col+1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col+1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col+1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

            elif col == self.N - 1:
                if self.get_number(row, col-1) == 0:
                    new_blank_position = [(row, col-1)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row, col-1)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row, col-1)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)

                if self.get_number(row-1, col) == 0:
                    new_blank_position = [(row-1, col)]
                    adjacent_values = set()

                    horizontal_adjacent_aux = self.adjacent_horizontal_numbers(row-1, col)
                    vertical_adjacent_aux = self.adjacent_vertical_numbers(row-1, col)

                    self.add_to_adjacent_values(adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux)

                    self.remove_old_blank_position_adjacent_to_value(row, col)
                    new_blank_position.append(adjacent_values)
                    self.blank_positions_adjacent_to_values.append(new_blank_position)
                
        return self

    def remove_old_blank_position_adjacent_to_value(self, row, col):

        for element in self.blank_positions_adjacent_to_values:
            position = element[0]
            if position == (row, col):
                self.blank_positions_adjacent_to_values.remove(element)

    # O(1)
    def add_to_adjacent_values(self, adjacent_values, value, horizontal_adjacent_aux, vertical_adjacent_aux):
        # O(1)
        for value in horizontal_adjacent_aux:
            if value != None and value != 0:
                adjacent_values.add(value)
        # O(1)
        for value in vertical_adjacent_aux:
            if value != None and value != 0:
                adjacent_values.add(value)

    """ def goal_test(self):

        goal = True

        for row in range(self.N):
            for col in range(self.N):
                horizontal_adjacent_numbers = self.adjacent_horizontal_numbers(row, col)
                vertical_adjacent_numbers = self.adjacent_vertical_numbers(row, col)

                # if a single position is empty then this is not a goal state
                if self.lines[row][col] == 0:
                    return False

                if not self.at_least_one_adjacent_number_is_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    goal = False

        return goal """

    # O(N^2)
    def goal_test(self):

        goal = True

        # O(N^2)
        for row in range(self.N):
            for col in range(self.N):

                # O(1)
                horizontal_adjacent_numbers = self.adjacent_horizontal_numbers(row, col)
                vertical_adjacent_numbers = self.adjacent_vertical_numbers(row, col)

                # if a single position is empty then this is not a goal state
                if self.lines[row][col] == 0:
                    return False

                # if not a single adjacent number is sequential then this is not a goal state
                # O(1)
                if not self.at_least_one_adjacent_number_is_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

                # if for a number != 1 and != N**2 no two sequential numbers are adjacent then this is not a goal state 
                # O(1)
                if not self.at_least_two_adjacent_numbers_are_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

        return goal

    # O(1)
    def at_least_one_adjacent_number_is_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        at_least_one_adjacent_is_sequential = False

        if current_number < 1 or current_number > self.N ** 2:
            raise Exception("at_least_one_adjacent_number_is_sequential: Input incorreto.")

        # O(1)
        for number in horizontal_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        # O(1)
        for number in vertical_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        return at_least_one_adjacent_is_sequential

    # O(1)
    def at_least_two_adjacent_numbers_are_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        sequential_numbers = 0
        if current_number > 1 and current_number < self.N ** 2:
            # O(1)
            for number in horizontal_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            # O(1)
            for number in vertical_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            if sequential_numbers != 2:
                return False
        return True

    def to_string(self):
        board_string = ""

        for line in self.lines:
            for number in line:
                board_string += str(number)
                if number != line[-1]:
                    board_string += '\t'
            if line != self.lines[-1]:
                board_string += "\n"
        
        return board_string

    # O(1)
    def get_total_number_of_blank_adjacent_positions(self):

        # O(1)
        return len(self.blank_positions_adjacent_to_values)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(copy.deepcopy(board))
        self.number_of_actions = 0

    # < O(N)
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        actionsResult = []

        # O(1)
        positionsAdjacentToValues = state.board.blank_positions_adjacent_to_values

        # < O(N)
        for element in positionsAdjacentToValues:
            position = element[0]
            adjacentValues = element[1]

            # O(1)
            possibleValues = state.get_possible_values(position, adjacentValues)

            # O(1)
            for possibleValue in possibleValues:

                action = self.createAction(position, possibleValue)

                """ if action not in actionsResult: """
                actionsResult.append(action)

        self.number_of_actions = len(actionsResult)
        return actionsResult

    # O(1)
    def createAction(self, position, possibleValue):
        return (position[0], position[1], possibleValue)

    # O(N^2) ???
    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """

        row = action[0]
        col = action[1]
        value = action[2]

        # O(N^2) ???
        new_state = copy.deepcopy(state)

        # < O(N)
        new_state.set_board_value(row, col, value)

        """ new_lines = list(state.board.lines[:])
        new_lines.insert(0, [board.N])
        new_board = Board(new_lines)
        new_state = NumbrixState(new_board)
        new_state.set_board_value(row, col, value) """

        return new_state

    # O(N^2)
    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """

        return state.board.goal_test()

    # < O(N)
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """

        # heuristica 1: numero total de posicoes adjacentes vazias + acoes possiveis
        #return self.get_total_number_of_blank_adjacent_positions_and_actions(node)

        # heuristica 2: numero total de acoes possiveis
        #return self.get_total_number_of_actions(node)

        # heuristica 3: numero total de posicoes adjacentes vazias
        #return node.state.board.get_total_number_of_blank_adjacent_positions()

        # heuristica 4: numero total de posicoes adjacentes vazias + acoes possiveis + posicoes vazias adjacentes 'a jogada
        return self.heuristic_4(node)

    # < O(N)
    def get_total_number_of_blank_adjacent_positions_and_actions(self, node):

        # O(1)
        number_of_blank_adjacent_positions = node.state.board.get_total_number_of_blank_adjacent_positions()

        # < O(N)
        actions = self.actions(node.state)
        number_of_actions = len(actions)

        """ # O(1)
        number_of_actions = self.number_of_actions """

        return number_of_blank_adjacent_positions + number_of_actions

    # < O(N)
    def get_total_number_of_actions(self, node):

        # < O(N)
        actions = self.actions(node.state)
        number_of_actions = len(actions)

        """ # O(1)
        number_of_actions = self.number_of_actions """

        return number_of_actions

    # < O(N)
    def heuristic_4(self, node):

        # < O(N)
        aux = self.get_total_number_of_blank_adjacent_positions_and_actions(node)
        number_of_blank_adjacent_positions = 0

        last_changed_position = node.state.board.last_changed_position
        row = last_changed_position[0]
        col = last_changed_position[1]

        # O(1)
        horizontal_numbers = board.adjacent_horizontal_numbers(row, col)
        vertical_numbers = board.adjacent_vertical_numbers(row, col)

        # O(1)
        for number in horizontal_numbers:
            if number == 0:
                number_of_blank_adjacent_positions += 1
        for number in vertical_numbers:
            if number == 0:
                number_of_blank_adjacent_positions += 1

        if last_changed_position == (-1, -1):
            number_of_blank_adjacent_positions = 0

        return aux + number_of_blank_adjacent_positions
        

if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Obter o nome do ficheiro do command line
    #input_file = sys.argv[1]
    #input_file = "tests_final_public/input2.txt"
    input_file = "i1.txt"
    #input_file = "i4.txt"
    #input_file = "i5.txt"
    
    # Criar board
    board = Board.parse_instance(input_file) 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Obter o nó solução usando a procura A*:
    #goal_node = astar_search(problem)
    goal_node = greedy_search(problem)
    # goal_node = breadth_first_tree_search(problem)
    # goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    """ print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.to_string(), sep="") """
    print(goal_node.state.board.to_string())
