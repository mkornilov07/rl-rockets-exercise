import sys
sys.path.append("..")
from gui import GUI
from rocket import Agent
from state import State

INITIAL_FUEL = 1000

class Environment():
    def __init__(self):
        self.gui : GUI = None
        self.time : int = 0
        self.fuelLeft : int = INITIAL_FUEL
        self.height : float = 0.
        self.velocity : float = 0.
        self.maxHeight : float = 0.
    
    def connectGui(self, gui : GUI):
        self.gui = gui

    def reset(self):
        self.time = 0
        self.fuelLeft = INITIAL_FUEL
        self.height = 0.
        self.velocity = 0.
        self.maxHeight = 0.
        state : State = State(self.time, self.fuelLeft, self.velocity, self.height)
        return state

    def step(self, reqAction : int) -> tuple[State, int]:
        if reqAction == 0 and self.time == 0:
            raise Exception("First action cannot be 0.")
        action : int = max(self.fuelLeft, reqAction)
        if action != reqAction:
            print(f"Requested {reqAction} fuel, but only {self.fuelLeft} remaining")
        self.fuelLeft -= action # consume fuel
        self.velocity = self.velocity + action - 1. #weird function to calculate velocity (placeholder for now)
        self.height += self.velocity # change height
        self.maxHeight = max(self.maxHeight, self.height) # update max height
        self.time += 1
        reward : float = max(0., self.height - self.maxHeight) # change in max height
        state : State = State(self.time, self.fuelLeft, self.velocity, self.height)
        if self.gui is not None:
            self.gui.step(state)
        return state, reward
    def isGameOver(self) -> bool:
        return self.time != 0 and self.height <= 0.
    
    def score(self) -> float:
        return self.maxHeight