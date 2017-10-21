import tkinter as tk
from json import JSONDecodeError
from tkinter import filedialog
from tkinter.messagebox import showinfo

from BackUpThread import BackUpThread
from LoadThread import Loadhread
from config import load_config, save_config


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.hostLabel = tk.Label(self, text="主机地址:")
        self.hostInput = tk.Entry(self, width=20)
        self.userLabel = tk.Label(self, text="用户名:")
        self.userInput = tk.Entry(self, width=15)
        self.passwordLabel = tk.Label(self, text="密码:")
        self.passwordInput = tk.Entry(self, width=15, show='*')
        self.pathLabel = tk.Label(self, text="远程路径:")
        self.pathInput = tk.Entry(self, width=40)
        self.localPathLabel = tk.Label(self, text="本地路径:")
        self.localPathInput = tk.Entry(self, width=40, )
        self.save = tk.Button(self, text="开始自动存档")
        self.load = tk.Button(self, text="读取存档", fg="red")
        self.consoleBox = tk.Listbox(self, width=100)
        self.init_config()
        self.layout()
        self.event()
        self.job = BackUpThread(self.consoleBox, self.config)

    def init_config(self):
        try:
            self.config = load_config()
            self.hostVar = tk.StringVar()
            self.hostVar.set(self.config["ip"])
            self.userVar = tk.StringVar()
            self.userVar.set(self.config["user"])
            self.passwordVar = tk.StringVar()
            self.passwordVar.set(self.config["password"])
            self.pathVar = tk.StringVar()
            self.pathVar.set(self.config["path"])
            self.localPathVar = tk.StringVar()
            self.localPathVar.set(self.config["localPath"])
            self.hostInput["textvariable"] = self.hostVar
            self.userInput["textvariable"] = self.userVar
            self.passwordInput["textvariable"] = self.passwordVar
            self.pathInput["textvariable"] = self.pathVar
            self.localPathInput["textvariable"] = self.localPathVar
        except JSONDecodeError:
            showinfo("错误", str("配置文件信息错误，请检查修复后运行"))
            exit(-1)

    def set_config(self):
        self.config["ip"] = self.hostVar.get()
        self.config["password"] = self.passwordVar.get()
        self.config["path"] = self.pathVar.get()
        self.config["localPath"] = self.localPathVar.get()
        self.config["user"] = self.userVar.get()
        save_config(self.config)

    def event(self):
        self.save["command"] = self.start_save
        self.load["command"] = self.start_load

    def layout(self):
        self.grid()
        # row 1
        self.hostLabel.grid(column=0, row=0, padx=20, sticky=tk.E)
        self.hostInput.grid(column=1, row=0, sticky=tk.W)
        # row 2
        self.userLabel.grid(column=0, row=1, padx=20, sticky=tk.E)
        self.userInput.grid(column=1, row=1, sticky=tk.W)
        # row 3
        self.passwordLabel.grid(column=0, row=2, padx=20, sticky=tk.E)
        self.passwordInput.grid(column=1, row=2, sticky=tk.W)
        # row 4
        self.pathLabel.grid(column=0, row=3, padx=20, sticky=tk.E)
        self.pathInput.grid(column=1, row=3, sticky=tk.W)
        # row 5
        self.localPathLabel.grid(column=0, row=4, padx=20, sticky=tk.E)
        self.localPathInput.grid(column=1, row=4, sticky=tk.W)
        # row 6
        self.save.grid(column=1, row=5, pady=10, columnspan=1, sticky=tk.W)
        self.load.grid(column=1, row=5, pady=10, columnspan=1, padx=30, sticky=tk.E)
        # row 7
        self.consoleBox.grid(column=0, row=6, columnspan=4, sticky=tk.E + tk.W)

    def start_save(self):
        if self.job.is_alive():
            self.save["text"] = "开始自动存档"
            self.job.stop()
        else:
            self.job = BackUpThread(self.consoleBox, self.config)
            self.set_config()
            self.job.start()
            self.save["text"] = "停止自动存档"

    def log(self, text):
        self.consoleBox.insert(0, text)

    def start_load(self):
        try:
            if self.job.is_alive():
                showinfo("请等待", "请等待存档完成再进行下载，否则容易存档不完整")
                return
            self.set_config()
            path = filedialog.askdirectory()
            if not path:
                return
            Loadhread(self.consoleBox, self.config, path).start()
        except Exception as e:
            showinfo("错误", "下载出现错误:" + str(e))


root = tk.Tk()
app = Application(root)
app.mainloop()
