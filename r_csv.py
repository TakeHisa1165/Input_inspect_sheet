import csv
import os
import PySimpleGUI as sg
import gui


class ReadCsv:
    def __init__(self):
        self.sf = gui.SelectFile()

    def read_csv(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            with open("path.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    file_path = row["file_path"]
                    if file_path == "":
                        sg.popup_ok('原紙ファイルの設定が間違っています。\n設定をやり直してください。')
                        self.sf.select_file()
                    print("file_path={}".format(file_path))
                    return file_path

        except FileNotFoundError:
            sg.popup_ok("初期設定が必要です。\n次の画面で検査成績書原紙ファイルを選んでください")
            self.sf.select_file()