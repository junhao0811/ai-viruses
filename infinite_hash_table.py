from __future__ import annotations
from algorithms.mergesort import *
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack

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
            return self.get_item_aux(current_table.array[pos][1], key)
        
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        if key not in self.key_list:
            self.count += 1
            self.key_list.append(key)

        # Call the auxiliary method
        self.set_item_aux(self, key, value)

    def set_item_aux(self, current_table: InfiniteHashTable, key: K, value: V):
        """
        Auxiliary method to set an (key, value) pair in our hash table.
        """
        # Hash the key to get the position
        pos = current_table.hash(key)

        # If the position is empty, insert the new (key, value) pair in our hash table
        if current_table.array[pos] is None:
            current_table.array[pos] = (key, value)
            return

        # Store what was previously in the position in a variable
        prev_key, prev_value = current_table.array[pos]

        # Update the previous (key, value) into new position
        if not isinstance(prev_value, InfiniteHashTable):
            # Base case: the key already exists in that position
            if current_table.array[pos][0] == key:
                current_table.array[pos] = (key, value)
                return
            # Create a new hash table to store previous (key, value) pair
            current_table.array[pos] = (prev_key[:current_table.level + 1], InfiniteHashTable(current_table.level))

            # Update the current table to the infinite hash table created
            current_table = current_table.array[pos][1]
            current_table.level += 1

            # Reinsert the previous key and value
            current_table[prev_key] = prev_value
            current_table.key_list.append(key)
            current_table.count += 1

        else:
            # Update the current table to the infinite hash table
            current_table = current_table.array[pos][1]

            # If the key is already existing, no need to update the count and key list
            if key not in current_table.key_list:
                current_table.count += 1
                current_table.key_list.append(key)

        # Recursive call with the updated current table and new key value
        current_table.set_item_aux(current_table, key, value)
        
    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # Initialise a pointer to the top table
        current_table = self

        # Create a linked stack to store the pointers to the hash tables
        stack = LinkedStack()

        # Traverse the infinite depth hash table to get to the last level hash table
        while True:
            # Hash the key to get the position
            pos = current_table.hash(key)

            # Raises KeyError if the key doesn't exist
            if current_table.array[pos] is None:
                raise KeyError(f"Key '{key}' doesn't exist because it's None")

            # Else if the bucket contains a pointer to the next level hash table, push the pointer to the stack and move the pointer to point to the next table
            elif isinstance(current_table.array[pos][1], InfiniteHashTable):
                stack.push(current_table)
                current_table = current_table.array[pos][1]
            
            # Else if the last level hash table is reached
            elif not isinstance(current_table.array[pos][1], InfiniteHashTable):
                # Check if it is the same key or not
                if current_table.array[pos][0] != key:
                    raise KeyError(f"Key '{key}' doesn't exist because it's not the same key")
                else:
                    # Delete the key from the hash table
                    current_table.array[pos] = None
                    current_table.count -= 1
                    break
            
        if len(current_table) == 1:
            return self.collapse_table(current_table, stack)

    def collapse_table(self, current_table: InfiniteHashTable, stack: LinkedStack[InfiniteHashTable]) -> None:
        """
        Collapse the hash table to a single entry in the parent table
        until there is a table with multiple pairs or it reaches the top table if there is
        only a single pair within the current table.
        """
        # Base case - if the length of the current table is greater than 1
        if len(current_table) > 1 or current_table.level == 0:
            return
        
        # Recursive call
        else:
            pos = 0
            for i in range(current_table.TABLE_SIZE):
                if current_table.array[i] is not None:
                    pos = i
                    break

            # Pop the parent table from the stack
            parent_table = stack.pop()
            
            # Store the key and value in a temporary variable
            item = current_table.array[pos]

            # Point the current table to the parent table
            current_table = parent_table

            # Hash the key to get the position in the previous table
            if item is not None:
                old_pos = current_table.hash(item[0])
            
            # Store the key and value in the parent table
            current_table.array[old_pos] = item

            # Update current_table to become the parent table
            return self.collapse_table(current_table, stack)

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
    

if __name__ == "__main__":
    ih = InfiniteHashTable()

    # test set & get_location
    ih["lin"] = 1
    ih["leg"] = 2

    print(ih.get_location("lin")) # [4, 1]
    print(ih.get_location("leg")) # [4, 23]
    print(len(ih)) # 2

    ih["mine"] = 3
    ih["linked"] = 4

    print(ih.get_location("mine")) # [5]
    print(ih.get_location("lin")) # [4, 1, 6, 26]
    print(ih.get_location("linked")) # [4, 1, 6, 3]
    print(len(ih)) # 4

    ih["limp"] = 5
    ih["mining"] = 6

    print(ih.get_location("limp")) # [4, 1, 5]
    print(ih.get_location("mine")) # [5, 1, 6, 23]
    print(ih.get_location("mining")) # [5, 1, 6, 1]
    print(len(ih)) # 6

    ih["jake"] = 7
    ih["linger"] = 8
    
    print(ih.get_location("jake")) # [2]
    print(ih.get_location("linger")) # [4, 1, 6, 25]
    print(len(ih)) # 8


    # test_delete
    ih["lin"] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    ih["jake"] = 7
    ih["linger"] = 8

    del ih["limp"]
    print(ih.get_location("linked")) # [4, 1, 6, 3]

    del ih["mine"]
    print(ih.get_location("mining")) # [5]

    del ih["mining"]
    del ih["jake"]
    del ih["leg"]
    del ih["linger"]
    del ih["linked"]

    print(ih["lin"]) # 1
    print(ih.get_location("lin")) # [4]

    del ih["lin"]

    ih["lin"] = 10
    print(ih.get_location("lin")) # [4]
    print(len(ih)) # 1
    

    # test get
    print(ih["lin"])
    print(ih["leg"])
    print(ih["jake"])
    print(ih["linger"])