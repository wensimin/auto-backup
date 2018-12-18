# auto-backup
自动备份文件夹上传至ftp  

bulid 使用 `pyinstaller Application.py -F --noconsole`  手动加入config.json  

config.json中支持全部变量修改,GUI不支持超时时间设置和端口设置  
支持中文需要修改ftplib.py中的encoding为UTF-8  
releases版本支持中文  
