# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OpenApps2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenApps(object):
    def setupUi(self, OpenApps):
        OpenApps.setObjectName("OpenApps")
        OpenApps.setWindowModality(QtCore.Qt.WindowModal)
        OpenApps.resize(732, 877)
        self.verticalLayout = QtWidgets.QVBoxLayout(OpenApps)
        self.verticalLayout.setObjectName("verticalLayout")
        self.run_all_button = QtWidgets.QPushButton(OpenApps)
        # self.run_all_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.run_all_button.setObjectName("run_all_button")
        self.verticalLayout.addWidget(self.run_all_button)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.app_button_container = QtWidgets.QVBoxLayout()
        self.app_button_container.setObjectName("app_button_container")
        self.insert_app_button = QtWidgets.QPushButton(OpenApps)
        # self.insert_app_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.insert_app_button.setObjectName("insert_app_button")
        self.app_button_container.addWidget(self.insert_app_button)
        self.remove_app_button = QtWidgets.QPushButton(OpenApps)
        # self.remove_app_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.remove_app_button.setObjectName("remove_app_button")
        self.app_button_container.addWidget(self.remove_app_button)
        self.run_app_button = QtWidgets.QPushButton(OpenApps)
        # self.run_app_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.run_app_button.setObjectName("run_app_button")
        self.app_button_container.addWidget(self.run_app_button)
        self.app_container = QtWidgets.QVBoxLayout()
        self.app_container.setObjectName("app_container")
        self.app_button_container.addLayout(self.app_container)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.app_button_container.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.app_button_container)
        self.line = QtWidgets.QFrame(OpenApps)
        self.line.setMinimumSize(QtCore.QSize(3, 0))
        self.line.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(10)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.website_button_container = QtWidgets.QVBoxLayout()
        self.website_button_container.setObjectName("website_button_container")
        self.insert_website_button = QtWidgets.QPushButton(OpenApps)
        # self.insert_website_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.insert_website_button.setObjectName("insert_website_button")
        self.website_button_container.addWidget(self.insert_website_button)
        self.remove_website_button = QtWidgets.QPushButton(OpenApps)
        # self.remove_website_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.remove_website_button.setObjectName("remove_website_button")
        self.website_button_container.addWidget(self.remove_website_button)
        self.run_website_button = QtWidgets.QPushButton(OpenApps)
        # self.run_website_button.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.run_website_button.setObjectName("run_website_button")
        self.website_button_container.addWidget(self.run_website_button)
        self.website_container = QtWidgets.QVBoxLayout()
        self.website_container.setObjectName("website_container")
        self.website_button_container.addLayout(self.website_container)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.website_button_container.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.website_button_container)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(OpenApps)
        QtCore.QMetaObject.connectSlotsByName(OpenApps)

    def retranslateUi(self, OpenApps):
        _translate = QtCore.QCoreApplication.translate
        OpenApps.setWindowTitle(_translate("OpenApps", "Form"))
        self.run_all_button.setText(_translate("OpenApps", "Run All"))
        self.insert_app_button.setText(_translate("OpenApps", "Insert App"))
        self.remove_app_button.setText(_translate("OpenApps", "Remove App"))
        self.run_app_button.setText(_translate("OpenApps", "Run"))
        self.insert_website_button.setText(_translate("OpenApps", "Insert Website"))
        self.remove_website_button.setText(_translate("OpenApps", "Remove Website"))
        self.run_website_button.setText(_translate("OpenApps", "Run"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenApps = QtWidgets.QWidget()
    ui = Ui_OpenApps()
    ui.setupUi(OpenApps)
    OpenApps.show()
    sys.exit(app.exec_())
