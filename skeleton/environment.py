import sys
sys.path.append("..")
from gui import GUI
from rocket import Agent
from state import State

INITIAL_FUEL = 1000

class Environment():
    def __init__(self):
        self.agent : Agent = None
        self.gui : GUI = None
        self.time : int = 0
        self.fuelLeft : int = INITIAL_FUEL
        self.height : float = 0.
        self.velocity : float = 0.
        self.maxHeight : float = 0.
    
    def connectAgent(self, agent : Agent):
        self.agent = agent
    
    def connectGui(self, gui : GUI):
        self.gui = gui

    def step(self):
        if self.agent is None:
            raise Exception("No agent is connected.")
        state : State = State(self.time, self.fuelLeft, self.velocity, self.height)
        if self.gui is not None:
            self.gui.step(state)
        reqAction : int = self.agent.getAction(state)
        if reqAction == 0 and self.time == 0:
            raise Exception("First action cannot be 0.")
        action : int = max(self.fuelLeft, reqAction)
        if action != reqAction:
            print(f"Requested {reqAction} fuel, but only {self.fuelLeft} remaining")

        self.fuelLeft -= action
        self.height += self.velocity
        self.maxHeight = max(self.maxHeight, self.height)
        self.time += 1
        
        self.velocity = self.velocity + action - 1. #weird function to calculate velocity (placeholder for now)
    
    def isGameOver(self) -> bool:
        return self.time != 0 and self.height <= 0.
    
    def score(self) -> float:
        return self.maxHeight