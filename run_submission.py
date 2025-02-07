from environment import Environment
import gym
import numpy as np
import sys
import importlib.util
import os
from state import State
from gui import GUI
# Loading agent
# Normally they should be in the /submission folder, we should upload to kaggle and check where submissions go
submission_path = "./submission/agent.py"
spec = importlib.util.spec_from_file_location("agent", submission_path)
agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_module)
if not hasattr(agent_module, "Agent"):
    raise ValueError("Submission must contain a class named 'Agent'.")



agent = agent_module.Agent()

# We can say that when users train a model like DQN or PPO, they can make the model file itself a field in their class
model_path = "./submission/mode.zip"
if os.path.exists(model_path):
    try:
        agent.model = agent_module.PPO.load(model_path)
    except Exception as e:
        raise ValueError(f"Could not load model: {e}")
    

# Grabbed from run.py
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
    if useGui:
        gui : GUI = GUI()
        env.connectGui(gui)
    while not env.isGameOver():
        action : int = agent.getAction(state)
        state, reward = env.step(action)
    score : float = env.score()
    print("(Round %d) Max height: %4f" % (roundNum, score))