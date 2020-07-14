"""
原紙ファイルのファイルパスをcsvに書き出し
"""

import csv
import os

class WriteCsv:
    def __init__(self):
        pass

    # ファイルパスをCSVに書き出し
    def write_csv(self, path_dict):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open('path.csv', 'w', newline='') as csvfile:
            fieldnames = ["file_path", "dir_path"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(path_dict)