from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack


class VirusType(ABC):
    """
    A VirusType is a type of virus that can be transmitted through a computer network.
    """

    def __init__(self) -> None:
        """
        Initializes the VirusType object with an empty list of computers that the virus has been transmitted through.

        Complexity: O(1) for best/worst case scenarios.
        """
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        """Allows a virus to note that computer they've just being transmitted through by

        Args:
            computer (Computer): The computer that the virus has just been transmitted through

        Complexity: O(1) for best/worst case scenarios.
        """
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """Given two Routes as input, decides which of them they will take by returning the Enum BranchDecision.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(1) for best/worst case scenarios.
        """
        pass


class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """Given two Routes as input, decides which of them they will take by returning the Enum BranchDecision.
        In this case, TopVirus always selects the top branch.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(1) for best/worst case scenarios.
        """
        # Always select the top branch
        return BranchDecision.TOP


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """Given two Routes as input, decides which of them they will take by returning the Enum BranchDecision.
        In this case, BottomVirus always selects the bottom branch.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(1) for best/worst case scenarios.
        """
        # Always select the bottom branch
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(1) for best/worst case scenarios.
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and likes to choose the path with the lowest risk factor.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(1) for best/worst case scenarios.
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        # If both branches are RouteSeries, it should continue with some additional comparisons
        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            # If it sees any computer with a risk factor of 0.0, it should take that path
            if top_comp.risk_factor == 0.0:
                return BranchDecision.TOP
            elif bot_comp.risk_factor == 0.0:
                return BranchDecision.BOTTOM
            
            # If there are multiple computers with a risk_factor of 0.0, it should take the path with the lowest hacking difficulty
            if top_comp.risk_factor == 0.0 and bot_comp.risk_factor == 0.0:
                if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                    return BranchDecision.TOP
                elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                    return BranchDecision.BOTTOM
                # Continue to the next comparisons if there is still a tie

            # Take the highest value between the hacking_difficulty and the half of the hacked_value then divide it by the risk factor
            top_path_value = max(top_comp.hacking_difficulty, top_comp.hacked_value / 2) / top_comp.risk_factor
            bot_path_value = max(bot_comp.hacking_difficulty, bot_comp.hacked_value / 2) / bot_comp.risk_factor
            
            # Compare the two paths and take the path with the higher value
            if top_path_value > bot_path_value:
                return BranchDecision.TOP
            elif top_path_value < bot_path_value:
                return BranchDecision.BOTTOM
            
            # IF there is a tie, take the path with the lowest risk factor
            if top_comp.risk_factor < bot_comp.risk_factor:
                return BranchDecision.TOP
            elif top_comp.risk_factor > bot_comp.risk_factor:
                return BranchDecision.BOTTOM
            # Stop if there is still a tie
            return BranchDecision.STOP

        # IF only one has a RouteSeries and the other is a RouteSplit, pick the RouteSplit
        if top_route:
            return BranchDecision.BOTTOM
        
        # In all other cases default to the Top path
        return BranchDecision.TOP


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """This virus has a fancy-pants and likes to overcomplicate its approach.

        Args:
            top_branch (Route): The top branch of the route
            bottom_branch (Route): The bottom branch of the route

        Returns:
            BranchDecision: A BranchDecision enum value

        Complexity: O(n) for best/worst case scenarios where n is the number of items in self.CALC_STR.
        """
        # Calculate a threshold by evaluating self.CALC_STR using reverse polish notation
        # (e.g. - "7 3 + 8 - 2 * 2 /" this string should result in the value 2)
        stack = LinkedStack()
        for item in self.CALC_STR.split():
            if type(item) == int:
                stack.push(item)
            else:
                y = stack.pop()
                x = stack.pop()
                match item:
                    case '+':
                        res = x + y
                    case '-':
                        res = x - y
                    case '*':
                        res = x * y
                    case '/':
                        res = x // y
                stack.push(res)
        threshold = stack.pop()
                
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        # If both top and bottom have computers
        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            # If top hacked_value < threshold, take top
            if top_comp.hacked_value < threshold:
                return BranchDecision.TOP
            # If bot hacked_value < threshold, take bottom
            elif bot_comp.hacked_value < threshold:
                return BranchDecision.BOTTOM
            # If neither, then stop
            return BranchDecision.STOP
        
        # If only one has a RouteSeries and the other a RouteSplit, pick the RouteSplit
        if top_route:
            return BranchDecision.BOTTOM
        
        # In all other cases default to the Top path
        return BranchDecision.TOP