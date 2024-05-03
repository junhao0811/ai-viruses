from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float

    def get_name(self) -> str:
        """
        Returns the name of the computer.

        Complexity: O(1) for best/worst case when getting the name of the computer.
        """
        return self.name
    
    def get_hacking_difficulty(self) -> int:
        """ Returns the hacking difficulty of the computer.

        Complexity: O(1) for best/worst case when getting the hacking difficulty of the computer.
        """
        return self.hacking_difficulty
    
    def get_risk_factor(self) -> float:
        """ Returns the risk factor of the computer.

        Complexity: O(1) for best/worst case when getting the risk factor of the computer.
        """
        return self.risk_factor
    
    def __gt__(self, other: Computer) -> bool:
        """ Returns True if this computer is greater than the other computer, False otherwise.
        
        Complexity: O(1) for best/worst case when comparing the attributes of two computers.
        """
        if not isinstance(other, Computer):
            return NotImplemented
        return (self.get_hacking_difficulty(), self.get_risk_factor(), self.get_name()) > (other.get_hacking_difficulty(), other.get_risk_factor(), other.get_name())

    def __lt__(self, other: Computer) -> bool:
        """ Returns True if this computer is less than the other computer, False otherwise.
        
        Complexity: O(1) for best/worst case when comparing the attributes of two computers.
        """
        if not isinstance(other, Computer):
            return NotImplemented
        return (self.get_hacking_difficulty(), self.get_risk_factor(), self.get_name()) < (other.get_hacking_difficulty(), other.get_risk_factor(), other.get_name())

    def __eq__(self, other: Computer) -> bool:
        """ Returns True if this computer is equal to the other computer, False otherwise.
        
        Complexity: O(1) for best/worst case when comparing the attributes of two computers.
        """
        if not isinstance(other, Computer):
            return NotImplemented
        return (self.get_hacking_difficulty(), self.get_risk_factor(), self.get_name()) == (other.get_hacking_difficulty(), other.get_risk_factor(), other.get_name())