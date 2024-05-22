# JetBrains IDE Reset Tool

This tool provides a graphical user interface (GUI) for resetting JetBrains IDEs. It allows users to select a JetBrains IDE, perform necessary reset actions, and open the selected IDE. 

## Features

- Select from a list of JetBrains IDEs.
- Reset the IDE by removing certain configuration files.
- Open the IDE after resetting.

## Setup

1. **Install Dependencies:**
   
   Make sure you have Python and PyQt5 installed. You can install the dependencies using pip:

   ```
   pip install PyQt5
   ```

2. **Download icon.ico:**

   Download or place an icon file named `icon.ico` in the same directory as the script.

## Usage

To run the application, execute the Python script `reset.py`:

```
python reset.py
```

## Creating Executable

You can create an executable file for the application using PyInstaller. 

### With Python Interpreter:

```
python -m PyInstaller --onefile reset.py
```

### Without Python Interpreter:

If you have PyInstaller installed globally, you can run:

```
pyinstaller --onefile reset.py
```

This will generate a standalone executable file in the `dist` directory.

---