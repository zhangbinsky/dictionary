"""
二级界面
"""

def fun():
    while True:
        print("""
               1. 查词 2.历史  3.注销
           """)

        cmd = input(">>")
        if cmd == '1':
            pass
        elif cmd == '2':
            pass
        elif cmd == '3':
            break

while True:
    print("""
        1. 注册 2.登录  3.退出
    """)

    cmd = input(">>")
    if cmd == '1':
        fun()
    elif cmd == '2':
        fun()
    elif cmd == '3':
        break