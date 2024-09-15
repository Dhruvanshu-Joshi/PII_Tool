import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class FullScreenWindow(QMainWindow):
    navigate_next = pyqtSignal()
    def __init__(self, image_path):
        super().__init__()

        # Create a QLabel to display the image
        self.label = QLabel(self)

        # Load the image and scale it to the screen size
        pixmap = QPixmap(image_path)
        screen_size = QApplication.primaryScreen().size()
        scaled_pixmap = pixmap.scaled(screen_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding)

        # Set the scaled pixmap to the label
        self.label.setPixmap(scaled_pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a QWidget for the overlay
        self.overlay = QWidget(self.label)
        self.overlay.setGeometry(0, 0, screen_size.width(), screen_size.height())

        # # Create the title label
        # self.title = QLabel("Automated Preferential Looking", self.overlay)
        # self.title.setStyleSheet("font-size: 48px; color: #EBFFC5; background: rgba(0, 0, 0, 0); font-weight: bold;")
        # self.title.setFixedSize(800, 60) 
        # self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.title.setGeometry(screen_size.width() // 2 - 400, screen_size.height() // 2 + 150, 800, 60)

        # Create the start button
        self.button = QPushButton("Start", self.overlay)
        self.button.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #ff66c4; background-color: white; padding: 10px 20px; border-radius: 10px;"
        )
        self.button.setFixedSize(250, 60)
        self.button.setGeometry(screen_size.width() // 2 + 270, screen_size.height() // 2 + 140, 250, 60)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.navigate_next.emit)
        self.close()

        # Set the central widget of the main window
        self.setCentralWidget(self.label)

        # Remove window borders and show the window in full screen mode
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

    def start_experiment(self):
        self.button.clicked.connect(self.navigate_next.emit)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Path to the provided image file
    image_path = '../resources/home.jpeg'
    window = FullScreenWindow(image_path)

    sys.exit(app.exec())