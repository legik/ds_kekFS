from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_deleteDialog(QtCore.QObject):
    pressDeleteButton = QtCore.pyqtSignal(['QString', 'bool'])
    fileName = ''
    isDir = False

    def setupUi(self, deleteDialog, filename, isDir):
        fileName = filename
        deleteDialog.setObjectName("deleteDialog")
        deleteDialog.setWindowModality(QtCore.Qt.NonModal)
        deleteDialog.resize(380, 193)
        deleteDialog.setStyleSheet("QDialog { \n"
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
        deleteDialog.setSizeGripEnabled(False)
        deleteDialog.setModal(False)
        self.frame = QtWidgets.QFrame(deleteDialog)
        self.frame.setGeometry(QtCore.QRect(20, 25, 339, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(24, 10, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.fileNameLabel = QtWidgets.QLabel(self.frame)
        self.fileNameLabel.setGeometry(QtCore.QRect(24, 50, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.fileNameLabel.setFont(font)
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.deleteButton = QtWidgets.QPushButton(self.frame)
        self.deleteButton.setGeometry(QtCore.QRect(24, 95, 291, 27))
        self.deleteButton.setObjectName("deleteButton")

############################## Events ##############################
        self.deleteButton.clicked.connect(self.deleteButtonClick)

        self.retranslateUi(deleteDialog)
        QtCore.QMetaObject.connectSlotsByName(deleteDialog)
        self.fileNameLabel.setText(filename)
        if isDir:
            self.isDir = True
            self.label.setText("Do you really want to delete directory:")

    def retranslateUi(self, deleteDialog):
        _translate = QtCore.QCoreApplication.translate
        deleteDialog.setWindowTitle(_translate("deleteDialog", "Delete"))
        self.label.setText(_translate("deleteDialog", "Do you really want to delete this file:"))
        self.fileNameLabel.setText(_translate("deleteDialog", ""))
        self.deleteButton.setText(_translate("deleteDialog", "Delete"))

    def deleteButtonClick(self):
        name = self.fileNameLabel.text()
        if self.isDir:
            name += '/'
        self.pressDeleteButton.emit(name, self.isDir)



'''if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    deleteDialog = QtWidgets.QDialog()
    ui = Ui_deleteDialog()
    ui.setupUi(deleteDialog)
    deleteDialog.show()
    sys.exit(app.exec_())'''
