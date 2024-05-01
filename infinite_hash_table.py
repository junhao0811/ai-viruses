from __future__ import annotations
from algorithms.mergesort import *
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
        self.key_list = []
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        # Call auxiliary method
        return self.get_item_aux(self, key)
    
    def get_item_aux(self, current_table: InfiniteHashTable, key: K) -> V:
        """
        Auxiliary method to get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        # Hash the key to get the position
        pos = current_table.hash(key)

        # Base case - if the key doesn't exist, raise a KeyError
        if current_table.array[pos] is None:
            raise KeyError(f"Key '{key}' doesn't exist")
        
        # Base case - if the key exists in the current position, return its value
        elif not isinstance(current_table.array[pos][1], InfiniteHashTable):
            if current_table.array[pos][0] != key:
                raise KeyError(f"Key '{key}' doesn't exist")
            return current_table.array[pos][1]
        
        # Recursive call to the next level of hash table
        else:
            current_table.level += 1
            return self.get_item_aux(current_table.array[pos][1], key)
        
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        self.key_list.append(key)

        # Call auxiliary method
        return self.set_item_aux(self, key, value)

    def set_item_aux(self, current_table: InfiniteHashTable, key: K, value: V):
        """
        Auxiliary method to set an (key, value) pair in our hash table.
        """
        # Hash the key to get position
        pos = current_table.hash(key)
        item_is_inserted = False

        # Base case: the position that we want to add the (key, value) pair is empty
        if current_table.array[pos] is None:
            current_table.array[pos] = (key, value)
            current_table.count += 1
            item_is_inserted = True
            return
        
        # Otherwise store what was previously in the position in a variable
        prev_key, prev_value = current_table.array[pos]

        # If the previous value is not an InfiniteHashTable
        if not isinstance(prev_value, InfiniteHashTable):
            # Base case: the key already exists in that position
            if current_table.array[pos][0] == key:
                current_table.array[pos] = (key, value)
                item_is_inserted = False
                return

            # Otherwise create a new hash table to store the previous (key, value) pair
            current_table.array[pos] = (prev_key[:current_table.level + 1], InfiniteHashTable())
            current_table.level += 1

            # Hash the previous key to get the position in the newly created hash table
            prev_key_pos = current_table.hash(prev_key)

            # Insert the previous (key, value) pair in the hash table of next level
            current_table.array[pos][1][prev_key_pos] = (prev_key, prev_value)

            # Recursive call to the next level of the table
            self.set_item_aux(current_table.array[pos][1], key, value)

            # Collapse the runtime stack and sum up all of current_table.count from all stacks
            # to get the total number of (key, value) pairs in the hash table
            if item_is_inserted:
                current_table.count += 1

        # Recursive call to the next level of the table
        else:
            current_table.level += 1
            return self.set_item_aux(current_table.array[pos][1], key, value)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos_list = self.get_location(key)

        # Call auxiliary method
        return self.delete_item_aux(self, key, pos_list)
    
    def delete_item_aux(self, current_table: InfiniteHashTable, key: K):
        """
        Auxiliary method to delete a (key, value) pair in our hash table.
        """
        # Hash the key to get the position
        pos = current_table.hash(key)

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        table_str = ""
        for i, item in enumerate(self.array):
            if item is not None:
                table_str += f"{i}: {item}\n"
        return table_str

    def get_location(self, key: K) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        # Call auxiliary method
        return self.get_location_aux(self, key, [])
    
    def get_location_aux(self, current_table: InfiniteHashTable, key: K, positions: list[int]) -> list[int]:
        """
        Auxiliary method to get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        # Hash the key to get the position
        pos = current_table.hash(key)

        # Base case - if the key doesn't exist, raise a KeyError
        if current_table.array[pos] is None:
            raise KeyError(f"Key '{key}' doesn't exist")

        # Base case - if the key exists in the current position, return the list of positions
        elif not isinstance(current_table.array[pos][1], InfiniteHashTable):
            if current_table.array[pos][0] != key:
                raise KeyError(f"Key '{key}' doesn't exist")
            positions.append(pos)
            return positions
        
        else:
            # Store the position in the list of positions first
            positions.append(pos)
            
            # Recursive call to the next level of the table
            current_table.level += 1
            return self.get_location_aux(current_table.array[pos][1], key, positions)

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        return mergesort(self.key_list)