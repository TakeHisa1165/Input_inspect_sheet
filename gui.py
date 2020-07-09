"""
検査成績書入力用GUI
"""

import sys
import PySimpleGUI as sg
import w_csv
import xlwings as xw
import input_to_inspectsheet


class InputGui:
    """
    検査成績書入力用フォーム表示
    """
    def __init__(self, file_path):
        """
        入力用フォームの表示と原紙ファイルを開く
        :param file_path: path.csvから読み込んだ原紙のファイルパス
        """
        self.inspect_sheet_book = xw.Book(file_path)
        self.input_sheet = self.inspect_sheet_book.sheets('検査成績(完全簡易）本社向け')
        self.data_sheet = self.inspect_sheet_book.sheets("データ入力")

    def gui(self):
        # テーマ設定
        sg.theme('systemdefault')

        frame1 = [
            [sg.Radio('成績書を送る', 1, key="送る", font=('メイリオ', 14))],
            [sg.Radio('成績書を送らない', 1, key="送らない", font=('メイリオ', 14))],
        ]
        frame2 = [
            [sg.Submit(button_text="実行", size=(12, 2), font=('メイリオ', 14))],
        ]
        frame3 = [
            [sg.Submit(button_text="途中保存", size=(12, 2), font=('メイリオ', 14))]
        ]

        layout = [
            [sg.MenuBar([['設定', ["Excelファイル選択"]]])],
            [sg.Text("検査日", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-inspect_day-")],
            [sg.Text("出荷日", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-shipping_day-")],
            [sg.Text("出荷数", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-qty-")],
            [sg.Text('指示書番号', size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-order_no-")],
            [sg.Text("引き当て番号", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-order_no2-")],
            [sg.Text("客先納期", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-delivery_day-")],
            [sg.Text("設備番号、西暦", size=(12, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-machine_no-"),
             sg.Text("ロット番号", size=(8, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-lot1-"),
             sg.Text("～", size=(1, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-lot2-")],
            [sg.Text("設備番号、西暦", size=(12, 1), font=('メイリオ', 14)),sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-machine_no2-"),
             sg.Text("ロット番号", size=(8, 1), font=('メイリオ', 14)),sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-lot3-"),
             sg.Text("～", size=(1, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), font=('メイリオ', 14), key="-lot4-")],
            [sg.Text("青島入荷日", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-arrival_day-")],
            [sg.Text("測定日", size=(12, 1), font=('メイリオ', 14)), sg.InputText(font=('メイリオ', 14), key="-measure_day-")],
            [sg.Text('入り数➀', size=(10, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), key="box1", font=('メイリオ', 14)),
             sg.Text("入り数➁", size=(12, 1), font=('メイリオ', 14)), sg.InputText(size=(10, 1), key="box2", font=('メイリオ', 14))],
            [sg.Frame("成績書送付", frame1, font=('メイリオ', 14)), sg.Frame("入力", frame2, font=('メイリオ', 14)), sg.Frame("途中保存", frame3, font=('メイリオ', 14))],
        ]

        window = sg.Window("AF-M-184030  成績書情報入力", layout)

        while True:
            event, values = window.read()
            if event is None:
                print('exit')
                sys.exit()

            if event == "実行":
                value_dict = values

                if values["送る"]:
                    value_dict["send"] = "送る"

                elif values["送らない"]:
                    value_dict["send"] = '送らない'

                # innput_to_inspectsheetのインスタンス
                iti = input_to_inspectsheet.to_Inspectionsheet(value_dict, sheet=self.data_sheet)
                iti.inpput_data()

            if event == "Excelファイル選択":
                sf = SelectFile()
                sf.select_file()

            if event == '途中保存':
                print('test')

        window.close()


class SelectFile:
    def __init__(self):
        pass

    def select_file(self):
        sg.theme("systemdefault")

        layout = [
            [sg.Text(text='検査成績書の原紙ファイルを選択してください', font=('メイリオ', 14))],
            [sg.InputText(font=('メイリオ', 14), size=(50, 1), key="-path-"), sg.FileBrowse(button_text="開く", font=('メイリオ', 14))],
            [sg.Submit(button_text="設定", font=('メイリオ', 14))]
        ]

        window = sg.Window("検査成績書原紙ファイル選択", layout)

        while True:
            event, values = window.read()
            if event is None:
                print("exit")
                sys.exit()

            if event == "設定":
                path_dict = {}
                path_dict["file_path"] = values["-path-"]
                print(path_dict)
                wcsv = w_csv.WriteCsv()
                wcsv.write_csv(path_dict=path_dict)
                sg.popup_ok('原紙ファイルの設定が完了しました。\nアプリを再起動してください。')
                sys.exit()


if __name__ == '__main__':
    a = SelectFile()
    a.select_file()
