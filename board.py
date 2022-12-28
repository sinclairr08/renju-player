import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from algorithm import Renju


class BoardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_fbtns()
        self.turn = 0
        self.color = "white"
        self.board = Renju()

    def changecolor(self):
        if self.turn % 2 == 1:
            self.color = "black"

        else:
            self.color = "white"

    def getStyleSheet(self):
        if self.turn % 2 == 1:
            return "background-color:{};color:white".format(self.color)

        else:
            return "background-color:{}".format(self.color)

    def initUI(self):
        self.setWindowTitle("Gomoku")
        self.setWindowIcon(QIcon('image\gomokuIcon.png'))
        self.setStyleSheet("background:rgb(181, 139, 91)")
        self.setGeometry(300, 300, 640, 640)

        self.statusBar().showMessage('Ready')
        self.show()

    def init_fbtns(self):
        self.fbtns = []
        for i in range(15):
            fbtns_i = []
            for j in range(15):
                fbtn = QPushButton(self)
                fbtn.move(37 + i * 40, 37 + j * 40)
                fbtn.resize(6, 6)
                fbtn.setStyleSheet("background-color:red")

                fbtns_i.append(fbtn)
            self.fbtns.append(fbtns_i)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.hide_forbidden()

            raw_x = event.x()
            raw_y = event.y()

            if raw_x < 25 or raw_x > 615 or raw_y < 25 or raw_y > 615:
                self.statusBar().showMessage("Out of Bounds")
                return

            rem_x = ((raw_x + 15) / 40) - ((raw_x + 15) // 40)
            rem_y = ((raw_y + 15) / 40) - ((raw_y + 15) // 40)

            if rem_x > 0.75 or rem_y > 0.75:
                self.statusBar().showMessage("Ambiguous Position")
                return

            cur_x = (raw_x - 25) // 40
            cur_y = (raw_y - 25) // 40

            self.turn += 1
            self.changecolor()
            btn = QPushButton(str(self.turn), self)

            btn.move(25 + (cur_x * 40), 25 + (cur_y * 40))
            btn.resize(30, 30)
            btn.setStyleSheet(self.getStyleSheet())

            btn.show()

            self.statusBar().showMessage("x = {}, y = {}".format(cur_x, cur_y))

            if not self.board.is_end:
                message, forbidden_list = self.board.put_stone(cur_x, cur_y, self.color)

                if self.board.is_end:
                    self.msgbox = QMessageBox()
                    self.msgbox.setIcon(QMessageBox.Information)
                    self.msgbox.setText(message)
                    self.msgbox.exec_()

                else:
                    self.show_forbidden(forbidden_list)

    def show_forbidden(self, forbidden_list):
        for coord in forbidden_list:
            self.fbtns[coord[0]][coord[1]].show()

    def hide_forbidden(self):
        for fbtns_i in self.fbtns:
            for fbtn in fbtns_i:
                fbtn.hide()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        qp.setPen(QPen(Qt.black, 1))
        for i in range(15):
            qp.drawLine(40 + (i * 40), 40, 40 + (i * 40), 600)
            qp.drawLine(40, 40 + (i * 40), 600, 40 + (i * 40))

        qp.setPen(QPen(Qt.black, 3))

        for i in range(15):
            for j in range(15):
                qp.drawPoint(40 + (i * 40), 40 + (j * 40))

        qp.setPen(QPen(Qt.black, 6))
        qp.drawPoint(320, 320)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    board = BoardWindow()
    sys.exit(app.exec_())