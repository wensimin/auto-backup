import os
from ftplib import error_perm


def placeFiles(ftp, path, bash_path="/"):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("上传文件", bash_path + name, localpath)
            ftp.storbinary('STOR ' + bash_path + name, open(localpath, 'rb'))
        elif os.path.isdir(localpath):
            print("创建目录", bash_path + name)
            try:
                ftp.mkd(bash_path + name)
            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'):
                    raise
            print("移动到", bash_path + name)
            ftp.cwd(bash_path + name)
            placeFiles(ftp, localpath, bash_path + name + "/")
            print("移动到", "..")
            ftp.cwd("..")
