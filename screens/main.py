import sys
import os
from PyQt6.QtWidgets import QApplication
from home import FullScreenWindow
from screen2 import chooseScreenWindow
from screen3 import ResultWindow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyse import *
from src.fetch_data import fetch_data
from src.visualise import *

class ScreenManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self.show_home_screen()

    def show_home_screen(self):
        if self.window:
            self.window.close()  # Close any currently open window
        screen_dir = os.path.dirname(__file__)

        # Construct the relative path to img.png
        img_path = os.path.join(screen_dir, '..', 'resources', 'home.jpeg')

        # Convert to absolute path (optional, but safer)
        img_path = os.path.abspath(img_path)
        self.window = FullScreenWindow(img_path)
        self.window.navigate_next.connect(self.show_choose_screen)
        self.window.show()

    def show_choose_screen(self):
        if self.window:
            self.window.close()  # Close the home screen
        screen_dir = os.path.dirname(__file__)

        # Construct the relative path to img.png
        img_path = os.path.join(screen_dir, '..', 'resources', 'bg.png')

        # Convert to absolute path (optional, but safer)
        img_path = os.path.abspath(img_path)
        self.window = chooseScreenWindow(img_path)
        self.window.navigate_next.connect(self.handle_next)
        self.window.navigate_previous.connect(self.show_home_screen)
        self.window.show()

    def handle_next(self, source):
        # Fetch data and analyze based on the source
        data = fetch_data(source)
        analysis_results = analyse(data)
        
        # After fetching data and analysis, show result screen
        self.show_result_screen(data, analysis_results)

    def show_result_screen(self, data, analysis_results):
        if self.window:
            self.window.close()
        self.window = ResultWindow(data, analysis_results)
        self.window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    screen_manager = ScreenManager()
    screen_manager.run()
