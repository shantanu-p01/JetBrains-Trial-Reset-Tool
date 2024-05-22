def display_menu():
    print("Select a JetBrains tool by entering the corresponding number:")
    tools = [
        "WebStorm",
        "IntelliJ",
        "CLion",
        "Rider",
        "GoLand",
        "PhpStorm",
        "ReSharper",
        "PyCharm"
    ]
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool}")
    return tools

def main():
    tools = display_menu()

    try:
        choice = int(input("Enter your choice (1-8): "))
        if 1 <= choice <= len(tools):
            print(f"You have selected: {tools[choice - 1]}")
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
