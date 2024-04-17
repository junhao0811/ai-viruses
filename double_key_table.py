from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialize the Double Key Table.

        :param sizes: The size of the top-level table, defaults to None
        :type sizes: list | None, optional
        :param internal_sizes: The size of the bottom-level table, defaults to None
        :type internal_sizes: list | None, optional
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        :param key1: Top-level key
        :type key1: K1
        :param key2: Bottom-level key
        :type key2: K2 | None
        :param is_insert: A boolean variable to determine if we are creating an internal hash table or not.
        :type is_insert: bool

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        :return: If key2 = None, the Index to access the item in the top-level table.
            If key2 != None, a tuple containing the Index to access the item in the top-level table and the Index to access the item in the bottom-level table.
        :rtype: tuple[int, int] | int
        """
        # If key2 = None, the Index to access the item in the top-level table
        if key2 is None:

            # Initial position
            position = self.hash1(key1)

            for _ in range(self.table_size):
                if self.array[position] is None:
                    # Empty spot. Am I upserting or retrieving?
                    if is_insert:
                        return position
                    else:
                        raise KeyError("Key is not found")
                elif self.array[position][0] == key1:
                    return position
                else:
                    # The position is taken by something else. Time to linear probe.
                    position = (position + 1) % self.table_size

            if is_insert:
                raise FullError("Table is full!")
            else:
                raise KeyError("Key is not found")

        # Else if key2 != None, a tuple containing the Index to access the item in the top-level table and the Index to access the item in the bottom-level table
        else:
            
            

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        # The same functionality as above, but this should return an iterator that yields the keys/values one by one rather than searching the entire table at the start.
        # You should NOT get all the keys/values at the start and just iterate through those. That won't be very efficient.
        # Your iterator should only get the next item when it's needed.

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        # The same functionality as above, but this should return an iterator that yields the keys/values one by one rather than searching the entire table at the start.
        # You should NOT get all the keys/values at the start and just iterate through those. That won't be very efficient.
        # Your iterator should only get the next item when it's needed.

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        # If key = None, return all top-level keys in the hash table


        # If key != None, return all low-level keys in the sub-table of top-level key. In the case that the key isn't found, raise KeyError.


    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        # If key = None, return all values in all entries in the entire double key hash table (including both the top level and bottom levels)


        # If key != None, restrict to all values in the sub-table of top-level key. In the case that the key isn't found, raise KeyError.


    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # When deleting, if the key1, key2 pair was the only key1 element in the table,
        # you should clear out the entirety of that internal table so that a new key1 with the same hash can be inserted in that position. (See test_delete for more info.)

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        # Have both your top-level table and internal tables resize when the load factor of that table increases past 0.5 (See hash_table.py for an example of this logic)
        # These resizes should occur independently (One internal table may be a different size to another, and the top level table should resize when the number of internal tables exceeds 0.5 irrespective of the resizing of the internal tables)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()