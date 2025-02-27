from __future__ import annotations
import os
from typing import Iterator, Sequence

from datastructures.iarray import IArray
from datastructures.array import Array
from datastructures.iarray2d import IArray2D, T

class Array2D(IArray2D[T]):

    class Row(IArray2D.IRow[T]):
        def __init__(self, row_index: int, array: IArray, num_columns: int) -> None:
            # Initialize Row with row_index, the array it belongs to, and the number of columns
            self.__row_index = row_index
            self.__array = array
            self.__num_columns = num_columns

        def map_index(self, row_index: int, col_index: int) -> int:
            # Calculate the index in the underlying 1D array for the 2D coordinates
            return row_index * self.__num_columns + col_index
        
        def __getitem__(self, column_index: int) -> T:
            # Get the item at the specified column_index in this row
            if column_index >= self.__num_columns:
                raise IndexError("Column index out of range")
            index: int = self.map_index(self.__row_index, column_index)
            return self.__array[index]
        
        def __setitem__(self, column_index: int, value: T) -> None:
            # Set the item at the specified column_index in this row
            if column_index >= self.__num_columns:
                raise IndexError("Column index out of range")
            index: int = self.map_index(self.__row_index, column_index)
            self.__array[index] = value
        
        def __iter__(self) -> Iterator[T]:
            # Allow iteration over items in this row
            return (self[i] for i in range(self.__num_columns))
        
        def __reversed__(self) -> Iterator[T]:
            # Allow reversed iteration over items in this row
            return (self[i] for i in range(self.__num_columns - 1, -1, -1))

        def __len__(self) -> int:
            # Return the number of columns in this row
            return self.__num_columns
        
        def __str__(self) -> str:
            # Return string representation of this row
            return f"[{', '.join(str(self[column_index]) for column_index in range(self.__num_columns))}]"
        
        def __repr__(self) -> str:
            # Return detailed string representation of this row
            return f"Row {self.__row_index}: [{', '.join(str(self[column_index]) for column_index in range(self.__num_columns))}]"


    def __init__(self, starting_sequence: Sequence[Sequence[T]] = [[]], data_type=object) -> None:
        # Validate starting_sequence and ensure all items have the same data type
        try:
            if not all(isinstance(row, Sequence) and not isinstance(row, str) for row in starting_sequence):
                raise ValueError("must be a sequence of sequences")
        except TypeError:
            raise ValueError("must be a sequence of sequences")
        
        self.__data_type = type(starting_sequence[0][0]) if data_type == object else data_type
        self.__rows_len = len(starting_sequence)
        self.__cols_len = len(starting_sequence[0])

        if not all(len(row) == self.__cols_len and all(isinstance(item, self.__data_type) for item in row) for row in starting_sequence):
            raise ValueError("All items must be of the same type and all rows must have the same length")
        
        py_list = [item for row in starting_sequence for item in row]
        self.__elements2d = Array(starting_sequence=py_list, data_type=self.__data_type)
        

    @staticmethod
    def empty(rows: int = 0, cols: int = 0, data_type: type = object) -> Array2D:
        # Create an empty Array2D with the specified rows, columns, and data type
        sequence2d = [[data_type() for _ in range(cols)] for _ in range(rows)]
        return Array2D(starting_sequence=sequence2d, data_type=data_type)

    def __getitem__(self, row_index: int) -> Array2D.IRow[T]: 
        # Get the row at the specified row_index
        if row_index >= self.__rows_len:
            raise IndexError("Row index out of range")
        return self.Row(row_index=row_index, array=self.__elements2d, num_columns=self.__cols_len)    
    
    def __iter__(self) -> Iterator[Sequence[T]]:
        # Allow iteration over rows in the 2D array
        return (self[row] for row in range(self.__rows_len))
    
    def __reversed__(self) -> Iterator[Sequence[T]]:
        # Allow reversed iteration over rows in the 2D array
        return (self[row] for row in range(self.__rows_len - 1, -1, -1))
    
    def __len__(self) -> int:
        # Return the number of rows in the 2D array
        return self.__rows_len
                                  
    def __str__(self) -> str: 
        # Return string representation of the 2D array
        return f"[{', '.join(str(row) for row in self)}]"
    
    def __repr__(self) -> str: 
        # Return detailed string representation of the 2D array
        return f"Array2D {self.__rows_len} Rows x {self.__cols_len} Columns, items: {str(self)}"


if __name__ == '__main__':
    # If this file is run as a script, output the filename and a prompt for the user
    filename = os.path.basename(__file__)
    print(f"This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.")
