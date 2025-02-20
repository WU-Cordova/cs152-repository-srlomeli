# datastructures.array.Array

""" This module defines an Array class that represents a one-dimensional array. 
    See the stipulations in iarray.py for more information on the methods and their expected behavior.
    Methods that are not implemented raise a NotImplementedError until they are implemented.
"""

from __future__ import annotations
from collections.abc import Sequence
import os
from typing import Any, Iterator, overload
import numpy as np
from numpy.typing import NDArray
import copy


from datastructures.iarray import IArray, T


class Array(IArray[T]):  
    def __init__(self, starting_sequence: Sequence[T]=[], data_type: type=object) -> None: 
        """
        Initialize the Array with an optional starting sequence and a required data_type.
        
        Parameters:
          starting_sequence: A sequence of items to populate the array.
                             All items must be of the same type as data_type.
          data_type: The expected type for all items in the array.
        
        Raises:
          ValueError: If starting_sequence is not a valid sequence.
          TypeError:  If any item in starting_sequence is not of the specified data_type.
        """
        # Ensure starting_sequence is a valid sequence.
        if not isinstance(starting_sequence, Sequence):
            raise ValueError("starting_sequence must be a valid sequence type")
        
        # Set the logical size (number of used elements) from the starting sequence
        self.__logical_size = len(starting_sequence)
        # Initially, the physical size will equal the logical size
        self.__physical_size = self.__logical_size
        # Store the expected data type for all items in the array
        self.__data_type = data_type
        
        # Check that every item in the starting sequence is of the expected type
        for index in range(self.__logical_size):
            if not isinstance(starting_sequence[index], self.__data_type):
                raise TypeError("The items in the starting sequence must be the same data type")
        
        # Create the underlying NumPy array with the same number of elements.
        # (We use np.empty to allocate space; contents will be filled next.)
        self.__elements = np.empty(self.__logical_size, dtype=self.__data_type)
            
        # Deep copy each element from the starting sequence into the internal array.
        for index in range(self.__logical_size):
            self.__elements[index] = copy.deepcopy(starting_sequence[index])

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...
    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        """
        Retrieve an element or a slice of elements from the array.
        
        If the index is an integer, return the corresponding element (supporting negative indexing).
        If the index is a slice, convert the used portion of the array to a list and return a new Array.
        
        Raises:
          IndexError: If an integer index is out of range.
          TypeError:  If the index is neither an int nor a slice.
        """
        if isinstance(index, slice):
            # Convert the underlying array to a list and apply the slice.
            # Create a new Array from the sliced data, preserving the data_type.
            return Array(self.__elements.tolist()[index], data_type=self.__data_type)
        elif isinstance(index, int):
            # Adjust for negative indexing.
            if index < 0:
                index += self.__logical_size
            if index < 0 or index >= self.__logical_size:
                raise IndexError("Index is out of range")
            return self.__elements[index]
        else:
            raise TypeError("Index is not an int or slice")
    
    def __setitem__(self, index: int, item: T) -> None:
        """
        Set the item at a specific index in the array.
        
        Raises:
          IndexError: If the index is out of range.
          TypeError:  If the item is not of the expected data_type.
        """
        if not isinstance(item, self.__data_type):
            raise TypeError("Item does not contain same type as Array")
        if index < 0:
            index += self.__logical_size
        if index < 0 or index >= self.__logical_size:
            raise IndexError("Index is out of range")
        self.__elements[index] = item
    
    def append(self, data: T) -> None:
        """
        Append an item to the end of the array.
        
        This increases the logical size by one. If the logical size matches the physical size,
        the underlying array is grown (doubled in capacity) to accommodate more elements.
        """
        # Convert the NumPy array to a list and append the new data.
        listElements = self.__elements.tolist()
        listElements.append(data)
        # Update the underlying array with the new list.
        self.__elements = np.array(listElements, dtype=self.__data_type)
        self.__logical_size += 1
        self.__grow()
    
    def __grow(self) -> None:
        """
        Grow the underlying array if the logical size equals the physical size.
        
        The physical size is doubled, and all current elements are deep-copied to the new array.
        """
        if self.__logical_size == self.__physical_size:
            self.__physical_size *= 2
            # Create a new NumPy array with the new physical size.
            self.__newElements = np.empty(self.__physical_size, dtype=self.__data_type)
            # Copy existing elements into the new array.
            for index in range(self.__logical_size):
                self.__newElements[index] = copy.deepcopy(self.__elements[index])
            self.__elements = self.__newElements
        # If growth is not needed, do nothing.
    
    def __shrink(self) -> None:
        """
        Shrink the underlying array when the logical size is half the physical size.
        
        The physical size is halved and current elements are copied over to the new, smaller array.
        """
        if self.__logical_size == self.__physical_size // 2:
            self.__physical_size //= 2
            self.__newElements = np.empty(self.__physical_size, dtype=self.__data_type)
            for index in range(self.__logical_size):
                self.__newElements[index] = copy.deepcopy(self.__elements[index])
            self.__elements = self.__newElements
        # Nothing is done if shrinking is not neccessary
    
    def append_front(self, data: T) -> None:
        """
        Insert an item at the front of the array.
        
        All existing elements are shifted to the right, the logical size is increased,
        and the underlying array is grown if necessary.
        
        (Currently not implemented.)
        """
        # Convert to list, insert at index 0, and update the underlying array.
        listElements = self.__elements.tolist()
        listElements.insert(0, data)
        self.__elements = np.array(listElements, dtype=self.__data_type)
        self.__logical_size += 1
        self.__grow()
    
    def pop(self) -> None:
        """
        Remove the last element of the array.
        
        The logical size is decreased by one and the array is shrunk if necessary.
        """
        self.__delitem__(self.__logical_size - 1)
        self.__logical_size -= 1
        self.__shrink()
    
    def pop_front(self) -> None:
        """
        Remove the first element of the array.
        
        Remaining elements are shifted to the left, the logical size is decreased,
        and the underlying array is shrunk if necessary.
        """
        self.__delitem__(0)
        self.__logical_size -= 1
        self.__shrink()
    
    def __len__(self) -> int:
        """
        Return the number of used elements in the array.
        """
        return self.__logical_size
    
    def __eq__(self, other: object) -> bool:
        """
        Compare this array to another for equality.
        
        Two arrays are considered equal if their used elements are equal.
        """
        # Check that the other object supports indexing and has the same logical size.
        if not hasattr(other, "__getitem__") or len(other) != self.__logical_size:
            return False
        for index in range(self.__logical_size):
            if self.__elements[index] != other[index]:
                return False
        return True
    
    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator over the elements of the array.
        """
        for element in self.__elements:
            yield element
    
    def __reversed__(self) -> Iterator[T]:
        """
        Return an iterator over the elements of the array in reverse order.
        """
        reversedArray = self.__elements[::-1]
        return iter(reversedArray)
    
    def __delitem__(self, index: int) -> None:
        """
        Delete the element at the specified index.
        
        This method removes the element from the underlying array.
        """
        self.__elements = np.delete(self.__elements, index)
    
    def __contains__(self, item: Any) -> bool:
        """
        Check if an item is present in the array.
        
        Uses NumPy's isin function.
        """
        return np.isin(item, self.__elements)
    
    def clear(self) -> None:
        """
        Clear the array.
        
        Both the logical and physical sizes are reset, and the underlying array becomes empty.
        """
        self.__logical_size = 0
        self.__physical_size = 0
        self.__elements = np.empty(self.__logical_size, dtype=self.__data_type)
    
    def __str__(self) -> str:
        """
        Return a simple string representation of the array.
        """
        return '[' + ', '.join(str(item) for item in self) + ']'
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the array, including its logical size,
        physical capacity, and data type.
        """
        return f'Array {self.__str__()}, Logical: {self.__logical_size}, Physical: {len(self.__elements)}, type: {self.__data_type}'
    

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
