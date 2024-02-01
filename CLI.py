# Importing necessary classes and modules for the app to work
from DatabaseAnalysis import Database_analyzer
from PredefinedHabits import predefine_habits
from Habit import Habit, delete_habit_object
from Database import Database

from sqlite3 import IntegrityError
from tabulate import tabulate
import questionary as q



class Command_line_interface:
    """
    A class to represent the user interface."""
        
    def __init__(self) -> None:
        self.database = Database()
        self.analyzer = Database_analyzer(self.database.name)
        self.habit_container: dict[str, Habit] = {}
        self.upload_existing_habits()

    def upload_existing_habits(self) -> None:
        """
        Uploads already created habits from database to the habit_container for the application to work.

        No parameters."""
        habits = self.analyzer.return_currently_tracked_habits()
        for habit in habits:
            habit = Habit(*habit)
            self.habit_container[habit.name] = habit



    # Functions for processing
    def start_menu(self) -> None:
        """
        Processes user input. Based on the user's response, this function calls another one to perform the corresponding action.
        Example: user chooses to 'Check-off habit', then the funciton 'check_off_habit' is called.

        No parameters."""
        choice_handler = {
            "Add, update, or delete habit": self.habit_handler,
            "Check-off habit": self.check_off_habit, 
            "Analyze habits": self.analyze_database,
            "Additional options": self.additional_options,
            "Quit": self.quit_program
        }
        question = q.select(
            "What do you want to do?",
            choices = [
                "Add, update, or delete habit", 
                "Check-off habit", 
                "Analyze habits", 
                "Additional options",
                "Quit"
                ]
        ).ask()
        choice_handler[question]()

    def back_to_start_menu(self) -> None:
        """
        Returns the user to the start menu.

        No parameters."""
        pass



    # Functions to work with habits and database
    def habit_handler(self) -> None:
        """
        Based on the user's response, this function calls another one to perform the corresponding action.
        Example: user chooses to 'Add habit', then the funciton 'add_habit' is called.

        No parameters."""
        choice_handler = {
            "Add habit" : self.add_habit,
            "Update habit" : self.update_habit,
            "Delete habit" : self.delete_habit,
            "Return back" : self.back_to_start_menu
        }
        question = q.select(
            "What do you want to do?",
            choices = [
                "Add habit",
                "Update habit",
                "Delete habit",
                "Return back"
            ]
        ).ask()
        choice_handler[question]()

    def add_habit(self) -> None:
        """
        Adds habit to the habit container and to the database.

        No parameters."""
        name = q.text("Write name for your habit. " + 
                      "\nRemember, you won't change it later: ").ask()
        
        periodicity = q.select(
            "Choose a periodicity for your habit, i.e., how often you will perform your habit?",
            choices = [
                "Hour",
                "Day",
                "Week",
                "Month",
                "Year"
            ]
        ).ask()
        time_span = q.text(f"How many {periodicity.lower()}s do you want to develop your habit?\nWrite a number: ").ask()
        try:
            new_habit = Habit(name, periodicity, time_span)
            self.database.insert_habit_to_database(new_habit)
            self.habit_container[new_habit.name] = new_habit
            print(f"Habit \"{new_habit.name}\" added successfully!")
            delete_habit_object(new_habit)
        except IntegrityError:
            print(f"""You already have habit with the name \'{name}\'!\nTry again.""")


    def update_habit(self) -> None:
        """
        Updates habit in the habit container and in the database.

        No parameters."""
        try:
            name = q.select("Select a habit you want to update: ",
                            choices = list(self.habit_container.keys())).ask()
            habit = self.habit_container[name]
            characteristic = q.select(
                "Which parameter do you want to change?",
                choices = [
                    "periodicity",
                    "time_span"
                ]
                ).ask()
            if characteristic == "periodicity":
                new_value = q.select(
                    f"Select new {characteristic}: ", 
                    choices = [
                        "Hour",
                        "Day",
                        "Week",
                        "Month",
                        "Year"
                    ]
                ).ask()
            else:
                new_value = q.text("Write new value for chosen characteristic: ").ask()
            habit.update_habit_characteristic(characteristic, new_value)
            self.database.update_habit_characteristic_in_database(habit, characteristic, new_value)
            print(f"Habit \"{habit.name}\" updated successfully!")
            delete_habit_object(habit)
        except ValueError:
            print("You don't have any trackable habits!")

    def check_off_habit(self) -> None:
        """
        Updates streaks of a habit.

        No parameters."""
        choices = list(self.habit_container.keys())
        choices.append("Return back")
        name = q.select("Select a habit you want to check-off: ",
                        choices = choices).ask()
        if name == "Return back": return
        habit = self.habit_container[name]
        habit.check_off_habit()
        print(f"Habit \"{habit.name}\" shecked-off successfully!")
        self.database.update_habit_characteristic_in_database(habit, "end_date", habit.end_date)
        self.database.update_habit_characteristic_in_database(habit, "end_time", habit.end_time)

        if habit.complete_habit():
            self.database.update_habit_characteristic_in_database(habit, "state", habit.state)
            print("You've developed your habit successfully! Congratulations!")

        self.database.update_habit_characteristic_in_database(habit, "current_streak", habit.current_streak)
        self.database.update_habit_characteristic_in_database(habit, "longest_streak", habit.longest_streak)
        delete_habit_object(habit)

    def delete_habit(self) -> None:
        """
        Deletes habit from the habit container and from the database.

        No parameters."""
        try:
            name = q.select("Select a habit you want to delete: ",
                            choices = list(self.habit_container.keys())).ask()
            habit = self.habit_container[name]
            self.database.delete_habit_from_database(habit.name)
            del self.habit_container[name]
            print(f"Habit \"{habit.name}\" deleted successfully!")
            delete_habit_object(habit)
        except ValueError:
            print("You don't have any trackable habits!")



    # Functions for analysis
    def analyze_database(self) ->None:
        """
        Based on the user's response, this function calls another one to perform the corresponding action.
        Example: user chooses 'Show me all currently tracked habits', then the funciton 'show_currently_tracked_habits' is called.

        No parameters."""
        choice_handler = {
            "Show me all currently tracked habits": self.show_currently_tracked_habits,
            "Show me all habits with the same periodicity": self.show_habits_with_the_same_periodicity,
            "Show me the longest streak among currently tracked habits": self.show_longest_streak_of_all_habits,
            "Show me the longest streak of a certain habit": self.show_longest_streaks_of_given_habit,
            "Show the whole information of a certain habit": self.show_detailed_info,
            "Return back" : self.back_to_start_menu

        }
        question = q.select(
            "What do you want to analyze?",
            choices = [
                "Show me all currently tracked habits",
                "Show me all habits with the same periodicity",
                "Show me the longest streak among currently tracked habits",
                "Show me the longest streak of a certain habit",
                "Show the whole information of a certain habit",
                "Return back"
            ]
        ).ask()
        choice_handler[question]()
   
    def show_currently_tracked_habits(self) -> None:
        """
        Displays all currently tracked habits with the corresponding names, periodicities,
        time spans, states, start times and start dates.

        No parameters."""
        habits = self.analyzer.return_currently_tracked_habits()
        details = []
        if habits != []:
            for habit in habits:
                habit = Habit(*habit)
                details.append((habit.name, habit.periodicity, habit.time_span,
                                habit.state, habit.start_time, habit.start_date))
            columns = ("Name", "Periodicity", "Time span", "State", "Start time", "Start date")
            print(tabulate(details, headers = columns, tablefmt="github"))
        else: 
            print("You don't have any trackable habits!")

    def show_habits_with_the_same_periodicity(self) -> None:
        """
        Displays all currently tracked habits with the same periodicity.

        No parameters."""
        periodicity = q.select(
            "What is the periodicity of habits you'd like to see?",
            choices = [
                "Hour",
                "Day",
                "Week",
                "Month",
                "Year"
            ]
        ).ask()        
        habits = self.analyzer.return_habits_with_the_same_periodicity(periodicity)
        if habits != []:
            for habit in habits:
                print(habit)
        else: 
            print(f"You don't have any trackable habits with \'{periodicity}\' periodicity!")

    def show_longest_streak_of_all_habits(self) -> None:
        """
        Displays the longest streak among all defined habits.

        No parameters."""
        habits_name, longest_streak = self.analyzer.return_longest_streak_of_all_habits()
        if habits_name != []:
            habits_name = [str(habit[0]) for habit in habits_name]            
            print(f"The longest streak is on habit(s): {', '.join(map(str, habits_name))}." + 
                  "\nDuration of the streak:", longest_streak)
        else: 
            print("You don't have any trackable habits!")

    def show_longest_streaks_of_given_habit(self) -> None:
        """
        Displays the longest streak of a given habit.

        No parameters."""
        try:
            name = q.select("Select the name of the habit whose longest streak you want to see: ",
                            choices = list(self.habit_container.keys())).ask()
            longest_streak = self.analyzer.return_longest_streaks_of_given_habit(name)
            print(f"The longest streak you have ever had for \'{name}\' is: ", longest_streak)
        except ValueError:
            print("You don't have any trackable habits!")

    def show_detailed_info(self) -> None:
        """
        Displays detailed information about the habit.

        No parameters."""
        try:
            name = q.select("Select the name of the habit whose longest streak you want to see: ",
                            choices = list(self.habit_container.keys())).ask()
            details = self.analyzer.return_detailed_information_about_habit(name)
            details = list(zip(details[0], details[1]))
            print(tabulate(details, headers = ["Parameter", "Value"], tablefmt="github"))
        except ValueError:
            print("You don't have any trackable habits!")



    # Additional option functions
    def additional_options(self) -> None:
        """
        Allows to select one of the additional options.

        No parameters."""
        choice_handler = {
            "Upload predefined habits" : self.upload_predefined_habits,
            "Delete predefined habits" : self.delete_predefined_habits,
            "Delete all habits": self.delete_all_habits,
            "Return back": self.back_to_start_menu
        }
        question = q.select(
            "What do you want to do?",
            choices = [
                "Upload predefined habits",
                "Delete predefined habits",
                "Delete all habits",
                "Return back"
                ]
        ).ask()
        choice_handler[question]()

    def upload_predefined_habits(self) -> None:
        """
        Uploads predefined habits to the database and to the habit_container.

        No parameters."""
        try:
            habits = predefine_habits()
            for habit in habits:
                self.habit_container[habit.name] = habit
                self.database.insert_habit_to_database(habit)
            print("All predefined habits added successfully!")
        except IntegrityError:
            print("Predefined habits already uploaded!")

    def delete_predefined_habits(self) -> None:
        try:
            habits = predefine_habits()
            for habit in habits:
                del self.habit_container[habit.name]
                self.database.delete_habit_from_database(habit.name)
            print("All predefined habits deleted successfully!")
        except KeyError:
            print("Predefined habits already deleted!")

    def delete_all_habits(self) -> None:
        """
        Deletes all defined habits from database and from the habit_container if the user confirmed so.

        No parameters."""
        def perform_action() -> None:
            self.habit_container.clear(),
            self.database.clean_tables_in_database()

        choice_handler = {
            "Yes": perform_action,
            "No": self.back_to_start_menu,
        }
        question = q.select(
            "Are you sure you want to delete all defined habits?",
            choices = [
                "Yes",
                "No"
            ]
        ).ask()
        choice_handler[question]()
        print("All defined habits deleted successfully!")
        



    # Exiting the application
    def quit_program(self) -> None:
        """
        Terminates program is the user confirmed so.

        No parameters."""
        def perform_action():
            self.database.disconnect_database()
            quit()

        choice_handler = {
            "Yes": perform_action,
            "No": self.back_to_start_menu,
        }
        question = q.select(
            "Are you sure you want to quit the program?",
            choices = [
                "Yes",
                "No"
            ]
        ).ask()
        choice_handler[question]()
