import sys
sys.path.append("..")
from gui import GUI
from rocket import Agent
from state import State
import random, math

MAX_NUM_ROUNDS = 2000
INITIAL_FUEL = 1000
GRAVITY = 20
WIND_RESISTANCE = 12

class Environment():
    def __init__(self, logging=True):
        self.logging = logging
        self.time = 0
        self.fuelLeft = INITIAL_FUEL
        self.height = 0.0
        self.velocity = 0.0
        self.maxHeight = 0.0
        self.prevHeight = 0.0
        self.wind = random.uniform(-WIND_RESISTANCE, WIND_RESISTANCE)
        self.gravity = random.uniform(-GRAVITY, GRAVITY)
        if self.logging:
            self.f = open("log.txt", "w")
            self.f.write("Time,Height,Fuel\n")

    def reset(self):
        if self.logging:
            self.f.close()
            self.f = open("log.txt", "w")
            self.f.write("Time,Height,Fuel\n")
        self.__init__()
        return State(self.time, self.fuelLeft, self.wind, self.gravity)

    def step(self, reqAction: int):
        if self.logging:
            self.f.write(f"{self.time},{self.height},{self.fuelLeft}\n")

        action = min(self.fuelLeft, int(reqAction))
        self.fuelLeft -= action
        self.velocity = self.calculateVelocity(action)
        self.height = max(0.0, self.height + self.velocity)

        reward = max(0, self.height - self.prevHeight)

        self.maxHeight = max(self.maxHeight, self.height)
        self.prevHeight = self.height
        self.time += 1

        self.prevAction = action
        self.wind = random.uniform(-WIND_RESISTANCE, WIND_RESISTANCE)
        self.gravity = random.uniform(-GRAVITY, GRAVITY)
        state = State(self.time, self.fuelLeft, self.wind, self.gravity)
        isTerminalState = (self.fuelLeft == 0 and self.height <= 0) or (self.time >= MAX_NUM_ROUNDS)

        return state, reward, isTerminalState

    def calculateVelocity(self, action: int) -> float:
        return ((self.velocity + action ** 0.66) * 0.9 - (self.wind * action + self.gravity) % 4. - math.cos(math.exp(self.gravity * self.wind + random.random()) + action) * 4 / (1000 + self.fuelLeft) ** 1.2
                - ((abs(self.wind) ** 1.12 * self.fuelLeft +action ** 1.6 + 2.*random.random()) % 10.5) % 6.3 + action ** 1.2 / (2.5 + action ** 0.7) + action ** 0.2 * math.sin(self.wind * action * self.gravity * self.fuelLeft + 0.2 * random.random()))

    def score(self) -> float:
        return self.maxHeight