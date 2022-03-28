# -*- coding:utf8 -*-
import tkinter
from tkinter import *
from tkinter import ttk

import mysql
import mysql.connector  # python连接到数据库，需要使用第三方库 mysql-connector
import requests  # 模拟浏览器向服务器发送请求，需要使用到第三方库 requests
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# 爬取网页数据
def get_soup(url):
    try:
        # 添加头部信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        resp = requests.get(url, headers=headers)  # resp是响应结果
        # 进行状态码判断，是否正确读取到网页
        if resp.status_code == 200:
            resp.encoding = "utf-8"
            # soup = BeautifulSoup(resp.text, "html.parser")  # 解析网页（因HTML中没有我需要的歌曲列表数据，此处不能使用，若想使用正则表达式和BuestifulSoup解析提取，模拟当中有数据）
            return resp.json()
        return None
    except RequestException:
        return None

# 提取信息保存到列表
def save_list(url):
    lst = []  # 创建lst列表用于存储获取到的数据（可变序列）
    # 调用函数获取json数据
    soup_json = get_soup(url)
    # 从字典当中根据detail的键获取值(获取到歌曲信息)
    list_song = soup_json['detail']['data']['data']['song']

    # 遍历列表获取每首歌曲的字典(序号，歌曲名，歌手名),并把这些歌曲数据元组加到列表中
    for item in list_song:
        lst.append((item['rank'], item['rankValue'], item['title'], item['singerName']))
    return lst

# 储存数据到数据库
def save_database(lst):
    # 获取连接对象
    mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='12345', database='music_play', charset="utf8")   # 主机名，账号和密码
    # 获取cursor（游标）的对象
    mycursor = mydb.cursor()

    # 编写sql插入语句（事先创建好的一个数据库）
    sql = 'insert into musicPlay values(%s,%s,%s,%s)'  # 向表中插入数据(排名，上升率，歌曲名，歌手名)
    # 获取储存歌曲的列表
    val = lst
    # 开始执行sql语句(sql语句和值value)
    mycursor.executemany(sql, val)  # 同时执行多条语句
    # 执行完成提交
    mydb.commit()
    print(mycursor.rowcount, '记录插入成功！')

# 子窗口展示
def sub_page(url):
    sub_win = tkinter.Toplevel()  # 创建window子窗口
    sub_win.title('QQ音乐排行榜')     # 设置子窗口标题
    image2 = Image.open(r'D:\PyCharm\playMusic\子窗口背景.jpg')
    background_image = ImageTk.PhotoImage(image2)  # 设置子窗口背景图片
    sub_win.geometry('480x700')
    background_label = Label(sub_win, image=background_image).place(x=0, y=0)
    lab2 = Label(sub_win, text='排行榜前20首歌曲', font=('宋体', 20), bg='gold').place(x=220, y=100, anchor='n')
    tree = ttk.Treeview(sub_win)     # 创建表格对象
    tree["columns"] = ("排名", "上升率", "歌曲名", "歌手名")  # 定义列
    tree["height"] = 20
    tree.column("排名", width=50)    # 设置列宽度
    tree.column("上升率", width=50)
    tree.column("歌曲名", width=150)
    tree.column("歌手名", width=200)
    tree.heading("排名", text='排名')   # 设置列头名称
    tree.heading("上升率", text='上升率')
    tree.heading("歌曲名", text='歌曲')
    tree.heading("歌手名", text='歌手')
    sub_win.focus_force()    # 新窗口获得焦点

    lst1 = save_list(url)

    for i in range(20):
        tree.insert('', 'end', values=lst1[i])   # 插入Tk树
    tree.place(x=150, y=400, anchor='center')
    sub_win.mainloop()
    return save_database(lst1)   # 最终将数据保存到数据库

def case(string):
    d = string
    if d == '流行':
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI4081542370876272&g_tk=2005615097&sign=zza8qz11gvevyc4eab6fd08bb3b1594280779c07896cdbd&loginUin=2473003395&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A4%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222021-06-30%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
        sub_page(url)
    if d == '热歌':
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI2064020383876517&g_tk=2005615097&sign=zzalcwtlzqts4n311b31e7614f684551d53e458d26e8e00d&loginUin=2473003395&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A26%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222021_25%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
        sub_page(url)
    if d == '飙升':
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI3412351863727161&g_tk=2005615097&sign=zzag4c5sygm6cpf162td606e5eb9c780a6d3142c0a2daf28491&loginUin=2473003395&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A62%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222021-06-30%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
        sub_page(url)
    if d == '新歌':
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getUCGI08603667637115375&g_tk=2005615097&sign=zza4wrhoj13p3i0wxp9a3e7a9c83e6eca2485ea3228b210d72&loginUin=2473003395&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A27%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222021-06-30%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
        sub_page(url)

# 首页展示
def music_index():
    win = tkinter.Tk()  # 创建window窗口对象
    win.title('QQ音乐排行榜')    # 设置窗口标题
    image1 = Image.open(r'D:\PyCharm\playMusic\music.jpeg')
    background_image = ImageTk.PhotoImage(image1)   # 设置背景图片
    win.geometry('404x300')
    background_label = Label(win, image=background_image, bg='blue').place(x=0, y=0)
    lab1 = Label(win, text='请选择排行榜的类型', font=('仿宋', 20), bg='lavender').place(x=200, y=50, anchor='n')     # 显示lab1组件
    button1 = Button(win, text='流行榜', font=('隶书', 15), fg='green', bg='gold', command=lambda: case('流行')).place(x=40, y=230)
    button2 = Button(win, text='热歌榜', font=('隶书', 15), fg='green', bg='orange', command=lambda: case('热歌')).place(x=120, y=230)
    button3 = Button(win, text='飙升榜', font=('隶书', 15), fg='green', bg='yellow', command=lambda: case('飙升')).place(x=200, y=230)
    button4 = Button(win, text='新歌榜', font=('隶书', 15), fg='green', bg='pink', command=lambda: case('新歌')).place(x=280, y=230)
    win.mainloop()  # 进入消息循环，显示窗口

if __name__ == '__main__':
    music_index()
