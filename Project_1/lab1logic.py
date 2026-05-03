from PyQt6.QtWidgets import QMainWindow, QButtonGroup
from lab1ui import Ui_MainWindow
import sys
import os
import random
class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """This constructs the program. Sets what buttons activate which functions, adds the radio buttons into the
        radio group in order to clear selection later on."""
        super().__init__()
        self.setupUi(self)
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.isabella_button)
        self.radio_group.addButton(self.genji_button)
        self.radio_group.addButton(self.hannah_button)
        #Had to hard code the color for the exception labels after realizing they were in the minimum requirements.
        self.exception_label.setStyleSheet("color: red;")
        self.exception_label_no_selection.setStyleSheet("color: red;")
        self.exception_label_used_id.setStyleSheet("color: red;")
        self.vote_button.clicked.connect(self.candidate_menu_show)
        self.submit_button.clicked.connect(self.results_vote_menu)
        self.exit_button.clicked.connect(self.close_window)
        self.results_button.clicked.connect(self.show_results)
        self.isabella = 0
        self.genji = 0
        self.hannah = 0
        self.load_votes()

    def load_votes(self) -> None:
        """This function reads from the csv file and increments the total votes for each candidate
        accordingly."""
        if not os.path.exists("used_ids.csv"):
            return
        with open("used_ids.csv", "r") as file:
            for line in file:
                self.user_id, candidate = line.strip().split(",")
                if candidate == "Isabella":
                    self.isabella += 1
                elif candidate == "Genji":
                    self.genji += 1
                elif candidate == "Hannah":
                    self.hannah += 1
        #This was the most effective way we could think of tracking the votes, hope there wasn't something easier.
    def exception_handle_clear(self) -> None:
        """This clears all 3 of the exception labels so the messages don't overlap later on."""
        self.exception_label_no_selection.setText("")
        self.exception_label.setText("")
        self.exception_label_used_id.setText("")

    def load_used_ids(self) -> set[str]:
        """This loads all previous IDs to help keep the ID generator unique for each voter."""
        if not os.path.exists("used_ids.csv"):
            return set()
        with open("used_ids.csv", "r") as file:
            return {line.strip().split(",")[0] for line in file}

    def id_generator(self) -> str:
        """This is what actually creates the unique ID. First, it loads the used IDs, next it generates randrange
        string between 100 million and 999 million and uses a while True loop to check against the IDs in the csv file.
        If the ID is not found, it then returns it to the user in the label in the candidate menu."""
        self.used_ids = self.load_used_ids()
        while True:
            self.unique_id = str(random.randrange(100000000, 999999999))
            if self.unique_id not in self.used_ids:
                return self.unique_id
    def candidate_menu_show(self) -> None:
        """This menu appears after the user clicks the vote option on the vote menu. It hides all of the buttons from
        the vote menu and then shows all of the buttons from the candidate menu. It's also where the user is given
        their unique ID which is then displayed in a label below."""
        self.user_id = self.id_generator()
        self.vote_button.hide()
        self.vote_menu.hide()
        self.exit_button.hide()
        self.results_button.hide()
        self.candidate_menu.show()
        self.hannah_button.show()
        self.genji_button.show()
        self.isabella_button.show()
        self.submit_button.show()
        self.isabella_votes.hide()
        self.genji_votes.hide()
        self.hannah_votes.hide()
        self.id_insertion.show()
        self.id_label.show()
        self.id_insertion.clear()
        self.id_label.setText(f"Your unique voter ID is: ({self.user_id}), please re-type before you click submit:")
        #Unfortunately the FMan PyQt6 designer doesn't have multi-window support (that we could find), so we had
        #to hard code all of the button hiding and showing ourselves.
    def results_vote_menu(self) -> None:
        """This appears after the user has typed their correct idea and chosen a radio button
        before clicking submit. Exception handling for correct ID input and checking whether or not they chose
        a candidate appears here as well. If the user has followed the instructions, it takes their choice and adds
        their user ID alongside their candidate choice to the csv file. After it does that it clears the radio buttons
        to prevent the next candidate from seeing who the previous candidate voted for."""
        self.exception_handle_clear()
        if not (self.isabella_button.isChecked() or self.genji_button.isChecked() or self.hannah_button.isChecked()):
            self.exception_label_no_selection.setText("Please select a candidate before pressing submit.")
            return
        self.user_id_match = self.id_insertion.text().strip()
        if self.user_id_match != self.user_id:
            self.exception_label_used_id.setText("ID doesn't match! Please try again.")
            return
        if self.user_id_match in self.used_ids:
            self.exception_label.setText("ID already used. Please try again.")
            return
        self.vote_button.show()
        self.vote_menu.show()
        self.exit_button.show()
        self.results_button.show()
        self.candidate_menu.hide()
        self.hannah_button.hide()
        self.genji_button.hide()
        self.isabella_button.hide()
        self.submit_button.hide()
        self.id_label.hide()
        self.exception_label.hide()
        self.id_insertion.hide()
        with open("used_ids.csv", "a") as file:

            if self.isabella_button.isChecked():
                file.write(f"{self.user_id},Isabella\n")
                self.isabella += 1
            if self.genji_button.isChecked():
                file.write(f"{self.user_id},Genji\n")
                self.genji += 1
            if self.hannah_button.isChecked():
                file.write(f"{self.user_id},Hannah\n")
                self.hannah += 1

        self.radio_group.setExclusive(False)
        self.isabella_button.setChecked(False)
        self.genji_button.setChecked(False)
        self.hannah_button.setChecked(False)
        self.radio_group.setExclusive(True)

    def close_window(self) -> None:
        """Closes the window whenever the user clicks the exit button on the vote menu."""
        sys.exit(0)
    def show_results(self) -> None:
        """Shows the voting results for the candidates whenever the user clicks view results."""
        self.hannah_votes.show()
        self.genji_votes.show()
        self.isabella_votes.show()
        self.hannah_votes.setText(f"Hannah - {self.hannah}")
        self.genji_votes.setText(f"Genji - {self.genji}")
        self.isabella_votes.setText(f"Isabella - {self.isabella}")
