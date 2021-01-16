#!/usr/bin/env python
# coding: utf-8

# In[2]:


# get_ipython().run_line_magic('run', 'gui.py')


# In[5]:


# %load gui.py
import tkinter as tk
from tkinter import Label


class GUI:
    def __init__(self):
        """设置窗体"""
        self.top = tk.Tk()#将窗体命名为top
        self.top.title("地铁车站")#设置窗体名称
        self.top.geometry("1080x710")#设置窗体尺寸
        self.top.resizable(width=False, height=False)#设置不可调整尺寸
        """设置画布"""
        self.c = tk.Canvas(self.top, width=1080, height=680, bg="A9A9A9")
        #设置top上的画布，1080*680，颜色A9A9A9，命名为c
        self.c.pack()#将画布c放置在top上
        self.label = Label(self.top, text="Time = 0.0 s")#设置标签，命名为label，内容为
        self.label.pack()#将标签放置在top上
    """绘制障碍物"""
    def add_barrier(self):
        #  添加房间边框
        self.c.create_rectangle(0, 0, 1080, 40, fill="#696969", outline="#696969")
        #画布c上画矩形，1080*40，内部颜色#696969，外部边框#696969
        self.c.create_rectangle(0, 640, 1080, 680, fill="#696969", outline="#696969")
        #下方（0，640）1080*40，颜色边框
        self.c.create_rectangle(0, 0, 40, 680, fill="#696969", outline="#696969")
        #左侧，颜色边框
        self.c.create_rectangle(1040, 0, 1080, 140, fill="#696969", outline="#696969")
        #右上40*140，颜色边框
        self.c.create_rectangle(1040, 220, 1080, 680, fill="#696969", outline="#696969")
        #右下40*460，颜色边框
        #  添加房间中间的障碍物
        self.c.create_rectangle(400, 160, 720, 280, fill="#696969", outline="#696969")
        self.c.create_rectangle(400, 400, 720, 520, fill="#696969", outline="#696969")
        #中间两个320*120的矩形障碍
    """更新显示时间"""
    def update_time(self, _time):
        self.label['text'] = "Time = "+_time + " s"
        #tkinter的秒表功能，将标签改为显示秒表
    """绘制圆"""
    def add_oval(self, x1, y1, x2, y2, oval_tag):
        self.c.create_oval(x1, y1, x2, y2, fill="#FFE4B5", tag=oval_tag)#绘制圆，添加tag
    """删除圆"""
    def del_oval(self, oval_tag):
        self.c.delete(oval_tag)#删除带有oval_tag标签的圆
    '''更新'''
    def update_gui(self):
        self.top.update()
        self.c.update()#更新窗体以及画布
    '''启动GUI'''
    def start(self):
        self.top.mainloop()#运行窗体top


# In[6]:


# %load people.py
import random
import math
from astar import AStar
class People:
    def __init__(self, _id, _loc_x, _loc_y,):
        self.id = _id  # 行人编号
        self.m = 50 + random.randint(0, 20)  # 行人质量/kg
        self.r = (35 + random.randint(0, 5))/2  # 行人半径(肩宽/2)/cm
        self.d_v = (60 + random.randint(0, 20)) / 100  # 期望速度大小/m/s
        self.loc = (_loc_x, _loc_y)  # 当前位置
        self.v = (0, 0)  # 当前速度
        self.a = (0, 0)  # 当前加速度



class PeopleList:
    def __init__(self):
        self.list = []
        count = 0
        #  依次添加行人至self.list，三列行人，每列15人
        for i in range(0, 15):
            self.list.append(People("o"+str(count), 60, 60 + i * 40))#id，横坐标，纵坐标
            count = count + 1
            self.list.append(People("o"+str(count), 100, 60 + i * 40))
            count = count + 1
            self.list.append(People("o"+str(count), 140, 60 + i * 40))
            count = count + 1

        # 在一开始就计算好各个位置的下一步方向向量，并存储到矩阵中，以节省算力
        k = 5 
        self.matrix = [[0 for i in range(17)] for i in range(27)]#创建17*27的空矩阵
        for i in range(0, 27):
            for j in range(0, 17):
                if i == 0:  # 将障碍物的位置也设置对应的方向向量，以便在特殊情况撞墙后能及时调整回来
                    self.matrix[i][j] = (k, 0)
                elif i == 26:
                    self.matrix[i][j] = (-1 * k, 0)
                elif j == 0:
                    self.matrix[i][j] = (0, k)
                elif j == 16:
                    self.matrix[i][j] = (0, -1 * k)
                elif i == 10:
                    if (j == 4) or (j == 10):
                        self.matrix[i][j] = (-1 * k, -1 * k)
                    elif (j == 5) or (j == 11):
                        self.matrix[i][j] = (-1 * k, 0)
                    elif (j == 6) or (j == 12):
                        self.matrix[i][j] = (-1 * k, k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)#i为10时，如果没有障碍物，则方向向量为A*算法的下一步位置
                elif i == 17:
                    if (j == 4) or (j == 10):
                        self.matrix[i][j] = (k, -1 * k)
                    elif (j == 5) or (j == 11):
                        self.matrix[i][j] = (k, 0)
                    elif (j == 6) or (j == 12):
                        self.matrix[i][j] = (k, k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)#i为17时，如果没有障碍物，则方向向量为A*算法的下一步位置
                elif (j == 4) or (j == 10):
                    if (i > 10) and (i < 17):#障碍物的上边界
                        self.matrix[i][j] = (0, -1 * k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif (j == 6) or (j == 12):
                    if (i > 10) and (i < 17):
                        self.matrix[i][j] = (0, k)#障碍物的下边界
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif (i > 10) and (i < 17) and ((j == 5) or (j == 11)):#障碍物的中间位置
                    self.matrix[i][j] = (0, k)
                else:
                    self.matrix[i][j] = AStar.next_loc(i, j)
        self.matrix[26][4] = (1, 0)#目标点的方向向量


    def move(self):
        #  设置间隔时间、A、B参数
        deta_time = 0.005
        A = 2000
        B = -0.08
        #  下面开始依次计算各个行人下一时刻的加速度
        for i in range(0, len(self.list)):#遍历self.list内行人
            now = self.list[i]#当前人
            #  下面计算社会力模型的第一项，期望力
            next_desired = self.matrix[int(now.loc[0]//40)][int(now.loc[1]//40)]  # 获取下一位置的方向向量，每一小格为40
            desired_v = (now.d_v*next_desired[0], now.d_v*next_desired[1])#期望速度
            #  下面计算社会力模型的第二项fij
            sum_of_fij = (0, 0)
            for j in range(0, len(self.list)):
                if i == j:#如果是同一个人，则跳过
                    continue
                temp = self.list[j] 
                d = (((now.loc[0] - temp.loc[0])/100)**2 + ((now.loc[1] - temp.loc[1])/100)**2)**0.5#计算两人距离，temp.loc是周围八个人
                if d >= 1.4:  # 如果两个行人质心距离超过1.4m（或距离超过1m），之间的作用力可以忽略不计
                    continue
                fij = A * math.exp((d-now.r/100-temp.r/100)/B)
                sum_of_fij = (sum_of_fij[0] + fij * (now.loc[0] - temp.loc[0])/100,
                              sum_of_fij[1] + fij * (now.loc[1] - temp.loc[1])/100)#行人间力及方向向量
            #  下面计算社会力模型的第三项fiW
            sum_of_fiw = (0, 0)
            #  首先计算四周墙壁的fiW
            d = now.loc[0] - 40#行人的边与左边墙距离
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])#计算力及方向向量
            d = 1040 - now.loc[0]#行人边与右边墙距离
            if (d < 120) and (now.loc[1] > 220 or now.loc[1] < 140):#距离小于120且不在门旁边
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])#计算力及方向向量
            d = now.loc[1] - 40#与上方墙距离
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])#计算力及方向向量
            d = 640 - now.loc[1]#与下方墙距离
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])#计算力及方向向量
            #  下面计算中间障碍物1的fiW
            d = 400 - now.loc[0]#与中间障碍物左侧距离
            if (d < 120) and (d > 0) and (now.loc[1] > 160) and (now.loc[1] < 280):#纵坐标大于160小于280
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])#计算力及方向向量
            d = now.loc[0] - 720#与中间障碍物右侧距离
            if (d < 120) and (d > 0) and (now.loc[1] > 160) and (now.loc[1] < 280):#纵坐标大于160小于280
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])#计算力及方向向量
            d = 160 - now.loc[1]#与中间上方障碍物上方距离
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):#横坐标大于400小于720
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])#计算力及方向向量
            d = now.loc[1] - 280#与中间障碍物下方距离
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):#横坐标大于400小于720
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])#计算力及方向向量
            #  下面计算障碍物2的fiW
            d = 400 - now.loc[0]
            if (d < 120) and (d > 0) and (now.loc[1] > 400) and (now.loc[1] < 520):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = now.loc[0] - 720
            if (d < 120) and (d > 0) and (now.loc[1] > 400) and (now.loc[1] < 520):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = 400 - now.loc[1]
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])
            d = now.loc[1] - 520
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])
            #  下面计算各个行人的加速度分量
            a_x = ((now.m * (desired_v[0] - now.v[0]) / 0.5) + sum_of_fij[0] + sum_of_fiw[0]) / now.m#和力比质量
            a_y = ((now.m * (desired_v[1] - now.v[1]) / 0.5) + sum_of_fij[1] + sum_of_fiw[1]) / now.m
            self.list[i].a = (a_x, a_y)

        #  开始计算各个行人新的速度、下一位置，并更新
        for i in range(0, len(self.list)):
            now = self.list[i]
            a_x = now.a[0]
            a_y = now.a[1]
            v0_x = now.v[0]
            v0_y = now.v[1]
            v_x = v0_x + a_x * deta_time  # 计算新速度并更新，初速度加加速度乘时间
            v_y = v0_y + a_y * deta_time
            self.list[i].v = (v_x, v_y)
            l_x = (v0_x * deta_time + deta_time * a_x * deta_time * deta_time)*100 + now.loc[0]  # 计算新的行走距离并更新
            l_y = (v0_y * deta_time + deta_time * a_y * deta_time * deta_time)*100 + now.loc[1]
            self.list[i].loc = (l_x, l_y)



# In[7]:


class Node:
    def __init__(self):
        #  初始化各个坐标点的g值、h值、f值、父节点
        self.g = 0
        self.h = 0
        self.f = 0
        self.father = (0, 0)

#A*算法，找最短路
class AStar:
    @staticmethod
    def next_loc(x, y):
        # 初始化各种状态
        start_loc = (x, y)  # 初始化起始点
        aim_loc = [(26, 4)]  # 初始化目标地点
        open_list = []  # 初始化打开列表
        close_list = []  # 初始化关闭列表
        barrier_list = []  # 初始化障碍列表
        #  添加障碍，房间中障碍的坐标
        for i in range(0, 27):
            barrier_list.append((i, 0))
            barrier_list.append((i, 16))
        for i in range(1, 16):
            barrier_list.append((0, i))
            barrier_list.append((26, i))
        barrier_list.remove((26, 4))
        for i in range(10, 18):
            for j in range(4, 7):
                barrier_list.append((i, j))
            for j in range(10, 13):
                barrier_list.append((i, j))

        # 创建存储节点的矩阵，17*27的空矩阵，每个节点等于Node()
        node_matrix = [[0 for i in range(17)] for i in range(27)]
        for i in range(0, 27):
            for j in range(0, 17):
                node_matrix[i][j] = Node()

        open_list.append(start_loc)  # 起始点添加至打开列表
        # 开始算法的循环
        while True:
            now_loc = open_list[0]
            for i in range(1, len(open_list)):  # （1）获取f值最小的点，遍历openlist的所有点
                if node_matrix[open_list[i][0]][open_list[i][1]].f < node_matrix[now_loc[0]][now_loc[1]].f:
                    now_loc = open_list[i]#如果openlist里的点的f值小于当前位置点的f值，则将当前位置点换为openlist内的i点
            #   （2）切换到关闭列表
            open_list.remove(now_loc)#openlist中删除起始点即i点
            close_list.append(now_loc)#closelist中加入起始点即i点
            #  （3）对相邻格中的每一个
            list_offset = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]#周围的八个点的方向向量
            for temp in list_offset:#遍历这八个点
                temp_loc = (now_loc[0] + temp[0], now_loc[1] + temp[1])
                if temp_loc[0] < 0 or temp_loc[0] > 26 or temp_loc[1] < 0 or temp_loc[1] > 16:#如果在界面外面，则跳过
                    continue
                if temp_loc in barrier_list:  # 如果在障碍列表，则跳过
                    continue
                if temp_loc in close_list:  # 如果在关闭列表，则跳过
                    continue

                #  该节点不在open列表，添加，并计算出各种值
                if temp_loc not in open_list:
                    open_list.append(temp_loc)
                    #计算g值，当前所在位置点的g值加上下一点的g值
                    node_matrix[temp_loc[0]][temp_loc[1]].g = (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5))
                    #计算h值，横纵坐标之和
                    node_matrix[temp_loc[0]][temp_loc[1]].h = (abs(aim_loc[0][0]-temp_loc[0])
                                                               + abs(aim_loc[0][1]-temp_loc[1]))*10
                    #计算f值，h+g
                    node_matrix[temp_loc[0]][temp_loc[1]].f = (node_matrix[temp_loc[0]][temp_loc[1]].g +
                                                               node_matrix[temp_loc[0]][temp_loc[1]].h)
                    #父节点为当前位置
                    node_matrix[temp_loc[0]][temp_loc[1]].father = now_loc
                    continue

                #  如果在open列表中，比较，重新计算，取小的g值
                if node_matrix[temp_loc[0]][temp_loc[1]].g > (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5)):
                    node_matrix[temp_loc[0]][temp_loc[1]].g = (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5))
                    node_matrix[temp_loc[0]][temp_loc[1]].father = now_loc
                    node_matrix[temp_loc[0]][temp_loc[1]].f = (node_matrix[temp_loc[0]][temp_loc[1]].g +
                                                               node_matrix[temp_loc[0]][temp_loc[1]].h)

            #  判断是否停止
            if aim_loc[0] in close_list:
                break

        #  依次遍历父节点，找到下一个位置
        temp = aim_loc[0]
        while node_matrix[temp[0]][temp[1]].father != start_loc:
            temp = node_matrix[temp[0]][temp[1]].father
        #  返回下一个位置的方向向量，例如：（-1,0），（-1,1）......
        re = (temp[0] - start_loc[0], temp[1] - start_loc[1])
        return re


# In[ ]:


# %load main.py
from gui import GUI
from people import PeopleList

#  创建GUI
gui = GUI()
gui.add_barrier()
gui.update_gui()

#  创建行人列表
people_list = PeopleList()
time = 0
#  在GUI初始化各个行人
for people in people_list.list:
    gui.add_oval(people.loc[0]-people.r, people.loc[1]-people.r,
                 people.loc[0]+people.r, people.loc[1]+people.r, people.id)#x1,y1,x2,y2,tag为行人的id
gui.update_gui()#更新画布及窗体

#  各个行人开始移动
while people_list.list:
    i = 0
    while i < len(people_list.list):
        gui.del_oval(people_list.list[i].id)
        if people_list.list[i].loc[0] > 1040:  # 如果有人走出房间，则移除
            people_list.list.pop(i)
            continue
        i += 1
    people_list.move()  # 行人移动，根据社会力模型移动
    for people in people_list.list:  # 在GUI中更新行人位置
        gui.add_oval(int(people.loc[0]) - people.r, 
                     int(people.loc[1]) - people.r, int(people.loc[0]) + people.r,
                     int(people.loc[1]) + people.r, people.id)#重新绘制圆
    time = time + 0.005  # 更新时间
    gui.update_time(str(round(time, 3)))#返回三位小数
    gui.update_gui()#更新gui

gui.start()#开始


# In[8]:





# In[ ]:




