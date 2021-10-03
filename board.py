import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class BoardWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initvar()

    def initvar(self):
        self.turn = 0

    def getStyleSheet(self):
        if self.turn % 2 == 1:
            return "background-color:black;color:white"

        else:
            return "background-color:white"

    def initUI(self):
        self.setWindowTitle("Gomoku")
        self.setWindowIcon(QIcon('image\gomokuIcon.png'))
        self.setStyleSheet("background:rgb(181, 139, 91)")
        self.setGeometry(300, 300, 640, 640)

        self.statusBar().showMessage('Ready')
        self.show()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
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
            btn = QPushButton(str(self.turn), self)

            btn.move(25 + (cur_x * 40), 25 + (cur_y * 40))
            btn.resize(30, 30)
            btn.setStyleSheet(self.getStyleSheet())

            btn.show()

            self.statusBar().showMessage("x = {}, y = {}".format(cur_x, cur_y))

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    board = BoardWindow()
    sys.exit(app.exec_())