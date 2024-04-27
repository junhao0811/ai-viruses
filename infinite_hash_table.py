from __future__ import annotations
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
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        pos_list = self.get_location(key)
        current = self.array
        final_index = pos_list.pop()
        # update the current array
        # Collision occurs >> update
        count = 1
        # iterate through the location list
        for i in pos_list:
            prev_key, prev_value = current[i]      # retrieve the previous collided key
            prev_list = self.get_location(prev_key)

            # if previously haven create an infinite hash table, create now
            if not isinstance(prev_value, InfiniteHashTable):
                current[i] = (prev_key[:count], InfiniteHashTable())       # update the key to the first letter
                current[i][1].level = count     # update the level of hash table
            count += 1
            current = current[i][1].array

            if i == pos_list[-1]:
                current[prev_list[-1]] = (prev_key, prev_value)

        current[final_index] = (key, value)

        # Update the level of the current hash table
        current.level = len(pos_list) + 1

        self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

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
        # create an empty list to store the location
        res = []

        # track current table level
        current = self
        if type(current) != int:
            current.level = 0

        # iterate through the length of the key and slice to calculate the hash value
        while True:
            pos = self.hash(key)
            # print(f"Position for {temp_key}: {pos}")  # Debugging print statement
            res.append(pos)

            if type(current) == int or current.array[pos] is None:  # use for check in set method
                break
            elif current.array[pos][0] == key and type(current.array[pos][1]) == int:      # use in direct retrieving
                break
            else:
                current.level += 1
                current = current.array[pos][1]     # update the current to the next internal table

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
        raise NotImplementedError()

if __name__ == "__main__":
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    print(ih.get_location("lin"))
    print(ih.get_location("leg"))

    ih["mine"] = 3
    ih["linked"] = 4
    print(ih.get_location("mine"))
    print(ih.get_location("lin"))
    print(ih.get_location("linked"))

    #
    #
    # ih["limp"] = 5
    # ih["mining"] = 6
    # print(ih.get_location("limp"))
    # print(ih.get_location("mine"))
    # print(ih.get_location("mining"))
    # # # self.assertEqual(ih.get_location("limp"), [4, 1, 5])
    # # # self.assertEqual(ih.get_location("mine"), [5, 1, 6, 23])
    # # # self.assertEqual(ih.get_location("mining"), [5, 1, 6, 1])
    # # # self.assertEqual(len(ih), 6)
    # ih["jake"] = 7
    # ih["linger"] = 8
    # print(ih.get_location("mine"))
    # print(ih.get_location("lin"))
    # print(ih.get_location("linked"))
    # self.assertEqual(ih.get_location("mine"), [5])
    # self.assertEqual(ih.get_location("lin"), [4, 1, 6, 26])
    # self.assertEqual(ih.get_location("linked"), [4, 1, 6, 3])
    # self.assertEqual(len(ih), 4)
