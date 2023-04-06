from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QPushButton, QLineEdit, QSizePolicy


class SliderWidget(QtWidgets.QWidget):
    def __init__(self, name='feature', min_value=0, max_value=100, initial_value=50):
        super().__init__()

        # Load the UI from the .ui file
        uic.loadUi("QT_UI\\sliderwidget.ui", self)
        self.label.setText(name)

        # Set up the slider
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.value_label.setText(str(initial_value))

        # Connect the signals and slots
        self.slider.valueChanged.connect(self._on_slider_value_changed)
        self.value_label.editingFinished.connect(self._on_value_label_editing_finished)
        self.increment_button.clicked.connect(self._on_increment_button_clicked)
        self.decrement_button.clicked.connect(self._on_decrement_button_clicked)

    def _on_slider_value_changed(self, value):
        self.value_label.setText(str(value))

    def _on_value_label_editing_finished(self):
        value = int(self.value_label.text())
        self.slider.setValue(value)

    def _on_increment_button_clicked(self):
        value = self.slider.value()
        self.slider.setValue(value + 1)

    def _on_decrement_button_clicked(self):
        value = self.slider.value()
        self.slider.setValue(value - 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderWidget(name='力道' ,min_value=0, max_value=255, initial_value=128)
    window.show()
    sys.exit(app.exec_())
