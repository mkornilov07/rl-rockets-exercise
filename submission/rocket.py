import sys
from typing import NamedTuple
class State(NamedTuple):
    time : int
    fuelLeft : int
    velocity : float
    height : float
# sys.path.append("skeleton")
# from state import State

class Agent:
    def __init__(self):
        '''
        Define any local variables here
        '''
        pass
    def getAction(self, state : State) -> int:
        '''
        Return the amount of fuel to burn
        '''
        return 1 if state.fuelLeft > 990 else state.fuelleft