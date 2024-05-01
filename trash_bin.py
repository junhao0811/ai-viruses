from __future__ import annotations
from algorithms.mergesort import *
from typing import Generic, TypeVar
from infinite_hash_table import InfiniteHashTable

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # Initialise a pointer to the top table
        current_table = self

        # Traverse the inifinite depth hash table to get to the last level hash table
        while True:
            # Hash the key to get the position
            pos = self.hash(key)            

            # Access the bucket at the hashed position
            # Raises KeyError if the key doesn't exist
            if current_table.array[pos] is None:
                raise KeyError(f"Key '{key}' doesn't exist")

            # Else if the bucket contains a pointer to the next level hash table, move the pointer (current_table) to point to the next table
            elif isinstance(current_table.array[pos][1], InfiniteHashTable):
                # Keep a reference to the parent table
                parent_table = current_table
                current_table.level += 1
                current_table = current_table.array[pos][1]
            
            # Else if the last level hash table is reached
            elif not isinstance(current_table.array[pos][1], InfiniteHashTable):
                # Check if it is the same key or not
                if current_table.array[pos][0] != key:
                    raise KeyError(f"Key '{key}' doesn't exist")
                else:
                    target_deletion = key
                    # Delete the key from the hash table
                    current_table.array[pos] = None
                    current_table.count -= 1
                    break

        # Make a recursive call to delete_item_aux with the nested hash table to collapse the table if the table only consists of only the target delete item
        if len(current_table) == 1:
            self._collapse_table(parent_table, current_table, current_table.array[pos])
            self.key_list.remove(key)

def _collapse_table(self, parent_table: InfiniteHashTable, current_table: InfiniteHashTable, item: tuple[K, V]):
    """Recursively collapse the hash table to a single entry in the parent table
    until there is a table with multiple pairs or it reaches the top table if there is
    only a single pair within the current table.

    :param current_table: The current hash table
    :type current_table: ArrayR
    :param pos_list: The list of positions to access the key
    :type pos_list: List[int]
    """
    # Hash the key to get the position
    pos = self.hash(item[0])

    # Base case - if the length of the current table is greater than 1
    if len(current_table) > 1 or current_table.level == 0:
        return
    
    # Recursive call
    else:
        # Store the key and value in a temporary variable
        key, value = current_table.array[pos]
        current_table = parent_table
        # Hash the key
        self.hash(key)
        
        # Store the key and value in the parent table
        current_table.array[pos] = (key, value)
        # Update current_table to become the parent table (in the recursive call)
        # Update the parent table to become the grandparent table (in the recursive call)
        return self._collapse_table(parent_table, current_table, item)