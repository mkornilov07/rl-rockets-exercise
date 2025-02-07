import sys
sys.path.append("skeleton")
from state import State

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
        return 10 if state.fuelLeft > 10 else state.fuelLeft