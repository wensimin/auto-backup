import threading
from ftplib import FTP

from FtpUtil import downFiles


class Loadhread(threading.Thread):
    def __init__(self, console, config, path):
        super().__init__()
        self.console = console
        self.config = config
        self.path = path

    def run(self):
        try:
            self.log("开始下载")
            with FTP(self.config["ip"], self.config["user"], self.config["password"]) as ftp:
                downFiles(ftp, self.path, self.config["path"], self.log)
                self.log("下载完成")
        except Exception as e:
            self.log("下载出现错误:" + str(e))

    def log(self, text):
        self.console.insert(0, text)

