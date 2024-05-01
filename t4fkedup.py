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
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        # Initialize a pointer to the top table
        current_table = self.array

        # Reset the level of the hash table
        self.level = 0

        # Iterate through the infinite depth hash table
        while True:
            # Hash the key to get the position
            pos = self.hash(key)

            # Raise KeyError if there is nothing in the position
            if current_table[pos] is None:
                raise KeyError(key)

            # Check if there is a value in the tuple
            elif not isinstance(current_table[pos][1], ArrayR):
                return current_table[pos][1]

            # Update the current table and move on to the next level of hash table
            current_table = current_table[pos][1]
            self.level += 1

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        # Initialize a pointer to the top table
        current_table = self.array

        # Reset the level of the hash table
        self.level = 0
        self.key_list.append(key)
        
        # Traverse the infinite depth hash table
        while True:
            # Hash the key to get the position
            pos = self.hash(key)

            # If the position is empty, insert the new (key, value) pair in our hash table
            if current_table[pos] is None:
                current_table[pos] = (key, value)
                self.count += 1
                return

            else:
                # Store what was previously in the position in a variable
                prev_key, prev_value = current_table[pos]

                if not isinstance(prev_value, ArrayR):
                    current_table[pos] = (prev_key[:self.level + 1], ArrayR(self.TABLE_SIZE))
                    self.level += 1
                    # Hash the previous key to get the position in the newly created hash table
                    prev_key_pos = self.hash(prev_key)

                    # Move on to the hash table in the next level
                    current_table = current_table[pos][1]

                    # Insert the previous (key, value) pair in the hash table of next level
                    current_table[prev_key_pos] = (prev_key, prev_value)

                else:
                    # Update and move on to the hash table in the next level
                    self.level += 1
                    current_table = current_table[pos][1]

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # Get the positions of the key
        pos_list = self.get_location(key)
        current_table = self.array
        self.key_list.remove(key)

        # Traverse the hash table
        for pos in pos_list:
            # If there is a pointer to another hash table, update the current table
            if isinstance(current_table[pos][1], ArrayR):
                current_table = current_table[pos][1]
            # Else if it reaches the final position of the table, remove the key and value pair from the table
            elif pos == pos_list[-1]:
                current_table[pos] = None
        
        # Update self.count and call the recursive delete method
        self.count -= 1
        self._collapse_table(current_table, pos_list)

    def _collapse_table(self, current_table: ArrayR[tuple[K, V] | None], pos_list: list[int]) -> None:
        """Recursively collapse the hash table to a single entry in the parent table
        until there is a table with multiple pairs or it reaches the top table if there is
        only a single pair within the current table.

        :param current_table: The current hash table
        :type current_table: ArrayR
        :param pos_list: The list of positions to access the key
        :type pos_list: List[int]
        """
        index_list = []

        # iterate through the current table to determine the length of the current table
        for i in range(len(current_table)):
            if current_table[i] is not None:
                index_list.append(i)

        # Base case should be when there are multiple pairs or when it reaches the top table
        if len(index_list) != 1 or len(pos_list) == 0:
            return
        
        # Recursive call to collapse the hash table to a single entry in the parent table
        else:
            # Unpack the (key, value) pair of the remaining item in the hash table
            key, value = current_table[index_list[0]]

            # Reset the pointer to point to the top table
            current_table = self.array

            # If the item left does not have any internal ArrayR, update the (key, value) pair back to previous level position
            if isinstance(value, int):

                # Remove the last level index from the pos list
                pos_list.pop()

                # Iterate through pos_list until it reaches correct table level
                # Update the (key, value) pair at the previous level position
                for i in pos_list:
                    if i == pos_list[-1]:
                        current_table[i] = (key, value)
                    else:
                        current_table = current_table[i][1]

                # Recursively call the method again until it reaches the base case
                self._collapse_table(current_table, pos_list)

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

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        res = []

        # Initialize a pointer to the top table
        current_table = self.array

        # Iterate until it reaches the final position
        while True:
            # Iterate through the table in each level
            for pos in range(len(current_table)):
                # Check if the position is None
                if current_table.array[pos] is not None:
                    # Retrieve the key inserted to compare with the new key
                    if current_table.array[pos][0] in key:
                        res.append(pos)
                        break
                # If it reaches the final position in the table and no key is found, raise KeyError
                if pos == len(current_table) - 1:
                    raise KeyError(key)

            # Check if there is next level of hash table
            if isinstance(current_table[pos][1], ArrayR):
                current_table = current_table[pos][1]
            else:
                return res

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
    ih["lin"] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    ih["jake"] = 7
    ih["linger"] = 8

    del ih["limp"]
    print(ih.get_location("linked"))

    del ih["mine"]
    print(ih.get_location("mining"))

    del ih["mining"]
    del ih["jake"]
    del ih["leg"]
    del ih["linger"]
    del ih["linked"]
    print(ih.get_location("lin"))
    #
    # self.assertEqual(ih["lin"], 1)
    # self.assertEqual(ih.get_location("lin"), [4])
    #
    del ih["lin"]
    #
    ih["lin"] = 10
    print(ih.get_location("lin"))

    # self.assertEqual(ih.get_location("lin"), [4])
    # self.assertEqual(len(ih), 1)
    # Should do nothing
    # self.assertEqual(ih.get_location("linked"), [4, 1, 6, 3])

    # print(ih.get_location("mo"))
    # print(ih['mo'])
    # print(ih.get_location("lin"))
    # print(ih.get_location("linked"))

    # print(ih.get_location("limp"))
    # print(ih.get_location("mine"))
    # print(ih.get_location("mining"))

    # print(ih["lin"])
    # print(ih["leg"])
    # print(ih["jake"])
    # print(ih["linger"])
