from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_createDialog(QtCore.QObject):
    pressCreateButton = QtCore.pyqtSignal(['QString','bool'])

    def setupUi(self, createDialog):
        createDialog.setObjectName("createDialog")
        createDialog.setWindowModality(QtCore.Qt.NonModal)
        createDialog.resize(380, 193)
        createDialog.setMinimumSize(QtCore.QSize(380, 193))
        createDialog.setMaximumSize(QtCore.QSize(380, 193))
        createDialog.setLayoutDirection(QtCore.Qt.RightToLeft)
        createDialog.setStyleSheet("QDialog { \n"
"color: #333333; \n"
"background-color: #F2F2F2; \n"
"}\n"
"QLineEdit { \n"
"color: #333333; \n"
"background-color: #FFFFFF;\n"
"border: 1px solid #8BAFE0;\n"
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
        createDialog.setSizeGripEnabled(False)
        createDialog.setModal(False)
        self.frame = QtWidgets.QFrame(createDialog)
        self.frame.setGeometry(QtCore.QRect(20, 25, 339, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.createButton = QtWidgets.QPushButton(self.frame)
        self.createButton.setGeometry(QtCore.QRect(24, 95, 291, 27))
        self.createButton.setObjectName("createButton")
        self.createButton.setStyleSheet(
"QPushButton { \n"
"color: #FFFFFF; \n"
"background-color: #F27C7C; \n"
"border-radius: 5px;\n"
"}")
        self.fileNameEdit = QtWidgets.QLineEdit(self.frame)
        self.fileNameEdit.setGeometry(QtCore.QRect(24, 20, 291, 27))
        self.fileNameEdit.setObjectName("fileNameEdit")
        self.dirCheckBox = QtWidgets.QCheckBox(self.frame)
        self.dirCheckBox.setGeometry(QtCore.QRect(24, 58, 151, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dirCheckBox.setFont(font)
        self.dirCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dirCheckBox.setObjectName("dirCheckBox")
        self.chooseButton = QtWidgets.QPushButton(self.frame)
        self.chooseButton.setGeometry(QtCore.QRect(220, 60, 91, 20))
        self.chooseButton.setStyleSheet("color: #333333;\n"
"background: #FFFFFF")
        self.chooseButton.setObjectName("chooseButton")

############################## Events ##############################
        self.createButton.clicked.connect(self.createButtonClick)
        self.chooseButton.clicked.connect(self.chooseButtonClick)
        self.fileNameEdit.selectionChanged.connect(self.fileNameEditClick)
        self.fileNameEdit.editingFinished.connect(self.fileNameEditFinished)

        self.retranslateUi(createDialog)
        QtCore.QMetaObject.connectSlotsByName(createDialog)

    def retranslateUi(self, createDialog):
        _translate = QtCore.QCoreApplication.translate
        createDialog.setWindowTitle(_translate("createDialog", "Create"))
        self.createButton.setText(_translate("createDialog", "Create"))
        self.fileNameEdit.setText(_translate("createDialog", "Name"))
        self.dirCheckBox.setText(_translate("createDialog", "Directory"))
        self.chooseButton.setText(_translate("createDialog", "Choose file.."))

    def createButtonClick(self):
        name = self.fileNameEdit.text()
        self.pressCreateButton.emit(name, self.dirCheckBox.isChecked())

    def chooseButtonClick(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.frame, 'Open file')[0]
        self.fileNameEdit.setText(fname)

    def fileNameEditClick(self):
        self.fileNameEdit.setText("")

    def fileNameEditFinished(self):
        if self.fileNameEdit.text() == "":
            self.fileNameEdit.setText("Name")
