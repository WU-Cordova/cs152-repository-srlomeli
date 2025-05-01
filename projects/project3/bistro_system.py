from datastructures.deque import Deque
from projects.project3.customer_order import CustomerOrder
from projects.project3.order_item import OrderItem
from projects.project3.menu import Menu


class BistroSystem:
    def __init__(self):
        self.menu = Menu()
        self.open_orders = Deque()        # FIFO structure for open orders
        self.completed_orders = []        # List of completed orders

    def display_menu(self):
        self.menu.display()

    def take_new_order(self):
        name = input("\n What’s the name on the order? ").strip()
        order = CustomerOrder(name)
        try:
            count = int(input("How many drinks would you like to order? "))
        except ValueError:
            print("Invalid number. Canceling order.")
            return

        for i in range(count):
            while True:
                try:
                    index = int(input(f"Drink #{i + 1} - Enter drink number (1-5): ")) - 1
                    selected = self.menu.get(index)
                    break
                except (ValueError, IndexError):
                    print("Invalid selection. Try again.")
            customization = input(f"Any customization for {selected.name}? ")
            order.add_item(OrderItem(selected, customization))

        print(f"\n Order Summary for {order.customer_name}:")
        print(order)

        while True:
            confirm = input("Confirm order? (yes/no): ").strip().lower()
            if confirm.startswith("y"):
                self.open_orders.enqueue(order)
                print("Order placed successfully!")
                break
            elif confirm.startswith("n"):
                print("Order canceled.")
                break
            else:
                print("Please type 'yes' or 'no'.")


    def view_open_orders(self):
        print("\n Open Orders:")
        if not self.open_orders:
            print("No open orders.")
        for i, order in enumerate(self.open_orders, 1):
            print(f"{i}. {order}")

    def complete_next_order(self):
        if self.open_orders:
            order = self.open_orders.dequeue()
            self.completed_orders.append(order)
            print(f"\n Completed Order for {order.customer_name}!")
        else:
            print("\nNo open orders to complete.")

    def end_of_day_report(self):
        print("\n End-of-Day Report")
        summary = {}
        revenue = 0.0

        for order in self.completed_orders:
            for item in order.items:
                name = item.drink.name
                price = item.drink.price
                if name not in summary:
                    summary[name] = {"qty": 0, "sales": 0.0}
                summary[name]["qty"] += 1
                summary[name]["sales"] += price
                revenue += price

        print(f"{'Drink Name':<25} {'Qty Sold':<10} {'Total Sales'}")
        for name, data in summary.items():
            print(f"{name:<25} {data['qty']:<10} ${data['sales']:.2f}")
        print(f"\nTotal Revenue: ${revenue:.2f}")

    def run(self):
        while True:
            print("\n Main Menu")
            print("1. Display Menu")
            print("2. Take New Order")
            print("3. View Open Orders")
            print("4. Mark Next Order as Complete")
            print("5. View End-of-Day Report")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.display_menu()
            elif choice == "2":
                self.take_new_order()
            elif choice == "3":
                self.view_open_orders()
            elif choice == "4":
                self.complete_next_order()
            elif choice == "5":
                self.end_of_day_report()
            elif choice == "6":
                print("👋 Thanks for using Bearcat Bistro POS System!")
                break
            else:
                print("Invalid choice. Please try again.")
