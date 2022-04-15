# Grupo 39:
# 90398 Joao Silva
# 95633 Maria Varanda

#v4

import sys
import copy
from turtle import position
from search import InstrumentedProblem, Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # < O(N)
    def get_sequential_values(self, adjacent_values):

        max = self.board.N ** 2
        result = []
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

        # < O(N)
        sequential_values = self.get_sequential_values(adjacentValues)

        # O(N)
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
        horizontal_adjacent_numbers = self.board.adjacent_horizontal_numbers(position[0], position[1])
        vertical_adjacent_numbers = self.board.adjacent_vertical_numbers(position[0], position[1])

        return self.board.at_least_two_adjacent_numbers_are_sequential(number, horizontal_adjacent_numbers, vertical_adjacent_numbers)

    # O(1) - WWW
    def set_board_value(self, row, col, value):
        """ return NumbrixState(self.board.set_value(row, col, value))  """
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
    
    # O(1)
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """

        # Validar input
        """ self.validate_row_and_col(row, col) """

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

                    for verticalValue in verticalAdjacentValues:
                        if verticalValue != 0 and verticalValue != None:
                            adjacentToNonBlankPosition = True
                            adjacentValuesOfThisPosition.add(verticalValue)

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

        horizontal_values = self.adjacent_horizontal_numbers(row, col)
        vertical_values = self.adjacent_vertical_numbers(row, col)

        for value in horizontal_values:
            if value != None and value == 0:
                number_of_blank_positions += 1
        for value in vertical_values:
            if value != None and value == 0:
                number_of_blank_positions += 1

        return number_of_blank_positions

    # O(n^2)
    def get_filled_values(self):

        filledValues = []
        
        for line in self.lines:
            for element in line:
                if element != 0:
                    filledValues.append(element)

        return filledValues

    # O(1) - WWW
    def set_value(self, row, col, value):
        self.lines[row][col] = value
        self.filled_values.append(value)
        return self

    # O(1)
    def validate_row_and_col(self, row, col):
    
        if (row < 0 or row >= self.N or col < 0 or col >= self.N):
            raise Exception("validate_row_and_col: Input incorreto.")

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
                horizontal_adjacent_numbers = self.adjacent_horizontal_numbers(row, col)
                vertical_adjacent_numbers = self.adjacent_vertical_numbers(row, col)
                """ sequential_numbers = 0 """

                # if a single position is empty then this is not a goal state
                if self.lines[row][col] == 0:
                    return False

                # if not a single adjacent number is sequential then this is not a goal state
                if not self.at_least_one_adjacent_number_is_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

                # if for a number != 1 and != N**2 no two sequential numbers are adjacent then this is not a goal state 
                if not self.at_least_two_adjacent_numbers_are_sequential(self.lines[row][col], horizontal_adjacent_numbers, vertical_adjacent_numbers):
                    return False

                """ if self.lines[row][col] > 1 and self.lines[row][col] < self.N ** 2:
                    for number in horizontal_adjacent_numbers:
                        if number != None:
                            if number == self.lines[row][col] + 1 or number == self.lines[row][col] - 1:
                                sequential_numbers += 1
                    for number in vertical_adjacent_numbers:
                        if number != None:
                            if number == self.lines[row][col] + 1 or number == self.lines[row][col] - 1:
                                sequential_numbers += 1
                    if sequential_numbers != 2:
                        return False """

        return goal

    # O(1)
    def at_least_one_adjacent_number_is_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        at_least_one_adjacent_is_sequential = False

        if current_number < 1 or current_number > self.N ** 2:
            raise Exception("at_least_one_adjacent_number_is_sequential: Input incorreto.")

        for number in horizontal_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        for number in vertical_adjacent_numbers:
            if number != None:
                if number == current_number + 1 or number == current_number - 1:
                    at_least_one_adjacent_is_sequential = True

        return at_least_one_adjacent_is_sequential

    # O(1)
    def at_least_two_adjacent_numbers_are_sequential(self, current_number, horizontal_adjacent_numbers, vertical_adjacent_numbers):

        sequential_numbers = 0
        if current_number > 1 and current_number < self.N ** 2:
            for number in horizontal_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            for number in vertical_adjacent_numbers:
                if number != None:
                    if number == current_number + 1 or number == current_number - 1:
                        sequential_numbers += 1
            if sequential_numbers != 2:
                return False
        return True


    """ def get_number_of_blank_positions(self):

        number_of_blank_positions = 0

        for line in self.lines:
            for number in line:
                if number == 0:
                    number_of_blank_positions += 1

        return number_of_blank_positions """

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

    # O(N^2)
    def get_total_number_of_blank_adjacent_positions(self):

        # O(N^2)
        blank_positions = self.get_blank_positions_adjacent_to_values()
        return len(blank_positions)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(copy.deepcopy(board))

    # O(N^2)
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        actionsResult = []

        # O(N^2)
        positionsAdjacentToValues = state.board.get_blank_positions_adjacent_to_values()

        # < O(N)
        for element in positionsAdjacentToValues:
            position = element[0]
            adjacentValues = element[1]

            # O(1)
            possibleValues = state.get_possible_values(position, adjacentValues)

            for possibleValue in possibleValues:

                action = self.createAction(position, possibleValue)
                actionsResult.append(action)

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

        new_state = copy.deepcopy(state)
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

    # O(N^2)
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """

        # heuristica 2: numero total de posicoes adjacentes vazias
        #return node.state.board.get_total_number_of_blank_adjacent_positions()

        # heuristica 3: numero total de posicoes adjacentes vazias
        return self.get_total_number_of_blank_adjacent_positions_and_actions(node)

    # O(N^2)
    def get_total_number_of_blank_adjacent_positions_and_actions(self, node):

        # O(N^2)
        number_of_blank_adjacent_positions = node.state.board.get_total_number_of_blank_adjacent_positions()

        # O(N^2)
        actions = self.actions(node.state)
        number_of_actions = len(actions)

        return number_of_blank_adjacent_positions + number_of_actions


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    """ # Obter o nome do ficheiro do command line
    file_name = sys.argv[1]

    # Criar board
    board = Board.parse_instance(file_name) """

    # Exemplo 1
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt")
    print("Initial:\n", board.to_string(), sep="")

    # Imprimir valores adjacentes
    print(board.adjacent_vertical_numbers(2, 2))
    print(board.adjacent_horizontal_numbers(2, 2))
    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1)) """


    # Exemplo 2
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt") 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Criar um estado com a configuração inicial:
    initial_state = NumbrixState(board) 

    # Mostrar valor na posição (2, 2):
    print(initial_state.board.get_number(2, 2))

    # Realizar acção de inserir o número 1 na posição (2, 2)
    result_state = problem.result(initial_state, (2, 2, 1)) 

    # Mostrar valor na posição (2, 2):
    print(result_state.board.get_number(2, 2)) """


    # Exemplo 3
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt") 
    
    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Criar um estado com a configuração inicial:
    s0 = NumbrixState(board)
    print("Initial:\n", s0.board.to_string(), sep="")

    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (2, 2, 1))
    s2 = problem.result(s1, (0, 2, 3))
    s3 = problem.result(s2, (0, 1, 4))
    s4 = problem.result(s3, (1, 1, 5))
    s5 = problem.result(s4, (2, 0, 7))
    s6 = problem.result(s5, (1, 0, 8))
    s7 = problem.result(s6, (0, 0, 9))

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(s7))
    print("Solution:\n", s7.board.to_string(), sep="") """


    # Exemplo 4
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt") 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Obter o nó solução usando a procura A*:
    goal_node = astar_search(problem) #TODO isto esta' a retornar None

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.to_string(), sep="") """

    # Moosh
    #input_file = sys.argv[1]
    #input_file = "tests_final_public/input2.txt"
    input_file = "i1.txt"
    
    # Ler tabuleiro do ficheiro input_file:
    board = Board.parse_instance(input_file) 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board)

    # Obter o nó solução usando a procura A*:
    goal_node = astar_search(problem)
    #goal_node = greedy_search(problem)
    # goal_node = breadth_first_tree_search(problem)
    # goal_node = depth_first_tree_search(problem)

    # Verificar se foi atingida a solução
    """ print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.to_string(), sep="") """
    print(goal_node.state.board.to_string())
