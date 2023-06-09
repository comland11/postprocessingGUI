import datetime as dt

import numpy as np
from PyQt5.QtWidgets import QMenu
from widget.imageview_widget import ImageViewWidget
from widget.history_list_widget import HistoryListWidget


class HistoryListController(HistoryListWidget):
    def __init__(self, *args, **kwargs):
        super(HistoryListController, self).__init__(*args, **kwargs)

        self.hist_dict = {}  # Dictionary to store historical images
        self.operations_dict = {}  # Dictionary to store operations history
        self.matrix_infos = None
        self.image_view = None

        # Connect methods to item click
        self.itemDoubleClicked.connect(self.updateHistoryFigure)
        self.itemClicked.connect(self.updateHistoryTable)

    def addItemWithTimestamp(self, text):
        # Add an item with a timestamp to the history list
        current_time = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.matrix_infos = f"{current_time} - {text}"
        self.addItem(self.matrix_infos)

    def updateHistoryFigure(self, item):
        # Update the displayed image based on the selected item in the history list
        selected_text = item.text()
        if selected_text in self.hist_dict.keys():
            self.main.image_view_widget.main_matrix = self.hist_dict.get(selected_text)
            self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))
        if self.image_view is not None:
            self.image_view.close()
            self.image_view = None

        self.moveKeyAndValuesToEnd(self.operations_dict, selected_text)

    def updateOperationsHist(self, infos, text):
        # Update the operations history dictionary with the given information
        if len(self.operations_dict) == 0:
            self.operations_dict[infos] = [text]
        else:
            list1 = list(self.operations_dict.values())
            new_value = list1[-1].copy()
            new_value.append(text)
            self.operations_dict[infos] = new_value

    def updateHistoryTable(self, item):
        # Update the operations history table based on the selected item in the history list
        self.main.history_widget.clear()
        selected_text = item.text()
        values = self.operations_dict.get(selected_text, [])

        for value in values:
            self.main.history_widget.addItem(value)

    def moveKeyAndValuesToEnd(self, dictionary, key):
        # Check if the key exists in the dictionary
        if key in dictionary:
            # Create a list to store the values associated with the key
            values = dictionary[key]
            # Remove the key and its values from the dictionary
            del dictionary[key]
            # Add the key and its values to the end of the dictionary
            dictionary[key] = values

    def contextMenuEvent(self, event):
        # Create a context menu for right-click event
        context_menu = QMenu(self)
        if self.selectedItems():
            delete_action = context_menu.addAction('Delete')
            add_action = context_menu.addAction('New image')
            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == delete_action:
                self.deleteSelectedItem()
            if action == add_action:
                self.addImage()

    def deleteSelectedItem(self):
        # Delete the selected item from the history list
        selected_items = self.selectedItems()
        if selected_items:
            selected_item = selected_items[0]

            self.takeItem(self.row(selected_item))

        if selected_item.text() in self.hist_dict:
            # Remove the selected item from the historical images dictionary
            del self.hist_dict[selected_item.text()]
            self.main.history_widget.clear()
            self.main.image_view_widget.clear()
            self.image_view.clear()

        if selected_item.text() in self.operations_dict:
            # Remove the selected item from the operations history dictionary
            del self.operations_dict[selected_item.text()]

    def addImage(self):
        # Add an image to a new image view
        selected_items = self.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            text = selected_item.text()
            if text in self.hist_dict:
                image = self.hist_dict.get(text)

                # Check if an instance of ImageViewWidget already exists
                if self.image_view is None:
                    self.image_view = ImageViewWidget(parent=self.main)
                    self.main.image_view_splitter.addWidget(self.image_view)

                self.image_view.setImage(np.abs(image))
