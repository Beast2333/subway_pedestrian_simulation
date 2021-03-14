import numpy as np
import pandas as pd


class MapInit:
    def __init__(self):
        self.path_data = np.zeros([2, 7, 7], dtype='int')
        self.path = './data.npy'

    def dump_csv(self, path_data):
        np.save(self.path, path_data)
        return 0

    def load_csv(self):
        path_data = np.load(self.path)
        return path_data


if __name__ == "__main__":
    ACO_demo = MapInit()
    # ACO_demo.dump_csv()
    # ACO_demo.path_data = ACO_demo.load_csv()
    path_data = np.loadtxt('./map.csv', delimiter=',')
    ACO_demo.path_data[0] = path_data
    print(ACO_demo.path_data)
    ACO_demo.dump_csv(ACO_demo.path_data)
    # path_data = np.zeros([2, 9, 9], dtype='int')
    # # print(path_data)
    # path_data[0] = ACO_demo.path_data
    # print(path_data)
    #
    # np.save(file="data.npy", arr=path_data)

