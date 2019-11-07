import sys
from PyQt5.QtWidgets import QApplication
from board import Board

if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = Board()
    sys.exit(app.exec_())
