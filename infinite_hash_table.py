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
        """
        Initialise the Infinite Hash Table.

        :complexity: O(N) for best/worst case when initialising the array where N is self.TABLE_SIZE
        """
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level

    def hash(self, key: K) -> int:
        """
        Hash function to determine the position of the key in the hash table.
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        :complexity: O(get_item_aux)
        """
        # Call auxiliary method
        return self.get_item_aux(self, key)

    def get_item_aux(self, current_table: InfiniteHashTable, key: K) -> V:
        """
        Auxiliary method to get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        :complexity:
            :best case: O(1) when the key already exists at the top table.
            :worst case: O(N) when the key exists at the last level hash table, where N the depth of infinite hash table.
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
        Set a (key, value) pair in our hash table.
        :complexity: O(set_item_aux)
        """
        self.count += 1
        # Call the auxiliary method
        tracker = self.set_item_aux(self, key, value, LinkedStack())
        if tracker is not None:
            if tracker.peek() is True:
                self.count -= 1

    def set_item_aux(self, current_table: InfiniteHashTable, key: K, value: V, repeat_element: LinkedStack) -> LinkedStack | None:
        """
        Auxiliary method to set a (key, value) pair in our hash table.

        :complexity:
            :best case: O(1) when the position in the top table is empty or the key already exists in the position in the top table.
            :worst case: O(N * [S + I]) when the position we want to insert the (key, value) pair is at the last level hash table and whilst continuously creating a new hash table where
                N is the maximum depth of the hash table
                S is the complexity of the slice operation when slicing the key
                I is the complexity of initialising the InfiniteHashTable
        """
        # Hash the key to get the position
        pos = current_table.hash(key)

        # If the position is empty, insert the new (key, value) pair in our hash table
        if current_table.array[pos] is None:
            current_table.array[pos] = (key, value)
            repeat_element.push(False)
            return

        # Store what was previously in the position in a variable
        prev_key, prev_value = current_table.array[pos]

        # Update the previous (key, value) into new position
        if not isinstance(prev_value, InfiniteHashTable):
            # Base case: the key already exists in that position
            if current_table.array[pos][0] == key:  # O(comp)
                current_table.array[pos] = (key, value)
                current_table.count -= 1
                repeat_element.push(True)
                return

            # Create a new hash table to store previous (key, value) pair
            current_table.array[pos] = (prev_key[:current_table.level + 1], InfiniteHashTable(current_table.level))  # O(k) where k is the size of key + O(I)

            # Update the current table to the infinite hash table created
            current_table = current_table.array[pos][1]
            current_table.level += 1

            # Reinsert the previous key and value
            current_table[prev_key] = prev_value  # O(setitem)
            current_table.count += 1

        else:
            # Update the current table to the infinite hash table
            current_table = current_table.array[pos][1]

            # If the key is already existing, no need to update the count and key list
            current_table.count += 1

        # Recursive call with the updated current table and new key value
        self.set_item_aux(current_table, key, value, repeat_element)   
        if repeat_element.peek() is True:
            current_table.count -= 1
        return repeat_element

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        
        :complexity:
            :best case: O(1) when the item targeted for deletion appears at the top table
            :worst case: O(N + M) when the item targeted for deletion is the only item located at the last level hash table
                N is the maximum depth of the target key
                M is the complexity of self.collapse_table()
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
                raise KeyError(f"Key '{key}' doesn't exist")

            current_table.count -= 1

            # Else if the bucket contains a pointer to the next level hash table, push the pointer to the stack and
            # move the pointer to point to the next table
            if isinstance(current_table.array[pos][1], InfiniteHashTable):
                stack.push(current_table)
                current_table = current_table.array[pos][1]

            # Else if the last level hash table is reached
            elif not isinstance(current_table.array[pos][1], InfiniteHashTable):
                # Check if it is the same key or not
                if current_table.array[pos][0] != key:
                    raise KeyError(f"Key '{key}' doesn't exist")
                else:
                    # Delete the key from the hash table
                    current_table.array[pos] = None
                    break

        if len(current_table) == 1:
            return self.collapse_table(current_table, stack)

    def collapse_table(self, current_table: InfiniteHashTable, stack: LinkedStack[InfiniteHashTable]) -> None:
        """
        Collapse the hash table to a single entry in the parent table
        until there is a table with multiple pairs or it reaches the top table if there is
        only a single pair within the current table.
        :complexity:
            :best: O(1) when the current table has more than one (key, value) pair or it is the top table
            :worst: O(N * self.TABLE_SIZE) when there is only one element in each level, and it needs to recursively call the method until the base case where it reaches the top level, where
                N is the maximum depth of the hash table
        """
        # Base case - if the length of the current table is greater than 1
        if len(current_table) > 1 or current_table.level == 0:
            return

        # Recursive call
        else:
            for i in range(self.TABLE_SIZE):
                if current_table.array[i] is not None:
                    pos = i
                    break

            # Pop the parent table from the stack
            parent_table = stack.pop()

            # Unpack the key and value in a temporary variable
            key, value = current_table.array[pos]

            # Point the current table to the parent table
            current_table = parent_table

            # Hash the key to get the position in the previous table
            oldpos = current_table.hash(key)

            # Store the key and value in the parent table
            current_table.array[oldpos] = (key, value)

            # Update current_table to become the parent table
            self.collapse_table(current_table, stack)

    def __len__(self) -> int:
        """
        Returns the number of (key, value) pairs in the hash table.
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key: K) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        :complexity: O(get_location_aux)
        """
        # Call auxiliary method
        return self.get_location_aux(self, key, [])

    def get_location_aux(self, current_table: InfiniteHashTable, key: K, positions: list[int]) -> list[int]:
        """
        Auxiliary method to get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        :complexity:
            :best: O(1) when the item targeted for deletion appears at the top table
            :worst: O(N) when the key exists at the last level hash table, where N is the maximum depth of the infinite hash table
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

        :complexity: O(sort_keys_aux)
        """
        return self.sort_keys_aux(current, [])
    
    def sort_keys_aux(self, current_table: InfiniteHashTable, sorted_keys: list[str]) -> list[str]:
        """
        Auxiliary method for sort_keys

        :complexity:
            :best case: O(self.TABLE_SIZE) when there are no inner infinite hash table and all the (key, value) pairs are stored in the top table
            :worst case: O(N * A * L) when there are infinite hash tables in the table and the keys are stored in the last level hash table
                N is the number of words inserted
                A is the size of the alphabet (26)
                L is the length of the longest word
        """
        if current_table is None:
            current_table = self

        # Check whether the last element in the table is empty
        if current_table.array[self.TABLE_SIZE - 1] is not None:
            sorted_keys.append(current_table.array[self.TABLE_SIZE - 1][0])

        # Iterate through the table starting from position 'a'
        pos = self.hash('a')
        for _ in range(self.TABLE_SIZE - 1):
            if current_table.array[pos] is not None:
                # Append the key to the sorted list when there is a (key, value) pair
                if not isinstance(current_table.array[pos][1], InfiniteHashTable):
                    sorted_keys.append(current_table.array[pos][0])

                # Recursive call when there is an infinite hash table in the next level
                else:
                    self.sort_keys_aux(current_table.array[pos][1], sorted_keys)
                
            # Wrap around the table
            pos = (pos + 1) % (self.TABLE_SIZE - 1)

        return sorted_keys
    
if __name__ == "__main__":
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    ih["jake"] = 7
    ih["linger"] = 8
    res = ih.sort_keys()
    print(res)