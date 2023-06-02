from PyQt5.QtWidgets import QTextEdit, QMainWindow, QSizePolicy


class ConsoleWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the console widget
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.setCentralWidget(self.console)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setMaximumWidth(400)
