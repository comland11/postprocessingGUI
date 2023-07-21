from PyQt5.QtWidgets import QListWidget


class HistoryListWidget(QListWidget):
    """
    HistoryListWidget class for displaying a list of history items.

    Inherits from QListWidget to provide a widget for displaying a list of history items.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the HistoryListWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(HistoryListWidget, self).__init__(*args, **kwargs)

        # The 'main' attribute represents the parent widget, which is used to access the main window or controller.
        self.main = parent
