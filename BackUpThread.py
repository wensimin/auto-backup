import threading
from ftplib import FTP

import time

from FtpUtil import placeFiles


class BackUpThread(threading.Thread):
    def __init__(self, console, config):
        super().__init__()
        self.console = console
        self.running = True
        self.config = config

    def run(self):
        max_sec = int(self.config["interval"])
        while self.running:
            try:
                self.log("开始备份")
                with FTP(self.config["ip"], self.config["user"], self.config["password"]) as ftp:
                    placeFiles(ftp, self.config["localPath"], self.config["path"], self.log)
                    self.log("备份完成")
            except Exception as e:
                self.log("备份出现错误:" + str(e))
                self.log("备份将在" + str(max_sec) + "秒后重试")
            finally:
                for i in range(max_sec):
                    if not self.running:
                        break
                    time.sleep(1)
        self.log("备份已停止")

    def log(self, text):
        self.console.insert(0, text)

    def stop(self):
        self.running = False
