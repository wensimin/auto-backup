import json


def load_config():
    """加载json格式配置"""
    with open("config.json", "r+") as f:
        c = json.loads(f.read())
        return c


def save_config(c):
    """保存配置信息至文件"""
    with open("config.json", "w") as f:
        f.write(json.dumps(c))

