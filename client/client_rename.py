from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_renameDialog(QtCore.QObject):
    pressUploadButton = QtCore.pyqtSignal(['QString'])

    def setupUi(self, renameDialog):
        renameDialog.setObjectName("renameDialog")
        renameDialog.setWindowModality(QtCore.Qt.NonModal)
        renameDialog.resize(380, 173)
        renameDialog.setMinimumSize(QtCore.QSize(380, 173))
        renameDialog.setMaximumSize(QtCore.QSize(380, 173))
        renameDialog.setLayoutDirection(QtCore.Qt.RightToLeft)
        renameDialog.setStyleSheet("QDialog { \n"
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
        renameDialog.setSizeGripEnabled(False)
        renameDialog.setModal(False)
        self.frame = QtWidgets.QFrame(renameDialog)
        self.frame.setGeometry(QtCore.QRect(20, 25, 339, 120))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.uploadButton = QtWidgets.QPushButton(self.frame)
        self.uploadButton.setGeometry(QtCore.QRect(24, 70, 291, 27))
        self.uploadButton.setObjectName("uploadButton")
        self.fileNameEdit = QtWidgets.QLineEdit(self.frame)
        self.fileNameEdit.setGeometry(QtCore.QRect(24, 22, 291, 27))
        self.fileNameEdit.setObjectName("fileNameEdit")

############################## Events ##############################
        self.uploadButton.clicked.connect(self.uploadButtonClick)
        self.fileNameEdit.selectionChanged.connect(self.fileNameEditClick)
        self.fileNameEdit.editingFinished.connect(self.fileNameEditFinished)

        self.retranslateUi(renameDialog)
        QtCore.QMetaObject.connectSlotsByName(renameDialog)

    def retranslateUi(self, renameDialog):
        _translate = QtCore.QCoreApplication.translate
        renameDialog.setWindowTitle(_translate("renameDialog", "Rename"))
        self.uploadButton.setText(_translate("renameDialog", "Upload"))
        self.fileNameEdit.setText(_translate("renameDialog", "New name"))

    def uploadButtonClick(self):
        name = self.fileNameEdit.text()
        self.pressUploadButton.emit(name)

    def fileNameEditClick(self):
        self.fileNameEdit.setText("")

    def fileNameEditFinished(self):
        if self.fileNameEdit.text() == "":
            self.fileNameEdit.setText("New name")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    renameDialog = QtWidgets.QDialog()
    ui = Ui_renameDialog()
    ui.setupUi(renameDialog)
    renameDialog.show()
    sys.exit(app.exec_())
