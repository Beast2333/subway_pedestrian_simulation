import map_init as mp
import ant as at
import numpy as py


class AOC(object):
    def __init__(self):
        # 实例化
        self.map = mp.MapInit()
        self.ant = at.Ant()

        self.path = self.map.load_csv()
        self.pheromone_ini = 8
        self.alpha = 0.5
        self.beta = 3

    def pheromone_init(self):
        shape = self.path.shape
        # print(shape)
        for i in range(shape[1]):
            for j in range(shape[2]):
                if self.path[0, i, j] == 0:
                    continue
                else:
                    self.path[1, i, j] = self.pheromone_ini
        return 0

    def ant_generator(self):
        self.ant_path_list = self.ant.path_search()


if __name__ == "__main__":
    AOC_demo = AOC()
    AOC_demo.pheromone_init()
    AOC_demo.map.dump_csv(AOC_demo.path)

    # step = AOC_demo.ant.path_choose_possibility((0, 1), AOC_demo.path, AOC_demo.alpha, AOC_demo.beta)
    # print(step)
