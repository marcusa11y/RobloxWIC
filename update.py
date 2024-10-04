import requests as _0
import subprocess as _1
import sys as _2
from time import sleep as _3

class _4():
    def __init__(self):
        self._5 = '1.8.8'
        self._6 = 'https://raw.githubusercontent.com/marcusa11y/RobloxWIC//update.py'
        self._7 = 'https://github.com/https://github.com/marcusa11y/RobloxWIC//archive/refs/heads/RobuxWIC.zip'
        self._8()

    def _8(self):
        _9 = _0.get(self._6).text
        if f"self._5 = '{self._5}'" in _9:
            print('This version is up to date!')
            _3(1)
            _2.exit(0)
        else:
            print('''
                    ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                    ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                    ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                    ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                    ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                                      Your version of RobuxWIC is outdated!''')
            _A = input('\nWould you like to update? (y/n): ')
            if _A.lower() == 'y':
                print('Downloading Update...')
                _B = _0.get(self._7)
                with open("Update.zip", 'wb') as _C:
                    _C.write(_B.content)

                _1.Popen([_2.executable, '\\updater.py'])
                _2.exit(2)
            if _A.lower() == 'n':
                _2.exit(0)

if __name__ == '__main__':
    _4()