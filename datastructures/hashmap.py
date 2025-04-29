import copy
from typing import Callable, Iterator, Optional, Tuple
from datastructures.ihashmap import KT, VT, IHashMap
from datastructures.array import Array
import pickle
import hashlib
import math

from datastructures.linkedlist import LinkedList

class HashMap(IHashMap[KT, VT]):

    def __init__(self, number_of_buckets=7, load_factor=0.75, custom_hash_function: Optional[Callable[[KT], int]]=None) -> None:
        self._buckets: Array[LinkedList[Tuple[KT, VT]]] = Array(starting_sequence=[LinkedList(data_type=tuple) for _ in range(number_of_buckets)],data_type=LinkedList)
        self._count: int = 0
        self._load_factor: float = load_factor
        self._hash_function = custom_hash_function or self._default_hash_function

    def get_bucket_index(self, key: KT, bucket_size:int) -> int:
        bucket_index = self._hash_function(key)
        return bucket_index % bucket_size

    def __getitem__(self, key: KT) -> VT:
        for (k,v) in self._buckets[self.get_bucket_index(key, len(self._buckets))]:
            if k == key:
                return v
        raise KeyError(f"Key: {key} does not exist in the HashMap")
    
    def _resize(self):
        new_size = self._next_prime(len(self._buckets) * 2)
        new_buckets = Array(starting_sequence=[LinkedList(data_type=tuple) for _ in range(new_size)], data_type=LinkedList)
        for bucket in self._buckets:
            for k, v in bucket:
                new_index = self.get_bucket_index(k, new_size)
                new_buckets[new_index].append((k, v))
        self._buckets = new_buckets
        
    def _next_prime(self, n: int) -> int:
        def is_prime(num: int) -> bool:
            if num <= 1:
                return False
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    return False
            return True
        while not is_prime(n):
            n += 1 
        return n

    def __setitem__(self, key: KT, value: VT) -> None:        
        if self._count / len(self._buckets) >= self._load_factor:
            self._resize()
        bucket_index = self.get_bucket_index(key, len(self._buckets))
        bucket_chain = self._buckets[bucket_index]
        for i, (k, v) in enumerate(bucket_chain):
            if k == key:
                # Update the value for the existing key
                bucket_chain.remove((k, v))
                bucket_chain.append((key, value))
                return
        # Add a new key-value pair if the key does not exist
        bucket_chain.append((key, value))
        self._count += 1

    def keys(self) -> Iterator[KT]:
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def values(self) -> Iterator[VT]:
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self) -> Iterator[Tuple[KT, VT]]:
        for bucket in self._buckets:
            for k, v in bucket:
                yield (k, v)

    def __delitem__(self, key: KT) -> None:
        bucket_index = self.get_bucket_index(key, len(self._buckets))
        bucket_chain = self._buckets[bucket_index]
        for k, v in bucket_chain:
            if k == key:
                # Use LinkedList's remove method to delete the item
                bucket_chain.remove((k, v))
                self._count -= 1
                return
        raise KeyError(f"Key: {key} does not exist in the HashMap")

    def __contains__(self, key: KT) -> bool:
        bucket_index = self.get_bucket_index(key, len(self._buckets))
        bucket_chain:LinkedList = self._buckets[bucket_index]

        for k,v in bucket_chain:
            if k == key:
                return True
        return False

    def __len__(self) -> int:
        return self._count
    
    def __iter__(self) -> Iterator[KT]:
        for key in self.keys():
            yield key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMap):
            return False
        if len(self) != len(other):
            return False
        for key, value in self.items():
            if key not in other or other[key] != value:
                return False
        return True

    def __str__(self) -> str:
        return "{" + ", ".join(f"{key}: {value}" for key, value in self) + "}"
    
    def __repr__(self) -> str:
        return f"HashMap({str(self)})"

    @staticmethod
    def _default_hash_function(key: KT) -> int:
        """
        Default hash function for the HashMap.
        Uses Pickle to serialize the key and then hashes it using SHA-256. 
        Uses pickle for serialization (to capture full object structure).
        Falls back to repr() if the object is not pickleable (e.g., open file handles, certain C extensions).
        Returns a consistent integer hash.
        Warning: This method is not suitable
        for keys that are not hashable or have mutable state.

        Args:
            key (KT): The key to hash.
        Returns:
            int: The hash value of the key.
        """
        try:
            key_bytes = pickle.dumps(key)
        except Exception:
            key_bytes = repr(key).encode()
        return int(hashlib.md5(key_bytes).hexdigest(), 16)