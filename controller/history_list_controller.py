import datetime as dt
from widget.history_list_widget import HistoryListWidget


class HistoryListController(HistoryListWidget):
    def __init__(self, *args, **kwargs):
        super(HistoryListController, self).__init__(*args, **kwargs)

        self.hist_dict = {}  # Dictionary to store historical images
        self.operations_dict = {}  # Dictionary to store operations history

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
            value = self.hist_dict.get(selected_text)
            self.main.image_view_widget.setImage(value)
        if "BM4D" not in selected_text:
            self.main.bm4d_slider.setVisible(False)
            self.main.bm4d_slider
        else:
            self.main.bm4d_slider.setVisible(True)


    def uptadeOperationsHist(self, infos, text):
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
