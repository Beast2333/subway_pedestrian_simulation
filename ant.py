import map_init as mp


class Ant(object):
    def __init__(self):
        self.map = mp.MapInit()
        self.ant_path_list = []
        self.forbidden_list = []
        self.next_step = (0, 0)
        self.end = 6

    def path_choose_possibility(self, begin, path, alpha, beta):
        i = begin
        possibility_list = []
        length = path.shape[2]
        next_step = ()
        # heuristic = 1 / path[0, i, j]
        # ph = path[1, i, j]
        denominator = 0
        # 分母计算
        for s in range(length):
            if path[0, i, s] != 0:
                denominator += path[0, i, s]**alpha + path[1, i, s]**beta

        # 计算所有可能性
        flag = 0
        for k in range(length):
            if path[0, i, k] != 0 and k not in self.forbidden_list:
                self.forbidden_list.append(k)
                # print(self.forbidden_list)
                heuristic = 1 / path[0, i, k]
                ph = path[1, i, k]
                possibility = (heuristic**alpha + ph**beta) / denominator
                possibility_list.append((possibility, k))
            elif path[0, i, k] == 0 or k in self.ant_path_list:
                flag += 1
                # print("flag=" + str(flag), end=' ')
        if flag == length:
            print("进入死路！")
            exit()
        # 排序，选择下一节点
        next_p = (0, 0)
        for p in possibility_list:
            if next_p[0] < p[0]:
                next_p = p
        return next_p[1]

    def path_search(self, begin, end, path, alpha, beta):
        print("开始寻找" + str(begin) + "到" + str(end) + "最短路径")
        current_spot = begin
        self.ant_path_list.append(current_spot)
        self.forbidden_list.append(current_spot)
        while current_spot != end:
            current_spot = self.path_choose_possibility(current_spot, path, alpha, beta)
            self.ant_path_list.append(current_spot)
            print(current_spot)
        return 0


if __name__ == "__main__":
    ant = Ant()
    path = ant.map.load_csv()
    # print(path)
    a = ant.path_search(0, ant.end, path, 0.1, 10)
