import subprocess
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

class OutputReaderThread(QThread):
    output_updated = pyqtSignal(str)

    def __init__(self, command, working_directory):
        super().__init__()
        self.command = command
        self.working_directory = working_directory

    def run(self):
        os.chdir(self.working_directory)  # 切换工作目录
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True)
        while True:
            line = process.stdout.readline().decode().strip()
            self.output_updated.emit(line)
            if line.startswith("Result:"):
                break

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 300, 30)
        self.label.setText("Waiting for result...")

    @pyqtSlot(str)
    def update_output(self, result):
        self.label.setText(result)

    def recognize_image(self):
        command = 'python main.py --test --exp_name=hwdb1 --test_dataset=input/ --radical --resume=data/handwriting_radical.pth'
        working_directory = 'D:\\#Personal_Data\\BigFiles_of_Academic\\CAPAT_Program\\benchmarking-chinese-text-recognition\\models\\TransOCR'
        self.thread = OutputReaderThread(command, working_directory)
        self.thread.output_updated.connect(self.update_output)
        self.thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.recognize_image()
    sys.exit(app.exec_())
