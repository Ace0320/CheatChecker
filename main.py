import os, sys, tkinter
from tkinter import filedialog
from threading import Thread, active_count
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from logic import get_cheaters
from layout import Ui_CheatChecker
import zipfile
#import shutil
from shutil import copyfile, rmtree
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
            newFolder = unziped_path+ "\\" +folder
#            try:
            zip_ref1 = zipfile.ZipFile(newFolder, 'r')
#            except PermissionError:
                #removes folder completly, and replaces it with new unzipped foldsers
#                rmtree(newFolder)
#                zip_ref1 = zipfile.ZipFile(newFolder, 'r')
#                Edit above not working yet
#                print("Exists")
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
        #planning on implementing a file naming system that uses date and time EX: submissions 3 21 - 15 24
        root = tkinter.Tk()
        root.withdraw()
        ziped_path = filedialog.askopenfilename()
        if ziped_path != "":
            zip_ref = zipfile.ZipFile(ziped_path, 'r')
#This is so if the folder exists, it will delete it so files will update, otherwise files and folders won't update, only new things
            #will be added to the file
            if os.path.exists(unziped_path):
                rmtree(unziped_path)
                os.mkdir(unziped_path)
            zip_ref.extractall(unziped_path)
            zip_ref.close()
            fileType = os.listdir(unziped_path)[1]
            extension = os.path.splitext(fileType)[1]
            print("________\nThe file extention of the first file is: "+extension+"\n________")
            #if extesnion is .zip, then run this line, but if not, need to skip
            try:
                self.unzip_rest(unziped_path)
            except PermissionError:
                self.folderEdit.setText(cheatCheck)
            try:
                os.mkdir(cheatCheck)
            except FileExistsError:
                print("Exists")
#This is to see if I can tell if it is a folder or not, a folder with have a blank extension, thus ""
#                if os.path.splitext(cheatCheck)[1] == "":
#                    print("true")
#                else:
#                    print("false")
            self.cht_setup()
            self.folderEdit.setText(cheatCheck)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = CheatChecker()
    main.show()
    sys.exit(app.exec_())