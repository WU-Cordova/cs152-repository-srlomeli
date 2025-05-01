class Drink:
    def __init__(self, name, price):
        self.name = name
        self.size = "Medium"  # Default size
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.size}) - ${self.price:.2f}"
