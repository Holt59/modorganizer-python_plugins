# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simpleinstalldialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimpleInstallDialog(object):
    def setupUi(self, SimpleInstallDialog):
        SimpleInstallDialog.setObjectName("SimpleInstallDialog")
        SimpleInstallDialog.resize(400, 83)
        self.verticalLayout = QtWidgets.QVBoxLayout(SimpleInstallDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SimpleInstallDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nameCombo = QtWidgets.QComboBox(SimpleInstallDialog)
        self.nameCombo.setEditable(True)
        self.nameCombo.setObjectName("nameCombo")
        self.horizontalLayout.addWidget(self.nameCombo)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.manualBtn = QtWidgets.QPushButton(SimpleInstallDialog)
        self.manualBtn.setObjectName("manualBtn")
        self.horizontalLayout_2.addWidget(self.manualBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okBtn = QtWidgets.QPushButton(SimpleInstallDialog)
        self.okBtn.setDefault(True)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout_2.addWidget(self.okBtn)
        self.cancelBtn = QtWidgets.QPushButton(SimpleInstallDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SimpleInstallDialog)
        QtCore.QMetaObject.connectSlotsByName(SimpleInstallDialog)

    def retranslateUi(self, SimpleInstallDialog):
        _translate = QtCore.QCoreApplication.translate
        SimpleInstallDialog.setWindowTitle(_translate("SimpleInstallDialog", "Quick Install - Python"))
        self.label.setText(_translate("SimpleInstallDialog", "Name"))
        self.manualBtn.setToolTip(_translate("SimpleInstallDialog", "Opens a Dialog that allows custom modifications."))
        self.manualBtn.setWhatsThis(_translate("SimpleInstallDialog", "Opens a Dialog that allows custom modifications."))
        self.manualBtn.setText(_translate("SimpleInstallDialog", "Manual"))
        self.okBtn.setText(_translate("SimpleInstallDialog", "OK"))
        self.cancelBtn.setText(_translate("SimpleInstallDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SimpleInstallDialog = QtWidgets.QDialog()
    ui = Ui_SimpleInstallDialog()
    ui.setupUi(SimpleInstallDialog)
    SimpleInstallDialog.show()
    sys.exit(app.exec_())
