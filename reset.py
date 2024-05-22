import os
import subprocess
import glob
import sys
import time

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

def display_menu():
    tools = list(TOOL_DETAILS.keys())
    print("Select a JetBrains tool by entering the corresponding number:")
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool}")
    return tools

def find_tool_executable(tool_keyword, executable_name):
    program_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    jetbrains_path = os.path.join(program_files, "JetBrains")
    
    # Search for directories containing the tool keyword
    search_pattern = os.path.join(jetbrains_path, f"*{tool_keyword}*\\bin\\{executable_name}")
    matching_executables = glob.glob(search_pattern)

    if matching_executables:
        return matching_executables[0]  # Return the first matching executable
    else:
        return None

def check_tool_installed(tool_name):
    tool_keyword, executable_name = TOOL_DETAILS[tool_name]
    tool_executable = find_tool_executable(tool_keyword, executable_name)
    
    if tool_executable:
        return True
    else:
        print(f"[ ! ] {tool_name} not found. Please make sure it is installed.")
        return False

def remove_javasoft_key():
    print("[ INFO ] Removing JavaSoft key for user...")
    result = subprocess.run(["reg", "delete", "HKEY_CURRENT_USER\\Software\\JavaSoft", "/f"], capture_output=True, text=True)
    if result.returncode == 0:
        print("[ OK ] Key removed successfully.")
        return True
    else:
        print(f"[ ! ] Failed to remove the key. Error: {result.stderr}")
        return False

def remove_permanent_files():
    print("[ INFO ] Removing PermanentDeviceId and PermanentUserId...")
    appdata_path = os.getenv("APPDATA")
    jetbrains_path = os.path.join(appdata_path, "JetBrains")
    try:
        os.remove(os.path.join(jetbrains_path, "PermanentUserId"))
        os.remove(os.path.join(jetbrains_path, "PermanentDeviceId"))
        print("[ OK ] PermanentDeviceId and PermanentUserId removed successfully.")
        return True
    except FileNotFoundError:
        print("[ ! ] PermanentDeviceId or PermanentUserId file not found.")
        return False
    except Exception as e:
        print(f"[ ! ] Failed to remove PermanentDeviceId or PermanentUserId. Error: {e}")
        return False

def open_ide(tool_name):
    tool_keyword, executable_name = TOOL_DETAILS[tool_name]
    tool_executable = find_tool_executable(tool_keyword, executable_name)
    
    if tool_executable:
        print(f"[ INFO ] Opening {tool_name}...")
        try:
            subprocess.Popen([tool_executable])
            print(f"[ OK ] {tool_name} opened successfully.")
            return True
        except Exception as e:
            print(f"[ ! ] Failed to open {tool_name}. Error: {e}")
            return False
    else:
        print(f"[ ! ] Executable for {tool_name} not found. Make sure it is installed.")
        return False

def main():
    tools = display_menu()
    
    try:
        choice = int(input("Enter your choice (1-8): "))
        if 1 <= choice <= len(tools):
            selected_tool = tools[choice - 1]
            print(f"You have selected: {selected_tool}")
            if check_tool_installed(selected_tool):
                if remove_javasoft_key() and remove_permanent_files():
                    if open_ide(selected_tool):
                        time.sleep(3)  # Delay for 3 seconds
                        sys.exit(0)  # Terminate the script
                    else:
                        print("Failed to open IDE. Aborting.")
                else:
                    print("Failed to perform pre-requisite operations. Aborting.")
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
