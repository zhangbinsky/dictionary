"""
发送请求,获得结果
"""

from socket import *
from getpass import getpass
import sys

# 服务器地址
ADDR = ('127.0.0.1',8000)
s = socket()
s.connect(ADDR)

# 注册函数
def do_register():
  while True:
    name = input("User:")
    passwd = getpass()
    passwd_ = getpass('Again:')

    if passwd != passwd_:
      print("两次密码不一致")
      continue
    if (' ' in name) or (' ' in passwd):
      print("用户名或密码不能有空格")
      continue


    msg = "R %s %s"%(name,passwd)
    s.send(msg.encode()) # 发送请求
    data = s.recv(128).decode() # 接收反馈信息
    if data == 'OK':
      print("注册成功")
      login(name)
    else:
      print("注册失败")
    return

# 登录处理
def do_login():
  name = input("User:")
  passwd = getpass()

  msg = "L %s %s"%(name,passwd)
  s.send(msg.encode())  # 发送请求
  data = s.recv(128).decode()
  if data == 'OK':
    print("登录成功")
    login(name)
  else:
    print("登录失败")

# 单词查找
def do_query(name):
  while True:
    word = input("单词:")
    if word == '##': # 结束单词查询
      break
    msg = "Q %s %s"%(name,word)
    s.send(msg.encode())
    # 直接发送查询结果(或者没找到)
    data = s.recv(2048).decode()
    print(data)

#历史记录
def do_hist(name):
  msg = "H %s"%name
  s.send(msg.encode())
  data = s.recv(128).decode()
  if data == 'OK':
    while True:
      data = s.recv(1024).decode()
      if data == '##':
        break
      print(data)
  else:
    print("没有历史记录")

def login(name):
    while True:
        print("""
            ===============Query=============
            1. 查单词     2.历史记录     3.注销
            =================================
        """)
        cmd = input("输入选项:")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确选项")

# 链接服务器
def main():
    while True:
        print("""
            ===========Welcome=============
            1. 注册     2.登录      3.退出
            ===============================
        """)
        cmd = input("输入选项:")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")

main()