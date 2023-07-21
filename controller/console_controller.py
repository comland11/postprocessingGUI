import sys
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from widget.console_widget import ConsoleWidget


class ConsoleController(ConsoleWidget):
    """
    Controller class for the console widget.

    Inherits from ConsoleWidget.
    """

    def __init__(self):
        super().__init__()

        # Redirect the output of print to the console widget
        sys.stdout = EmittingStream(textWritten=self.write_console)

    def write_console(self, text):
        """
        Write text to the console widget.

        Args:
            text (str): The text to be written to the console widget.
        """
        cursor = self.console.textCursor()  # Get the text cursor
        cursor.movePosition(cursor.End)  # Move the cursor to the end of the text
        cursor.insertText(text)  # Insert the text at the cursor position
        self.console.setTextCursor(cursor)  # Set the updated cursor
        self.console.ensureCursorVisible()  # Ensure that the cursor is visible in the console


class EmittingStream(QObject):
    """
    Custom stream class that emits a signal whenever text is written.

    Inherits from QObject.
    """

    # Signal that will be emitted when text is written
    textWritten = pyqtSignal(str)

    def write(self, text):
        """
        Write text to the stream.

        Args:
            text (str): The text to be written to the stream.
        """
        self.textWritten.emit(str(text))  # Emit the textWritten signal with the text as an argument

    @pyqtSlot()
    def flush(self):
        """
        Flush the stream.
        """
        pass  # We don't need to do anything here, as this is just a placeholder for stream flushing
