import json
import time
from ftplib import FTP
from json import JSONDecodeError

from FtpUtil import placeFiles


def load_config():
    """加载json格式配置"""
    with open("config.json", "r+") as f:
        c = json.loads(f.read())
        return c


def write_config(c):
    """保存配置信息至文件"""
    with open("config.json", "r+") as f:
        f.write(json.dump(c))


try:
    config = load_config()
except JSONDecodeError:
    print("配置文件信息错误，请检查修复后运行")
    exit(-1)

while True:
    print("开始备份")
    with FTP(config["ip"], config["user"], config["password"]) as ftp:
        placeFiles(ftp, config["backUp"], config["workDir"])
    print("备份完成")
    time.sleep(int(config["interval"]))
