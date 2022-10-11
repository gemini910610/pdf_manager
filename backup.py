from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QStyleOption, QStyle, QTextBrowser, QScrollArea, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter
from PySide6.QtCore import Signal

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
    
    def choose_file(self, filter: str|None = None, mode: str = 'single') -> list[str]|str:
        '''
        filter: PDF Files (*.pdf, *.PDF)
        mode: single, multiple, save
        '''
        match mode:
            case 'single':
                file, _ = QFileDialog.getOpenFileName(filter=filter)
                return file
            case 'multiple':
                files, _ = QFileDialog.getOpenFileNames(filter=filter)
                return files
            case 'save':
                file, _ = QFileDialog.getSaveFileName(filter=filter)
                return file

class ConvertPdfWindow(ChildWindow):
    button_width = 50
    button_height = 50

    def init_ui(self):
        select_button = QPushButton('select', self)
        select_button.resize(self.button_width, self.button_height)
        select_button.move(0, 0)
        select_button.clicked.connect(self.on_click_select_button)
        
        self.text_browser = text_browser = QTextBrowser(self)
        text_browser.resize(self.width(), self.height() - self.button_height)
        text_browser.move(0, self.button_height)

        convert_button = QPushButton('convert', self)
        convert_button.resize(self.button_width, self.button_height)
        convert_button.move(self.button_width, 0)
        convert_button.clicked.connect(self.on_click_convert_button)
    
    def on_click_select_button(self):
        filename = self.choose_file('JSON File (*.json)')
        if filename == '':
            print('no file chose')
            return
        with open(filename, 'r') as file:
            content = file.readlines()
            self.text_browser.setText(''.join(content))
    def on_click_convert_button(self):
        content = self.text_browser.toPlainText()
        if content == '':
            print('please open json file first')
            return
        filename = self.choose_file('PDF File (*.pdf)', 'save')
        if filename == '':
            print('no file chose')
            return
        print('convert data into pdf:')
        print(content)
        print(f'save to file: {filename}')

class FileItem(Widget):
    button_width = 50
    button_height = 50

    def __init__(self, filename: str, parent: QWidget):
        super().__init__(parent)
        self.resize(parent.width(), self.button_height)
        label = QLabel(filename, self)
        label.resize(self.width() - self.button_width * 3, self.button_height)
        move_up_button = QPushButton('up', self)
        move_up_button.resize(self.button_width, self.button_height)
        move_up_button.move(label.width(), 0)
        
        move_down_button = QPushButton('down', self)
        move_down_button.resize(self.button_width, self.button_height)
        move_down_button.move(label.width() + self.button_width, 0)

        remove_button = QPushButton('remove', self)
        remove_button.resize(self.button_width, self.button_height)
        remove_button.move(label.width() + self.button_width * 2, 0)

class MergePdfWindow(ChildWindow):
    remove_item_signal = Signal()
    move_up_signal = Signal()
    move_down_signal = Signal()
    button_width = 50
    button_height = 50
    item_height = 50

    def init_ui(self):
        select_button = QPushButton('select', self)
        select_button.resize(self.button_width, self.button_height)
        select_button.move(0, 0)
        select_button.clicked.connect(self.on_click_select_button)

        scroll_area = QScrollArea(self)
        scroll_area.resize(self.width(), self.height() - self.button_height)
        scroll_area.move(0, self.button_height)
        scroll_area.setWidgetResizable(True)
        scroll_area_content = QWidget()
        scroll_area.setWidget(scroll_area_content)
        self.scroll_area_layout = scroll_area_layout = QVBoxLayout()
        # scroll_area_layout.addWidget(widget)
        scroll_area_content.setLayout(scroll_area_layout)

        merge_button = QPushButton('merge', self)
        merge_button.resize(self.button_width, self.button_height)
        merge_button.move(self.button_width, 0)
        merge_button.clicked.connect(self.on_click_merge_button)
    
    def on_click_select_button(self):
        files = self.choose_file('PDF Files (*.pdf)', 'multiple')
        if files == []:
            print('no file chose')
            return
        print(f'chose file: {", ".join(files)}')
    def on_click_merge_button(self):
        # if files is []
        filename = self.choose_file('PDF Files (*.pdf)', 'save')
        if filename == '':
            print('no file chose')
            return
        print(f'merge pdf to file: {filename}')

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
        self.parent().turn_page_signal.emit(self.page)

class TopBar(Widget):
    turn_page_signal = Signal(int)
    page = 0
    button_width = 75

    def __init__(self, parent: QWidget, height: int, pages: list[ChildWindow], labels: list[str]):
        super().__init__(parent)
        self.turn_page_signal.connect(self.turn_page)
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
