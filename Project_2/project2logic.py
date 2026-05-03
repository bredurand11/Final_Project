from PyQt6.QtWidgets import QMainWindow
from project2gui import Ui_MainWindow
import sys

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """Sets up the window for the user. Sets what each enter button leads to as well as the exit button.
        Hides and shows what is supposed to be displayed on the first window (option to enter number of students,
        the first enter button, and the exit button."""
        super().__init__()
        self.scores = []
        self.setupUi(self)
        self.enter_button_1.clicked.connect(self.student_grade_input)
        self.enter_button_2.clicked.connect(self.show_final_results)
        self.exit_button.clicked.connect(self.close)
        self.enter_button_2.hide()
        self.grade_label1.hide()
        self.grade_label2.hide()
        self.grade_label3.hide()
        self.grade_label4.hide()
        self.grade_input1.hide()
        self.grade_input2.hide()
        self.grade_input3.hide()
        self.grade_input4.hide()
        self.name_label1.hide()
        self.name_label2.hide()
        self.name_label3.hide()
        self.name_label4.hide()
        self.name_input1.hide()
        self.name_input2.hide()
        self.name_input3.hide()
        self.name_input4.hide()
    #Same situation with the first project, a bunch of code for just hiding labels due to FMAN's PyQt6 lack of
    #multi-window support.
    def student_grade_input(self) -> None:
        """First checks if the user inputs one of the valid ranges (1-4) and makes sure they don't use characters. Then
        it displays the labels accordingly."""
        try:
            self.score_count = int(self.stu_input_label.text().strip())
        except ValueError:
            self.error_label.setText("Please enter a number.")
            return
        if self.score_count <= 0 or self.score_count > 4:
            self.error_label.setText("Enter a number between 1 and 4.")
            return

        self.error_label.setText("")

        for label in [self.final_label, self.final_label_2, self.final_label_3, self.final_label_4]:
            label.hide()

        for student_count in [
            self.name_input1, self.name_input2, self.name_input3, self.name_input4,
            self.grade_input1, self.grade_input2, self.grade_input3, self.grade_input4
        ]:
            student_count.clear()

        self.grade_labels = [self.grade_label1, self.grade_label2, self.grade_label3, self.grade_label4]
        self.grade_inputs = [self.grade_input1, self.grade_input2, self.grade_input3, self.grade_input4]
        self.name_labels = [self.name_label1, self.name_label2, self.name_label3, self.name_label4]
        self.name_inputs = [self.name_input1, self.name_input2, self.name_input3, self.name_input4]
        self.final_labels = [self.final_label, self.final_label_2, self.final_label_3, self.final_label_4]

        for i in range(self.score_count):
            self.grade_labels[i].show()
            self.grade_inputs[i].show()
            self.name_labels[i].show()
            self.name_inputs[i].show()

        for i in range(self.score_count, 4):
            self.grade_labels[i].hide()
            self.grade_inputs[i].hide()
            self.name_labels[i].hide()
            self.name_inputs[i].hide()

        self.enter_button_1.hide()
        self.enter_button_2.show()

    def letter(self, grade, highest) -> str:
        """Letter grading scale borrowed from lab 2. Returns the proper grade based on score."""
        if grade >= highest - 10:
            return 'A'
        elif grade >= highest - 20:
            return 'B'
        elif grade >= highest - 30:
            return 'C'
        elif grade >= highest - 40:
            return 'D'
        else:
            return 'F'

    def show_final_results(self):
        """This function starts off by validating user input. It checks for the user leaving names blank, as well as
        checks if the user input any numbers for the name. Also checks if they input characters for the grade instead
        of numbers. If user inputs information correctly it appends the grade and name to a csv file, and then it
        displays it onto labels using a for loop."""
        self.scores = []
        names = []

        for i in range(self.score_count):
            name = self.name_inputs[i].text().strip()
            grade_text = self.grade_inputs[i].text().strip()
            #Not sure if there is an easier way to make it dynamic, that was just the first solution we came up with.

            if not name:
                self.error_label.setText("All students must have a name.")
                return

            try:
                float(name)
                self.error_label.setText("Names cannot be numbers.")
                return
            except ValueError:
                pass

            try:
                grade = float(grade_text)
            except ValueError:
                self.error_label.setText("All grades must be numeric.")
                return

            names.append(name)
            self.scores.append(grade)

        self.error_label.setText("")

        highest = max(self.scores)
        avg = sum(self.scores) / len(self.scores)
        avg_letter = self.letter(avg, highest)

        with open("grading_info.csv", "a") as file:
            for i in range(self.score_count):
                file.write(f"{names[i]}, {self.scores[i]}\n")

        for i in range(self.score_count):
            grade = self.scores[i]
            letter_grade = self.letter(grade, highest)
            self.final_labels[i].setText(
                f"{names[i]} received a {grade:.2f}, which is a {letter_grade}."
            )
            self.final_labels[i].show()

        self.final_label_3.setText(f"Class Average: {avg:.2f}")
        self.final_label_4.setText(f"Class Average Letter Grade: {avg_letter}")
        self.final_label_3.show()
        self.final_label_4.show()

        self.enter_button_2.hide()
        for labels in (
            self.grade_label1, self.grade_label2, self.grade_label3, self.grade_label4,
            self.grade_input1, self.grade_input2, self.grade_input3, self.grade_input4,
            self.name_label1, self.name_label2, self.name_label3, self.name_label4,
            self.name_input1, self.name_input2, self.name_input3, self.name_input4
        ):
            labels.hide()

        self.enter_button_1.show()
        self.exit_button.show()
        self.stu_input_label.clear()

    def close(self):
        sys.exit(0)
