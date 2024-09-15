import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from analyse import *
from fetch_data import fetch_data
from visualise import *


from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextEdit, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from analyse import *
from fetch_data import fetch_data
from visualise import *

class ResultWindow(QWidget):
    def __init__(self, texts, analysis_results):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Analysis Results')

        # Full screen setup
        self.showFullScreen()

        # Set the layout
        self.layout = QVBoxLayout()

        # Add padding, spacing, and margins
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)

        # Set the background color and text styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1d2b64;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
            }
            QTextEdit {
                border: 2px solid #ffffff;
                border-radius: 10px;
                background-color: #2a3f87;
                padding: 10px;
                color: white;
                font-size: 16px;
            }
            QPushButton {
                font-size: 18px;
                color: white;
                background-color: #1d72b8;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #135a96;
            }
        """)

        # Create a title label
        self.title_label = QLabel("Analysis Results")
        self.title_label.setFont(QFont('Segoe UI', 22, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add title to the layout
        self.layout.addWidget(self.title_label)

        # Create a QTextEdit to display the results
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)  # Make the text edit read-only

        # Display Collection Risk Score at the top with a bigger font for emphasis
        self.result_display.append(f"<b>Collection Risk Score: {analysis_results.risk_score_mean:.2f}</b>\n")

        # Add the detailed analysis results to the QTextEdit
        for result in analysis_results.to_dict()['analyses']:
            original_text = texts[result['index']]
            sanitized_text = result['sanitized_text']
            risk_score_mean = result['risk_score_mean']

            # Add the text with proper formatting
            self.result_display.append(f" ")
            self.result_display.append(f"<b>Original Text:</b> {original_text}")
            self.result_display.append(f"<b>Sanitized Text:</b> {sanitized_text}")
            self.result_display.append(f"<b>Risk Score Mean:</b> {risk_score_mean:.2f}")
            self.result_display.append("<b>Detected PII:</b>")

            for pii in result['analysis']:
                pii_type = pii.get('pii_type_detected', None)
                if pii_type:
                    risk_level = pii.get('risk_level', 'Unknown')
                    risk_level_definition = pii.get('risk_level_definition', 'Unknown')
                    score = pii.get('score', 'N/A')
                    start_index = pii.get('start', 'N/A')
                    end_index = pii.get('end', 'N/A')

                    self.result_display.append(f"  - <b>PII Type Detected:</b> {pii_type}")
                    self.result_display.append(f"    <b>Risk Level:</b> {risk_level} ({risk_level_definition})")
                    self.result_display.append(f"    <b>Score:</b> {score if score != 'N/A' else 'N/A'}")
                    self.result_display.append(f"    <b>Start Index:</b> {start_index}")
                    self.result_display.append(f"    <b>End Index:</b> {end_index}")

        # Add the result display to the layout
        self.layout.addWidget(self.result_display)

        # Add a "Visualise" button
        self.visualise_button = QPushButton("Visualise")
        self.visualise_button.setFont(QFont('Segoe UI', 18))
        self.visualise_button.clicked.connect(lambda: self.visualise_button_clicked(texts, analysis_results))  # Connect button click to a function
        self.layout.addWidget(self.visualise_button)

        self.setLayout(self.layout)

    # Define the function to be called when the 'Visualise' button is clicked
    def visualise_button_clicked(self, texts, analysis_results):
        # This function can call any visualisation logic from the 'visualise' module
        print("Visualise button clicked")
        # Example call (you can replace this with actual logic):
        visualise(texts, analysis_results)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Q:
            self.close()

# Example usage
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get data and analysis results
    source_input = input("Enter data source (database/cloud): ").strip().lower()
    data = fetch_data(source_input)
    analysis_results = analyse(data)

    # Display results in PyQt6 window
    window = ResultWindow(data, analysis_results)
    window.show()

    sys.exit(app.exec())
