from CLI import Command_line_interface as CLI



if __name__ == "__main__":
    input_analyzer = CLI()
    print("Welcome to the Habit tracker!")
    while True:
        input_analyzer.start_menu()
