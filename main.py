import os
import sys
import json
import re
import webbrowser
from os import path as file
from inspect import currentframe, getframeinfo

from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QCheckBox, QVBoxLayout, QFormLayout, \
    QLabel, QLineEdit, QPushButton
from OpenApps2 import Ui_OpenApps

# this regex is used to find the name of the app in the path
name_regex = r"(?<=/|\\)(\w* ?){0,4}(?=\.)"
valid_website_regex = r"(https://|http://)?(www\.)?.*(\.).*"


# this loads the data from the json file when the app starts or creates the
# json file if there is no json file
def load_json():
    data_template = {
        'desktop': [],
        'desktop_is_checked': [],
        'website': [],
        'website_is_checked': [],
        'website_name': []
    }
    if file.isfile("data.json"):
        if file.getsize("data.json") == 0:
            try:
                with open("data.json", "w") as json_file:
                    json.dump(data_template, json_file)
            except IOError as error:
                print(error)

        # IMPORTANT this will be used later to load data into application note self.data is globally accessible
        else:
            try:
                with open("data.json", "r") as json_file:
                    json.load(json_file)
                    # print(self.data)
            except IOError:
                print("there was an error")
    elif not file.isfile("data.json"):
        with open("data.json", "w") as json_file:
            json.dump(data_template, json_file)


load_json()


# Adds a messagebox
def add_messagebox(text, title="there was an error"):
    message = QMessageBox()
    message.setWindowTitle(title)
    message.setIcon(QMessageBox.Warning)
    message.setText(text)
    message.setWindowIcon(QIcon("icon.png"))
    message.exec_()


# Adds a checkbox
def add_checkbox(name, checked):
    checkbox = QCheckBox()
    checkbox.setChecked(checked)
    checkbox.setText(name)
    checkbox.setObjectName(name)
    return checkbox


class Main(QWidget, Ui_OpenApps):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        self.setupUi(self)
        # Updates the window
        self.update()
        self.form = Form()

        QFontDatabase.addApplicationFont("montserrat.regular.ttf")
        self.my_font = QFont("Montserrat", 18)
        self.setFont(self.my_font)

        self.setWindowIcon(QIcon("icon.png"))

        # All the connections
        self.insert_app_button.clicked.connect(self.add_desktop)
        self.remove_app_button.clicked.connect(self.delete_desktop_apps)
        self.run_app_button.clicked.connect(self.run_desktop_app)
        self.insert_website_button.clicked.connect(self.open_form)
        self.remove_website_button.clicked.connect(self.delete_website)
        self.run_website_button.clicked.connect(self.run_website)
        self.run_all_button.clicked.connect(self.run_all)

    # Adds desktop apps to file and in the widget
    def add_desktop(self):
        path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")[0]
        # print(path)
        if path != "":
            try:
                with open("data.json", "r") as json_file_read:
                    print(path)
                    data = json.load(json_file_read)
                    if path in data["desktop"]:
                        app_name = re.search(name_regex, path).group()
                        text = f"the program '{app_name}' is already in your list"
                        add_messagebox(text)

                    elif path not in data["desktop"]:
                        print(f"adding path to file")
                        data["desktop"].append(path)
                        data["desktop_is_checked"].append(True)
                        try:
                            app_name = re.search(name_regex, path).group()
                            checkbox = add_checkbox(app_name, True)
                            checkbox.stateChanged.connect(self.update_checked)
                            self.app_container.addWidget(checkbox)
                            with open("data.json", "w") as json_file_write:
                                json.dump(data, json_file_write, indent=2)
                        except IOError as error:
                            print(f"there was an error on line 158: {error}")
            except IOError as error:
                print(f"there was an error in the add_data method: {error}")


    # Method used to update the window when it is necessary
    def update(self):
        load_json()
        self.show_desktop_apps(self)
        self.show_website(self)

    # Shows the desktop apps in the window and is also called in the update function
    @staticmethod
    def show_desktop_apps(self):
        try:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
                apps = data["desktop"]
                is_checked = data["desktop_is_checked"]

                try:
                    for i in range(0, len(apps)):
                        app_name = re.search(name_regex, apps[i]).group() or "Invalid name"
                        print(apps[i])
                        checkbox = add_checkbox(app_name, is_checked[i])
                        checkbox.stateChanged.connect(self.update_checked)
                        self.app_container.addWidget(checkbox)
                except Exception as error:
                    print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        except IOError as error:
            print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Updates the state of the checkbox to determine whether it should run or not
    def update_checked(self):
        try:
            with open("data.json", "r") as json_file_read:
                data = json.load(json_file_read)
                updated_app_list = []
                updated_website_list = []

                for i in range(0, len(data["desktop_is_checked"])):
                    app_items = self.app_container.itemAt(i).widget().isChecked()
                    updated_app_list.append(app_items)
                data["desktop_is_checked"] = updated_app_list
                for i in range(0, len(data["website_is_checked"])):
                    website_items = self.website_container.itemAt(i).widget().isChecked()
                    updated_website_list.append(website_items)
                data["website_is_checked"] = updated_website_list
                try:
                    with open("data.json", "w") as json_file_write:
                        json.dump(data, json_file_write, indent=2)
                except IOError as error:
                    print(f"there was an error in the update_checked method on line 235 {error}")

        except IOError as error:
            print(f"there was an error in the update_checked method on line 230 {error}")


    # Deletes desktop apps from the window as well as the json file
    def delete_desktop_apps(self):
        try:
            with open("data.json", "r") as json_file_read:
                data = json.load(json_file_read)
                number_of_apps = len(data["desktop"])

                updated_app_list = []
                updated_state_list = []
                for i in range(0, number_of_apps):
                    app_is_checked = self.app_container.itemAt(i).widget().isChecked()
                    if app_is_checked:
                        updated_app_list.append(data["desktop"][i])
                        updated_state_list.append(data["desktop_is_checked"][i])
                    elif not app_is_checked:
                        self.app_container.itemAt(i).widget().deleteLater()
                data["desktop"] = updated_app_list
                data["desktop_is_checked"] = updated_state_list
                try:
                    with open("data.json", "w") as json_file_write:
                        json.dump(data, json_file_write, indent=2)
                except IOError as error:
                    print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        except IOError as error:
            print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Runs all the desktop apps that are checked
    @staticmethod
    def run_desktop_app():
        load_json()
        try:
            with open("data.json", "r") as json_read_file:
                data = json.load(json_read_file)
                active_apps = data["desktop_is_checked"].count(True)
                if active_apps > 5:
                    text = f"Unable to run more than 5 apps"
                    title = "Too many apps selected"
                    add_messagebox(text, title)
                elif active_apps == 0:
                    text = f"Please select an app to start"
                    title = "There is no app to run"
                    add_messagebox(text, title)
                else:
                    for i in range(0, len(data["desktop"])):
                        if data["desktop_is_checked"][i]:
                            try:
                                os.startfile(data["desktop"][i])
                            except Exception as error:
                                print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        except IOError as error:
            print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Opens a form window to enter information about the website
    @staticmethod
    def open_form():
        global form
        form = Form()
        form.show()
        main.hide()

    # This is the end of the desktop side
    # The website side starts from this point

    # Shows the websites in the window and is also called in the update function
    @staticmethod
    def show_website(self):
        try:
            with open("data.json", "r") as json_file_read:
                data = json.load(json_file_read)
                website_names = data["website_name"]
                website_is_checked = data["website_is_checked"]
                try:
                    for i in range(0, len(website_names)):
                        checkbox = add_checkbox(website_names[i], website_is_checked[i])
                        checkbox.stateChanged.connect(self.update_checked)
                        self.website_container.addWidget(checkbox)
                except Exception as error:
                    print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        except IOError as error:
            print(
                f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Deletes websites from the json file and removes them from the window
    def delete_website(self):
        try:
            with open("data.json", "r") as json_file_read:
                data = json.load(json_file_read)
                number_of_websites = len(data["website"])

                updated_website_list = []
                updated_state_list = []
                updated_name_list = []
                for i in range(0, number_of_websites):
                    website_is_checked = self.website_container.itemAt(i).widget().isChecked()
                    if website_is_checked:
                        updated_website_list.append(data["website"][i])
                        updated_state_list.append(data["website_is_checked"][i])
                        updated_name_list.append(data["website_name"][i])
                    elif not website_is_checked:
                        self.website_container.itemAt(i).widget().deleteLater()
                data["website"] = updated_website_list
                data["website_is_checked"] = updated_state_list
                data["website_name"] = updated_name_list
                try:
                    with open("data.json", "w") as json_file_write:
                        json.dump(data, json_file_write, indent=2)
                except IOError as error:
                    print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        except IOError as error:
            print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Runs all the selected websites
    @staticmethod
    def run_website():
        try:
            with open("data.json", "r") as json_read_file:
                data = json.load(json_read_file)
                number_of_websites = data["website_is_checked"].count(True)
                if number_of_websites > 10:
                    text = f"You can only run 10 websites at a time"
                    title = "Too many websites"
                    add_messagebox(text, title)
                elif number_of_websites == 0:
                    text = "please enter a website to run"
                    title = "There is no website"
                    add_messagebox(text, title)
                else:
                    website_path = data["website"]
                    is_checked = data["website_is_checked"]
                    for i in range(0, len(website_path)):
                        if is_checked[i]:
                            webbrowser.open_new(website_path[i])
        except IOError as error:
            print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")

    # Runs all the selected websites and desktop apps
    def run_all(self):
        self.run_website()
        self.run_desktop_app()


# This is a form that opens when you insert a website and allows you to enter a website path and name
class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()

        vbox = QVBoxLayout()

        self.setLayout(vbox)

        form_layout = QFormLayout()

        vbox.addLayout(form_layout)

        self.done_button = QPushButton("Done")
        # self.done_button.setStyleSheet('font: 75 16pt "MS Shell Dlg 2";')

        vbox.addWidget(self.done_button)

        self.website_path_label = QLabel()
        self.website_path_label.setText("URL:")
        # self.website_path_label.setStyleSheet('font: 75 16pt "MS Shell Dlg 2";')
        self.website_path_input = QLineEdit()
        # self.website_path_input.setStyleSheet('font: 75 16pt "MS Shell Dlg 2";')

        self.website_name_label = QLabel("Name:")
        # self.website_name_label.setStyleSheet('font: 75 16pt "MS Shell Dlg 2";')
        self.website_name_input = QLineEdit()
        # self.website_name_input.setStyleSheet('font: 75 16pt "MS Shell Dlg 2";')

        QFontDatabase.addApplicationFont("montserrat.regular.ttf")
        self.my_font = QFont("Montserrat", 18)
        self.setFont(self.my_font)

        self.setWindowIcon(QIcon("icon.png"))

        form_layout.setWidget(0, QFormLayout.LabelRole, self.website_path_label)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.website_path_input)
        form_layout.setWidget(1, QFormLayout.LabelRole, self.website_name_label)
        form_layout.setWidget(1, QFormLayout.FieldRole, self.website_name_input)

        self.done_button.clicked.connect(self.get_data)

    # This function was poorly named it adds websites to the json file and adds them to the window
    def get_data(self):
        path = self.website_path_input.text()
        name = self.website_name_input.text()

        # add regex to ensure a valid url is entered
        validated_name = re.search(valid_website_regex, path)
        if validated_name:
            try:
                with open("data.json", "r") as json_file_read:
                    data = json.load(json_file_read)
                    if path in data["website"]:
                        text = f"The website is already loaded"
                        add_messagebox(text)
                    elif path not in data["website"]:
                        data["website"].append(path)
                        data["website_name"].append(name)
                        data["website_is_checked"].append(True)
                        checkbox = add_checkbox(name, True)
                        checkbox.stateChanged.connect(main.update_checked)
                        main.website_container.addWidget(checkbox)
                    try:
                        with open("data.json", "w") as json_file_write:
                            json.dump(data, json_file_write, indent=2)
                    except IOError as error:
                        print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
            except IOError as error:
                print(f"there was an error on line {getframeinfo(currentframe()).lineno}: {error}")
        else:
            text = f"Please enter a valid URL"
            title = "Invalid URL"
            add_messagebox(text, title)
        self.close()
        main.show()


brown = "#864F0E"
blue = "#00659D"
# This is a global stylesheet to change the overall look and feel of the app
main_stylesheet = """
    QWidget {
        background-color: #2E2E2E;
        color: white;
    }
    QPushButton {
        background-color: #EC1C24;
        color: white;
        border-radius: 15px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    QPushButton:pressed {
        background-color: #00EF18;
    }
    QCheckBox {
        margin-left: 20px;
        font: 35px
    }
    QCheckBox::indicator {
        width: 35px;
        height: 35px
    }
    QCheckBox::indicator:checked {
        image: url(tick.png)
    }
    QCheckBox::indicator:unchecked {
        image: url(cross.png)
    }
    QFrame {
        border: 10px solid white;
        padding: 10px
    }
  
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.setWindowTitle("Runner")
    main.setStyleSheet(main_stylesheet)
    main.show()
    sys.exit(app.exec_())
