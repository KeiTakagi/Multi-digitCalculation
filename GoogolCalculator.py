#! /usr/local/bin/python3.5.3
'''
 Googole Calculator
 電卓の名前は10の100乗を表すGoogoleからとってGoogole Calculator(グーゴルカルキュレーター）としました

 Copyright (c) 2018 Kei Takagi
 Released under the MIT license
 http://opensource.org/licenses/mit-license.php
 

'''

import getch
import TaketaCalc
import sys
import os


class GoogolCalculator:

    VERSION = '1.0'

    def run(self):
        buf = ''
        buf1 = ''
        op = ''
        mode = 0

        calObj = TaketaCalc.TaketaCalc()

        self.cls()  # 画面クリア
        print(
            '\033[07m\033[31mG\033[33mo\033[32mo\033[34mg\033[36mo\033[35ml\033[0m', end='', flush=True)
        print(' ', end='', flush=True)
        print('\033[37m\033[08mCalculator\033[0m\n', end='', flush=True)
        print('\033[07m          ' + 'Ver ', end='', flush=True)
        print(self.VERSION + '   \033[0m' + '\n\n', end='', flush=True)

        while(True):
            key = ord(getch.getch())
            c = chr(key)

            if key == 3:  # Ctrl-C: 終了
                print('bye!!\n', end='', flush=True)
                break
            if key == 8 or key == 127:  # バックスペースキー
                if len(buf) > 0:
                    buf = buf[:-1]
                    buf1 = buf
                    print('\b \b', end='', flush=True)
            if key == 9:  # タブキー
                self.cls()  # 画面クリア
                buf = ''
                buf1 = ''
                buf2 = ''
                op = ''
                mode += 1
                if mode == 1:
                    # PI MODE (モンテカルロ法)
                    digit = 0
                    incremental = 10000
                    count = 0
                    print('PI MODE\n', end='', flush=True)
                elif mode == 2:
                    # POWER OFF
                    print('\033[31mPOWER OFF\033[0m\n', end='', flush=True)
                else:
                    # CALC MODE
                    print('Calculation MODE\n',
                          end='', flush=True)
                    mode = 0

            if key == 13:  # リターンキー
                if mode == 0:
                    # CALC MODE
                    if len(buf1) > 0 and len(op) > 0 and len(buf) > 0:
                        # 正しく入力されていたら四則演算を実行
                        print('\n\033[36mCalculating...\033[0m',
                              end='', flush=True)

                        buf2 = buf
                        if '+' == op:
                            ans = calObj.add(buf1, buf2)
                        elif '-' == op:
                            ans = calObj.sub(buf1, buf2)
                        elif '*' == op:
                            ans = calObj.mul(buf1, buf2)
                        elif '/' == op:
                            ans = calObj.div(buf1, buf2)

                        print('\n' + ans, end='', flush=True)
                        buf = ans
                        buf1 = ans
                        buf2 = ''
                        op = ''
                    else:
                        buf = ''
                        buf1 = ''
                        buf2 = ''
                        op = ''
                        print('\n', end='', flush=True)

                elif mode == 1:
                    # PI MODE
                    digit += incremental
                    count, ans = calObj.piMode(digit, incremental, count)
                    print('\nn=' + str(digit) + ', PI=' +
                          ans, end='', flush=True)

                elif mode == 2:
                    if os.name == 'nt':
                        # EXIT
                        print('bye!!\n', end='', flush=True)
                        break
                    else:
                        # POWER OFF
                        os.system("sudo sync")
                        os.system("sudo sync")
                        os.system("sudo sync")
                        os.system("sudo poweroff")

            elif mode == 0 and (('0' <= c and c <= '9')or c == '.'):  # 数字(0-9)
                buf += c
                print(c, end='', flush=True)

            elif mode == 0 and ('+' == c or '-' == c or '*' == c or '/' == c):  # 四則演算
                if op == '':
                    buf1 = buf
                    buf = ''
                    op = c
                    print(' ' + c + ' ', end='', flush=True)

    def cls(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


obj = GoogolCalculator()
obj.run()
