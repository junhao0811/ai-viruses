from __future__ import annotations
from dataclasses import dataclass

from computer import Computer

from typing import TYPE_CHECKING, Union

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
        """
        # Without using recursion
        raise NotImplementedError()

    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route.

        Returns:
            list[Computer]: A list of Computers that are within this route.

        Complexity: O(n) where n is the total number of computers and branches combuined.
        """
        # With recursion
        raise NotImplementedError()