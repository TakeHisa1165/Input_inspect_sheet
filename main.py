"""
メイン制御用プログラム
"""
import gui
import r_csv


# path.csvからファイルパスを取得
rcsv = r_csv.ReadCsv()
file_path, dir_path = rcsv.read_csv()


# GUI起動
app = gui.InputGui(file_path, dir_path)
app.gui()
