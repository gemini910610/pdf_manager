from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QScrollArea
from PySide6.QtCore import Qt
import os

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

        change_directory_button = QPushButton('change\ndirectory')
        self.addWidget(change_directory_button)
        change_directory_button.setFixedSize(self.button_width, self.button_height)
        change_directory_button.clicked.connect(self.change_directory)

        global path
        self.directory_label = directory_label = QLabel(path)
        self.addWidget(directory_label)
        directory_label.setFixedHeight(self.button_height)
    
    def change_directory(self):
        global path
        path = QFileDialog.getExistingDirectory()
        self.directory_label.setText(path)
        '''
        TODO
        clear directories_view_scroll_area
        add all directories into directories_view_scroll_area
        scroll directories_view_scroll_area to top
        clear files_view_scroll_area
        '''

class ScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        self.setWidget(content)
        content.setLayout(VBoxLayout())
    
    def add_widget(self, widget: QWidget):
        layout = self.widget().layout()
        layout.addWidget(widget)
    
    def end_list(self):
        self.widget().layout().addStretch()
    
    def clear_list(self):
        layout = self.widget().layout()
        while layout.count() > 0:
            layout.takeAt(0)

class DirectoryItem(QPushButton):
    button_height = 50

    def __init__(self, directory_name: str):
        super().__init__(directory_name)
        self.setFixedHeight(self.button_height)
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        print(self.text())
        '''
        TODO
        clear files_view_scroll_area
        add all file(hyper link) into files_view_scroll_area
        scroll files_view_scroll_area to top
        '''

class DirectoriesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)

        self.scroll_area = scroll_area = ScrollArea()
        layout.addWidget(scroll_area)

        global path
        self.change_directory(path)
    
    def change_directory(self, path):
        self.scroll_area.clear_list()
        directories = os.listdir(path)
        for directory in directories:
            self.scroll_area.add_widget(DirectoryItem(directory))
        self.scroll_area.end_list()

class FilesViewTopBar(HBoxLayout):
    button_height = 50
    button_width = 50

    def __init__(self):
        super().__init__()
        select_button = QPushButton('v')
        select_button.setFixedSize(self.button_width, self.button_height)
        select_button.clicked.connect(self.select_all_file)
        self.addWidget(select_button)

        convert_button = QPushButton('c')
        convert_button.setFixedSize(self.button_width, self.button_height)
        convert_button.clicked.connect(self.convert_file)
        self.addWidget(convert_button)

        self.addStretch()
    
    def select_all_file(self):
        ...
        '''
        TODO
        select all file, click twice will cancel select
        '''
    
    def convert_file(self):
        ...
        '''
        TODO
        convert json into pdf
        merge pdf
        '''

'''
TODO
add class FileItem
select box/button
hyper link to open file
'''

class FilesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)
        layout.addLayout(FilesViewTopBar())
        scroll_area = ScrollArea()
        layout.addWidget(scroll_area)
        '''
        TODO
        add file into scroll_area
        '''

class MainContent(QSplitter):
    def __init__(self):
        super().__init__()

        self.addWidget(DirectoriesView())
        self.addWidget(FilesView())

        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 4)

class MainWindow(QMainWindow):
    window_width = 500
    window_height = 500

    def __init__(self):
        super().__init__()
        self.resize(self.window_width, self.window_height)
        self.move(0, 0)
        '''
        TODO
        set window title
        '''

        global path

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
path = QFileDialog.getExistingDirectory()
window = MainWindow()
window.show()
app.exec()
