import sys
import qdarkstyle

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QApplication, QStatusBar, QMenuBar

from controller.history_list_controller import HistoryListController
from controller.imageview_controller import ImageViewController
from controller.postpocessing_tab_controller import PostProcessingTabController
from controller.slider_controller import SliderController
from controller.toolbar_controller import ToolBarController
from widget.history_list_widget import HistoryListWidget
from controller.tab_controller import TabController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set stylesheet
        self.styleSheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(self.styleSheet)

        # Set window parameters
        self.setWindowTitle('Test')
        self.setGeometry(0, 0, 1100, 800)

        # Add a status bar and a menu bar
        self.setStatusBar(QStatusBar(self))
        self.setMenuBar(QMenuBar(self))

        # Set the central widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Set layouts
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # Add an image view
        self.image_view_widget = ImageViewController(parent=self)
        self.right_layout.addWidget(self.image_view_widget)

        self.bm4d_slider = SliderController(parent=self)
        self.right_layout.addWidget(self.bm4d_slider)

        # Add history
        self.history_layout = QHBoxLayout()
        self.right_layout.addLayout(self.history_layout)

        self.history_controller = HistoryListController(parent=self)
        self.history_layout.addWidget(self.history_controller)
        self.history_controller.setMaximumHeight(200)

        self.history_widget = HistoryListWidget(parent=self)
        self.history_layout.addWidget(self.history_widget)
        self.history_widget.setMaximumHeight(200)

        self.toolbar_controller = ToolBarController(parent=self)
        self.addToolBar(self.toolbar_controller)

        self.tab_controller = TabController(parent=self)
        self.left_layout.addWidget(self.tab_controller)
        self.tab_controller.setMaximumSize(500, 1000)

        self.postprocessing_controller = PostProcessingTabController(parent=self)
        self.tab_controller.postprocessing_layout.addWidget(self.postprocessing_controller)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = MainWindow()

    sys.exit(app.exec())
