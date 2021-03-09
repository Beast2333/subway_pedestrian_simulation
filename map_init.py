import numpy as np
import pandas as pd


class ACO:
    def __init__(self):
        self.path_data = np.zeros([9, 9], dtype='int')
        self.path = './map.csv'

    def dump_csv(self):
        np.savetxt(self.path, self.path_data, delimiter=',')
        return 0

    def load_csv(self):
        path_data = np.loadtxt(self.path, delimiter=',')
        return path_data


if __name__ == "__main__":
    ACO_demo = ACO()
    # ACO_demo.dump_csv()
    ACO_demo.path_data = ACO_demo.load_csv()
    print(ACO_demo.path_data)


