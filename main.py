from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QStyleOption, QStyle
from PySide6.QtGui import QPainter

class Widget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
    
    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)

class ChildWindow(Widget):
    def __init__(self, parent: QWidget, top_bar_height: int, is_default: bool = False):
        super().__init__(parent)
        self.resize(parent.width(), parent.height() - top_bar_height)
        self.move(0, top_bar_height)
        if is_default:
            self.show()
        else:
            self.hide()
        self.init_ui()

    def init_ui(self):
        ...

class ConvertPdfWindow(ChildWindow):
    def init_ui(self):
        ...
        # select json file: button
        # show json file content: text browser
        # start convert: button (select direction and filename)

class MergePdfWindow(ChildWindow):
    def init_ui(self):
        ...
        # select pdf files: button
        # show selected files: ?
        # start merge: button (select direction and filename)
    
    def choose_file(self, filter: str):
        '''
        filter: PDF Files (*.pdf, *.PDF)
        '''
        files, _ = QFileDialog.getOpenFileNames(filter=filter)
        print('no file chose' if len(files) == 0 else files)

class ShowPdfWindow(ChildWindow):
    def init_ui(self):
        ...
        # file browser
        # maybe use os.listdir ?
        # hyper link to open pdf

class TopBarButton(QPushButton):
    def __init__(self, text: str, parent: QWidget, page: int, width: int):
        super().__init__(text, parent)
        self.resize(width, parent.height())
        self.page = page
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        self.parent().turn_page(self.page)

class TopBar(Widget):
    page = 0
    button_width = 75

    def __init__(self, parent: QWidget, height: int, pages: list[ChildWindow], labels: list[str]):
        super().__init__(parent)
        self.resize(parent.width(), height)
        self.pages = pages
        for i in range(len(pages)):
            label = labels[i]
            button = TopBarButton(label, self, i, self.button_width)
            button.move(self.button_width * i, 0)
    
    def turn_page(self, page: int):
        if self.page == page:
            return
        self.pages[self.page].hide()
        self.page = page
        self.pages[page].show()

class MainWindow(QMainWindow):
    page = 0
    pages = []
    top_bar_height = 50
    screen_width = 500
    screen_height = 500

    def __init__(self):
        super().__init__()
        self.resize(self.screen_width, self.screen_height)
        self.move(0, 0)
        self.init_ui()
    
    def init_ui(self):
        self.pages.append(ConvertPdfWindow(self, self.top_bar_height, True))
        self.pages.append(MergePdfWindow(self, self.top_bar_height))
        self.pages.append(ShowPdfWindow(self, self.top_bar_height))
        TopBar(self, self.top_bar_height, self.pages, ['convert', 'merge', 'show'])

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
