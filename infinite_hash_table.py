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
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        current_table = self.array

        # reset the level of the hash table
        self.level = 0
        # iterate through the infinite depth hash table
        while True:

            # hash the key to get the position
            position = self.hash(key)

            # raise KeyError if there is no element in the position
            if current_table[position] is None:
                raise KeyError(key)

            # check if there is a value in the tuple
            elif not isinstance(current_table[position][1], ArrayR):
                return current_table[position][1]

            # update the current table and move to the next level
            current_table = current_table[position][1]
            self.level += 1

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        # Traverse the infinite depth hash table
        current_table = self.array
        # reset the level
        self.level = 0
        while True:
            # Hash the key to get the position
            position = self.hash(key)

            # If the position is empty, insert the new (key, value) pair in our hash table
            if current_table[position] is None:
                current_table[position] = (key, value)
                self.count += 1
                break

            # Store what was previously in the position in a variable
            else:
                prev_key, prev_value = current_table[position]
                if not isinstance(prev_value, ArrayR):
                    current_table[position] = (prev_key[:self.level + 1], ArrayR(self.TABLE_SIZE))
                    self.level += 1
                    # Hash the previous key to get the position in the newly created hash table
                    prev_key_position = self.hash(prev_key)

                    # Move to the next level hash table
                    current_table = current_table[position][1]

                    # insert the previous (key, value) pair in the next level hash table
                    current_table[prev_key_position] = (prev_key, prev_value)
                else:
                    # update and move to the next level hash table
                    current_table = current_table[position][1]
                    self.level += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # get the position of the key
        pos_list = self.get_location(key)
        current_table = self.array

        # traverse the hash table to update the current table
        for i in pos_list:
            # if there is an inner hash table, update the current table
            if isinstance(current_table[i][1], ArrayR):
                current_table = current_table[i][1].array
            # if it reaches the final position of the table, remove the key and value
            elif i == pos_list[-1]:
                current_table[i] = None
        self.count -= 1
        self._del_recursion(current_table, pos_list)

    def _del_recursion(self, current_table, pos_list) -> None:
        index_list = []

        # iterate through the current table to determine the length of the current table
        for i in range(len(current_table)):
            if current_table[i] is not None:
                index_list.append(i)

        # updating the hash table from back to the front
        # base case: if there is more than 1 item in the index list or it reaches the first level hash table
        if len(index_list) != 1 or len(pos_list) == 0:
            return
        else:
            # unpacked the key value of the left item in the table
            key, value = current_table[index_list[0]]

            # update the current table back to first level table
            current_table = self.array

            # if the item left does not have any internal ArrayR, update the (key,value) back to previous level position
            if isinstance(value, int):

                # remove the last level index from the pos list
                pos_list.pop()

                # iterate through position list until it reaches correct table level
                # update the key,value at the previous level position
                for i in pos_list:
                    if i == pos_list[-1]:
                        current_table[i] = (key, value)
                    else:
                        current_table = current_table[i][1].array

                # call the method again until it reaches the base case
                self._del_recursion(current_table, pos_list)

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
        # traverse through the list
        res = []
        current = self.array

        # iterate until it reaches the final position
        while True:
            # iterate through the table in each level
            for i in range(len(current)):
                # check if the position is none
                if current[i] is not None:
                    # retrieve the key inserted to compare with the new key
                    if current[i][0] in key:
                        res.append(i)
                        break
                # if it reaches the final position in the table and no key is found, raise KeyError
                if i == len(current) - 1:
                    raise KeyError(key)

            # check if there is next level of hash table
            if isinstance(current[i][1], ArrayR):
                current = current[i][1]
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
        raise NotImplementedError()


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
