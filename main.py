import random
from Spot import Spot

MOVE_DIRECTIONS = {tuple([1, 0]): 'D', tuple(
    [-1, 0]): 'U', tuple([0, 1]): 'R', tuple([0, -1]): 'L'}


class Game2048:
    def __init__(self) -> None:
        self.rows: int = 4
        self.no_spots = False
        self.random = random
        self.score = 0

    def generate_number(self) -> int:
        """_summary_
        Used to generate a random number on the board for the game
        Args:
            random (random): _description_
        Returns:
            int: generates a random number either 2 or 4
        """
        return self.random.choice([2, 4])

    def available_moves(self, board: list[list[Spot]]) -> list[Spot]:
        """_summary_
        Updates the array of available moves where px and py is the move of the user which is to be remove from the moves list.   
        Args:
            px (int): position of x
            py (int): position of y 
        """
        empty_spaces = []
        for row in board:
            for spot in row:
                if(spot.is_Empty()):
                    empty_spaces.append(spot)
        return empty_spaces

    def update_board(self, board: list[list], previous: tuple[int], current: tuple[int]) -> None:
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
        if(direction != None):
            if(direction == 'R'):
                # print("latest version")
                self.on_direction_left(board)
            elif(direction == 'L'):
                self.on_direction_right(board)
            elif(direction == 'D'):
                self.on_direction_up(board)
            elif(direction == 'U'):
                self.on_direction_down(board)
            self.make_random_move(board)

    def on_direction_left(self, board: list[list[Spot]]):
        for i in range(self.rows):
            for j in range(1, self.rows):
                if(board[i][j].is_Empty()):
                    continue
                row: int = i
                col: int = j
                while(col > 0 and board[row][col-1].is_Empty()):
                    board[row][col-1].number = board[row][col].number
                    board[row][col].reset()
                    col -= 1

                if(board[row][col].number != None and board[row][col-1].number == board[row][col].number):
                    board[row][col -
                               1].number = str(int(board[row][col-1].number) << 1)
                    self.score += int(board[row][col-1].number)
                    board[row][col].reset()

    def on_direction_left_v2(self, board: list[list[Spot]]):
        for i in range(self.rows):
            stack: list = []
            for j in range(self.rows):
                if(board[i][j].is_Empty()):
                    continue
                num = int(board[i][j].number)
                if(len(stack) == 0):
                    stack.append(num)
                elif(stack[len(stack)-1] == num):
                    last_num = (stack.pop() << 1)
                    self.update_score(last_num)
                    stack.append(last_num)
                else:
                    stack.append(num)
                board[i][j].reset()
            index = 0
            while stack and index < self.rows:
                board[i][index].set_number(str(stack.pop()))
                index += 1

    def update_score(self, value) -> None:
        self.score += value

    def on_direction_right(self, board: list[list[Spot]]):
        for i in range(self.rows):
            for j in range(self.rows-2, -1, -1):
                if(board[i][j].is_Empty()):
                    continue
                row: int = i
                col: int = j
                while(col < self.rows-1 and board[row][col+1].is_Empty()):
                    board[row][col+1].number = board[row][col].number
                    board[row][col].reset()
                    col += 1
                if(col == 3):
                    continue
                if(board[row][col].number != None and board[row][col+1].number == board[row][col].number):
                    board[row][col +
                               1].number = str(int(board[row][col+1].number) << 1)
                    self.score += int(board[row][col+1].number)
                    board[row][col].reset()

    def on_direction_up(self, board: list[list[Spot]]) -> None:
        for i in range(1, self.rows):
            for j in range(self.rows):
                if(board[i][j].is_Empty()):
                    continue
                row: int = i
                col: int = j
                while(row > 0 and board[row-1][col].is_Empty()):
                    board[row-1][col].number = board[row][col].number
                    board[row][col].reset()
                    row -= 1

                if(board[row][col].number != None and board[row-1][col].number == board[row][col].number):
                    board[row -
                          1][col].number = str(int(board[row-1][col].number) << 1)
                    self.score += int(board[row-1][col].number)
                    board[row][col].reset()

    def on_direction_down(self, board: list[list[Spot]]):
        for i in range(self.rows-2, -1, -1):
            for j in range(self.rows):
                if(board[i][j].is_Empty()):
                    continue
                row: int = i
                col: int = j
                while(row < self.rows-1 and board[row+1][col].is_Empty()):
                    board[row+1][col].number = board[row][col].number
                    board[row][col].reset()
                    row += 1
                if(row == 3):
                    continue
                if(board[row][col].number != None and board[row][col].number == board[row+1][col].number):
                    board[row +
                          1][col].number = str(int(board[row+1][col].number) << 1)
                    self.score += int(board[row+1][col].number)
                    board[row][col].reset()

    def make_random_move(self, board: list[list[Spot]]) -> None:
        num: int = self.generate_number()
        available_spots: list[Spot] = self.available_moves(board)
        self.no_spots = len(available_spots) == 0
        if(self.no_spots):
            return
        spot = random.choice(available_spots)
        spot.number = str(num)
        self.print_grid(board)

    def is_feasible_move(self) -> bool:
        """Checks if their is any possible move the board when the board is full
        ** Not Implemented yet **
        Returns:
            bool: false if not possible moves can be made 
        """
        return False

    def game_over(self) -> bool:
        return self.no_spots and not self.is_feasible_move()

    def print_grid(self, board: list[list[Spot]]):
        print("\033[H\033[J", end="")
        for row in board:
            for spot in row:
                print(spot.number if spot.number != None else 0, end=" ")
            print("\n")


if __name__ == "__main__":
    game = Game2048()
