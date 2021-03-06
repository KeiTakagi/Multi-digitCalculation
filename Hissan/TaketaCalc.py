#! /usr/local/bin/python3.5.3
'''
 多桁計算(かけ算・わり算を筆算で解いたバージョン)

 Copyright (c) 2018 Kei Takagi
 Released under the MIT license
 http://opensource.org/licenses/mit-license.php

'''


import random


class TaketaCalc:

    # 桁数の設定
    KETA = 100

    #
    # テスト
    #
    def test(self):
        try:
            x = 0
            y = 0
            wk = ''
            print('TEST START!!')

            # print(self.mul('-0.9', '0.1'))
            wk = '+'
            for x in range(-1000, 1000, 10):
                for y in range(-1000, 1000, 10):
                    tx = round(x*0.01, 5)
                    ty = round(y*0.01, 5)

                    a = self.add(str(tx), str(ty))
                    b = tx + ty
                    c = round(b, 3)
                    if(str(c).find('.') > 0):
                        c = str(c).rstrip('0')
                        c = str(c).rstrip('.')
                    if a != c:
                        print("NG " + str(tx) + " + " + str(ty) +
                              " = " + str(a) + " = " + str(c))

            wk = '-'
            for x in range(-1000, 1000, 10):
                for y in range(-1000, 1000, 10):
                    tx = round(x*0.01, 5)
                    ty = round(y*0.01, 5)

                    a = self.sub(str(tx), str(ty))
                    b = tx - ty
                    c = round(b, 3)
                    if(str(c).find('.') > 0):
                        c = str(c).rstrip('0')
                        c = str(c).rstrip('.')
                    if a != c:
                        print("NG " + str(tx) + " - " + str(ty) +
                              " = " + str(a) + " = " + str(c))

            wk = '*'
            for x in range(-1000, 1000, 10):
                for y in range(-1000, 1000, 10):
                    tx = round(x*0.01, 5)
                    ty = round(y*0.01, 5)

                    a = self.mul(str(tx), str(ty))
                    b = tx * ty
                    c = round(b, 5)
                    if(str(c).find('.') > 0):
                        c = str(c).rstrip('0')
                        c = str(c).rstrip('.')
                    if a != c:
                        print("NG " + str(tx) + " * " + str(ty) +
                              " = " + str(a) + " = " + str(c))

            wk = '/'
            for x in range(-1000, 1000, 10):
                for y in range(-1000, 1000, 10):
                    if y == 0:
                        continue
                    tx = round(x*0.001, 5)
                    ty = round(y*0.001, 5)

                    a = self.div(str(tx), str(ty))
                    b = tx / ty
                    if (abs(float(a)) - abs(float(b))) > 0.00001:
                        if a != str(b).replace('.0', ''):
                            print("NG " + str(tx) + " / " + str(ty) +
                                  " = " + str(a) + " = " + str(b))

            print('DONE!!')
        except Exception as e:
            print("NG " + str(x) + " " + wk + " " + str(y))
            raise

    #
    # 比較
    #
    # 復帰値:
    #   x　が大きい場合  1
    #   y  が大きい場合 -1
    #   x　と　yが等しい 0
    #
    def comp(self, x, y):
        try:
            ret = 0

            # xに-が含まれているか検索
            xSign = x.find('-')
            # yに-が含まれているか検索
            ySign = y.find('-')

            # xに.が含まれているか検索
            xPit = x.find('.')
            # yに.が含まれているか検索
            yPit = y.find('.')

            # xの長さ
            xLen = len(x)
            # yの長さ
            yLen = len(y)

            if xSign == -1 and ySign != -1:
                ret = 1  # xが大きい
            elif xSign != -1 and ySign == -1:
                ret = -1  # yが大きい
            elif xPit > yPit:
                ret = 1  # xが大きい
            elif xPit < yPit:
                ret = -1  # yが大きい
            elif xLen > yLen:
                ret = 1  # xが長い
            elif xLen < yLen:
                ret = -1  # yが長い
            else:
                if xLen > yLen:
                    # xbufの右を0で埋める
                    for num in range(xLen - yLen):
                        y += '0'

                elif xLen < yLen:
                    # zbufの右を０で埋める
                    for num in range(yLen - xLen):
                        y += '0'

                buffLen = max(xLen, yLen)

                for num in range(buffLen):
                    if x[num] != y[num]:
                        if int(x[num]) > int(y[num]):  # xが大きい
                            ret = 1
                            break
                        elif int(x[num]) < int(y[num]):  # yが大きい
                            ret = -1
                            break
            return ret

        except Exception as e:
            raise

    #
    # 小数点の位置を変更する:pointPosition
    #
    def pointPosition(self, sign, afterDecPointLen, buffLen, carry, ans):
        try:

            # 小数点をつけなおす
            if afterDecPointLen > 0:
                point = buffLen - afterDecPointLen + carry
                ans = ans[0:point] + '.' + ans[point:]
                # 小数点があるときだけ右の０をトリム
                ans = ans.rstrip('0')
                #　小数点だけだとトリム
                ans = ans.rstrip('.')

            # 左の０をトリム
            if len(ans) > 1:
                ans = ans.lstrip('0')
                # 左の文字が.から始まる場合は０をつける
                if len(ans) == 0:
                    ans = '0'
                elif ans[0] == '.':
                    ans = '0' + ans

            # 符号処理
            if sign == 1:
                ans = '-' + ans
            return ans
        except Exception as e:
            raise

    #
    # 桁揃え:alignment
    #
    def alignment(self, xin, yin):
        try:
            # -を除去
            xin = xin.replace('-', '')
            yin = yin.replace('-', '')

            # 整数部と小数部の分離
            xList = xin.split('.')
            xCount = len(xList)
            yList = yin.split('.')
            yCount = len(yList)

            # 整数部
            xbuf = xList[0]
            xlen = len(xbuf)
            ybuf = yList[0]
            ylen = len(ybuf)

            if xlen > ylen:
                # ybufの左を０で埋める
                ybuf = ybuf.zfill(xlen)
            elif xlen < ylen:
                # zbufの左を０で埋める
                xbuf = xbuf.zfill(ylen)

            xWork = xbuf
            yWork = ybuf

            # 小数部
            xlen = 0
            xbuf = ''
            if xCount == 2:
                xbuf = xList[1]
                xlen = len(xbuf)
            ylen = 0
            ybuf = ''
            if yCount == 2:
                ybuf = yList[1]
                ylen = len(ybuf)

            if xlen > ylen:
                # xbufの右を0で埋める
                for num in range(xlen - ylen):
                    ybuf += '0'

            elif xlen < ylen:
                # zbufの右を０で埋める
                for num in range(ylen - xlen):
                    xbuf += '0'

            # 小数点以下の桁数
            afterDecPointLen = len(xbuf)

            xWork = xWork + xbuf
            yWork = yWork + ybuf

            # 不要変数開放
            del xin
            del yin
            del xbuf
            del ybuf

            return xWork, yWork, afterDecPointLen
        except Exception as e:
            raise

    #
    # たし算:addition
    #
    def add(self, xin, yin):
        try:
            sign = 0
            # 符号処理
            # xに-が含まれているか検索
            xSign = xin.find('-')
            # yに-が含まれているか検索
            ySign = yin.find('-')

            if xSign != -1 and ySign != -1:
                sign = 1  # マイナス同士のたし算
            elif xSign == -1 and ySign == -1:
                sign = 0  # プラス同士のたし算
            elif xSign == -1 and ySign != -1:
                # yがマイナス
                yin = yin.replace('-', '')
                return self.sub(xin, yin)
            elif xSign != -1 and ySign == -1:
                # xがマイナス
                xin = xin.replace('-', '')
                return self.sub(yin, xin)

            # 入力値の位を合わせる
            xin, yin, afterDecPointLen = self.alignment(xin, yin)

            # たし算処理
            # 初期化
            carry = 0
            buffLen = len(xin)
            ans = ''

            # 小さい桁からたし算するため文字列の並びを逆順にする
            xbuf = xin[::-1]
            ybuf = yin[::-1]

            # 文字数分ループ
            for num in range(buffLen):
                # 文字列から足したい桁を取り出して、文字から整数に戻してからたし算する
                wk = int(xbuf[num]) + int(ybuf[num]) + carry

                carry = 0
                if wk > 9:
                    # 繰りあがり
                    carry = 1
                    wk = wk - 10
                # たし算の結果は文字列に保存
                ans = str(wk) + ans

            if carry > 0:
                # ループを抜けた際、繰りあがりがあれば文字列の先頭に１をつける
                ans = '1' + str(ans)

            # 不要変数開放
            del xin
            del yin
            del xbuf
            del ybuf

            # 小数点位置をつけなおす
            return self.pointPosition(sign, afterDecPointLen, buffLen, carry, ans)

        except Exception as e:
            raise

    #
    # ひき算:subtraction
    #
    def sub(self, xin, yin):
        try:
            sign = 0
            # 符号処理
            # xに-が含まれているか検索
            xSign = xin.find('-')
            # yに-が含まれているか検索
            ySign = yin.find('-')

            # ひき算は(x>y x>=0 y>=0)の場合のみ有効
            if xSign != -1 and ySign == -1:
                # xに-が含まれている
                yin = '-' + yin
                return self.add(xin, yin)
            elif xSign == -1 and ySign != -1:
                # yに-が含まれている
                yin = yin.replace('-', '')
                return self.add(xin, yin)
            elif xSign != -1 and ySign != -1:
                # x,yに-が含まれている
                yin = yin.replace('-', '')
                xin = xin.replace('-', '')
                return self.sub(yin, xin)

            # 入力値の位を合わせる
            xin, yin, afterDecPointLen = self.alignment(xin, yin)

            # ひき算は(x>y x>=0 y>=0)の場合のみ有効
            ret = self.comp(xin, yin)
            if ret == 1:
                # xが大きい
                if xSign != -1 and ySign != -1:
                    sign = 1
                else:
                    sign = 0
            elif ret == 0:
                # xとyは等しい
                return '0'
            else:
                # yが大きい
                sign = 1
                work = xin
                xin = yin
                yin = work
                del work

            # ひき算処理
            # 初期化
            carry = 0
            buffLen = len(xin)
            ans = ''

            # 小さい桁からひき算するため文字列の並びを逆順にする
            xbuf = xin[::-1]
            ybuf = yin[::-1]

            # 文字数分ループ
            for num in range(buffLen):
                # 文字列からひきたい桁を取り出して、文字から整数に戻してからひき算する
                wk = int(xbuf[num]) - carry - int(ybuf[num])

                carry = 0
                if wk < 0:
                    # 繰り下がり
                    carry = 1
                    wk = 10 + wk

                # ひき算の結果は文字列に保存
                ans = str(wk) + ans

            # 不要変数開放
            del xin
            del yin
            del xbuf
            del ybuf

            # 小数点位置をつけなおす
            return self.pointPosition(sign, afterDecPointLen, buffLen, carry, ans)

        except Exception as e:
            raise

    #
    # かけ算：multiplication
    #
    def mul(self, xin, yin):
        try:
            # 符号処理
            # xに-が含まれているか検索
            xSign = xin.find('-')
            # yに-が含まれているか検索
            ySign = yin.find('-')

            if xSign == ySign:
                # 符号がおなじもの同士のかけ算
                sign = 0
            else:
                sign = 1

            # -を除去
            xin = xin.replace('-', '')
            yin = yin.replace('-', '')

            # 入力値の位を合わせる
            xin, yin, afterDecPointLen = self.alignment(xin, yin)
            afterDecPointLen = 2 * afterDecPointLen

            # 0に何をかけても0
            if len(xin.lstrip('0')) == 0:
                return '0'

            if len(yin.lstrip('0')) == 0:
                return '0'

            # かけ算処理
            # 初期化
            ans = ''
            total = ''
            carry = 0

            # 小さい桁からかけ算するため数値を逆転する
            xrbuf = xin[::-1]
            yrbuf = yin[::-1]

            zero = ''
            for numx in range(len(xin)):
                ans = ''
                carry = 0
                for numy in range(len(yin)):
                    wk = int(xrbuf[numx]) * int(yrbuf[numy]) + carry

                    carry = 0
                    if wk > 9:
                        # 繰り上げ
                        carry = wk // 10
                        wk = wk % 10
                    ans = str(wk) + ans

                if carry > 0:
                    # 繰り上げ
                    ans = str(carry) + str(ans)

                # たし算
                total = self.add(total, ans + zero)
                zero += '0'

            total = '0' * afterDecPointLen + total

            buffLen = len(total)

            # 不要変数開放
            del ans
            del zero
            del xin
            del yin

            # 小数点位置をつけなおす
            return self.pointPosition(sign, afterDecPointLen, buffLen, 0, total)

        except Exception as e:
            raise

    #
    # わり算：division
    #
    def div(self, xin, yin):
        try:
            # 符号処理
            # xに-が含まれているか検索
            xSign = xin.find('-')
            # yに-が含まれているか検索
            ySign = yin.find('-')

            if xSign == ySign:
                # 符号がおなじもの同士のわり算
                sign = 0
            else:
                sign = 1

            # -を除去
            xin = xin.replace('-', '')
            yin = yin.replace('-', '')

            # 入力値の位を合わせる
            xin, yin, afterDecPointLen = self.alignment(xin, yin)

            # yinの左の０を消去
            yin = yin.lstrip('0')
            # xinの左の０を消去
            xin = xin.lstrip('0')

            # 0は割れない
            if len(xin.lstrip('0')) == 0:
                return '0'

            # 0では割れない
            if len(yin.lstrip('0')) == 0:
                return '\033[31mZERO DIVISION ERROR\033[0m'

            # わり算処理
            # 初期化
            ans = ''
            subans = ''
            cnt = 0
            xlen = len(xin)
            ylen = len(yin)
            work = xin[0:ylen]

            point = False

            # 無限ループ
            while (True):

                # 上の位の桁からひき算
                subans = work
                subans = self.sub(subans, yin)

                if subans == '0':
                    # ひき算して０になった
                    cnt += 1
                    ans += str(cnt)
                    xlen -= ylen
                    xin = xin[ylen:]
                    work = xin[0:ylen]
                    if len(xin.lstrip('0')) == 0 :
                        # 割られる数が全て０になった
                        if xlen > 0:
                            ans += '0' * xlen
                        break
                    cnt = 0

                elif ('-' in subans) == True:
                    ans += str(cnt)
                    xlen -= 1
                    # マイナスの場合は引けなくなった
                    if xlen > ylen: 
                        # 下の位に値がある
                        xin = work + xin[1:]
                    else:
                        # 下の位に値がない
                        xin = work + '0'              
                        if point == False:
                            ans += '.'
                            point = True
                    work = xin[0:ylen+1]
                    cnt = 0
                else:
                    cnt += 1
                    work = subans

                if len(ans) >= int(self.KETA):
                    # 指定した桁数に達した場合ループを抜ける
                    ans = ans[0:self.KETA]
                    break

            pp = ans.find('.')
            if pp > 1:
                # 小数点がある場合の不要な0を消去
                ans = ans.lstrip('0')
            elif pp ==-1:
                # 小数点がない場合の不要な0を消去
                ans = ans.lstrip('0')

            # 符号処理
            if sign == 1:
                ans = '-' + ans

            # 不要変数開放
            del work
            del subans
            del xin
            del yin

            return ans

        except Exception as e:
            raise

    #
    # PI MODE：モンテカルロ法でπを計算
    #
    def piMode(self, digit, incremental, count):
        try:
            ans = ''
            for num in range(incremental):
                x = random.random()
                y = random.random()
                if x*x+y*y <= 1:
                    # 円に含まれる
                    count += 1

            ans = self.mul('4', str(count))
            ans = self.div(ans, str(digit))
            return count, ans

        except Exception as e:
            raise

'''
# TEST
obj = TaketaCalc()
obj.test()
'''
