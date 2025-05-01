class Cell:
    def __init__(self, alive: bool = False):
        self.alive = alive

    def next_state(self, num_neighbors: int) -> bool:
        """
        Determines the next state of the cell based on the number of neighbors.
        :param num_neighbors: The number of alive neighboring cells.
        :return: The next state of the cell (True if alive, False if dead).
        """
        if self.alive:
            return num_neighbors == 2 or num_neighbors == 3
        else:
            return num_neighbors == 3

    @property
    def is_alive(self) -> bool:
        return self.alive

    @is_alive.setter
    def is_alive(self, alive: bool):
        self.alive = alive

    def __eq__(self, value):
        if isinstance(value, Cell):
            return self.alive == value.alive
        return False

    def __str__(self):
        return "🦠" if self.alive else " "
