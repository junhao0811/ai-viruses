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
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialize the Double Key Table.
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

        :complexity best:  O(hash1(key1) + I) when key2 is None and the first position is empty
        :complexity worst: O([hash1(key1) + M*comp(key1) + I] + [hash2(key2) + N*comp(key2)]) when we've searched the entire table where N is the tablesize when key2 is not None
            I is the complexity of initialising the DoubleKeyTable.
            M is self.table_size
            N is the table size of the internal hash table.
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
        table: LinearProbeTable = self.array[position1][1]
        
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

        :complexity best: O(1) when two scenarios:
                            1. if key is None and there is an element located at the first position in the top level table
                            2. if key is not None and the key is located at the first position in the top level table,
                               and then when a (key, value) pair exists in the first position in the internal hash table.
                               
        :complexity worst: O(N + M + comp(K)) when two scenarios:
                            1. if key is None and there is only an element located at the last position in the top level table
                            2. if key is not None and the (key, value) pair is the only element at the last position in the top level table 
                               and then when a (key,value) pair is the only existing pair in the last position in the internal hash table
                            Where N is the table size of the top-level table
                            Where M is the table size of the internal hash table
                            Where K is the key
        """
        # Iterate through self.array and use yield to produce the keys one by one
        if key is None:
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None:
                    yield self.array[pos][0]

        else:
            # Iterate through the top level table
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None and self.array[pos][0] == key: # O(comp(K))
                    sub_table: LinearProbeTable = self.array[pos][1]
                    # Yield the keys one by one
                    for sub_pos in range(sub_table.table_size): # O(M) where M is the table size of the internal hash table
                        if sub_table[sub_pos] is not None:
                            yield sub_table[sub_pos][0]

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        :complexity best: O(1) when two scenarios:
                            1. if key is None and there is an element located at the first position in the top level table
                            2. if key is not None and the key is located at the first position in the top level table,
                               and then when a (key, value) pair exists in the first position in the internal hash table.
                               
        :complexity worst: O(N + M + comp(K)) when two scenarios:
                            1. if key is None and there is only an element located at the last position in the top level table
                            2. if key is not None and the (key, value) pair is the only element at the last position in the top level table 
                               and then when a (key,value) pair is the only existing pair in the last position in the internal hash table
                            Where N is the table size of the tope-level table
                            Where M is the table size of the internal hash table
                            Where K is the key
        """
        # Iterate through the hash table and generate the values one by one
        if key is None:
            for pos in range(self.table_size):  # O(N) where N is self.table_size
                if self.array[pos] is not None: 
                    sub_table = self.array[pos][1]
                    # Get all values in the internal hash table
                    value_list = sub_table.values()  # O(M) where M is the table size of the internal hash table
                    yield value_list[pos] 

        else:
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None and self.array[pos][0] == key: # O(comp(K))
                    sub_table: LinearProbeTable = self.array[pos][1]
                    # Yield the values one by one
                    for sub_pos in range(sub_table.table_size): # O(M) where M is the table size of the internal hash table
                        if sub_table[sub_pos] is not None:
                            yield sub_table[sub_pos][1]

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        :complexity best: O(N) when key is None
        :complexity worst: O(N * M) when key is not None
            Where N is the table size of the top-level table
            Where M is the table size of the internal hash table
        """
        res = []

        # If key = None, return all top-level keys in the hash table
        if key is None:
            # Traverse each item in the top-level table and append all the keys to res
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None:
                    res.append(self.array[pos][0])
            return res

        # If key != None, return all low-level keys in the sub-table of top-level key
        else:
            # Iterate through the top level table
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None and self.array[pos][0] == key:
                    # Get the sub table and return its values
                    sub_table: LinearProbeTable = self.array[pos][1]
                    return sub_table.keys() # O(M) where M is the table size of the internal hash table
            return res

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        
        :complexity best: O(N * [M + comp(K)]) when key is not None
        :complexity worst: O(N * [M + E]) when key is None
            Where N is the table size of the top-level table
            Where M is the table size of the internal hash table
            Where E is the complexity of extend() method 
        """
        res = []

        # If key = None, return all values in all entries in the entire double key hash table (including both the top level and bottom levels)
        if key is None:
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None:
                    sub_table: LinearProbeTable = self.array[pos][1]
                    # Get all values in the internal hash table
                    res.extend(sub_table.values()) # O(M + E) where M is the table size of the internal hash table
            return res

        # If key != None, restrict to all values in the sub-table of top-level key
        else:
            # Iterate through the top level table
            for pos in range(self.table_size): # O(N) where N is self.table_size
                if self.array[pos] is not None and self.array[pos][0] == key: # O(comp(K))
                    # Get the sub table and return its values
                    sub_table: LinearProbeTable = self.array[pos][1]
                    return sub_table.values() # O(M) where M is the table size of the internal hash table
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

        :complexity best: O(L) when the spot after probing one position downwards is empty after deleting a (key, value) pair from the top level table.
            Where L is the complexity of _linear_probe

        :complexity worst: See LinearProbeTable.__delitem__, this is only when key2 is not the only element in the internal table if key1

        :raises KeyError: when the key doesn't exist.
        """
        # Get the position of the key in the top-level table
        position = self._linear_probe(key[0], None, False) # O(_linear_probe)

        # Get the internal hash table from the position
        sub_table = self.array[position][1]

        # Check if key2 is the only element in the internal table of key1
        if len(sub_table) == 1:
            # Remove the element and clear out the entirely of that internal table
            self.array[position] = None
            self.count -= 1
            # Start moving over the cluster
            position = (position + 1) % self.table_size
            while self.array[position] is not None: # O(N)
                key2, value = self.array[position]
                self.array[position] = None
                # Reinsert
                newpos = self._linear_probe(key2, None, True) # O(_linear_probe)
                self.array[newpos] = (key2, value)
                position = (position + 1) % self.table_size

        # Otherwise, delete the (key, value) pair in the internal hash table
        else:
            del sub_table[key[1]] # See LinearProbeTable.__delitem__

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity: O(A + N*hash1(K)) for best/worst case
            Where A is the complexity of initialising ArrayR with size self.TABLE_SIZES[self.size_index]
            Where N is len(self)
            Where K is key1
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
        pass
    
if __name__ == "__main__":
    class TestingDKT(DoubleKeyTable):
        def hash1(self, k):
            return ord(k[0]) % self.table_size
        def hash2(self, k, sub_table):
            return ord(k[-1]) % sub_table.table_size

    dt = TestingDKT(sizes=[3, 5], internal_sizes=[3, 5])

    dt["Tim", "Bob"] = 1
    # No resizing yet.
    print(dt.table_size) # 3
    print(dt._linear_probe("Tim", "Bob", False)) # (0, 2)
    dt["Tim", "Jen"] = 2

    # Internal resize.
    print(dt.table_size) # 3
    print(dt._linear_probe("Tim", "Bob", False)) # (0, 3)

    # External resize
    dt["Pip", "Bob"] = 4
    print(dt.table_size) # 5
    print(dt._linear_probe("Tim", "Bob", False)) # (4, 3)
    print(dt._linear_probe("Pip", "Bob", False)) # (0, 2)