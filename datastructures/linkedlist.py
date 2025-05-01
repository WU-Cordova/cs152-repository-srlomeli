from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional, Sequence
from datastructures.ilinkedlist import ILinkedList, T


class LinkedList[T](ILinkedList[T]):

    @dataclass
    class Node:
        data: T
        next: Optional[LinkedList.Node] = None
        previous: Optional[LinkedList.Node] = None

    def __init__(self, data_type: type = object) -> None:
        self.head: Optional[LinkedList.Node] = None
        self.tail: Optional[LinkedList.Node] = None
        self.count: int = 0
        self.data_type = data_type

    @staticmethod
    def from_sequence(sequence: Sequence[T], data_type: type=object) -> LinkedList[T]:
        linked_list:LinkedList[T] = LinkedList(data_type=data_type)

        for item in sequence:
            linked_list.append(item)
        return linked_list
    
    def append(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")

        new_node:LinkedList.Node = LinkedList.Node(data=item)

        if self.empty:
            self.head = self.tail = new_node
        else: 
            if self.tail:
                self.tail.next = new_node
                new_node.previous = self.tail
                self.tail = new_node

        self.count += 1

    def prepend(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")

        new_node: LinkedList.Node = LinkedList.Node(data=item)

        if self.empty:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node

        self.count += 1

    def insert_before(self, target: T, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")
        if not isinstance(target, self.data_type):
            raise TypeError(f"Target must be of type {self.data_type.__name__}")


        current = self.head
        while current:
            if current.data == target:
                new_node = LinkedList.Node(data=item)
                new_node.next = current
                new_node.previous = current.previous

                if current.previous:
                    current.previous.next = new_node
                else:
                    self.head = new_node

                current.previous = new_node
                self.count += 1
                return

            current = current.next

        raise ValueError(f"The target item {target} is not in the linked list.")

    def insert_after(self, target: T, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")
        if not isinstance(target, self.data_type):
            raise TypeError(f"Target must be of type {self.data_type.__name__}")

        current = self.head
        while current:
            if current.data == target:
                new_node = LinkedList.Node(data=item)
                new_node.previous = current
                new_node.next = current.next

                if current.next:
                    current.next.previous = new_node
                else:
                    self.tail = new_node

                current.next = new_node
                self.count += 1
                break

            current = current.next
        else:
            raise ValueError(f"The target item {target} is not in the linked list.")
    def remove(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")

        current = self.head
        while current:
            if current.data == item:
                # Update pointers to remove the node
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next  # Update head if removing the first node

                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous  # Update tail if removing the last node

                self.count -= 1
                return

            current = current.next

        raise ValueError(f"The item {item} is not in the linked list.")

    def remove_all(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Item must be of type {self.data_type.__name__}")

        current = self.head
        while current:
            if current.data == item:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next  # Update head if removing the first node

                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous  # Update tail if removing the last node

                self.count -= 1

                # Move to the next node after removal
                current = current.next
            else:
                # Move to the next node if no removal
                current = current.next
        
    def pop(self) -> T:
        if self.empty:
            raise IndexError("LinkedList is empty")

        data = self.tail.data  # Get the data of the last node

        if self.head == self.tail:
            # If there's only one node, clear the list
            self.head = self.tail = None
        else:
            # Update the tail to the previous node
            self.tail = self.tail.previous
            self.tail.next = None

        self.count -= 1
        return data

    def pop_front(self) -> T:
        if self.empty:
            raise IndexError("LinkedList is empty")

        data = self.head.data  # Get the data of the first node

        if self.head == self.tail:
            # If there's only one node, clear the list
            self.head = self.tail = None
        else:
            # Update the head to the next node
            self.head = self.head.next
            self.head.previous = None

        self.count -= 1
        return data

    @property
    def front(self) -> T:
        if self.empty:
            raise IndexError("LinkedList is empty")
        return self.head.data  # Return the data of the head node
    @property
    def back(self) -> T:
        if not self.tail or self.count == 0:
            raise IndexError("LinkedList is empty")
        return self.tail.data

    @property
    def empty(self) -> bool:
        return self.head is None and self.tail is None and self.count == 0
    
    def __len__(self) -> int:
        return self.count
    
    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.count = 0

    def __contains__(self, item: T) -> bool:
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def __iter__(self) -> ILinkedList[T]:
        self._current = self.head  # Start iteration from the head
        return self

    def __next__(self) -> T:
        if self._current is None:
            raise StopIteration  # End of the linked list

        data = self._current.data  # Get the current node's data
        self._current = self._current.next  # Move to the next node
        return data
    
    def __reversed__(self):
        current = self.tail  # Start from the tail
        while current:
            yield current.data  # Yield the data of the current node
            current = current.previous  # Move to the previous node
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinkedList):
            return False
        if len(self) != len(other):
            return False

        current_self = self.head
        current_other = other.head

        while current_self and current_other:
            if current_self.data != current_other.data:
                return False
            current_self = current_self.next
            current_other = current_other.next

        return True

    def __str__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return '[' + ', '.join(items) + ']'

    def __repr__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return f"LinkedList({' <-> '.join(items)}) Count: {self.count}"


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
