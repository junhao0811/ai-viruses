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
        # Check whether key1 is passed in as an argument
        if key1 is None:
            raise KeyError("key1 is empty")

        # Hash key1 to get the position of key1 in the top-level table
        position1 = self.hash1(key1)

        # Traverse each item in our hash table from the position
        for _ in range(self.table_size):
            # If an empty spot is found in the top-level table
            if self.array[position1] is None:
                # Create a new internal hash table if is_insert is true and this is the first pair with key1
                if is_insert:
                    table = LinearProbeTable(self.internal_sizes)

                    # This ensures any internal table uses hash2 for hashing keys
                    table.hash = lambda k, tab=table: self.hash2(k, tab)
                    
                    # Update the top-level table to contain key1 and the internal hash table
                    self.array[position1] = (key1, table)
                    break
                
                # Otherwise raise an error if the key is not found
                raise KeyError(f"{key1} is not found in the top-level table")
                
            # Else if key1 already exists in that spot, break out the from the loop
            elif self.array[position1][0] == key1:
                break

            # Otherwise the position is taken by something else, time to linear probe
            position1 = (position1 + 1) % self.table_size

        # If key2 = None, return the index to access the item in the top-level table
        if key2 is None:
            return position1
            
        # Otherwise get the internal hash table from the top-level table
        table = self.array[position1][1]
        
        # Get the position of key2 in the internal table
        position2 = table._linear_probe(key2, is_insert)

        # Return the index to access the item in the top-level table and the index to access the item in the bottom-level table
        return position1, position2

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        # Iterate through self.array and use yield to produce the keys one by one
        if key is None:
            for k in range(self.table_size):
                if self.array[k] is not None:
                    yield self.array[k][0]

        else:
            position = self._linear_probe(key, None, False)
            sub_table = self.array[position][1]
            for k in range(sub_table.table_size):
                if sub_table[k] is not None:
                    yield sub_table[k][0]

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        # Iterate through the hash table and generate the values one by one
        if key is None:
            for k in range(self.table_size):
                if self.array[k] is not None:
                    yield self.array[k][1]

        else:
            position = self._linear_probe(key, None, False)
            sub_table = self.array[position][1]
            for k in range(sub_table.table_size):
                if sub_table[k] is not None:
                    yield sub_table[k][1]

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        res = []

        # If key = None, return all top-level keys in the hash table
        if key is None:
            # Traverse each item in the top-level table and append all the keys to res
            for x in range(self.table_size):
                if self.array[x] is not None:
                    res.append(self.array[x][0])

        # If key != None, return all low-level keys in the sub-table of top-level key
        else:
            # Get the position of the key in the top-level table
            position = self._linear_probe(key, None, False)

            # Get the internal hash table from the position
            sub_table = self.array[position][1]

            # Get all keys in the internal hash table
            res = sub_table.keys()
            
        return res

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        # If key = None, return all values in all entries in the entire double key hash table (including both the top level and bottom levels)
        res = []
        if key is None:
            for x in range(self.table_size):
                if self.array[x] is not None:
                    sub_table = self.array[x][1]
                    for y in range(sub_table.table_size):
                        if sub_table.array[y] is not None:
                            res.append(sub_table.array[y][1])
        
        # If key != None, restrict to all values in the sub-table of top-level key
        else:
            # Get the position of the key in the top-level table
            position = self._linear_probe(key, None, False)

            # Get the internal hash table from the position
            sub_table = self.array[position][1]

            # Get all values in the internal hash table
            res = sub_table.values()

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
        # Get the position of the key in the top-level table
        position = self._linear_probe(key[0], None, False)

        # Get the internal hash table from the position
        sub_table = self.array[position][1]

        # Check if the key1, key2 pair was the only key1 element in the table
        if len(sub_table) == 1:
            # Remove the element and clear out the entirely of that internal table
            self.array[position] = None
            self.count -= 1
            # Start moving over the cluster
            position = (position + 1) % self.table_size
            while self.array[position] is not None:
                key2, value = self.array[position]
                self.array[position] = None
                # Reinsert
                newpos = self._linear_probe(key2, None, True)
                self.array[newpos] = (key2, value)
                position = (position + 1) % self.table_size

        # Otherwise, delete the (key, value) pair in the internal hash table
        else:
            del sub_table[key[1]] # This time you're cute fr :)

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # Cannot be resized further
            return
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                position = self.hash1(item[0])
                self.array[position] = item

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
        res = ""
        for i, item in enumerate(self.array):
            if item is None:
                res += f"{i}: None\n"
            else:
                res += f"{i}: {item}\n"
        return res
    
if __name__ == "__main__":
    # Test that these are actually iterators,
    # and so changing the underlying data structure changes the next value.
    dt = DoubleKeyTable()
    dt["May", "Jim"] = 1
    dt["Kim", "Tim"] = 2

    key_iterator = dt.iter_keys()
    value_iterator = dt.iter_values()

    key = next(key_iterator)
    print(key) # Either one of ["May", "Kim"]
    value = next(value_iterator) # <data_structures.hash_table.LinearProbeTable object at 0x00000297AEA88A40> not found in [1, 2]
    print(value) # Either one of [1, 2]

    del dt["May", "Jim"]
    del dt["Kim", "Tim"]

    # Retrieving the next value should either raise StopIteration or crash entirely.
    # Note: Deleting from an element being iterated over is bad practice
    # We just want to make sure you aren't returning a list and are doing this
    # with an iterator.
    next(key_iterator) # Should raise BaseException
    next(value_iterator) # Should raise BaseException