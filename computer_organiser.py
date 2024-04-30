from __future__ import annotations
from algorithms.binary_search import *
from algorithms.mergesort import *
from computer import Computer


class ComputerOrganiser:

    def __init__(self) -> None:
        self.computers = []

    def cur_position(self, computer: Computer) -> int:
        """
        Finds the rank of the provided computer given all computers included so far.
        Raises KeyError if this computer hasn't been added

        Complexity: O(log(N)) where N is the total number of computers included so far.
        """
        if computer not in self.computers:
            raise KeyError(f"Computer {computer} not found in the organiser")
        
        return binary_search(computer)

    def add_computers(self, computers: list[Computer]) -> None:
        """
        Adds a list of computers to the organiser.

        Complexity: O(M log(M) + N) where
            M is the length of the input list, and
            N is the total number of computers included so far.
        """
        # To determine the threat of the virus we are going to rank each potential virus by its hacking difficulty.


        # In cases where the hacking difficulty is the same, you should then order them by their risk factor in ascending order.

        
        # If there is still a tie, you should order them by name lexicographically increasing (you can assume the name is unique)
        # hacking difficulty > risk factor > name lexicographically increasing (unique name)