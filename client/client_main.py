from PyQt5 import QtCore, QtGui, QtWidgets
from client_create import Ui_createDialog
from client_del import Ui_deleteDialog
from client_queries import *
import webbrowser
import tempfile
import shutil
import atexit
import os

class Ui_MainWindow(object):
    userName = ''
    cookies = {}
    directoryTree = []
    dirpath = tempfile.mkdtemp(suffix='', prefix = 'FStmp', dir = None)

    def setupUi(self, MainWindow, username, cookie):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(692, 494)
        MainWindow.setMinimumSize(QtCore.QSize(692, 494))
        MainWindow.setMaximumSize(QtCore.QSize(692, 494))
        MainWindow.setWindowOpacity(0.95)
        MainWindow.setStyleSheet("QMainWindow { \n"
"color: #333333; \n"
"background-color: #F2F2F2; \n"
"}\n"
"QLineEdit { \n"
"color: #333333; \n"
"background-color: #FFFFFF;\n"
"border: 1px solid #8BAFE0;\n"
"border-radius: 5px;\n"
"}\n"
"QPushButton { \n"
"color: #FFFFFF; \n"
"background-color: #F27C7C; \n"
"border-radius: 5px;\n"
"}\n"
"QToolButton { \n"
"color: #333333; \n"
"background-color: #FFFFFF; \n"
"border: 0px;\n"
"}\n"
"QFrame { \n"
"color: #333333; \n"
"background-color: #FFFFFF;\n"
"border-radius: 5px; \n"
"}\n"
"QLabel {\n"
"color: #333333; \n"
"background-color: #F2F2F2;\n"
"}\n"
"QToolTip {\n"
"border-radius:20px;\n"
"background-color: #FFFFFF;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(60, 75, 571, 361))
        self.treeView.setStyleSheet("border: 1px solid #8BAFE0;\n"
"border-radius: 5px;")
        self.treeView.setObjectName("treeView")
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pathLabel = QtWidgets.QLabel(self.centralwidget)
        self.pathLabel.setGeometry(QtCore.QRect(60, 40, 481, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pathLabel.setFont(font)
        self.pathLabel.setObjectName("pathLabel")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(18)
        sizePolicy.setVerticalStretch(18)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.createButton = QtWidgets.QToolButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(560, 35, 30, 30))
        self.createButton.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.createButton.setFont(font)
        self.createButton.setStatusTip("")
        self.createButton.setStyleSheet("QToolButton {\n"
"color: #FFFFFF;\n"
"background-repeat: none; \n"
"background-position: center;\n"
"background-color: #F27C7C;\n"
"border-radius: 5px;\n"
"}\n"
"QToolTip {\n"
"border-radius:2px;\n"
"color: #8BAFE0;\n"
"border: 1px   #8BAFE0;\n"
"background-color: #FFFFFF;\n"
"}")
        self.createButton.setObjectName("createButton")
        self.deleteButton = QtWidgets.QToolButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(600, 35, 30, 30))
        self.deleteButton.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("QToolButton {\n"
"color: #FFFFFF;\n"
"background-repeat: none; \n"
"background-position: center;\n"
"background-color: #F27C7C;\n"
"border-radius: 5px;\n"
"}\n"
"QToolTip {\n"
"border-radius:2px;\n"
"color: #8BAFE0;\n"
"border: 1px   #8BAFE0;\n"
"background-color: #FFFFFF;\n"
"}")
        self.deleteButton.setObjectName("deleteButton")
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.userName = username
        self.cookies = cookie

############################## Events ##############################
        self.createButton.clicked.connect(self.createButtonClick)
        self.deleteButton.clicked.connect(self.deleteButtonClick)
        self.treeView.doubleClicked.connect(self.treeViewDoubleClick)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.updateDirTree()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "File System"))
        self.pathLabel.setText(_translate("MainWindow", "Current path: /"))
        self.createButton.setToolTip(_translate("MainWindow", "Create"))
        self.createButton.setText(_translate("MainWindow", "C"))
        self.deleteButton.setToolTip(_translate("MainWindow", "Delete"))
        self.deleteButton.setText(_translate("MainWindow", "D"))

    def createButtonClick(self):
        self.createDialog = QtWidgets.QDialog()
        self.ui = Ui_createDialog()
        self.ui.setupUi(self.createDialog)
        self.ui.pressCreateButton.connect(self.slotCloseCreateDialog)
        self.createDialog.show()

    def deleteButtonClick(self):
        index = self.treeView.currentIndex().row()
        if index > 1:
            fileName = self.directoryTree[index - 2][0]
            isDir = True
            if self.directoryTree[index - 2][2] == 'file':
                isDir = False
            self.deleteDialog = QtWidgets.QDialog()
            self.ui = Ui_deleteDialog()
            self.ui.setupUi(self.deleteDialog, fileName, isDir)
            self.ui.pressDeleteButton.connect(self.slotCloseDeleteDialog)
            self.deleteDialog.show()

    def updateDirTree(self):
        model = QtGui.QStandardItemModel()
        model.appendRow(QtGui.QStandardItem('root'))
        model.appendRow(QtGui.QStandardItem('back'))
        path = self.pathLabel.text()[15:]
        model.setHorizontalHeaderLabels(["Name","Size","Type"])
        try:
            self.directoryTree = client_queries.lstdir(path, self.userName, self.cookies)
            for string in self.directoryTree:
                items = []
                for item in string:
                    items.append(QtGui.QStandardItem(item));
                model.appendRow(items)
        except:
            print('Connection failed')
        self.treeView.setModel(model)
        self.treeView.setColumnWidth(0,250)
        self.treeView.setColumnWidth(1,160)
        self.treeView.setColumnWidth(2,150)

    def treeViewDoubleClick(self):
        index = self.treeView.currentIndex().row()
        if index == 0:
            self.pathLabel.setText("Current path: /")
            self.updateDirTree()
        elif index == 1:
            pos = self.pathLabel.text()[:-1].rfind('/')
            if pos >= 14:
                self.pathLabel.setText(self.pathLabel.text()[:pos + 1])
            self.updateDirTree()
        else:
            name = self.directoryTree[index - 2][0]
            if self.directoryTree[index - 2][2] == 'file':
                prefixed = [filename for filename in os.listdir(self.dirpath) if filename.startswith(name)]
                if prefixed:
                    webbrowser.open(self.dirpath + '/' + prefixed[0])
                else:
                    if self.pathLabel.text()[15:] == '':
                        path = name
                    else:
                        path = self.pathLabel.text()[15:] + name
                    mfile = client_queries.read(path, self.userName, self.cookies)
                    tmpfile = tempfile.mkstemp(prefix = name, dir = self.dirpath)
                    with open(tmpfile[1],'wb') as handle:
                        for block in mfile.iter_content(1024):
                            handle.write(block)
                    webbrowser.open(tmpfile[1])
            else:
                self.pathLabel.setText(self.pathLabel.text() + name + '/')
                self.updateDirTree()

    def slotCloseCreateDialog(self, name, isDir):
        if isDir == True:
            try:
                if self.pathLabel.text()[15:] == '':
                    path = name
                else:
                    path = self.pathLabel.text()[15:] + name
                client_queries.mkdir(path, self.userName, self.cookies)
                self.updateDirTree()
                self.createDialog.close()
            except:
                print('Connection failure')
        else:
            try:
                files = {'file': open(name, 'rb')}
                fileName = name[name.rfind('/') + 1:]
                if self.pathLabel.text()[15:] == '':
                    path = fileName
                else:
                    path = self.pathLabel.text()[15:] + fileName
                client_queries.write(path, self.userName, self.cookies, files)
                print('Successfully created')
                self.createDialog.close()
                self.updateDirTree()
            except:
                print('Wrong path')

    def slotCloseDeleteDialog(self, fileName, isDir):
        path = self.pathLabel.text()[15:] + fileName
        try:
            if isDir:
                client_queries.rmdir(path, self.userName, self.cookies)
            else:
                client_queries.delete(path, self.userName, self.cookies)
            self.deleteDialog.close()
            self.updateDirTree()
        except:
            print('Connection failure')

    def exit_handler():
        shutil.rmtree(Ui_MainWindow.dirpath)

    atexit.register(exit_handler)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    coo = {'user': 'name', 'auth': '1A0KiTjUhe5NFur2yLWs68qBSglpvwmZEn3DM7xI'}
    ui.setupUi(MainWindow, 'name', coo)
    MainWindow.show()
    sys.exit(app.exec_())
