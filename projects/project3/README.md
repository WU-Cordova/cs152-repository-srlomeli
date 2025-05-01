# Bearcat Bistro Ordering System

## Project Overview

This program simulates a simplified point-of-sale system for the Bearcat Bistro. It allows users to take customized drink orders, queue them for preparation, mark them as complete, and view an end-of-day report. 

The drink menu is based on AAPISA Heritage Month offerings that was obtained from the bistro's instagram page. 

## Data Structures Used

### Menu
The `Menu` class encapsulates a list of five hardcoded `Drink` objects. It provides methods to display the menu and retrieve drinks by index. This abstraction keeps menu-related logic separate and reusable.

### Drink
Each `Drink` has a name, price, and a fixed medium size. These are immutable once created and serve as the base unit for orders.

### OrderItem
Represents a single drink within an order, with optional customization. It wraps a `Drink` and a customization string, allowing clean tracking of individual order details.

### CustomerOrder
Stores the customer’s name and a list of `OrderItem` objects. It provides methods to add drinks, format the order for confirmation, and calculate the total price. A standard Python list is used here due to its flexibility and fast iteration.

### Deque (Custom)
The open order queue is implemented using a custom `Deque` class backed by a linked list. It supports enqueue and dequeue operations from both ends and is designed to maintain the first-in, first-out order of drink preparation.

### Completed Orders
Completed orders are stored in a standard Python list. This is suitable for appending finished orders and generating the final sales report efficiently.

## Running the Program

From the root directory of the repository, run:

```
python -m projects.project3.program
```


## Example Menu

The drink menu used in this project includes:

1. Calpico Lemonade - $4.00  
2. Banana Milk - $4.25  
3. Durian Red Bull - $5.00  
4. Ube White Mocha - $4.75  
5. Golden Milk Latte - $4.50


## Known Issues and Limitations

- Orders cannot be edited or removed once placed.
- The program does not currently support saving or loading order history.
- Drink size is fixed to "Medium."
- No authentication system is implemented for baristas.
- All interaction is done via text; there is no GUI.

## Potential Improvements

- Add file I/O to support saving and loading daily order history.
- Introduce multiple drink sizes with variable pricing.
- Implement login/authentication for baristas.
- Simulate order preparation times and display current order status.
- Add terminal formatting or color to improve user interface.

## Author

Salvador Lomeli  
Willamette University