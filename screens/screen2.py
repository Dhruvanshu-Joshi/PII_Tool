import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class chooseScreenWindow(QMainWindow):
    navigate_next = pyqtSignal(str)  # Signal for next screen
    navigate_previous = pyqtSignal()  # Signal for previous screen

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

        # Create the Database button (Button2)
        self.button2 = QPushButton("Database", self.overlay)
        self.button2.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #ff66c4; background-color: white; padding: 10px 20px; border-radius: 10px;"
        )
        self.button2.setFixedSize(250, 60)
        self.button2.setGeometry(screen_size.width() // 2 + 270, screen_size.height() // 2 - 100, 250, 60)
        self.button2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button2.clicked.connect(lambda: self.on_next_button_clicked('database'))

        # Create the Start button (Button1)
        self.button1 = QPushButton("Cloud", self.overlay)
        self.button1.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #ff66c4; background-color: white; padding: 10px 20px; border-radius: 10px;"
        )
        self.button1.setFixedSize(250, 60)
        self.button1.setGeometry(screen_size.width() // 2 + 270, screen_size.height() // 2 + 100, 250, 60)
        self.button1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button1.clicked.connect(lambda: self.on_next_button_clicked('cloud'))

        # Create the Previous Page button (Button3)
        self.button3 = QPushButton("Previous Page", self.overlay)
        self.button3.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: white; background-color: #ff66c4; padding: 10px 20px; border-radius: 10px;"
        )
        self.button3.setFixedSize(250, 60)
        self.button3.setGeometry(screen_size.width() - 260, screen_size.height() - 150, 250, 60)
        self.button3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button3.clicked.connect(self.on_previous_button_clicked)

        # Set the central widget of the main window
        self.setCentralWidget(self.label)

        # Remove window borders and show the window in full screen mode
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

    def on_next_button_clicked(self, source):
        # Emit signal to navigate to the next screen
        self.navigate_next.emit(source)

    def on_previous_button_clicked(self):
        # Emit signal to navigate to the previous screen
        self.navigate_previous.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Path to the provided image file
    image_path = '../resources/bg.png'
    window = chooseScreenWindow(image_path)

    # Connect the signals to actions
    window.navigate_next.connect(lambda: print("Navigating to next screen..."))  # Placeholder for actual navigation
    window.navigate_previous.connect(lambda: print("Navigating to previous screen..."))  # Placeholder for actual navigation

    sys.exit(app.exec())
