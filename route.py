from __future__ import annotations
from dataclasses import dataclass
from branch_decision import BranchDecision
from computer import Computer
from data_structures.linked_stack import LinkedStack
from typing import TYPE_CHECKING, Union
from virus import *

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route.

        Returns:
            RouteStore: A RouteStore object which is the result of removing the branch.
        """
        return self.following.store

@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.

        Returns:
            RouteStore: A RouteStore object which is the result of removing the computer.
        """
        return self.following.store

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding a computer in series before the current one.

        Args:
            computer (Computer): A new computer object to be added.

        Returns:
            RouteStore: A RouteSeries object with the new computer added before the current computer.
        """
        return RouteSeries(computer, Route(self))

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.

        Args:
            computer (Computer): A new computer object to be added.

        Returns:
            RouteStore: A RouteSeries object with the new computer added after the current computer.
        """
        return RouteSeries(self.computer, Route(RouteSeries(computer, self.following)))
    
    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.

        Returns:
            RouteStore: A RouteSplit object with an empty branch in between current computer and following route.
        """
        return RouteSplit(Route(None), Route(None), Route(self))

    def add_empty_branch_after(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.

        Returns:
            RouteStore: A RouteSeries object with an empty branch in between current computer and following route.
        """
        return RouteSeries(self.computer, Route(RouteSplit(Route(None), Route(None), self.following)))


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:
    """
    A route is a series of computers and branches.
    """

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.

        Args:
            computer (Computer): A new computer object to be added.

        Returns:
            Route: A new route with the a new computer added before.
        """
        return Route(RouteSeries(computer, self))

    def add_empty_branch_before(self) -> Route:
        """Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.

        Returns:
            Route: A new route with the empty branch added.
        """
        return Route(RouteSplit(Route(None), Route(None), self))

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type.

        Args:
            virus_type (VirusType): The virus type to follow the path with.

        Complexity: O(n) for best/worst case where n is the number of paths in the route.
        """
        
        # Without using recursion
        next_route = LinkedStack()
        current = self.store
        reaches_the_end = False

        while not reaches_the_end:
            if isinstance(current, RouteSplit):
                decision = virus_type.select_branch(current.top, current.bottom)

                next_route.push(current.following.store)
                if decision == BranchDecision.TOP:
                    current = current.top.store   # keep track the split node for the following
                elif decision == BranchDecision.BOTTOM:
                    current = current.bottom.store

                elif decision == BranchDecision.STOP:
                    reaches_the_end = True

            elif isinstance(current, RouteSeries):
                virus_type.add_computer(current.computer)

                if current is not None:
                #if isinstance(current.following.store, RouteSeries) or isinstance(current.following.store, RouteSplit):
                    current = current.following.store
                else:
                    if not next_route.is_empty():
                        current = next_route.pop()
                    else:
                        current = None

            elif current is None:
                # detect whether there is still next route
                if not next_route.is_empty():
                    current = next_route.pop()
                else:
                    reaches_the_end = True

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route.

        Returns:
            list[Computer]: A list of Computers that are within this route.

        Complexity: O(n) for best/worst case where n is the total number of computers and branches combined.
        """
        current = self
        computers = []

        # Base case
        if current.store is None:
            return computers
        
        # Recursive case when current.store is a RouteSeries object
        elif isinstance(current.store, RouteSeries):
            if current.store.computer is not None:
                computers.append(current.store.computer)
            if current.store.following is not None:
                computers.extend(current.store.following.add_all_computers())
                
        # Recursive case when current.store is a RouteSplit object
        else:
            if current.store.top is not None:
                computers.extend(current.store.top.add_all_computers())
            if current.store.bottom is not None:
                computers.extend(current.store.bottom.add_all_computers())

        return computers
    
if __name__ == "__main__":
    top_top = Computer("top-top", 5, 3, 0.1)
    top_bot = Computer("top-bot", 3, 5, 0.2)
    top_mid = Computer("top-mid", 4, 7, 0.3)
    bot_one = Computer("bot-one", 2, 5, 0.4)
    bot_two = Computer("bot-two", 0, 0, 0.5)
    final = Computer("final", 4, 4, 0.6)
    route = Route(RouteSplit(
        Route(RouteSplit(
            Route(RouteSeries(top_top, Route(None))),
            Route(RouteSeries(top_bot, Route(None))),
            Route(RouteSeries(top_mid, Route(None))),
        )),
        Route(RouteSeries(bot_one, Route(RouteSplit(
            Route(RouteSeries(bot_two, Route(None))),
            Route(None),
            Route(None),
        )))),
        Route(RouteSeries(final, Route(None)))
    ))
    fv = FancyVirus()
    FancyVirus.CALC_STR = "7 3 + 8 - 2 *"
    route.follow_path(fv)