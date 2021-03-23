import ast
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)  # Загружаем дизайн

        self.buttons = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5,
                        self.pushButton_6, self.pushButton_7, self.pushButton_8, self.pushButton_9, self.pushButton_10]

        self.set_settings()

        self.pushButton_14.clicked.connect(self.set_settings)
        self.pushButton_13.clicked.connect(self.confirm)
        for button in self.buttons:
            button.clicked.connect(self.run)

    def run(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.sender().setStyleSheet("background-color: {}".format(color.name()))

    def set_settings(self):
        with open('ClientSettings.txt') as f:
            data = ast.literal_eval(f.read())

        # colors
        colors = [j for _, i in data['Colors'].items() for j in i]
        for button, color in zip(self.buttons, colors):
            button.setStyleSheet(f"background-color:rgb{color}")

        # speed
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(5000)
        self.spinBox_3.setValue(data['Speed'])

        # resolution
        self.spinBox.setMinimum(4)
        self.spinBox.setValue(data['Resolution'][0])  # x

        self.spinBox_2.setMinimum(7)
        self.spinBox_2.setValue(data['Resolution'][1])  # y

    def confirm(self):
        colors = [i.palette().button().color().getRgb()[:3] for i in self.buttons]
        data = {
            "Colors":
                {
                    "FigureColors":
                        colors[:6],
                    "FontColors":
                        colors[6:8],
                    "BorderColors":
                        colors[8:10],
                },
            "Speed": self.spinBox_3.value(),
            "Resolution": (self.spinBox.value(), self.spinBox_2.value())
        }
        with open('ClientSettings.txt', 'w') as f:
            f.write(str(data))
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    ex.show()
    sys.exit(app.exec_())
