import xlwings as xw
from tkinter import messagebox
import sys


class to_Inspectionsheet:
    def __init__(self, value_dict, sheet):
        """
        成績書原紙シートへ入力
        :param value_dict:PysimpleGuiで取得したvalues
        :param sheet: データ入力用シート
        """
        self.inspect_day = value_dict["-inspect_day-"]
        self.ship_day = value_dict["-shipping_day-"]
        self.qty = value_dict["-qty-"]
        self.order_no = value_dict["-order_no-"]
        self.order_no2 = value_dict["-order_no2-"]
        self.delivery_day = value_dict["-delivery_day-"]
        self.send = value_dict["send"]
        self.machine_no1 = value_dict["-machine_no-"]
        self.lot1 = value_dict["-lot1-"]
        self.lot2 = value_dict["-lot2-"]
        self.machine_no2 = value_dict["-machine_no2-"]
        self.lot3 = value_dict["-lot3-"]
        self.lot4 = value_dict["-lot4-"]
        self.arrivale_day = value_dict["-arrival_day-"]
        self.measure_day = value_dict["-measure_day-"]
        self.ws = sheet
        self.bag_qty = 500
        self.box1 = value_dict["box1"]
        self.box2 = value_dict["box2"]

    def inpput_data(self):
        """
        ワークシートへの入力
        """
        # GUIで入力した文字をワークシートへ入力
        self.ws.range("B1").value = self.inspect_day
        self.ws.range("B2").value = self.ship_day
        self.ws.range("B3").value = self.qty
        self.ws.range("B4").value = self.order_no
        self.ws.range("B5").value = self.order_no2
        self.ws.range("B6").value = self.delivery_day
        self.ws.range("B7").value = self.send
        self.ws.range("B8").value = self.machine_no1
        self.ws.range("B9").value = self.lot1
        self.ws.range("B10").value = self.lot2
        self.ws.range("B11").value = self.machine_no2
        self.ws.range("B12").value = self.lot3
        self.ws.range("B13").value = self.lot4
        self.ws.range('B14').value = self.arrivale_day
        self.ws.range('B15').value = self.measure_day

        # ワークシート記入用の計算式を受け取る
        cal1, cal2, cal3, cal_qty = self.cal_lot(self.lot1, self.lot2, self.lot3, self.lot4)
        # 計算式を入力　袋数の計算
        self.ws.range('B16').value = cal1
        self.ws.range('B17').value = cal2
        self.ws.range("B18").value = cal3
        self.cal_qty = cal_qty

        cal_box_qty1, cal_box_qty2 = self.cal_box_qty(box1=self.box1, box2=self.box2, bag_qty=self.bag_qty,
                                                      qty=self.qty)
        self.ws.range("B19").value = cal_box_qty1
        self.ws.range("B20").value = cal_box_qty2

        cal_ship_qty1, cal_ship_qty2 = self.cal_ship_qty(box1=self.box1, box2=self.box2, qty=self.qty)
        self.ws.range("B21").value = cal_ship_qty1
        self.ws.range('B22').value = cal_ship_qty2

    def cal_lot(self, lot1, lot2, lot3, lot4):
        """
        :param lot1: lot1を渡す
        :param lot2: lot2を渡す
        :param lot3: lot3を渡す
        :param lot4: lot4を渡す
        :return:計算式を返す
        """

        if lot3 == '-' and lot4 == '-':
            # 袋数を計算
            self.result = int(lot2) - int(lot1) + 1
            # シートへ書き込む用の計算式を作成　袋数計算
            self.str_cal1 = "(" + lot2 + "-" + lot1 + ")" + "+" + "1" + "=" + str(self.result)
            # シートへ書き込む用の計算式を作成　員数計算
            bags = self.result
            qty_result = self.bag_qty * bags
            self.str_cal3 = str(bags) + "×" + str(self.bag_qty) + "=" + str(qty_result)

            self.str_cal2 = ''

            return self.str_cal1, self.str_cal2, self.str_cal3, qty_result

        elif lot3 != '-' and lot4 == '-':
            # 袋数を計算
            self.result = int(lot2) - int(lot1) + 1
            # シートへ書き込む用の計算式を作成　袋数計算
            self.str_cal1 = "(" + lot2 + "-" + lot1 + ")" + "+" + "1" + "=" + str(self.result)
            # シートへ書き込む用の計算式を作成　員数計算
            bags = self.result
            qty_result = self.bag_qty * (bags + 1)
            self.str_cal3 = str(bags) + "×" + str(self.bag_qty) + "=" + str(qty_result)
            self.str_cal2 = ''
            return self.str_cal1, self.str_cal2, self.str_cal3, qty_result

        else:
            # 袋数を計算
            self.result = int(lot2) - int(lot1) + 1
            self.result2 = int(lot4) - int(lot3) + 1
            # シートへ書き込む用の計算式を作成 袋数計算
            self.str_cal1 = "(" + lot2 + "-" + lot1 + ")" + "+" + "1" + "=" + str(self.result)
            self.str_cal2 = "(" + lot4 + "-" + lot3 + ")" + "+" + "1" + "=" + str(self.result2)
            # シートへ書き込む等の計算式を作成　員数計算
            bags = self.result + self.result2
            qty_result = self.bag_qty * bags
            self.str_cal3 = str(bags) + "×" + str(self.bag_qty) + "=" + str(qty_result)
            return self.str_cal1, self.str_cal2, self.str_cal3, qty_result

    # 1ケースの梱包数を計算
    def cal_box_qty(self, qty, box1, box2, bag_qty):

        if box2 == "-":
            no_of_bags = int(box1) / int(bag_qty)
            no_of_bags = int(no_of_bags)
            cal_box_qty1 = str(bag_qty) + "個/袋" + "×" + str(no_of_bags) + "袋" + "=" + str(box1) + "個/ケース"
            cal_box_qty2 = ''
            return cal_box_qty1, cal_box_qty2

        else:
            no_of_bags = int(box1) / int(bag_qty)
            no_of_bags = int(no_of_bags)
            cal_box_qty1 = str(bag_qty) + "個/袋" + "×" + str(no_of_bags) + "袋" + "=" + str(box1) + "個/ケース"
            no_of_bags2 = int(box2) / int(bag_qty)
            no_of_bags2 = int(no_of_bags2)
            cal_box_qty2 = str(bag_qty) + "個/袋" + "×" + str(no_of_bags2) + "袋" + "=" + str(box2) + "個/ケース"
            return cal_box_qty1, cal_box_qty2

    def cal_ship_qty(self, box1, box2, qty):
        if box2 == "-":
            no_of_carton = int(qty) // int(box1)
            ship_qty1 = int(no_of_carton) * int(box1)
            cal_ship_qty1 = str(box1) + "個/ケース" + "×" + str(no_of_carton) + "ケース" + "=" + str(ship_qty1) + "個"
            cal_ship_qty2 = ''
            return cal_ship_qty1, cal_ship_qty2

        else:
            no_of_carton = int(qty) // int(box1)
            ship_qty1 = int(no_of_carton) * int(box1)
            ship_qty2 = 1 * int(box2)
            cal_ship_qty1 = str(box1) + "個/ケース" + "×" + str(no_of_carton) + "ケース" + "=" + str(ship_qty1) + "個"
            cal_ship_qty2 = str(box2) + "個/ケース" + "×" + "1" + "ケース" + "=" + str(ship_qty2) + "個"
            return cal_ship_qty1, cal_ship_qty2
