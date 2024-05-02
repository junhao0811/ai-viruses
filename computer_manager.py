from __future__ import annotations
from algorithms.mergesort import *
from computer import Computer
from data_structures.hash_table import LinearProbeTable
from double_key_table import DoubleKeyTable
from infinite_hash_table import InfiniteHashTable


class ComputerManager:

    def __init__(self) -> None:
        """
        Initialisation
        """
        self.manager = DoubleKeyTable()

    def add_computer(self, computer: Computer) -> None:
        """
        Add a computer to the manager

        :param computer: The computer to be added to the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when adding the computer to the hash table
        """
        self.manager[(str(computer.get_hacking_difficulty()), computer.get_name())] = computer

    def remove_computer(self, computer: Computer) -> None:
        """
        Remove a computer from the manager

        :param computer: The computer to be removed from the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when removing the computer from the hash table
        """
        del self.manager[computer.get_name()]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """
        Remove the old computer and add the new computer.

        :param old: The computer to be removed from the manager
        :type old: Computer
        :param new: The computer to be added to the manager
        :type new: Computer

        :complexity: O(1) for best/worst case when removing the old computer and adding the new computer to the hash table
        """
        self.remove_computer(old)
        self.add_computer(new)

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """
        Return a list of all computers with this hacking difficulty.

        :param diff: Hacking difficulty of the computers
        :type diff: int
        :return: A list of computers with the given hacking difficulty
        :rtype: list[Computer]

        :complexity: O(1) for best/worst case
        """
        return self.manager.values(str(diff))

    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        Returns a list of lists of all computers, grouped by and sorted by ascending hacking difficulty.

        :return: List of lists of all computers grouped by hacking difficulty
        :rtype: list[list[Computer]]

        :complexity: O(N log (N) + M) for best/worst case where N is the number of computers in the hash table
        """
        res = []

        # Retrieve all the top level keys in the DoubleKeyTable, which is a list of hacking difficulties
        # and sort the list of hacking difficulties by ascending order using mergesort
        diff_lst = mergesort(self.manager.keys())

        # Iterate through the sorted list of hacking difficulties
        for diff in diff_lst:
            # Retrieve all the computer with the hacking difficulty and append it to res
            res.append(self.manager.values(str(diff)))

        return res