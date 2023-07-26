import numpy as np
import datetime as dt
from PyQt5.QtWidgets import QMenu
from widget.imageview_widget import ImageViewWidget
from widget.history_list_widget import HistoryListWidget


def moveKeyAndValuesToEnd(dictionary, key):
    """
    Move the given key and its associated values to the end of the dictionary.

    Args:
        dictionary (dict): The dictionary containing the key and values.
        key (str): The key to be moved to the end of the dictionary.
    """
    # Check if the key exists in the dictionary
    if key in dictionary:
        # Get the values associated with the key
        values = dictionary[key]
        # Delete the key from the dictionary
        del dictionary[key]
        # Add the key back to the dictionary with its associated values at the end
        dictionary[key] = values


class HistoryListController(HistoryListWidget):
    """
    Controller class for the history list widget.

    Inherits from HistoryListWidget.

    Attributes:
        hist_dict (dict): Dictionary to store historical images.
        operations_dict (dict): Dictionary to store operations' history.
        matrix_infos (str): Information about the matrix.
        image_view (ImageViewWidget): Reference to the ImageViewWidget.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the HistoryListController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Call the constructor of the parent class (HistoryListWidget)
        super(HistoryListController, self).__init__(*args, **kwargs)
        # Initialize dictionaries and attributes
        self.hist_dict = {}  # Dictionary to store historical images
        self.operations_dict = {}  # Dictionary to store operations history
        self.matrix_infos = None
        self.image_view = None

        # Connect methods to item click events in the history list widget
        self.itemDoubleClicked.connect(self.updateHistoryFigure)
        self.itemClicked.connect(self.updateHistoryTable)

    def addItemWithTimestamp(self, text):
        """
        Add an item with a timestamp to the history list.

        Args:
            text (str): The text to be added to the history list.
        """
        # Get the current timestamp in the format "dd-mm-yyyy HH:mm:ss"
        current_time = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Combine the timestamp and the provided text and store it in matrix_infos attribute
        self.matrix_infos = f"{current_time} - {text}"
        # Add the combined text to the history list
        self.addItem(self.matrix_infos)

    def updateHistoryFigure(self, item):
        """
        Update the displayed image based on the selected item in the history list.

        Args:
            item (QListWidgetItem): The selected item in the history list.
        """
        # Get the text of the selected item
        selected_text = item.text()
        # Check if the selected_text exists in the hist_dict dictionary
        if selected_text in self.hist_dict.keys():
            # Update the main image view with the selected historical image
            self.main.image_view_widget.main_matrix = self.hist_dict.get(selected_text)
            # Display the absolute value of the image in the image view
            self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Clear the second image view
        self.clearSecondImageView()
        # Move the selected item and its associated values to the end of operations_dict
        moveKeyAndValuesToEnd(self.operations_dict, selected_text)

    def updateOperationsHist(self, infos, text):
        """
        Update the operations history dictionary with the given information.

        Args:
            infos (str): Information for the operations' history.
            text (str): Text to be added to the operations' history.
        """
        # Check if the operations_dict is empty
        if len(self.operations_dict) == 0:
            # If empty, add the new information as a key and the text as a value in a list
            self.operations_dict[infos] = [text]
        else:
            # If not empty, retrieve the last value (list) from operations_dict
            list1 = list(self.operations_dict.values())
            new_value = list1[-1].copy()
            # Append the new text to the list of values
            new_value.append(text)
            # Update the operations_dict with the new list of values
            self.operations_dict[infos] = new_value

    def updateHistoryTable(self, item):
        """
        Update the operations history table based on the selected item in the history list.

        Args:
            item (QListWidgetItem): The selected item in the history list.
        """
        # Clear the history table widget
        self.main.history_widget.clear()
        # Get the text of the selected item
        selected_text = item.text()
        # Get the values (list of texts) associated with the selected_text from operations_dict
        values = self.operations_dict.get(selected_text, [])
        # Add each value to the history table widget
        for value in values:
            self.main.history_widget.addItem(value)

    def contextMenuEvent(self, event):
        """
        Create a context menu for the right-click event.

        Args:
            event (QContextMenuEvent): The context menu event.
        """
        # Create a context menu for the widget
        context_menu = QMenu(self)
        # Check if any items are selected in the history list
        if self.selectedItems():
            # Add actions (options) to the context menu
            delete_action = context_menu.addAction('Delete')
            add_action = context_menu.addAction('New image')
            phase_action = context_menu.addAction('Plot phase')
            # Display the context menu at the position of the right-click event
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            # Based on the selected action, perform the appropriate action
            if action == delete_action:
                self.deleteSelectedItem()
            if action == add_action:
                self.addImage()
            if action == phase_action:
                self.plotPhase()

    def deleteSelectedItem(self):
        """
        Delete the selected item from the history list.
        """
        # Get the selected items in the history list widget
        selected_items = self.selectedItems()
        # Check if there is any selected item
        if selected_items:
            # Get the first selected item
            selected_item = selected_items[0]
            # Remove the selected item from the history list
            self.takeItem(self.row(selected_item))

        # Check if the selected item text exists in hist_dict
        if selected_item.text() in self.hist_dict:
            # If yes, remove the corresponding image from hist_dict
            del self.hist_dict[selected_item.text()]
            # Clear the history widget and the main image view
            self.main.history_widget.clear()
            self.main.image_view_widget.clear()
            # Clear the second image view
            self.clearSecondImageView()

        # Check if the selected item text exists in operations_dict
        if selected_item.text() in self.operations_dict:
            # If yes, remove the corresponding operations from operations_dict
            del self.operations_dict[selected_item.text()]

    def addImage(self):
        """
        Add an image to a new image view.
        """
        # Get the selected items in the history list widget
        selected_items = self.selectedItems()
        # Check if there is any selected item
        if selected_items:
            # Get the first selected item
            selected_item = selected_items[0]
            # Get the text of the selected item
            text = selected_item.text()
            # Check if the text exists in hist_dict
            if text in self.hist_dict:
                # Get the image corresponding to the text from hist_dict
                image = self.hist_dict.get(text)

                # Check if the image view is not yet created
                if self.image_view is None:
                    # If not, create a new image view widget
                    self.image_view = ImageViewWidget(parent=self.main)
                    # Add the new image view widget to the main image view splitter
                    self.main.image_view_splitter.addWidget(self.image_view)

                # Display the absolute value of the image in the new image view
                self.image_view.setImage(np.abs(image))

    def clearSecondImageView(self):
        """
        Clear the second image view.
        """
        # Check if the image view exists
        if self.image_view is not None:
            # If yes, close the image view
            self.image_view.close()
            # Set the image view reference to None
            self.image_view = None

    def plotPhase(self):
        """
        Plot the phase of the selected image in a new image view.
        """
        # Get the selected items in the history list widget
        selected_items = self.selectedItems()
        # Check if there is any selected item
        if selected_items:
            # Get the first selected item
            selected_item = selected_items[0]
            # Get the text of the selected item
            text = selected_item.text()
            # Check if the text exists in hist_dict
            if text in self.hist_dict:
                # Get the image corresponding to the text from hist_dict
                image = self.hist_dict.get(text)
                # Check if the image view is not yet created
                if self.image_view is None:
                    # If not, create a new image view widget
                    self.image_view = ImageViewWidget(parent=self.main)
                    # Add the new image view widget to the main image view splitter
                    self.main.image_view_splitter.addWidget(self.image_view)
                # Display the phase of the image in the new image view
                self.image_view.setImage(np.angle(image))
