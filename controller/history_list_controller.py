import datetime as dt
from widget.history_list_widget import HistoryListWidget


class HistoryListController(HistoryListWidget):
    def __init__(self, *args, **kwargs):
        super(HistoryListController, self).__init__(*args, **kwargs)
        self.hist_dict = {}
        self.operations_dict = {}

        self.itemDoubleClicked.connect(self.updateHistoryFigure)
        self.itemClicked.connect(self.updateHistoryTable)

    def addItemWithTimestamp(self, text):
        current_time = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.matrix_infos = f"{current_time} - {text}"
        self.addItem(self.matrix_infos)

    def updateHistoryFigure(self, item):
        selected_text = item.text()
        if selected_text in self.hist_dict.keys():
            value = self.hist_dict.get(selected_text)
            self.main.image_view_widget.setImage(value)

    def uptadeOperationsHist(self, infos, text):
        if len(self.operations_dict) == 0:
            self.operations_dict[infos] = [text]
        else:
            list1 = list(self.operations_dict.values())
            new_value = list1[-1].copy()
            new_value.append(text)
            self.operations_dict[infos] = new_value
        print(self.operations_dict)

    def updateHistoryTable(self, item):
        self.main.history_widget.clear()
        selected_text = item.text()
        values = self.operations_dict.get(selected_text, [])

        for value in values:
            self.main.history_widget.addItem(value)