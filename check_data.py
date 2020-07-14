"""
数量チェック用モジュール
"""
import sys
import PySimpleGUI as sg


class CheckData:
    def __init__(self, qty, cal_qty):
        self.qty = qty
        self.cal_qty = cal_qty

    def check_qty(self):
        if str(self.qty) != self.cal_qty:
            sg.theme('systemdefault')
            sg.popup_error("入力された出荷数とロット番号から計算した出荷数が違います。", title="数量エラー")
            sys.exit()

        else:
            pass


if __name__ == "__main__":
    a = CheckData(qty=1000, cal_qty=2000)
    a.check_qty()
