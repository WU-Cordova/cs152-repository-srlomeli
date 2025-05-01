from typing import Iterable, Optional
from datastructures.ibag import IBag, T


class Bag(IBag[T]):
    def __init__(self, *items: Optional[Iterable[T]]) -> None:
        self.__bag = {}

        if items is not None:
            for item in items:
                self.add(item)
                    
    def add(self, item: T) -> None:
        if item is None:
            raise TypeError("Cannot add None to the bag")
        if item in self.__bag:
            self.__bag[item] += 1
        else:
            self.__bag[item] = 1
            
    def remove(self, item: T) -> None:
        if item not in self.__bag:
            raise ValueError(f"Item {item} not in the bag")
        self.__bag[item] -= 1
        if self.__bag[item] == 0:  # Remove item entirely if count reaches 0
            del self.__bag[item]

    def count(self, item: T) -> int:
        return self.__bag.get(item, 0)  # Return 0 if item is not in the bag

    def __len__(self) -> int:
        return sum(self.__bag.values())  # Total number of items in the bag
    
    def distinct_items(self) -> Iterable[T]:
        return self.__bag.keys()  # Return distinct items as an iterable
    
    def __contains__(self, item) -> bool:
        return item in self.__bag  # Check if the item exists in the bag

    def clear(self) -> None:
        self.__bag.clear()  # Remove all items from the bag