from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

from kivy.core.window import Window
Window.size = (400, 600)

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.lang import Builder
from pdf2docx import Converter
import os

KV = """
Screen:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        MDToolbar:
            title: 'PDF to DOCX Converter'
            elevation: 10
            left_action_items: [['menu', lambda x: None]]
        MDTextField:
            id: pdf_file_input
            hint_text: 'Select PDF file'
            readonly: True
            icon_right: 'folder'
            icon_right_color: app.theme_cls.primary_color
            on_focus: if self.focus: app.file_manager_open('pdf')
        MDRaisedButton:
            id: convert_button
            text: 'Convert'
            on_release: app.convert_pdf_to_docx()
"""

class PDFtoDOCXConverterApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_string(KV)

    def file_manager_open(self, file_type):
        self.file_manager.filetype = file_type
        self.file_manager.show('/')

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        if self.file_manager.filetype == 'pdf':
            self.root.ids.pdf_file_input.text = path
        self.file_manager.close()

    def convert_pdf_to_docx(self):
        pdf_file_path = self.root.ids.pdf_file_input.text
        if pdf_file_path:
            docx_file_path = os.path.splitext(pdf_file_path)[0] + '.docx'
            try:
                cv = Converter(pdf_file_path)
                cv.convert(docx_file_path)
                cv.close()
                self.root.ids.convert_button.text = 'Converted Successfully'
                self.root.ids.convert_button.md_bg_color = (0, 0.8, 0, 1)
            except Exception as e:
                self.root.ids.convert_button.text = 'Conversion Failed'
                self.root.ids.convert_button.md_bg_color = (0.8, 0, 0, 1)
                print(e)
        else:
            self.root.ids.convert_button.text = 'Choose a PDF file'
            self.root.ids.convert_button.md_bg_color = (0.8, 0, 0, 1)

    def on_start(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path
        )

if __name__ == '__main__':
    PDFtoDOCXConverterApp().run()
