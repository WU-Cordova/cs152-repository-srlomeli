from projects.project2.grid import Grid
from projects.project2.gamecontroller import GameController

def main():
    rows, cols = 10, 10
    grid = Grid(rows, cols)

    choice = input("Random start (r) or config file (c)? ")
    if choice == 'r':
        grid.random_start()
    elif choice == 'c':
        filename = input("Enter configuration file name: ")
        grid.read_config(filename)
    
    controller = GameController(grid)
    controller.run()

if __name__ == "__main__":
    main()
