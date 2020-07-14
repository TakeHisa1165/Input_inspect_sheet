import xlwings as xw
import PySimpleGUI as sg

class FileSave:
    def __init__(self, wb, ws, dir_path):
        """
        上書き保存と新規保存のためのクラス
        :param wb: ワークブックを渡す
        :param ws: ワークシートを渡す
        :param dir_path: 保存先フォルダのpathを渡す
        """
        self.wb = wb
        self.ws = ws
        self.dir_path = dir_path

    def save_file(self):
        self.wb.save()

    def new_file_save(self, file_date):
        pass
        self.wb.save()
        self.wb.save(self.dir_path + "検査成績書AF-M-184030" + "(" + file_date + ")" + ".xlsm")