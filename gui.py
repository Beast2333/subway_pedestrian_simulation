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
        self.c = tk.Canvas(self.top, width=1080, height=680, bg="darkgray")
        #设置top上的画布，1080*680，颜色A9A9A9，命名为c
        self.c.pack()#将画布c放置在top上
        self.label = Label(self.top, text="Time = 0.0 s")#设置标签，命名为label，内容为
        self.label.pack()#将标签放置在top上
    """绘制障碍物"""
    def add_barrier(self):
        #  添加房间边框
        self.c.create_rectangle(0, 0, 1080, 40, fill="#696969", outline="#696969")
        # 画布c上画矩形，1080*40，内部颜色#696969，外部边框#696969
        self.c.create_rectangle(0, 640, 1080, 680, fill="#696969", outline="#696969")
        # 下方（0，640）1080*40，颜色边框
        self.c.create_rectangle(0, 0, 40, 680, fill="#696969", outline="#696969")
        # 左侧，颜色边框
        self.c.create_rectangle(1040, 0, 1080, 140, fill="#696969", outline="#696969")
        # 右上40*140，颜色边框
        self.c.create_rectangle(1040, 220, 1080, 680, fill="#696969", outline="#696969")
        # 右下40*460，颜色边框
        #  添加房间中间的障碍物
        self.c.create_rectangle(400, 160, 720, 280, fill="#696969", outline="#696969")
        self.c.create_rectangle(400, 400, 720, 520, fill="#696969", outline="#696969")
        # 中间两个320*120的矩形障碍
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

