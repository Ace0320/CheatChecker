from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from logic import get_cheaters
from layout import Ui_CheatChecker
# If layout shows an import error, generate it using:
# pyuic5 checker.ui -o layout.py


class CheatChecker(QMainWindow, Ui_CheatChecker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cheaters = self.folder = None
        self.setFolderButton.clicked.connect(self.setFolder)
        self.getCheatersButton.clicked.connect(self.getCheaters)

    def setFolder(self):
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Codes Directory"))
        self.folderEdit.setText(self.folder)

    def getCheaters(self):
        if not self.folder:
            self.setFolder()
        self.cheaters = get_cheaters(self.folder)
        for cheater in self.cheaters:
            self.cheatersList.addItem(f"{cheater[0]}% {cheater[1]}:{cheater[2]}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = CheatChecker()
    main.show()
    sys.exit(app.exec_())
