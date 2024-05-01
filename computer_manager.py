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
        self.computers = LinearProbeTable()

    def add_computer(self, computer: Computer) -> None:
        """
        Add a computer to the manager

        :param computer: The computer to be added to the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when adding the computer to the hash table
        """
        self.computers[computer.get_name()] = computer

    def remove_computer(self, computer: Computer) -> None:
        """
        Remove a computer from the manager

        :param computer: The computer to be removed from the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when removing the computer from the hash table
        """
        del self.computers[computer.get_name()]

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

        :complexity: O(N) for best/worst case where N is the number of computers in the hash table
        """
        # Retrieve all the computers in the hash table and store it in a list
        computers = self.computers.values()

        res = []
        for computer in computers:
            if computer.get_hacking_difficulty() == diff:
                res.append(computer)
        return res

    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        Returns a list of lists of all computers, grouped by and sorted by ascending hacking difficulty.

        :return: List of lists of all computers grouped by hacking difficulty
        :rtype: list[list[Computer]]

        :complexity: O(N log (N) + M) for best/worst case where N is the number of computers in the hash table
        """
        # Retrieve all the computers in the hash table and store it in a list
        computers = self.computers.values()

        # Sort the list of computers by ascending hacking difficulty
        computers = mergesort(computers, key=lambda computer: computer.get_hacking_difficulty())

        # Initialise the result list and the current list
        res = []
        cur = []

        # Iterate through the sorted list of computers
        for computer in computers:

            # If the current list is empty or the hacking difficulty is the same as the last computer then add the computer to the current list
            if len(cur) == 0 or computer.get_hacking_difficulty() == cur[-1].get_hacking_difficulty():
                cur.append(computer)

            # Otherwise add the current list to the result list and create a new current list with the current computer
            else:
                res.append(cur)
                cur = [computer]

        # Add the last current list to the result list
        res.append(cur)

        # Return the result list
        return res