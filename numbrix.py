# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 39:
# 90398 Joao Silva
# 95633 Maria Varanda

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe

    def getBlankPositionsAdjacentToValues(self):
        return self.board.getBlankPositionsAdjacentToValues()

    def getPossibleValues(self, adjacentValues):

        possibleValues = []
        filledValues = self.board.getFilledValues()

        for i in range(1,10):
            if i not in adjacentValues and i not in filledValues:
                possibleValues.append(i)

    def setBoardValue(self, row, col, value):
        return NumbrixState(self.board.setValue(row, col, value)) 

    def to_string(self):
        """ id_string = str(self.id) """
        return("board:\n" + self.board.to_string() + "\nid:\n" + str(self.id))


    """ def getValuesAdjacentToPositions():
        return self.board.getValuesAdjacentToPositions() """


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
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        # TO~DO

        # Validar input
        self.validate_row_and_col(row, col)

        return self.lines[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        # TO~DO

        # Testar input
        self.validate_row_and_col(row, col)

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

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        # TO~DO

        # Testar input
        self.validate_row_and_col(row, col)

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
        # TO~DO

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

    # TODO: outros metodos da classe

    def getBlankPositionsAdjacentToValues(self):
        """ Retorna uma lista em que cada elemento e' composto por uma 
        posicao vazia que esteja adjacente a pelo menos uma posicao nao
        vazia (posicao com um valor) e por o conjunto de valores que 
        lhe sao adjacentes """

        blankPositionsAdjacentToValues = []

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

    def getFilledValues(self):

        filledValues = []
        
        for line in self.lines:
            for element in line:
                if element != 0:
                    filledValues.append(element)

        return filledValues

    def setValue(self, row, col, value):
        self.lines[row][col] = value
        return self


    """ def getValuesAdjacentToPositions(self):
        pass """ # acho que nao preciso (???)

    def validate_row_and_col(self, row, col):
    
        if (row < 0 or row >= self.N or col < 0 or col >= self.N):
            raise Exception("validate_row_and_col: Input incorreto.")

    def to_string(self):
        board_string = ""

        for line in self.lines:
            for number in line:
                board_string += str(number) + "    "
            if line != self.lines[-1]:
                board_string += "\n"
        
        return board_string


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO # esta' feito???
        
        self.state = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

        actionsResult = []

        positionsAdjacentToValues = self.state.getBlankPositionsAdjacentToValues()

        for element in positionsAdjacentToValues:
            position = element[0]
            adjacentValues = element[1]

            possibleValues = self.state.getPossibleValues(adjacentValues)

            for possibleValue in possibleValues:

                action = self.createAction(position, possibleValue)
                actionsResult.append(action)

        return actionsResult

    def createAction(self, position, possibleValue):
        return (position[0], position[1], possibleValue)

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """

        # TO~DO

        row = action[0]
        col = action[1]
        value = action[2]

        return state.setBoardValue(row, col, value)

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Obter o nome do ficheiro do command line
    """ file_name = sys.argv[1] """

    # Criar board
    """ board = Board.parse_instance(file_name) """

    # Exemplo 1
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt")
    print("Initial:\n", board.to_string(), sep="")

    # Imprimir valores adjacentes
    print(board.adjacent_vertical_numbers(2, 2))
    print(board.adjacent_horizontal_numbers(2, 2))
    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1))

    blankPositionsAdjacentToValues = board.getBlankPositionsAdjacentToValues()

    for element in blankPositionsAdjacentToValues:
        print(element) """


    # Exemplo 2
    """ # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    board = Board.parse_instance("i1.txt") 

    # Criar uma instância de Numbrix:
    problem = Numbrix(board) # esta feito???

    # Criar um estado com a configuração inicial:
    initial_state = NumbrixState(board) 

    # Mostrar valor na posição (2, 2):
    print(initial_state.board.get_number(2, 2))

    # Realizar acção de inserir o número 1 na posição (2, 2)
    result_state = problem.result(initial_state, (2, 2, 1)) 

    # Mostrar valor na posição (2, 2):
    print(result_state.board.get_number(2, 2)) """

    
