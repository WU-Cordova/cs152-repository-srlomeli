class CustomerOrder:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []  # list of OrderItem instances

    def add_item(self, order_item):
        self.items.append(order_item)

    def total_cost(self):
        return sum(item.drink.price for item in self.items)

    def __str__(self):
        summary = f"{self.customer_name}:\n"
        for item in self.items:
            summary += f"- {item}\n"
        return summary.strip()
