from widget.imageview_widget import ImageViewWidget


class ImageViewController(ImageViewWidget):
    def __init__(self, *args, **kwargs):
        super(ImageViewController, self).__init__(*args, **kwargs)
        self.main_matrix = None