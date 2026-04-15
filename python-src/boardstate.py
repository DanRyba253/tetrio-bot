from enum import Enum

class Color(Enum):
    YELLOW = 0,
    BLUE = 1,
    RED = 2,
    GREEN = 3,
    ORANGE = 4,
    MAGENTA = 5,
    CYAN = 6,
    BLACK = 7

class BoardState:
    board: list[list[Color]]
    hold: Color
    future: list[Color]
    current: Color

    def __init__(self, board, hold, future):
        self.board = board
        self.hold= hold
        self.future = future

def initBoardState() -> BoardState:
    board = []
    for _ in range(20):
        board.append([Color.BLACK] * 10)
    future = [Color.BLACK] * 5
    return BoardState(board, Color.BLACK, future)

def printBoardState(boardState: BoardState):
    for row in boardState.board:
        for cell in row:
            printColor(cell)
        print()
    print("future:")
    for color in boardState.future:
        printColor(color)
    print()
    print("hold:")
    printColor(boardState.hold)
    print()
    print("current:")
    printColor(boardState.current)
    print()


def printColor(color: Color):
    match color:
        case Color.YELLOW:
            print("Y", end=' ')
        case Color.BLUE:
            print("B", end=' ')
        case Color.RED:
            print("R", end=' ')
        case Color.GREEN:
            print("G", end=' ')
        case Color.ORANGE:
            print("O", end=' ')
        case Color.MAGENTA:
            print("M", end=' ')
        case Color.CYAN:
            print("C", end=' ')
        case Color.BLACK:
            print("_", end=' ')
