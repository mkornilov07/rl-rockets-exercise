import sys
sys.path.append("skeleton")
from gui import GUI
from environment import Environment
from rocket import Agent
from state import State

numRounds : int = 1
if len(sys.argv) > 1:
    try:
        numRounds = int(sys.argv[1])
        assert(numRounds > 0)
    except:
        raise Exception(f"Number of rounds should be a positive integer (received {sys.argv[1]})")
useGui : bool = True
if len(sys.argv) > 2 and sys.argv[2] in ("-n", "--no-gui"):
    useGui = False

env : Environment = Environment()
for roundNum in range(1, numRounds+1):
    state : State = env.reset()
    agent : Agent = Agent()
    if useGui:
        gui : GUI = GUI()
        env.connectGui(gui)
    while not env.isGameOver():
        action : int = agent.getAction(state)
        state, reward = env.step(action)
    score : float = env.score()
    print("(Round %d) Max height: %4f" % (roundNum, score))