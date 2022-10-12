from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QScrollArea
from PySide6.QtCore import Qt, QUrl
import os

class Global:
    path = ''
    directory = ''
    directories_scroll_area = None
    files_scroll_area = None

'''
TODO
check path is not empty before do anything
'''

class HBoxLayout(QHBoxLayout):
    def __init__(self, spacing: int = 0):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(spacing)

class VBoxLayout(QVBoxLayout):
    def __init__(self, spacing: int = 0):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(spacing)

class MainTopBar(HBoxLayout):
    button_width = 100
    button_height = 50

    def __init__(self):
        super().__init__(10)

        change_path_button = QPushButton('change\npath')
        self.addWidget(change_path_button)
        change_path_button.setFixedSize(self.button_width, self.button_height)
        change_path_button.clicked.connect(self.change_path)

        self.path_label = path_label = QLabel(Global.path)
        self.addWidget(path_label)
        path_label.setFixedHeight(self.button_height)
    
    def change_path(self):
        Global.path = QFileDialog.getExistingDirectory()
        self.path_label.setText(Global.path)
        Global.directories_scroll_area.clear_list()
        Global.files_scroll_area.clear_list()
        directories = os.listdir(Global.path)
        for directory in directories:
            if os.path.isdir(f'{Global.path}/{directory}'):
                Global.directories_scroll_area.add_widget(DirectoryItem(directory))
        Global.directories_scroll_area.end_list()
        Global.directories_scroll_area.scroll_to_top()

class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        self.setWidget(content)
        content.setLayout(VBoxLayout())
    
    def add_widget(self, widget: QWidget):
        self.widget().layout().addWidget(widget)
    
    def end_list(self):
        self.widget().layout().addStretch()
    
    def clear_layout(layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
    def clear_list(self):
        ScrollArea.clear_layout(self.widget().layout())
    
    def scroll_to_top(self):
        self.verticalScrollBar().setValue(0)

class DirectoryItem(QPushButton):
    button_height = 50

    def __init__(self, directory_name: str):
        super().__init__(directory_name)
        self.setFixedHeight(self.button_height)
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        Global.directory = self.text()
        Global.files_scroll_area.clear_list()
        files = os.listdir(Global.path + '/' + self.text())
        for file in files:
            if file.endswith('.pdf') or file.endswith('.json'):
                Global.files_scroll_area.add_widget(FileItem(file))
        Global.files_scroll_area.end_list()
        Global.files_scroll_area.scroll_to_top()

class DirectoriesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)

        Global.directories_scroll_area = ScrollArea()
        layout.addWidget(Global.directories_scroll_area)

        self.change_directory(Global.path)
    
    def change_directory(self, path):
        scroll_area = Global.directories_scroll_area
        scroll_area.clear_list()
        directories = os.listdir(path)
        for directory in directories:
            if os.path.isdir(f'{path}/{directory}'):
                scroll_area.add_widget(DirectoryItem(directory))
        scroll_area.end_list()
        scroll_area.scroll_to_top()

class FileItem(QLabel):
    item_height = 50

    def __init__(self, filename: str):
        url = f'file:///{Global.path}/{Global.directory}/{filename}'
        '''
        TODO
        check following code
        '''
        url = bytearray(QUrl.fromLocalFile(url).toEncoded()).decode()
        super().__init__(f'<a href="{url}">{filename}</a>')
        self.setOpenExternalLinks(True)
        self.setFixedHeight(self.item_height)

class FilesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)

        Global.files_scroll_area = ScrollArea()
        layout.addWidget(Global.files_scroll_area)

class MainContent(QSplitter):
    def __init__(self):
        super().__init__()

        self.addWidget(DirectoriesView())
        self.addWidget(FilesView())

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 9)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.move(0, 0)
        '''
        TODO
        set window title
        '''

        widget = QWidget()
        layout = VBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        layout.addLayout(MainTopBar())
        layout.addWidget(MainContent())

app = QApplication([])
'''
TODO
select directory and write into config file
'''
Global.path = QFileDialog.getExistingDirectory()
window = MainWindow()
window.showMaximized()
app.exec()
