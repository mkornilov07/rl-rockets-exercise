# Visualize the last run

import pandas as pd
import matplotlib.pyplot as plt
if __name__ == "__main__":
    try:
        data = pd.read_csv("log.txt", index_col = "Time")
    except FileNotFoundError:
        raise Exception("Please run run.py to generate log file.")
    data.plot(secondary_y="Fuel")
    plt.show()
