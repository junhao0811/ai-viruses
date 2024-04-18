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

        # Check for key 1
        if key1 is None:
            raise KeyError("Key 1 is empty")
        else:
            position1 = self.hash1(key1)        # hash the first position
            for _ in range(self.table_size):
                if self.array[position1] is None:
                    if is_insert:   # if is_insert is true, create an internal table
                        lower_table = LinearProbeTable(self.internal_sizes)
                        lower_table.hash = lambda k, tab=lower_table: self.hash2(k, tab)
                        self.array[position1] = (key1, lower_table)     # update self.array
                    else:
                        raise KeyError(key1)
                elif self.array[position1][0] == key1:
                    break   # means position1 is already a correct value, we can break the loop
                else:
                    # Taken by something else. Time to linear probe.
                    position1 = (position1 + 1) % self.table_size

        if key2 is None:
            return position1
        elif key2 is not None:
            # access the lower table
            lower_table = self.array[position1][1]

            # hash the position
            position2 = self.hash2(key2, lower_table)

            # lower_table.array[position2] >> accessing the internal array
            # the hash table adt automatically help us to insert the value (refer to hash_table.py)
            for _ in range(self.internal_sizes[0]):
                if lower_table.array[position2] is None:
                    if is_insert:
                        break
                    else:
                        raise KeyError(key2)
                elif lower_table.array[position2][0] == key2:
                    break
                else:
                    # The position is taken by something else. Time to linear probe.
                    position2 = (position2 + 1) % self.internal_sizes[0]
            return position1, position2


        # Else if key2 != None, a tuple containing the Index to access the item in the top-level table and the Index to access the item in the bottom-level table


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
        res = []
        if key is None:
            for x in range(self.table_size):
                if self.array[x] is not None:
                    res.append(self.array[x][0])

        # If key != None, return all low-level keys in the sub-table of top-level key. In the case that the key isn't found, raise KeyError.
        else:
            res = self.iterate_lower_table(key)
        return res

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        # If key = None, return all values in all entries in the entire double key hash table (including both the top level and bottom levels)
        res = []
        position1 = self._linear_probe(key,None, True)

        sub_table = self.array[position1][1]
        print(sub_table[key])
        if key is None:
            for x in range(self.table_size):
                if self.array[x] is not None:
                    print("=================")
                    print(self.array)
                    print(self.array[x])
                    print(self.array[x][0])
                    print(self.array[x][1])
                    print("=================")
                    res.append(self.array[x][0])
                    lower_table = self.array[x][1]
                    if lower_table is not None:
                        self.iterate_lower_table(key)

        # If key != None, restrict to all values in the sub-table of top-level key. In the case that the key isn't found, raise KeyError.

        return res

    def iterate_lower_table(self, key) -> list:
        res = []
        pos = self._linear_probe(key, None, False)
        lower_table = self.array[pos][1]
        for y in range(self.internal_sizes[0]):
            if lower_table.array[y] is not None:
                res.append(lower_table.array[y][0])
        return res


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
        # print(position1,position2)
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
        result = ""
        for i, item in enumerate(self.array):
            if item is None:
                result += f"{i}: None\n"
            else:
                result += f"{i}: {item}\n"
        return result
