from __future__ import annotations
from algorithms.mergesort import *
from computer import Computer
from double_key_table import DoubleKeyTable


class ComputerManager:
    """
    Computer Manager.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    def __init__(self) -> None:
        """
        Initialise the Computer Manager.
        """
        self.manager = DoubleKeyTable()

    def add_computer(self, computer: Computer) -> None:
        """
        Adds a computer to the manager

        :param computer: The computer to be added to the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when adding the computer to the hash table
        """
        self.manager[(str(computer.get_hacking_difficulty()), computer.get_name())] = computer

    def remove_computer(self, computer: Computer) -> None:
        """
        Removes a computer from the manager

        :param computer: The computer to be removed from the manager
        :type computer: Computer

        :complexity: O(1) for best/worst case when removing the computer from the hash table
        """
        del self.manager[(str(computer.get_hacking_difficulty()), computer.get_name())]

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
    
if __name__ == "__main__":

    @staticmethod
    def make_set(my_list: list) -> set:
        """
        Since computers are unhashable, add a method to get a set of all computer ids.
        Ensures that we can compare two lists without caring about order.
        """
        return set(id(x) for x in my_list)

    # @number("6.1")
    c1 = Computer("c1", 2, 2, 0.1)
    c2 = Computer("c2", 2, 9, 0.2)
    c3 = Computer("c3", 3, 6, 0.3)
    c4 = Computer("c4", 3, 1, 0.4)
    c5 = Computer("c5", 4, 6, 0.5)
    c6 = Computer("c6", 7, 3, 0.6)
    c7 = Computer("c7", 7, 7, 0.7)
    c8 = Computer("c8", 7, 8, 0.8)
    c9 = Computer("c9", 7, 6, 0.9)
    c10 = Computer("c10", 8, 4, 1.0)

    cm = ComputerManager()
    cm.add_computer(c1)
    cm.add_computer(c2)
    cm.add_computer(c3)
    cm.add_computer(c6)
    cm.add_computer(c7)

    print(make_set(cm.computers_with_difficulty(3))) # make_set([c3])
    print(make_set(cm.computers_with_difficulty(4))) # make_set([])
    print(make_set(cm.computers_with_difficulty(7))) # make_set([c6, c7])

    cm.add_computer(c4)
    cm.add_computer(c5)
    cm.add_computer(c8)
    cm.add_computer(c9)

    res = cm.group_by_difficulty()
    print(len(res)) # 4
    print(make_set(res[0])) # make_set([c1, c2])
    print(make_set(res[1])) # make_set([c3, c4])
    print(make_set(res[2])) # make_set([c5])
    print(make_set(res[3])) # make_set([c6, c7, c8, c9])

    cm.add_computer(c10)
    cm.remove_computer(c5)

    res = cm.group_by_difficulty()
    print(len(res), 4)

    print(make_set(res[3])) # make_set([c10])

    # @number("6.2")
    c1 = Computer("c1", 4, 4, 0.1)
    c2 = Computer("c2", 3, 2, 0.2)
    c3 = Computer("c3", 3, 5, 0.3)
    c4 = Computer("c4", 4, 3, 0.4)
    c5 = Computer("c5", 3, 4, 0.5)
    c6 = Computer("c6", 5, 3, 0.6)
    c7 = Computer("c7", 5, 3, 0.7)
    c8 = Computer("c8", 6, 4, 0.8)
    c9 = Computer("c9", 6, 4, 0.9)
    c10 = Computer("c10", 4, 5, 1.0)

    cm = ComputerManager()
    cm.add_computer(c1)
    cm.add_computer(c2)
    cm.add_computer(c3)
    cm.add_computer(c6)
    cm.add_computer(c7)

    print(make_set(cm.computers_with_difficulty(3))) # make_set([c2, c3])
    print(make_set(cm.computers_with_difficulty(4))) # make_set([c1])
    print(make_set(cm.computers_with_difficulty(7))) # make_set([])

    cm.add_computer(c4)
    cm.add_computer(c5)
    cm.add_computer(c8)
    cm.add_computer(c9)

    res = cm.group_by_difficulty()
    print(len(res)) # 4

    print(make_set(res[0])) # make_set([c2, c3, c5])
    print(make_set(res[1])) # make_set([c1, c4])
    print(make_set(res[2])) # make_set([c6, c7])
    print(make_set(res[3])) # make_set([c8, c9])

    cm.add_computer(c10)
    cm.remove_computer(c9)

    res = cm.group_by_difficulty()
    print(len(res)) # 4

    print(make_set(res[3])) # make_set([c8])