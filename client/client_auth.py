from PyQt5 import QtCore, QtGui, QtWidgets
from client_main import Ui_MainWindow
from client_queries import *

class Ui_authDialog(object):
    isSignIn = True
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 255)
        Dialog.setMinimumSize(QtCore.QSize(280, 255))
        Dialog.setMaximumSize(QtCore.QSize(280, 255))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 51, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 242, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        Dialog.setPalette(palette)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("QDialog { \n"
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
"}")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 25, 241, 201))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.signInButton = QtWidgets.QPushButton(self.frame)
        self.signInButton.setGeometry(QtCore.QRect(30, 150, 181, 27))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 124, 124))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.signInButton.setPalette(palette)
        self.signInButton.setStyleSheet("background-color: #F27C7C\n"
"")
        self.signInButton.setObjectName("signInButton")
        self.nameEdit = QtWidgets.QLineEdit(self.frame)
        self.nameEdit.setGeometry(QtCore.QRect(30, 60, 181, 27))
        self.nameEdit.setObjectName("nameEdit")
        self.passEdit = QtWidgets.QLineEdit(self.frame)
        self.passEdit.setGeometry(QtCore.QRect(30, 100, 181, 27))
        self.passEdit.setObjectName("passEdit")
        self.signInLabel = QtWidgets.QToolButton(self.frame)
        self.signInLabel.setGeometry(QtCore.QRect(10, 20, 91, 25))
        self.signInLabel.setObjectName("signInLabel")
        self.signUpLabel = QtWidgets.QToolButton(self.frame)
        self.signUpLabel.setGeometry(QtCore.QRect(100, 20, 71, 25))
        self.signUpLabel.setObjectName("signUpLabel")
        self.signInLabel.setStyleSheet('color: #F27C7C;')

############################## Events ##############################
        self.signInLabel.clicked.connect(self.signInLabelClick)
        self.signUpLabel.clicked.connect(self.signUpLabelClick)
        self.nameEdit.selectionChanged.connect(self.nameEditClick)
        self.passEdit.selectionChanged.connect(self.passEditClick)
        self.nameEdit.editingFinished.connect(self.nameEditEdFinished)
        self.passEdit.editingFinished.connect(self.passEditEdFinished)
        self.signInButton.clicked.connect(self.signInClick)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "File System"))
        self.signInButton.setText(_translate("Dialog", "Sign in"))
        self.nameEdit.setText(_translate("Dialog", "Name"))
        self.passEdit.setText(_translate("Dialog", "Password"))
        self.signInLabel.setText(_translate("Dialog", "Sign In"))
        self.signUpLabel.setText(_translate("Dialog", "Sign Up"))

    def signInLabelClick(self):
        self.signInLabel.setStyleSheet('color: #F27C7C;')
        self.signUpLabel.setStyleSheet('color: #333333;')
        self.signInButton.setText("Sign in")
        self.nameEdit.setText("Name")
        self.passEdit.setText("Password")
        self.isSignIn = True

    def signUpLabelClick(self):
        self.signUpLabel.setStyleSheet('color: #F27C7C;')
        self.signInLabel.setStyleSheet('color: #333333;')
        self.signInButton.setText("Sign up")
        self.nameEdit.setText("Name")
        self.passEdit.setText("Password")
        self.isSignIn = False

    def nameEditClick(self):
        self.nameEdit.setText("")

    def passEditClick(self):
        self.passEdit.setText("")

    def nameEditEdFinished(self):
        if self.nameEdit.text() == "":
            self.nameEdit.setText("Name")

    def passEditEdFinished(self):
        if self.passEdit.text() == "":
            self.passEdit.setText("Password")

    def signInClick(self):
        username = self.nameEdit.text()
        password = self.passEdit.text()
        cookie = ''
        try:
            if self.isSignIn == True:
                cookie = client_queries.login(username, password)
            else:
                cookie = client_queries.register(username, password)
            if cookie != '':
                self.MainWindow = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.MainWindow, username, cookie)
                self.MainWindow.show()
                Dialog.close()
        except:
            print('Something goes wrong')
            self.nameEdit.setText("")
            self.passEdit.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_authDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
