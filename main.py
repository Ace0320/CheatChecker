import os, sys, tkinter
from threading import Thread, active_count
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from logic import get_cheaters
from layout import Ui_CheatChecker
import zipfile
from shutil import copyfile
# If layout shows an import error, generate it using:
# pyuic5 checker.ui -o layout.py

#Variables
ziped_path = "C:\\Users\\s526521\\Downloads\\submissions.zip"
unziped_path = "C:\\Users\\s526521\\Downloads\\submissions"
everything_unziped = "C:\\Users\\s526521\\Downloads\\submissions\\submissions_unziped"
cheatCheck = "C:\\Users\\s526521\\Downloads\\submissions\\cheat_check"


class CheatChecker(QMainWindow, Ui_CheatChecker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cheaters = self.folder = None
        self.setWindowIcon(QIcon(os.path.join(getattr(sys, "_MEIPASS", "."), "checker.ico")))
        self.folderEdit.textChanged.connect(self.setFolder)
        self.setFolderButton.clicked.connect(self.setFolder)
        self.getCheatersButton.clicked.connect(self.getCheaters)
        self.unzipSubmissions.clicked.connect(self.unzip)
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
        if active_count() == 1:
            Thread(target=self.processCheaters).start()

    def searchCheaters(self, keyword):
        if self.cheaters:
            keyword = keyword.lower()
            self.cheatersList.clear()
            self.cheatersList.addItems(key for key in self.cheaters.keys() if not keyword or keyword in key)

    def processCheaters(self):
        self.cheatersList.clear()
        self.cheatersSearchEdit.clear()
        self.cheaters = get_cheaters(self.folder, False)
#        self.cheaters = get_cheaters(self.folder, self.mainCheckBox.isChecked())
        self.cheatersList.addItems(self.cheaters.keys())
        self.cheatersList.setMinimumWidth(self.cheatersList.sizeHintForColumn(0) + 36)
#        self.cheatersLabel.setText("Cheaters in " + self.folder.rsplit("/", 1)[1] + ":")

    def openCodes(self, index):
        if not index: return
        file1, file2 = self.cheaters[index]
        self.code1Label.setText("Code 1: " + file1)
        self.code1TextArea.setText(open(os.path.join(self.folder, file1)).read())
        self.code2Label.setText("Code 2: " + file2)
        self.code2TextArea.setText(open(os.path.join(self.folder, file2)).read())


    def unzip_rest(self, files):
        for folder in os.listdir(files):
            zip_ref1 = zipfile.ZipFile(unziped_path+ "\\" +folder, 'r')
            zip_ref1.extractall(everything_unziped)
            zip_ref1.close()
            #print(folder)
    def cht_setup(self):
        badValues = ["build", "nbproject", "test", "build.xml", "manifest.mf"]
        for folder in os.listdir(everything_unziped):
            if folder in badValues:
                print("not zipped right: " + folder)
            elif folder == "src":
                self.srcBadZip()
            else:
                subFolder = everything_unziped+"\\"+folder
                for sub in os.listdir(subFolder):
                    if folder == sub:
                        srcFolder = subFolder+"\\"+sub.lower()+"\\src"
                    else:
                        srcFolder = subFolder+"\\src"
                    try:
                        for src in os.listdir(srcFolder):
                            srcFile = srcFolder + "\\" + src
                            for file in os.listdir(srcFile):
    #                            print(srcFile + "\\" + file)
                                theFile = srcFile + "\\" + file
                                newFile = cheatCheck + "\\" + file
                                copyfile(theFile, newFile)
                    except FileNotFoundError:
                        print("Path not implemented yet: "+srcFolder)
                    except NotADirectoryError:
                        print("Path not implemented yet: "+srcFolder)
    def srcBadZip(self):
        srcPath = everything_unziped + "\\src"
        try:
            for src in os.listdir(srcPath):
                srcFile = srcPath + "\\" + src
                for file in os.listdir(srcFile):
    #                            print(srcFile + "\\" + file)
                    theFile = srcFile + "\\" + file
                    newFile = cheatCheck + "\\" + file
                    copyfile(theFile, newFile)
        except FileNotFoundError:
            print("Path not implemented yet")

    def unzip(self):
        root = tkinter.Tk()
        root.withdraw()
        ziped_path = tk.filedialog.askopenfilename()
        zip_ref = zipfile.ZipFile(ziped_path, 'r')
        zip_ref.extractall(unziped_path)
        zip_ref.close()
        try:
            self.unzip_rest(unziped_path)
        except PermissionError:
            self.folderEdit.setText(cheatCheck)
        try:
            os.mkdir(cheatCheck)
        except FileExistsError:
            print("Exists")
        self.cht_setup()
        self.folderEdit.setText(cheatCheck)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = CheatChecker()
    main.show()
    sys.exit(app.exec_())
