import sys
sys.path.append("skeleton")
from environment import Environment
from rocket import Agent

numRounds : int = 1
if len(sys.argv) > 1:
    try:
        numRounds = int(sys.argv[1])
        assert(numRounds > 0)
    except:
        raise Exception(f"Number of rounds should be a positive integer (received {sys.argv[1]})")
for roundNum in range(1, numRounds+1):
    env : Environment = Environment()
    agent : Agent = Agent()
    env.connectAgent(agent)
    while not env.isGameOver():
        env.step()
    score = env.score()
    print(f"(Round {roundNum}) Max height: {score}")