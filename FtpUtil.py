import ftplib
import os
from ftplib import error_perm


def placeFiles(ftp, path, bash_path="/", log=lambda m: print(m)):
    if not bash_path.endswith("/"):
        bash_path += "/"
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            log("上传文件" + bash_path + name + localpath)
            ftp.storbinary('STOR ' + bash_path + name, open(localpath, 'rb'))
        elif os.path.isdir(localpath):
            log("创建目录" + bash_path + name)
            try:
                ftp.mkd(bash_path + name)
            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'):
                    raise
            ftp.cwd(bash_path + name)
            placeFiles(ftp, localpath, bash_path + name, log)
            ftp.cwd("..")


def downFiles(ftp, path, bash_path="/", log=lambda m: print(m)):
    if not path.endswith("/"):
        path += "/"
    for file in ftp.nlst(bash_path):
        remote_path = file
        name = os.path.basename(file)
        if is_ftp_dir(ftp, remote_path):
            new_path = os.path.join(path, name)
            os.mkdir(new_path)
            log("创建目录 " + new_path)
            downFiles(ftp, new_path, remote_path, log)
        else:
            local_path = os.path.join(path, name)
            with open(local_path, "wb") as f:
                log("下载文件 " + local_path)
                ftp.retrbinary('RETR %s' % remote_path, f.write)


def is_ftp_dir(ftp, path):
    try:
        ftp.cwd(path)
        return True
    except ftplib.error_perm:
        return False
