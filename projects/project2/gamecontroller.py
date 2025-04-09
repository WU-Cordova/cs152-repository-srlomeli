from time import sleep
from projects.project2.grid import Grid
from projects.project2.kbhit import KBHit

class GameController:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.generation = 0
        self.history = []

    def run(self):
        
        # Prompt the user to select the initial mode
        initial_mode = input("Choose mode: automatic (a) or manual (m): ").strip().lower()
        if initial_mode == 'm':
            mode = 'manual'
        else:
            mode = 'automatic'

        print("Press 'q' to quit, 'm' for manual mode, 'a' for automatic mode, 's' to step to the next generation in manual mode.")
        kbhit = KBHit()

        while True:
            if mode == 'automatic':
                sleep(1)
                # Check for key press to switch back to manual mode
                if kbhit.kbhit():
                    key = kbhit.getch()
                    if key == 'q':
                        print("You hit quit")
                        break
                    elif key == 'm':
                        print("Switching to manual mode")
                        mode = 'manual'
                        continue

            elif mode == 'manual':
                print("Press 's' to step to the next generation.")
                while not kbhit.kbhit():  # Wait for key press in manual mode
                    pass
                key = kbhit.getch()
                if key == 'q':
                    print("You hit quit")
                    break
                elif key == 'a':
                    print("Switching to automatic mode")
                    mode = 'automatic'
                elif key == 's':
                    print(f"Generation {self.generation}:")
                    self.grid.display()
                    self.history.append(self.grid)
                    self.generation += 1

                    # Advance to the next generation and check for stability or repeating patterns
                    next_grid = self.grid.next_gen()

                    if self.is_stable_or_repeating(next_grid) or self.is_dead_state(next_grid):
                        print(f"Game ended after {self.generation} generations.")
                        if self.is_dead_state(next_grid):
                            print("Game ended due to all cells being dead.")
                        else:
                            print("Game ended due to stability or repeating pattern.")
                        print("Next generation (repeated or dead):")
                        next_grid.display()  # Display the final generation
                        break

                    self.grid = next_grid
                    print("Press 'q' to quit, 'a' for automatic mode, 's' for the next generation.")
                    continue

            # Display the current generation
            print(f"Generation {self.generation}:")
            self.grid.display()
            self.history.append(self.grid)
            self.generation += 1

            # Advance to the next generation and check for stability or repeating patterns
            next_grid = self.grid.next_gen()

            if self.is_stable_or_repeating(next_grid) or self.is_dead_state(next_grid):
                print(f"Game ended after {self.generation} generations.")
                if self.is_dead_state(next_grid):
                    print("Game ended due to all cells being dead.")
                else:
                    print("Game ended due to stability or repeating pattern.")
                print("Next generation (repeated or dead):")
                next_grid.display()  # Display the final generation
                break

            self.grid = next_grid

        # Exit the loop and end the game
        print("Exiting the game. Thanks for playing!")

    def advance_generation(self):
        print(f"Generation {self.generation}:")
        self.grid.display()
        self.history.append(self.grid)
        self.grid = self.grid.next_gen()
        self.generation += 1

    def is_stable_or_repeating(self, next_grid: Grid) -> bool:
        if len(self.history) < 5:
            return False
        # Check if the next grid matches any of the last 5 generations
        for past_grid in self.history[-5:]:
            if next_grid == past_grid:
                return True
        return False

    def is_dead_state(self, grid: Grid) -> bool:
        for row in range(grid.rows):
            for col in range(grid.cols):
                if grid.grid[row][col].is_alive:
                    return False
        return True
