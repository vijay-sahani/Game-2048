DARK_GREY = (119, 110, 101)


class Spot:
    def __init__(self, row, col, width, height, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*height
        self.width = width
        self.height = height
        self.color = DARK_GREY
        self.total_rows = total_rows
        self.number: str = None

    def update_height_width(self, width, height):
        self.width = width
        self.height = height
        self.x = self.row*width
        self.y = self.col*height

    def is_Empty(self) -> bool:
        return self.number == None

    def set_color(self, COLOR: tuple) -> None:
        self.color = COLOR

    def set_number(self, number: str) -> None:
        self.number = number

    def reset(self) -> None:
        self.color = DARK_GREY
        self.number = None
