import sys
sys.path.append("..")
from gui import GUI
from rocket import Agent
from state import State
import random, math

INITIAL_FUEL = 1000

class Environment():
    def __init__(self, logging = True):
        self.logging : bool = logging
        self.time : int = 0
        self.fuelLeft : int = INITIAL_FUEL
        self.height : float = 0.
        self.velocity : float = 0.
        self.maxHeight : float = 0.
        if self.logging:
            self.f = open("log.txt", "w")

    def reset(self):
        if self.logging:
            self.f.close()
            self.f = open("log.txt", "w")
            self.f.write("Time,Height,Fuel\n")
        self.time = 0
        self.fuelLeft = INITIAL_FUEL
        self.height = 0.
        self.velocity = 0.
        self.maxHeight = 0.
        state : State = State(self.time, self.fuelLeft, self.velocity, self.height)
        return state

    def step(self, reqAction : int) -> tuple[State, int]:
        if self.logging:
            self.f.write(f"{self.time},{self.height},{self.fuelLeft}\n")
        
        action : int = min(self.fuelLeft, reqAction)
        if action != reqAction:
            print(f"Requested {reqAction} fuel, but only {self.fuelLeft} remaining")
        self.fuelLeft -= action # consume fuel
        self.velocity = self.calculateVelocity(action) #weird function to calculate velocity (placeholder for now)
        self.height += self.velocity # change height
        self.maxHeight = max(self.maxHeight, self.height) # update max height
        self.time += 1
        reward : float = max(0., self.height - self.maxHeight) # change in max height
        state : State = State(self.time, self.fuelLeft, self.velocity, self.height)

        isTerminalState : bool = self.fuelLeft < INITIAL_FUEL and self.height <= 0

        return state, reward, isTerminalState
    
    def calculateVelocity(self, action : int) -> float:
        return ((0.95 * self.velocity - 1 + math.log(random.random() * 5 * action + 0.2) + 0.1 * action ** 0.7) / (1 + self.height / 500) +
            + int(action ** 1.4 / (self.height + 1) - random.random() * action ** 0.3) - 0.0005 * self.fuelLeft)


    def score(self) -> float:
        return self.maxHeight