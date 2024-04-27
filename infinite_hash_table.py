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
        # Traverse the infinite depth hash table
        count = 0
        current_table = self.array
        while count <= self.level:
            try:
                position = self.hash(key)
            except:
                raise KeyError("Key doesn't exist")
            else:
                if isinstance(current_table[position][1], int):
                    return current_table[position][0]
                current_table = current_table[position][1]
                count += 1
            
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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