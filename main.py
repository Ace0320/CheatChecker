import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from threading import Thread
from logic import get_cheaters
from layout import Ui_CheatChecker
# If layout shows an import error, generate it using:
# pyuic5 checker.ui -o layout.py


class CheatChecker(QMainWindow, Ui_CheatChecker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cheaters = self.folder = None
        self.setWindowIcon(QIcon(os.path.join(getattr(sys, "_MEIPASS", "."), "checker.ico")))
        self.folderEdit.textChanged.connect(self.setFolder)
        self.setFolderButton.clicked.connect(self.setFolder)
        self.getCheatersButton.clicked.connect(self.getCheaters)
        self.cheatersList.currentTextChanged.connect(self.openCodes)
        self.cheatersSearchEdit.textChanged.connect(self.searchCheaters)
        self.getCheatersButton.setFocus()

    def setFolder(self, folder=None):
        self.folder = folder or str(QFileDialog.getExistingDirectory(self, "Select Codes Directory"))
        if not folder: self.folderEdit.setText(self.folder)

    def getCheaters(self):
        if not self.folder:
            self.setFolder()
            if not self.folder: return
        Thread(target=self.processCheaters).start()

    def searchCheaters(self, keyword):
        if self.cheaters and keyword:
            keyword = keyword.lower()
            self.cheatersList.clear()
            self.cheatersList.addItems(key for key in self.cheaters.keys() if keyword in key)

    def processCheaters(self):
        self.cheatersList.clear()
        self.cheatersSearchEdit.clear()
        self.cheaters = get_cheaters(self.folder)
        self.cheatersList.addItems(self.cheaters.keys())
        self.cheatersList.setMinimumWidth(self.cheatersList.sizeHintForColumn(0) + 36)
        self.cheatersLabel.setText("Cheaters in " + self.folder.rsplit("/", 1)[1] + ":")

    def openCodes(self, index):
        if not index: return
        file1, file2 = self.cheaters[index]
        self.code1Label.setText("Code 1: " + file1)
        self.code1TextArea.setText(open(os.path.join(self.folder, file1)).read())
        self.code2Label.setText("Code 2: " + file2)
        self.code2TextArea.setText(open(os.path.join(self.folder, file2)).read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = CheatChecker()
    main.show()
    sys.exit(app.exec_())
