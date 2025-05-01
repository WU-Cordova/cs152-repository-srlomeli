from projects.project3.drink import Drink

class Menu:
    def __init__(self):
        # AAPISA Heritage Month Menu
        self.drinks = [
            Drink("Calpico Lemonade", 4.00),
            Drink("Banana Milk", 4.25),
            Drink("Durian Red Bull", 5.00),
            Drink("Ube White Mocha", 4.75),
            Drink("Golden Milk Latte", 4.50),
        ]

    def display(self):
        print("\n AAPISA Heritage Month Menu:")
        for i, drink in enumerate(self.drinks, 1):
            print(f"{i}. {drink}")

    def get(self, index):
        if 0 <= index < len(self.drinks):
            return self.drinks[index]
        raise IndexError("Invalid drink selection.")

    def count(self):
        return len(self.drinks)
