from pyqtgraph import ImageView


class ImageViewWidget(ImageView):
    def __init__(self, parent, *args, **kwargs):
        super(ImageViewWidget, self).__init__(*args, **kwargs)
        self.main = parent

        self.setMinimumSize(400, 400)
