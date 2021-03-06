#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import os
from rich import print
from rich.markdown import Markdown


CLEAR = "cls" if os.name == "nt" else "clear"
SERVER_PWD = ""
SERVER_USER = ["root"]
IP_PRE = ["115.13.74.213", "153.86.118.134"]


DEPLOY_DOC = Markdown("""
# ðé¨ç½²æç¨

> ç´æ¥è¿è¡ `server` å³å¯å¯å¨å·¥å·

* å®è£ `JupyterLab`: https://github.com/mesondzh/internet-memory-backup/blob/main/post/jekyll/2018-11-03-build-jupyterlab-server.md

```shell
jupyter lab --generate-config
jupyter lab password
from notebook.auth import passwd
passwd()
```

* éç½® `JupyterLab` ç»ç«¯ `Shell`: https://github.com/jupyter/notebook/blob/d145301b5583366fc0c5e938ded80f07a0bc1bbf/notebook/terminal/__init__.py#L21-L23

* æ£æ¥ `Jupyter` åæ ¸

```shell
jupyter kernelspec list
jupyter kernelspec remove <kernel_name> 
```

* `WSL` å®è£ `sshpass` å¹¶éç½®èæ¬ç¯å¢åé

```shell
sudo apt-get install sshpass
vi /etc/profile
export PATH="/home/debian/app:$PATH"
source /etc/profile
sudo mv auto_login.py ~/app/server & chmod +x -R ~/app/server
```

* å¸¸ç¨å½ä»¤

```shell
/etc/init.d/ssh restart
```
""")

CMD_HELP = """
[bold yellow]ðððæ¬¢è¿è¿å¥ [bold green]AutoLogin[/bold green] v0.01[/bold yellow]

[bold green]help)[/bold green] æ¥çå¸®å© | h
[bold green]ssh)[/bold green] ç»å½èç¹ | login
[bold green]list)[/bold green] èç¹åè¡¨
[bold green]deploy)[/bold green] é¨ç½²æç¨
[bold green]exit)[/bold green] éåºç³»ç» | q | Ctrl+C

----------------------------------------------------------------
"""


def print_menu():
    print(CMD_HELP)


class AutoLogin(object):
    def __init__(self):
        self.SERVER_PWD = SERVER_PWD
        self.SERVER_USER = SERVER_USER
        self.IP_PRE = list(map(lambda x: ".".join(x.split(".")[:-1]) + ".", IP_PRE))

    def __login(self, ip, user, password):
        hidden = "*"*6
        print("--------------------------------------------------------------------------")
        print("[bold yellow]>>> å°è¯ç»å½èç¹ï¼IP={} USER={} PASSWORD={}[/bold yellow]".format(ip, hidden, hidden))
        cmd = "sshpass -p {} ssh {}@{} -q -o StrictHostKeyChecking=no".format(password, user, ip)
        result = os.system(cmd)
        return result

    def _pre_login(self, ip):
        for user in self.SERVER_USER:
            result = result = self.__login(ip, user, self.SERVER_PWD)
            if result == 0:
                return result
        return result

    def login(self, input_ip):
        self.dot_count = input_ip.count(".")
        if (self.dot_count == 0):
            for _ip in self.IP_PRE:
                ip = _ip + input_ip
                result = self._pre_login(ip)
                if result == 0:
                    return
        if (self.dot_count == 1):
            for _ip in self.IP_PRE:
                if input_ip.split(".")[0] in _ip:
                    index = self.IP_PRE.index(_ip)
                    ip = self.IP_PRE[index] + input_ip.split(".")[-1]
                    result = self._pre_login(ip)
                    if result == 0:
                        return
        elif (self.dot_count == 3):
            result = self._pre_login(input_ip)
            if result == 0:
                return


def main():
    server = AutoLogin()
    os.system(CLEAR)
    print_menu()
    while True:
        try:
            print("[bold cyan]>>> [/bold cyan]", end="")
            command = input().lower().strip()
            if command == "help" or command == "h":
                os.system(CLEAR)
                print_menu()
            elif command == "exit" or command == "q":
                os.system(exit())
            elif command == "deploy":
                os.system(CLEAR)
                print(DEPLOY_DOC)
            elif command == "list":
                print(IP_PRE) 
            elif command.startswith("ssh")or command.startswith("login"):
                ip = command.split(" ")[-1]
                print(ip)
                server.login(ip)
            elif command == "cls" or command == "clear":
                os.system(CLEAR)
                print_menu()
            else:
                os.system(command)
        except KeyboardInterrupt:
            os.system(exit())
        except Exception as e:
            print_menu()
            print("[bold red]âåé¨éè¯¯ï¼[/bold red]{}".format(e))


if __name__ == "__main__":
    main()
