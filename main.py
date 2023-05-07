import random
import math
from Spot import Spot

# Constants
MOVE_DIRECTIONS = {tuple([1, 0]): 'D', tuple(
    [-1, 0]): 'U', tuple([0, 1]): 'R', tuple([0, -1]): 'L'}
LEFT = 1
RIGHT = -1
UP = 1
DOWN = -1
HORIZONTAL = "horizontal"
VERTICAL = "vertical"


class Game2048:
    def __init__(self, rows) -> None:
        self.rows: int = rows
        self.no_spots = False
        self.random = random
        self.choices = [int(math.pow(2, i))
                        for i in range(1, rows-1)]
        self.score = 0

    def generate_number(self) -> int:
        """_summary_
        Used to generate a random number on the board for the game
        Args:
        Returns:
            int: generates a random number depending upon the number of rows
        """
        return self.random.choice(self.choices)

    def available_moves(self, board: list[list[Spot]]) -> list[Spot]:
        """_summary_
        Updates the array of available moves where px and py is the move of the user which is to be remove from the moves list.   
        Args:
        Returns:
            list[spot]: List of available spots where to generate the next number
        """
        empty_spaces = []
        for row in board:
            for spot in row:
                if (spot.is_Empty()):
                    empty_spaces.append(spot)
        return empty_spaces

    def update_board(self, board: list[list], previous: tuple[int], current: tuple[int], show_changes) -> None:
        """Updates the game view w.r.t the direction of move 
        Args:
            board (_type_): _description_
            previous (tuple[int]): _description_
            current (tuple[int]): _description_
        """
        move_direction = (previous[0] -
                          current[0], previous[1] -
                          current[1])
        direction = MOVE_DIRECTIONS.get(move_direction)
        if (direction != None):
            if (direction == 'R'):
                self.make_move(board, show_changes, HORIZONTAL, LEFT)
            elif (direction == 'L'):
                self.make_move(board, show_changes, HORIZONTAL, RIGHT)
            elif (direction == 'D'):
                self.make_move(board, show_changes, VERTICAL, UP)
            elif (direction == 'U'):
                self.make_move(board, show_changes, VERTICAL, DOWN)
            self.make_random_move(board)

    def make_move(self, board: list[list[Spot]], show_changes, scroll_direction, direction):
        for i in range(self.rows):
            array_deque: list = []
            for j in range(self.rows-1, -1, -1):
                # if (move_direction == VERTICAL and not self.feasible(board, j, True, False)):
                #     break
                if (scroll_direction == HORIZONTAL):
                    if (board[i][j].is_Empty()):
                        continue
                    array_deque.append(int(board[i][j].number))
                    board[i][j].reset()
                    show_changes(board[i][j])
                else:
                    if (board[j][i].is_Empty()):
                        continue
                    array_deque.append(int(board[j][i].number))
                    board[j][i].reset()
                    show_changes(board[j][i])
            self.merge(board, show_changes, i, array_deque,
                       scroll_direction, direction)

    def merge(self, board: list[list[Spot]], show_changes, row: int, array_deque: list, scroll_direction, direction):
        start = 0 if direction == LEFT else self.rows-1
        while array_deque:
            num: int = array_deque.pop() if direction == LEFT else array_deque.pop(0)
            if (array_deque and array_deque[len(array_deque)-1 if direction == LEFT else 0] == num):
                array_deque.pop() if direction == LEFT else array_deque.pop(0)
                num = (num << 1)
                self.update_score(num)
            if (scroll_direction == HORIZONTAL):
                board[row][start].set_number(str(num))
                show_changes(board[row][start])
            else:
                board[start][row].set_number(str(num))
                show_changes(board[start][row])
            start = abs(start+direction)

    def update_score(self, value) -> None:
        self.score += value

    def make_random_move(self, board: list[list[Spot]]) -> None:
        num: int = self.generate_number()
        available_spots: list[Spot] = self.available_moves(board)
        self.no_spots = len(available_spots) == 0
        if (self.no_spots):
            return
        spot = random.choice(available_spots)
        spot.number = str(num)
        available_spots.remove(spot)
        self.no_spots = len(available_spots) == 0
        self.print_grid(board)

    def is_feasible_move(self, board) -> bool:
        """Checks if their is any possible move the board when the board is full
        Returns:
            bool: false if not possible moves can be made 
        """
        return self.find_feasible(board)

    def feasible(self, board: list[list[Spot]], row, check_row: bool, check_col: bool) -> bool:
        for col in range(self.rows):
            if (check_row and row > 0 and row < len(board)):
                if (board[row-1][col].is_Empty() or board[row][col].is_Empty() or board[row-1][col].number == board[row][col].number or board[row+1][col].number == board[row][col].number):
                    return True
            if (check_col and col > 0 and col < len(board[row])):
                if (board[row][col - 1].number == board[row][col].number or board[row][col + 1].number == board[row][col].number):
                    return True
        return False

    def find_feasible(self, board: list[list[Spot]]):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if (row > 0 and row < len(board)-1):
                    if (board[row-1][col].number == board[row][col].number or board[row+1][col].number == board[row][col].number):
                        return True
                if (col > 0 and col < len(board[row])-1):
                    if (board[row][col - 1].number == board[row][col].number or board[row][col + 1].number == board[row][col].number):
                        return True
        return False

    def game_over(self, board) -> bool:
        return self.no_spots and not self.is_feasible_move(board)

    def print_grid(self, board: list[list[Spot]]):
        print("\033[H\033[J", end="")
        for row in board:
            for spot in row:
                print(spot.number if spot.number != None else 0, end=" ")
            print("\n")


if __name__ == "__main__":
    game = Game2048()
