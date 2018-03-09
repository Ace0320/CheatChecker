from PyQt5.QtWidgets import QApplication, QMainWindow
from .layout import Ui_CheatChecker
# If layout shows an import error, generate it using:
# pyuic5 checker.ui -o layout.py


class CheatChecker(QMainWindow, Ui_CheatChecker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = CheatChecker()
    main.show()
    sys.exit(app.exec_())
