class OrderItem:
    def __init__(self, drink, customization=""):
        self.drink = drink            # Instance of Drink
        self.customization = customization  # Optional string for customization

    def __str__(self):
        base = str(self.drink)
        if self.customization:
            return f"{base} - {self.customization}"
        return base
