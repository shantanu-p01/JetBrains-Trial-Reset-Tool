import os
import subprocess
import glob
import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui

# Define the mapping of tool names to their respective keywords and expected executable names
TOOL_DETAILS = {
    "WebStorm": ("WebStorm", "webstorm64.exe"),
    "IntelliJ": ("IntelliJ", "idea64.exe"),
    "CLion": ("CLion", "clion64.exe"),
    "Rider": ("Rider", "rider64.exe"),
    "GoLand": ("GoLand", "goland64.exe"),
    "PhpStorm": ("PhpStorm", "phpstorm64.exe"),
    "ReSharper": ("ReSharper", "resharper64.exe"),
    "PyCharm": ("PyCharm", "pycharm64.exe")
}

def find_tool_executable(tool_keyword, executable_name):
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    user_profile = os.environ.get("USERPROFILE")
    local_programs = os.path.join(user_profile, "AppData", "Local", "Programs")
    
    potential_paths = [
        os.path.join(program_files, "JetBrains"),
        os.path.join(local_programs)
    ]
    
    for jetbrains_path in potential_paths:
        # Debug: print the paths being searched
        print(f"Searching in: {jetbrains_path}")
        
        search_pattern = os.path.join(jetbrains_path, f"*{tool_keyword}*\\bin\\{executable_name}")
        matching_executables = glob.glob(search_pattern, recursive=True)
        
        # Debug: print the matching executables found
        print(f"Matching executables: {matching_executables}")

        if matching_executables:
            return matching_executables[0]  # Return the first matching executable
    
    return None

def remove_javasoft_key():
    result = subprocess.run(["reg", "delete", "HKEY_CURRENT_USER\\Software\\JavaSoft", "/f"], capture_output=True, text=True)
    if result.returncode == 0:
        return True, "JavaSoft key removed successfully."
    else:
        return False, f"Failed to remove the JavaSoft key:\n{result.stderr}"

def remove_permanent_files():
    appdata_path = os.getenv("APPDATA")
    jetbrains_path = os.path.join(appdata_path, "JetBrains")
    messages = []
    try:
        os.remove(os.path.join(jetbrains_path, "PermanentUserId"))
        messages.append("PermanentUserId removed successfully.")
    except FileNotFoundError:
        messages.append("PermanentUserId file not found.")
    except Exception as e:
        messages.append(f"Failed to remove PermanentUserId. Error: {e}")
    
    try:
        os.remove(os.path.join(jetbrains_path, "PermanentDeviceId"))
        messages.append("PermanentDeviceId removed successfully.")
    except FileNotFoundError:
        messages.append("PermanentDeviceId file not found.")
    except Exception as e:
        messages.append(f"Failed to remove PermanentDeviceId. Error: {e}")
    
    return messages

def open_ide(tool_name):
    tool_keyword, executable_name = TOOL_DETAILS[tool_name]
    tool_executable = find_tool_executable(tool_keyword, executable_name)
    
    if tool_executable:
        try:
            subprocess.Popen([tool_executable])
            return True, f"{tool_name} opened successfully."
        except Exception as e:
            return False, f"Failed to open {tool_name}. Error: {e}"
    else:
        return False, f"Executable for {tool_name} not found. Make sure it is installed."

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JetBrains IDE Reset")
        self.setGeometry(300, 300, 400, 300)
        
        # Set window icon
        self.setWindowIcon(QtGui.QIcon('icon.ico'))  # Make sure 'icon.ico' is in the same directory

        self.main_layout = QtWidgets.QVBoxLayout()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.group = QtWidgets.QButtonGroup(self)
        self.group.setExclusive(True)

        row = 0
        col = 0
        for i, tool_name in enumerate(TOOL_DETAILS.keys()):
            radio = QtWidgets.QRadioButton(tool_name)
            self.group.addButton(radio)
            self.grid_layout.addWidget(radio, row, col)
            col += 1
            if col == 2:  # Change this value to arrange items in more columns
                col = 0
                row += 1

        self.main_layout.addLayout(self.grid_layout)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        self.main_layout.addWidget(self.reset_button, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def reset(self):
        selected_button = self.group.checkedButton()
        if selected_button:
            selected_tool = selected_button.text()
            
            # Check if the tool is installed
            tool_keyword, executable_name = TOOL_DETAILS[selected_tool]
            tool_executable = find_tool_executable(tool_keyword, executable_name)
            if not tool_executable:
                QtWidgets.QMessageBox.critical(self, "Error", f"{selected_tool} not found. Please make sure it is installed.")
                return

            results = []

            # Perform the JavaSoft key removal
            success, message = remove_javasoft_key()
            results.append(message)
            if not success:
                QtWidgets.QMessageBox.critical(self, "Error", "\n".join(results))
                return

            # Perform the PermanentUserId and PermanentDeviceId removal
            results.extend(remove_permanent_files())
            for result in results:
                if "Error" in result:
                    QtWidgets.QMessageBox.critical(self, "Error", "\n".join(results))
                    return

            # Attempt to open the IDE
            success, message = open_ide(selected_tool)
            results.append(message)
            if success:
                QtWidgets.QMessageBox.information(self, "Success", "\n".join(results))
                QtCore.QTimer.singleShot(3000, self.close)
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "\n".join(results))
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select an IDE.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()