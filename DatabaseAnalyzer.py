import sqlite3



# Since we want to analyze data but not to change it, we only need the database name.
# Importing the whole Database class will be excessive.
class DatabaseAnalyzer:
    """
    A class to represent a database analyzer.
    
    Attributes:
    """

    def __init__(self, database_name: str) -> None:
        """
        Parameters:
            database_name: str
                Name of the database to be analyzed."""
        self.database_name = database_name

    def return_currently_tracked_habits(self) -> list:
        """
        Returns all currently tracked habits, i.e., which state is 'In progress'
        
        No parameters."""
        cursor = sqlite3.connect(self.database_name).cursor()
        cursor.execute("""SELECT 
                       habits.name, 
                       habits.periodicity, 
                       habits.time_span,
                       habits.state, 
                       habits_log.current_streak, 
                       habits_log.longest_streak,
                       habits_log.start_time, 
                       habits_log.start_date, 
                       habits_log.end_time, 
                       habits_log.end_date 
                       FROM habits
                       INNER JOIN habits_log ON habits.name = habits_log.name""")        
        habits = list(cursor.fetchall())
        cursor.close()
        return habits

    def return_habits_with_the_same_periodicity(self, periodicity: str) -> list:
        """
        Returns all currently tracked habits with a certain periodicity (hour/day/etc.).
        
        No parameters."""
        cursor = sqlite3.connect(self.database_name).cursor()
        cursor.execute("SELECT * FROM habits WHERE periodicity = ?", 
                       (periodicity,))
        habits = list(cursor.fetchall())
        cursor.close()
        return habits

    def return_longest_streak_of_all_habits(self) -> list:
        """
        Returns the longest streak among all defined habits.
        
        No parameters."""
        cursor = sqlite3.connect(self.database_name).cursor()
        cursor.execute("SELECT MAX(longest_streak) FROM habits_log")
        max_longest_streak = cursor.fetchone()[0]
        cursor.execute("SELECT name FROM habits_log WHERE longest_streak = ?", 
                       (max_longest_streak,))
        habits_names_with_longest_streak = cursor.fetchall()
        cursor.close()
        return [habits_names_with_longest_streak, max_longest_streak]

    def return_longest_streaks_of_given_habit(self, habit_name: str) -> int:
        """
        Returns the longest streak of the certain habit.
        
        No parameters."""
        cursor = sqlite3.connect(self.database_name).cursor()
        cursor.execute("SELECT longest_streak FROM habits_log WHERE name = ?", 
                       (habit_name,))
        streak = cursor.fetchone()[0]
        cursor.close()
        return streak
    
    def return_detailed_information_about_habit(self, habit_name: str) -> list:
        """
        Returns all information about the certain habit
        """
        cursor = sqlite3.connect(self.database_name).cursor()
        cursor.execute("""SELECT 
                       habits.name AS 'Habit name', 
                       habits.periodicity AS Periodicity, 
                       habits.time_span AS 'Time span',
                       habits.state AS 'State', 
                       habits_log.current_streak AS 'Current streak', 
                       habits_log.longest_streak AS 'Longest streak', 
                       habits_log.start_time AS 'Start time', 
                       habits_log.start_date AS 'Start date', 
                       habits_log.end_time AS 'End time',
                       habits_log.end_date AS 'End date' 
                       FROM habits
                       INNER JOIN habits_log ON habits.name = habits_log.name
                       WHERE habits.name = ?""", (habit_name,))
        row = cursor.fetchone()
        if row is None:
            return [None, None]
        habit_info = list(row)
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return [column_names, habit_info]
