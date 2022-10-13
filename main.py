from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSplitter, QScrollArea, QMessageBox, QCheckBox
from PySide6.QtCore import Qt
import os
import json
import pdf_manager
import logging

class Config:
    def __init__(self):
        if not os.path.exists('config.json'):
            self.default_path = ''
            # self.output_path = ''
            # self.ask_save_output_path = True
            self.save()
        else:
            self.load()
    
    def save(self):
        with open('config.json', 'w') as config_file:
            json.dump(self.__dict__, config_file)
    def load(self):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            self.default_path = config['default_path']
            # self.output_path = config['output_path']
            # self.ask_save_output_path = config['ask_save_output_path']

class Global:
    directory = ''
    config = Config()
    main_window = None
    directories = []
    directories_view = None
    files_view = None

'''
TODO
remove all print()
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

# class MessageBox(QMessageBox):
#     def __init__(self, parent: QWidget):
#         super().__init__(parent)
#         self.setText('Do you want to save as default output path?')
#         self.setInformativeText('You can edit default output path in config.json.')
#         self.yes_button = self.addButton(QMessageBox.Yes)
#         self.addButton(QMessageBox.No)
#         self.check_box = QCheckBox('Don\'t show this again.')
#         self.setCheckBox(self.check_box)

class MainTopBar(HBoxLayout):
    button_width = 100
    button_height = 50

    def __init__(self):
        super().__init__(10)

        change_path_button = QPushButton('change\npath')
        self.addWidget(change_path_button)
        change_path_button.setFixedSize(self.button_width, self.button_height)
        change_path_button.clicked.connect(self.change_path)

        self.path_label = path_label = QLabel(Global.config.default_path)
        self.addWidget(path_label)
        path_label.setFixedHeight(self.button_height)

        convert_button = QPushButton('merge\nconvert')
        self.addWidget(convert_button)
        convert_button.setFixedSize(self.button_width, self.button_height)
        convert_button.clicked.connect(self.convert_and_merge)
    
    def change_path(self):
        default_path = QFileDialog.getExistingDirectory()
        if default_path == '':
            return
        Global.config.default_path = default_path
        Global.config.save()
        self.path_label.setText(Global.config.default_path)
        Global.directories_view.change_path()
        Global.files_view.clear()
    
    '''
    TODO
    add progress bar
    '''
    def convert_and_merge(self):
        merge_output_filename = 'merge_result.pdf'

        # if Global.config.output_path == '':
        #     output_path = QFileDialog.getExistingDirectory()
        #     if Global.config.ask_save_output_path:
        #         message_box = MessageBox(Global.main_window)
        #         message_box.check_box.stateChanged.connect(self.switch_check_box)
        #         message_box.yes_button.clicked.connect(lambda: self.save_output_path(output_path))
        #         message_box.show()
        # else:
        #     output_path = Global.config.output_path

        for directory in Global.directories:
            path = f'{Global.config.default_path}/{directory}'
            files = os.listdir(f'{Global.config.default_path}/{directory}')
            if merge_output_filename in files:
                continue
            pdf_files = []
            for file in files:
                if file.endswith('json'):
                    Global.convert_done = False
                    print(f'[start convert] {file}', end='')
                    '''
                    TODO
                    replace into json to html code
                    '''
                    # json to html
                    filename = file.replace('.json', '')
                    html_code = pdf_manager.json_to_html(f'{path}/{file}')
                    with open(f'{path}/{filename}.html', 'w') as html_file:
                        html_file.write(html_code)
                    # html code to pdf
                    html_code_example = '''
                    <table>
                        <thead>
                            <tr>
                                <th width="50%">Header 1</th>
                                <th width="50%">Header 2</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>cell 1</td><td>cell 2</td></tr>
                            <tr><td>cell 3</td><td>cell 4</td></tr>
                        </tbody>
                    </table>
                    '''
                    pdf_manager.html_code_to_pdf(html_code_example, f'{path}/{filename}.pdf')
                    print(f'\r\033[K[convert done] {file}')
                    pdf_files.append(f'{path}/{filename}.pdf')
                    '''
                    TODO
                    add following code into pdf_manager
                    '''
                    os.remove(f'{path}/{filename}.html')
                elif file.endswith('pdf'):
                    pdf_files.append(f'{path}/{file}')
            # merge pdf
            if pdf_files != []:
                pdf_manager.merge(pdf_files, f'{path}/{merge_output_filename}')
                print(f'[merge success] {directory}')
    
    # def save_output_path(self, output_path):
    #     Global.config.output_path = output_path
    #     Global.config.save()
    
    # def switch_check_box(self):
    #     Global.config.ask_save_output_path = not Global.config.ask_save_output_path
    #     Global.config.save()

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
        Global.files_view.open_directory()

class DirectoriesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)

        self.scroll_area = ScrollArea()
        layout.addWidget(self.scroll_area)
        self.change_path()

    def change_path(self):
        if Global.config.default_path == '':
            return
        self.scroll_area.clear_list()
        directories = os.listdir(Global.config.default_path)
        Global.directories = []
        for directory in directories:
            if os.path.isdir(f'{Global.config.default_path}/{directory}'):
                self.scroll_area.add_widget(DirectoryItem(directory))
                Global.directories.append(f'{directory}')
        self.scroll_area.end_list()
        self.scroll_area.scroll_to_top()

class FileItem(QLabel):
    item_height = 50

    def __init__(self, filename: str):
        super().__init__(f'<a href="file:///{Global.config.default_path}/{Global.directory}/{filename}">{filename}</a>')
        self.setOpenExternalLinks(True)
        self.setFixedHeight(self.item_height)

class FilesView(QWidget):
    label_height = 50

    def __init__(self):
        super().__init__()
        layout = VBoxLayout()
        self.setLayout(layout)

        self.directory_label = directory_label = QLabel('')
        directory_label.setFixedHeight(self.label_height)
        layout.addWidget(directory_label)

        self.scroll_area = ScrollArea()
        layout.addWidget(self.scroll_area)
    
    def open_directory(self):
        self.clear()
        self.directory_label.setText(Global.directory)
        files = os.listdir(Global.config.default_path + '/' + Global.directory)
        for file in files:
            if file.endswith('.pdf') or file.endswith('.json'):
                self.scroll_area.add_widget(FileItem(file))
        self.scroll_area.end_list()
        self.scroll_area.scroll_to_top()
    
    def clear(self):
        self.directory_label.setText('')
        self.scroll_area.clear_list()

class MainContent(QSplitter):
    def __init__(self):
        super().__init__()

        Global.directories_view = DirectoriesView()
        self.addWidget(Global.directories_view)
        Global.files_view = FilesView()
        self.addWidget(Global.files_view)

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

'''
TODO
add exception catcher and will log exception into error.log
'''
app = QApplication([])
if Global.config.default_path == '':
    Global.config.default_path = QFileDialog.getExistingDirectory()
    Global.config.save()
Global.main_window = window = MainWindow()
window.showMaximized()
app.exec()
