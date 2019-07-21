"""
服务端
功能: 处理用户请求,处理数据
"""

from socket import *
from multiprocessing import Process
import signal,sys
from dict_db import Database
from time import sleep

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)
db = Database(database='dict')


# 注册处理
def do_register(c,data):
  tmp = data.split(' ')
  name = tmp[1]
  passwd = tmp[2]

  if db.register(name,passwd):
      c.send(b'OK')
  else:
      c.send(b'Fail')

def do_login(c,data):
  tmp = data.split(' ')
  name = tmp[1]
  passwd = tmp[2]

  if db.login(name,passwd):
      c.send(b'OK')
  else:
      c.send(b'Fail')

# 查询单词
def do_query(c,data):
  tmp = data.split(' ')
  name = tmp[1]
  word = tmp[2]

  db.insert_history(name,word) # 插入历史记录

  # 找到返回解释,没找到返回None
  mean = db.query(word)
  if not mean:
    c.send("没有找到该单词".encode())
  else:
    msg = "%s : %s"%(word,mean)
    c.send(msg.encode())

# 历史记录
def do_hist(c,data):
  name = data.split(' ')[1]
  r = db.history(name)
  if not r:
    c.send(b'Fail')
    return
  c.send(b'OK')

  for i in r:
    # i-->(name,word,time)
    msg = "%s   %-16s    %s"%i
    sleep(0.1)
    c.send(msg.encode())
  sleep(0.1)
  c.send(b'##')

# 处理具体客户端请求
def request(c):
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,data)
        elif data[0] == 'L':
            do_login(c,data)
        elif data[0] == 'Q':
            do_query(c,data)
        elif data[0] == 'H':
            do_hist(c,data)

# 搭建网络模型
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    print("Listen the port 8000")
    # 循环等待客户端链接
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #  创建新的进程
        p = Process(target = request,args=(c,))
        p.daemon = True
        p.start()

main()
