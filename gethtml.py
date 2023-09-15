import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import markdown
from markdownify import markdownify
import requests
import random
import os
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox
from threading import Thread

class window:
    def __init__(self):

        #构建GUI界面
        self.root = Tk()
        self.root.title('洛谷小爬虫')
        self.root.geometry('810x750')
        self.root.config(background='gray')
        menu = Menu(self.root)
        menu.add_command(label='保存题目需要时间，稍安勿躁~')
        self.root.config(menu=menu)

        #设置内容
        frame = Frame(self.root,borderwidth=5,relief=GROOVE)
        frame.config(background='gray')
        frame.place(x=2, y=65, width=810, height=650)
        scrollBar = Scrollbar(frame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.tree = Treeview(frame, columns=('题目序号', '题目名称', '显示算法', '难度', '通过率'), show="headings", yscrollcommand=scrollBar.set)
        self.tree.column('题目序号', width=140, anchor='center')
        self.tree.column('题目名称', width=180, anchor='center')
        self.tree.column('显示算法', width=180, anchor='center')
        self.tree.column('难度', width=160, anchor='center')
        self.tree.column('通过率', width=140, anchor='center')
        self.tree.heading('题目序号', text="题目序号")
        self.tree.heading('题目名称', text="题目名称")
        self.tree.heading('显示算法', text="显示算法")
        self.tree.heading('难度', text="难度")
        self.tree.heading('通过率', text="通过率")
        self.tree.pack(side=LEFT, fill=Y)
        scrollBar.config(command=self.tree.yview)

        #设置查询框
        frame1 = Frame(self.root, borderwidth=5, relief=GROOVE)
        frame1.place(x=122, y=15, width=500, height=43)
        self.label = Label(frame1, text="输入关键字：")
        self.label.grid(row=4, column=0)
        self.entry = Entry(frame1, width=37)
        self.entry.config(background='Light Blue')
        self.entry.grid(row=4, column=1)
        self.button = Button(frame1, text="查询", anchor='center',command=self.search)
        self.button.grid(row=4, column=4)
        self.var = StringVar()
        self.var.set('入门')
        self.m = ['入门', '普及', '提高', '省选', 'NOI', 'CTSC']
        self.menu = ttk.OptionMenu(frame1, self.var, '入门', *self.m)
        self.menu.grid(row=4, column=2)
        self.var1 = StringVar()
        self.var1.set('10')
        self.m = ['10', '20', '30', '40', '50', '100']
        self.menu = ttk.OptionMenu(frame1, self.var1, '10', *self.m)
        self.menu.grid(row=4, column=3)

        #使界面一直运行着
        self.root.mainloop()

    def search(self):
        self.key = self.entry.get()
        self.entry.delete(0, END)
        self.label1 = Label(self.root, text="正在查询，请稍后...")
        self.label1.place(x = 680, y=25)
        if self.key == '':
            messagebox.showerror("系统提示", "未输入关键字！")
        else:
            spsider = Thread(target=self.ground)
            spsider.start()

            # self.arr.sort(key=lambda x:(x[0],x[4]))
            # for i in self.arr:
            #     self.tree.insert('','end', values=i)

    def ground(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        # 创建 Chrome WebDriver 对象
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.luogu.com.cn/")

        # 删除没加入Cookies前，网页浏览器对象自行生成的Cookies
        self.driver.delete_all_cookies()

        # 给浏览器加入之前保存好的Cookies
        with open('cookies.txt', 'r') as f:
            cookies_list = json.load(f)
            for cookie in cookies_list:
                self.driver.add_cookie(cookie)

        # 刷新一下网页，就进入到已经登录的网站了
        self.driver.refresh()

        # 进入到题目列表
        list_url = self.driver.find_element(By.CSS_SELECTOR, '#app > nav > a:nth-child(3)').get_attribute('href')
        self.driver.get(list_url)
        search_box = self.driver.find_element(By.CSS_SELECTOR,"#app > div.main-container > main > div > section > div > section:nth-child(2) > div > div.refined-input.input-wrap.block-item.search-text.frame > input")
        search_button = self.driver.find_element(By.CSS_SELECTOR,"#app > div.main-container > main > div > section > div > section:nth-child(2) > div > div.search-option.no-wrap")
        key = self.key + self.var.get()
        search_box.send_keys(key)
        search_button.click()
        time.sleep(2)
        self.driver.implicitly_wait(10)

        # 获取和关键字有关的题目列表
        problems_list = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div/div/div/div[1]/div[2]")
        problems_row = problems_list.find_elements(By.CLASS_NAME, "row")
        i = 0

        #保存题目链接列表
        self.arr = []
        self.Problem_object = []
        List_key_url = self.driver.current_url
        # 对题目进行保存
        for problem_row in problems_row:
            if i > int(self.var1.get()):
                break
            i += 1
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/main/div/div/div/div[1]/div[2]")))
            problem_number = problem_row.find_elements(By.TAG_NAME, "span")[1]
            problem_name = problem_row.find_element(By.XPATH, "./div[1]/a")
            problem_label = problem_row.find_element(By.XPATH, "./div[2]")
            problem_level = problem_row.find_element(By.XPATH, "./div[3]")
            problem_pass1 = problem_row.find_element(By.XPATH, "./div[4]/div[1]")
            problem_pass2 = problem_pass1.find_element(By.TAG_NAME, "div")

            # 获取每一行题目的各个标签
            Number = problem_number.text
            Name = problem_name.text
            Label = problem_label.text
            Level = problem_level.text
            Pass = problem_pass2.size['width'] / problem_pass1.size['width']

            Number = Number.replace('/', 'or').replace('\\', 'or').replace("'", 'or').replace('"', 'or')
            Name = Name.replace('/', 'or').replace('\\', 'or').replace("'", 'or').replace('"', 'or')
            Label = Label.replace('/', 'or').replace('\\', 'or').replace("'", 'or').replace('"', 'or')
            Level = Level.replace('/', 'or').replace('\\', 'or').replace("'", 'or').replace('"', 'or')

            self.arr.append(problem_name.get_attribute('href'))
            self.Problem_object.append((Number, Name, Label, Level, Pass))
            self.tree.insert('', 'end', values=(Number, Name, Label, Level, Pass))

        self.label1.config(text='保存中，请稍后...', background='Light Blue')


        for problem_url,object in zip(self.arr,self.Problem_object):

            # 获取题目并保存为markdown格式
            self.driver.get(str(problem_url))
            time.sleep(random.randint(1,4))
            self.driver.implicitly_wait(10)

            # 获取题目所在位置
            element = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div/section[2]/section/div/div[2]")
            html = element.get_attribute('innerHTML')

            # 如果之前没有类似的搜索，则建立一个文件夹来保存题目文件
            if not os.path.exists(key):
                os.makedirs(key)

            with open(key + '/' + object[0] + '_' + object[1] + '.md', "w", encoding='utf-8') as f:
                f.write(markdownify(html))

            # 开始准备获取题解链接
            url = self.driver.find_element(By.XPATH,"/html/body/div/div[2]/main/div/section[1]/div[1]/a[2]").get_attribute('href')
            self.driver.get(url)
            time.sleep(random.randint(1, 4))
            self.driver.implicitly_wait(10)

            # 获取题解，并保存为markdown格式
            adjust = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/main/div/section[2]/div/div[1]/b")

            if adjust.text[0] != '0':
                element = self.driver.find_element(By.XPATH,"/html/body/div/div[2]/main/div/section[2]/div/div[2]/div/div[1]/div/div[1]")
                html = element.get_attribute('innerHTML')
                with open(key + '/' + object[0] + '_' + object[1] + '_题解' + '.md', "w", encoding='utf-8') as f:
                    f.write(markdownify(html))

        self.label1.destroy()
        self.driver.quit()


f = window()
