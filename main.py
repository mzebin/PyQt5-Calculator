# Importing Required Modules.
from functools import partial
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculatorUI(QMainWindow):

    def __init__(self):
        super(CalculatorUI, self).__init__()

        # Setting the Window title.
        self.setWindowTitle("Calculator")

        # Setting the Fixed size for the window.
        self.setFixedSize(400, 500)

        # Creating Layouts.
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QGridLayout()

        # Creating and Setting the Central widget.
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.layout_1)

        # Creating Display and Buttons.
        self._create_display()
        self._create_buttons()

    def _create_display(self):
        # Creating the Input Box.
        self.display = QLineEdit()

        # Setting some properties for the display.
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        # Adding the Display to layout 1.
        self.layout_1.addWidget(self.display)

    def _create_buttons(self):
        self.buttons = {}

        # Creating a Dictionary of Buttons
        # and it's positions.
        buttons = {
            "7": (0, 0), "8": (0, 1),
            "9": (0, 2), "/": (0, 3),
            "C": (0, 4), "4": (1, 0),
            "5": (1, 1), "6": (1, 2),
            "*": (1, 3), "(": (1, 4),
            "1": (2, 0), "2": (2, 1),
            "3": (2, 2), "-": (2, 3),
            ")": (2, 4), "0": (3, 0),
            "00": (3, 1), ".": (3, 2),
            "+": (3, 3), "=": (3, 4),
        }

        # Loop through the dictionary of buttons.
        for txt, pos in buttons.items():
            # Creating a button and adding it to the dictionary.
            self.buttons[txt] = QPushButton(txt)

            # Setting Some Properties of Button.
            self.buttons[txt].setFixedHeight(100)

            # Adding Button to layout 2.
            self.layout_2.addWidget(self.buttons[txt], pos[0], pos[1])

        # Adding layout 2 to layout 1.
        self.layout_1.addLayout(self.layout_2)

    def set_display_text(self, txt):
        # Changing the Display's text.
        self.display.setText(txt)

        # Setting the Focus to display.
        self.display.setFocus()


class CalculatorCtrl:

    def __init__(self, view: CalculatorUI):
        self._view = view
        self.error_msg = "ERROR"

        # Adding Button Actions.
        self._add_actions()

    def _build_expressions(self, sub_expression):
        # Check if the text is error message.
        if self._view.display.text() == self.error_msg:
            self._view.display.setText("")

        # Creating New Expression and Setting the text.
        expression = self._view.display.text()
        self._view.set_display_text(expression + sub_expression)

    def _evaluate(self):
        # Getting the expression.
        expression = self._view.display.text()

        try:
            result = str(eval(expression, {}, {}))
        except SyntaxError:
            result = self.error_msg

        # Setting the result.
        self._view.display.setText(result)

    def _add_actions(self):
        # Adding Key Bindings.
        self._view.display.returnPressed.connect(self._evaluate)

        # Adding Button Actions.
        for txt, btn in self._view.buttons.items():
            if txt == "C":
                btn.clicked.connect(lambda: self._view.display.setText(""))
            elif txt == "=":
                btn.clicked.connect(self._evaluate)
            else:
                btn.clicked.connect(partial(self._build_expressions, txt))


def main():
    # Creating the Application.
    calculator = QApplication(sys.argv)

    # Creating the Main window.
    main_window = CalculatorUI()
    main_window.show()

    # Calculator's Control.
    CalculatorCtrl(main_window)

    # Executing the App.
    calculator.exec_()
    # sys.exit(calculator.exec_())


if __name__ == "__main__":
    main()
