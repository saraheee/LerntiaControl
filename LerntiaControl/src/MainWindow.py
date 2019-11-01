# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'ui\MainWindow.ui'

from PyQt5 import QtCore, QtGui, QtWidgets

started = False
ui = 0


class Ui_MainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(870, 596)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("vertical_layout")

        self.camera_view = QtWidgets.QGraphicsView(self.central_widget)
        self.camera_view.setObjectName("camera_view")
        self.vertical_layout.addWidget(self.camera_view)
        self.verticalLayout_2.addLayout(self.vertical_layout)

        self.start_button = QtWidgets.QPushButton(self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.start_button.setFont(font)
        self.start_button.setAutoRepeatInterval(93)
        self.start_button.setObjectName("start_button")
        self.verticalLayout_2.addWidget(self.start_button)

        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 870, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu = QtWidgets.QMenu(self.menu_bar)
        self.menu.setObjectName("menu")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.do_something = QtWidgets.QAction(main_window)
        self.do_something.setObjectName("do_something")
        self.menu.addAction(self.do_something)
        self.menu_bar.addAction(self.menu.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        global ui
        ui = self
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "LerntiaControl"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menu.setTitle(_translate("MainWindow", "Menü"))
        self.do_something.setText(_translate("MainWindow", "Klick"))

        # connect signals to slots
        self.start_button.clicked.connect(self.on_click)

    @staticmethod
    def on_click():
        global started
        if not started:
            ui.start_button.setText("Pause")
            started = True
            print('started')
        else:
            ui.start_button.setText("Start")
            started = False
            print('paused')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())